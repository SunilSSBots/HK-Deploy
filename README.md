<div align="center">

# 🤖 SSLeech — Heroku Deploy Guide

**Google Colab se Heroku pe SSLeech Bot deploy karo**

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SunilSharmaNP/VidLM/blob/main/ssleech_hk_deploy.ipynb)
[![Bot Repo](https://img.shields.io/badge/Bot_Repo-SSLeech-blue?style=flat&logo=github)](https://github.com/SunilSharmaNP/SSLeech)
[![Base Image](https://img.shields.io/badge/Base_Image-ssbots__heroku-blue?style=flat&logo=docker)](https://hub.docker.com/r/sunilsharmanp/ssbots_heroku)

</div>

---

## 📦 Repo Structure

```
VidLM/
├── ssleech_hk_deploy.ipynb   ← Google Colab Notebook (MAIN FILE)
├── Dockerfile                ← Heroku Docker build file
├── heroku.yml                ← Heroku stack config
├── start.sh                  ← Bot startup script
├── update.py                 ← Auto git pull + pip install
└── requirements.txt          ← Python dependencies
```

---

## 🚀 Deploy Karne ke 2 Tarike

### Method 1: Google Colab (Recommended — Mobile Friendly ✅)

<details>
<summary><b>Steps Expand Karo 👆</b></summary>

**Step 1:** Niche badge pe click karo — Colab mein notebook khulegi

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SunilSharmaNP/VidLM/blob/main/ssleech_hk_deploy.ipynb)

**Step 2:** Har cell ko **upar se niche** order mein run karo:

| Step | Cell | Kya karna hai |
|------|------|---------------|
| 1️⃣ | Heroku Login | Email + API Token daalo |
| 2️⃣ | Create App | App naam aur region choose karo |
| 3️⃣ | Required Config | BOT_TOKEN, OWNER_ID, etc. set karo |
| 4️⃣ | Optional Config | GDrive, RClone, limits set karo (skip kar sakte ho) |
| 5️⃣ | Deploy Bot | App naam daalo — deploy start ho jayega |

**Step 3:** 5-10 minute wait karo — Docker build hoga

**Step 4:** Telegram mein bot ko `/start` bhejo ✅

</details>

---

### Method 2: GitHub Actions (Advanced)

<details>
<summary><b>Steps Expand Karo 👆</b></summary>

**Step 1:** [SSLeech repo](https://github.com/SunilSharmaNP/SSLeech) ko Fork karo

**Step 2:** Fork kiye repo mein ye secrets add karo (Settings → Secrets → Actions):

| Secret Name | Value |
|-------------|-------|
| `HEROKU_EMAIL` | Heroku account email |
| `HEROKU_API_KEY` | Heroku API token |
| `HEROKU_APP_NAME` | Heroku app naam |
| `BOT_TOKEN` | Telegram bot token |
| `OWNER_ID` | Apna Telegram ID |
| `TELEGRAM_API` | Telegram API ID |
| `TELEGRAM_HASH` | Telegram API Hash |
| `DATABASE_URL` | MongoDB URI |

**Step 3:** Actions tab → Deploy workflow → Run workflow

</details>

---

## ⚙️ Required Config Variables

| Variable | Description | Kahan se milega |
|----------|-------------|-----------------|
| `BOT_TOKEN` | Telegram Bot Token | [@BotFather](https://t.me/BotFather) |
| `OWNER_ID` | Apna Telegram User ID | [@userinfobot](https://t.me/userinfobot) |
| `TELEGRAM_API` | Telegram API ID | [my.telegram.org](https://my.telegram.org/apps) |
| `TELEGRAM_HASH` | Telegram API Hash | [my.telegram.org](https://my.telegram.org/apps) |
| `DATABASE_URL` | MongoDB Connection URI | [MongoDB Atlas](https://cloud.mongodb.com) (free) |
| `UPSTREAM_REPO` | Bot Source Repo | `https://github.com/SunilSharmaNP/SSLeech` |
| `UPSTREAM_BRANCH` | Bot Branch | `lp` |

---

## 🐳 Docker Info

```
Base Image : sunilsharmanp/ssbots_heroku:latest
Stack      : container (Heroku Docker)
Python     : 3.13-slim-bookworm
```

**Base image mein pre-installed:**
- `aria2c` (alias: `blitzfetcher`)
- `ffmpeg` (alias: `mediaforge`)
- `rclone` (alias: `ghostdrive`)
- `qbittorrent-nox` (alias: `stormtorrent`)

---

## ❓ Help

- 🔗 **Bot Repo Issues:** [SSLeech Issues](https://github.com/SunilSharmaNP/SSLeech/issues)
- 🐳 **Base Image:** [Docker Hub](https://hub.docker.com/r/sunilsharmanp/ssbots_heroku)
