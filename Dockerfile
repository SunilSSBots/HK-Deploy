FROM mysterysd/wzmlx:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

# ── Heroku Ban Bypass Symlinks ───────────────────────────────────────────────
# Rename standard binaries to custom names so process list shows obfuscated names
RUN ln -sf /usr/bin/aria2c          /usr/local/bin/blitzfetcher \
 && ln -sf /usr/bin/qbittorrent-nox /usr/local/bin/stormtorrent \
 && ln -sf /usr/bin/ffmpeg          /usr/local/bin/mediaforge   \
 && ln -sf /usr/bin/rclone          /usr/local/bin/ghostdrive
# ─────────────────────────────────────────────────────────────────────────────


COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt

# Patch lk21/exrex.py: 'sre_parse' removed from 're' in Python 3.13
RUN /usr/src/app/.venv/bin/python3 -c "\
import glob, os; \
OLD = 'from re import sre_parse, U'; \
NEW = 'try:\n    import sre_parse\nexcept ImportError:\n    import re; sre_parse = re._parser\nfrom re import U'; \
files = glob.glob('/usr/src/app/.venv/lib/python*/site-packages/lk21/thirdparty/exrex.py'); \
[open(f,'w').write(open(f).read().replace(OLD, NEW)) for f in files if OLD in open(f).read()] or print('exrex: already patched or not found'); \
print('lk21/exrex.py patch done:', files)"

COPY . .

CMD ["bash", "start.sh"]
