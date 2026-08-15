"""
update.py — HK-Deploy deployment helper for SSLeech on Heroku.

MINIMUM required Heroku config vars (only these 2 are truly mandatory):
  BOT_TOKEN     — identifies which MongoDB partition to load
  DATABASE_URL  — MongoDB connection string

Everything else (UPSTREAM_REPO, UPSTREAM_BRANCH, TELEGRAM_API, TELEGRAM_HASH,
OWNER_ID, etc.) is loaded from MongoDB automatically.
You only need them in Heroku config vars for the VERY FIRST boot.
After that they persist in MongoDB and can be removed from Heroku.

Key fixes vs original:
  1. config.env bridge — all MongoDB vars written to config.env AFTER git reset
     so bot/__init__.py can read them via load_dotenv (process boundary fix).
  2. uv --system — added so pip works outside a virtualenv.
  3. Venv-aware pip — if VIRTUAL_ENV is set (Heroku buildpack), uses the venv's
     own pip instead of uv to avoid "no venv found" conflicts.
  4. UPDATE_PKGS respected — True → -U upgrade, False → only install missing.
"""

from logging import ERROR, INFO, FileHandler, StreamHandler, basicConfig, getLogger
from os import environ, path
from subprocess import call as scall
from subprocess import run as srun
from sys import exit

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

getLogger("pymongo").setLevel(ERROR)

basicConfig(
    format="[%(asctime)s] [%(levelname)s] - %(message)s",
    datefmt="%d-%b-%y %I:%M:%S %p",
    handlers=[FileHandler("log.txt"), StreamHandler()],
    level=INFO,
)
_LOGGER = getLogger("update")

# ── Step 1: BOT_TOKEN (only truly mandatory Heroku var) ───────────────────────
BOT_TOKEN = environ.get("BOT_TOKEN", "").strip()
if not BOT_TOKEN:
    # Fallback: try config.env from a previous run
    if path.exists("config.env"):
        for line in open("config.env"):
            line = line.strip()
            if line.startswith("BOT_TOKEN="):
                BOT_TOKEN = line[len("BOT_TOKEN="):].strip().strip('"').strip("'")
                break
if not BOT_TOKEN:
    _LOGGER.error("BOT_TOKEN is missing! Set it in Heroku config vars. Exiting.")
    exit(1)

BOT_ID = BOT_TOKEN.split(":", 1)[0]
DATABASE_URL = environ.get("DATABASE_URL", "").strip()

# Fallback DATABASE_URL from config.env
if not DATABASE_URL and path.exists("config.env"):
    for line in open("config.env"):
        line = line.strip()
        if line.startswith("DATABASE_URL="):
            DATABASE_URL = line[len("DATABASE_URL="):].strip().strip('"').strip("'")
            break

# ── Step 2: Load ALL config from MongoDB ─────────────────────────────────────
# Reads every saved botsetting into os.environ (Heroku vars take priority).
# Also returns the raw doc so we can write it to config.env after git reset.
UPSTREAM_REPO   = environ.get("UPSTREAM_REPO", "").strip()
UPSTREAM_BRANCH = environ.get("UPSTREAM_BRANCH", "").strip()
UPDATE_PKGS     = environ.get("UPDATE_PKGS", "True").strip()
db_doc = None

if DATABASE_URL:
    try:
        conn = MongoClient(DATABASE_URL, server_api=ServerApi("1"), serverSelectionTimeoutMS=8000)
        db   = conn.wzmlx
        db_doc = db.settings.config.find_one({"_id": BOT_ID})
        if db_doc:
            loaded = 0
            for key, value in db_doc.items():
                if key == "_id" or value is None:
                    continue
                # Heroku config vars already set take priority — don't overwrite
                if not environ.get(key):
                    environ[key] = str(value).strip()
                    loaded += 1
            _LOGGER.info(f"MongoDB: loaded {loaded} config var(s) into environ.")
            # Use MongoDB UPSTREAM_* / UPDATE_PKGS if not set in Heroku env
            UPSTREAM_REPO   = environ.get("UPSTREAM_REPO", UPSTREAM_REPO).strip()
            UPSTREAM_BRANCH = environ.get("UPSTREAM_BRANCH", UPSTREAM_BRANCH).strip()
            UPDATE_PKGS     = environ.get("UPDATE_PKGS", UPDATE_PKGS).strip()
        conn.close()
    except Exception as e:
        _LOGGER.warning(f"MongoDB: could not load config — {e}")
else:
    _LOGGER.warning(
        "DATABASE_URL not set — skipping MongoDB load. "
        "All required vars must be present in Heroku config vars."
    )

UPSTREAM_BRANCH = UPSTREAM_BRANCH or "ssleech-hk"

# ── Step 3: git reset to upstream ────────────────────────────────────────────
if UPSTREAM_REPO:
    if path.exists(".git"):
        srun(["rm", "-rf", ".git"])

    update = srun(
        f"git init -q "
        f"&& git config --global user.email bot@ssleech.local "
        f"&& git config --global user.name SSLeech "
        f"&& git add . "
        f"&& git commit -sm update -q "
        f"&& git remote add origin {UPSTREAM_REPO} "
        f"&& git fetch origin -q "
        f"&& git reset --hard origin/{UPSTREAM_BRANCH} -q",
        shell=True,
    )
    _display = UPSTREAM_REPO.rstrip("/").rsplit("/", 2)
    _display = f"https://github.com/{_display[-2]}/{_display[-1]}" if len(_display) >= 3 else UPSTREAM_REPO
    if update.returncode == 0:
        _LOGGER.info("Successfully updated with Latest Updates !")
    else:
        _LOGGER.error("Git update failed! Check UPSTREAM_REPO/UPSTREAM_BRANCH.")
    _LOGGER.info(f"UPSTREAM_REPO: {_display} | UPSTREAM_BRANCH: {UPSTREAM_BRANCH}")
else:
    _LOGGER.warning("UPSTREAM_REPO not set — skipping git update.")

# ── Step 4: Write ALL MongoDB vars to config.env AFTER git reset ─────────────
# Critical fix: update.py runs as a subprocess. Any os.environ changes here do
# NOT reach the parent process or the subsequent `python3 -m bot` in start.sh.
# Writing to config.env is the only reliable way to pass MongoDB vars across
# the process boundary. bot/__init__.py reads this via load_dotenv().
_SKIP_KEYS = {"_id", "_____REMOVE_THIS_LINE_____"}

if db_doc:
    lines = [
        "# Auto-generated by update.py from MongoDB — do not edit manually.",
        "# These values were saved via /botsettings and loaded on startup.",
        "",
    ]
    written = 0
    for key, value in db_doc.items():
        if key in _SKIP_KEYS or value is None:
            continue
        str_val = str(value).strip()
        if str_val in ("", "None"):
            continue
        str_val_esc = str_val.replace('"', '\\"')
        lines.append(f'{key}="{str_val_esc}"')
        written += 1
    try:
        with open("config.env", "w") as f:
            f.write("\n".join(lines) + "\n")
        _LOGGER.info(
            f"MongoDB: wrote {written} config var(s) to config.env "
            "(bot/__init__.py will read them via load_dotenv)."
        )
    except Exception as e:
        _LOGGER.warning(f"Could not write config.env: {e}")

# ── Step 5: Install / upgrade packages ───────────────────────────────────────
# UPDATE_PKGS == True  → install with -U (upgrade to latest compatible)
# UPDATE_PKGS == False → only install missing packages
_do_upgrade = True
if isinstance(UPDATE_PKGS, str):
    _do_upgrade = UPDATE_PKGS.lower() not in ("false", "0", "no")
elif isinstance(UPDATE_PKGS, bool):
    _do_upgrade = UPDATE_PKGS

_LOGGER.info(f"Updating packages (UPDATE_PKGS={_do_upgrade}) ...")

from shutil import which as _which

# If inside an activated virtualenv (Heroku buildpack may set VIRTUAL_ENV),
# use the venv's own pip to avoid "uv: No virtual environment found" conflicts.
_venv = environ.get("VIRTUAL_ENV", "").strip()
_venv_pip = path.join(_venv, "bin", "pip") if _venv else ""

if _venv and path.exists(_venv_pip):
    _uflag   = "--upgrade " if _do_upgrade else ""
    _pip_cmd = f"{_venv_pip} install {_uflag}-r requirements.txt -q --no-warn-script-location"
    _LOGGER.info(f"Package installer: venv pip ({_venv_pip})")
else:
    _uv = _which("uv")
    if _uv:
        _uflag   = "-U " if _do_upgrade else ""
        _pip_cmd = f"{_uv} pip install --system {_uflag}-r requirements.txt -q"
        _LOGGER.info(f"Package installer: uv ({_uv})")
    else:
        _pip_candidates = ["/wzvenv/bin/pip", "/usr/local/bin/pip3", "/usr/local/bin/pip"]
        _pip_bin = next((p for p in _pip_candidates if path.exists(p)), None)
        if not _pip_bin:
            _pip_bin = _which("pip3") or _which("pip") or "pip3"
        _uflag   = "--upgrade " if _do_upgrade else ""
        _pip_cmd = (
            f"{_pip_bin} install {_uflag}-r requirements.txt -q "
            "--no-warn-script-location --break-system-packages"
        )
        _LOGGER.info(f"Package installer: pip ({_pip_bin})")

ret = scall(_pip_cmd, shell=True)
if ret == 0:
    _LOGGER.info("Successfully Updated all the Packages !")
else:
    _LOGGER.warning("Package install had warnings — continuing anyway.")
