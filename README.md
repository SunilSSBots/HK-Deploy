<div align="center">

# SSLeech — Heroku Deploy Kit

Deploy the SSLeech Telegram bot to Heroku Container Stack using a guided Google Colab notebook.

[![Open in Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/SunilSSBots/HK-Deploy/blob/main/ssleech_hk_deploy.ipynb)
[![Bot Repository](https://img.shields.io/badge/Bot_Repository-SSLeech-2563eb?style=flat&logo=github&logoColor=white)](https://github.com/SunilSSBots/ssleech-hk)
[![Docker Image](https://img.shields.io/badge/Docker_Image-ssbots__heroku-2496ed?style=flat&logo=docker&logoColor=white)](https://hub.docker.com/r/sunilsharmanp/ssbots_heroku)

<br>

<img src="https://te.legra.ph/file/c45e3fc9cba60c15f7cb5-9db34c454ba90b2640.jpg" alt="SSLeech Telegram bot thumbnail" width="760">

</div>

---

## Overview

HK-Deploy provides the deployment files and automation required to run SSLeech on Heroku. The included Google Colab notebook is optimized for a guided, mobile-friendly setup and supports creating, configuring, deploying, and monitoring one or multiple Heroku apps.

## Highlights

- Guided Google Colab deployment workflow
- Support for single-app and multi-app deployments
- Heroku Container Stack configuration
- MongoDB-backed bot configuration
- Optional GitHub Actions deployment workflow
- Built-in log viewing and Heroku logout steps

## Repository Structure

```text
HK-Deploy/
├── ssleech_hk_deploy.ipynb   # Main Google Colab deployment notebook
├── assets/
│   └── ssleech-thumbnail.jpg  # SSLeech project thumbnail
├── Dockerfile                 # Heroku container build file
├── heroku.yml                 # Heroku stack configuration
├── start.sh                   # Container startup script
├── update.py                  # Upstream sync and dependency installer
└── requirements.txt           # Python dependencies
```

---

## Deployment Options

### Option 1: Google Colab — Recommended

The Colab notebook provides the simplest deployment experience, especially on mobile devices.

<a href="https://colab.research.google.com/github/SunilSSBots/HK-Deploy/blob/main/ssleech_hk_deploy.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open ssleech_hk_deploy.ipynb in Google Colab">
</a>

Run the notebook cells from top to bottom:

| Step | Notebook section | Action |
|------|------------------|--------|
| 1 | Heroku Login | Enter your Heroku email and personal API token. |
| 2 | Create Heroku App | Choose app name, region, and optional team. |
| 3 | SSLeech Configuration | Enter bot credentials, MongoDB URI, and upstream branch. |
| 4 | Deploy Bot | Enter the configured app name or names and start deployment. |
| 5 | Logs / Logout | Monitor the deployment, then log out of Heroku when finished. |

The Docker build typically takes several minutes. Once deployment is complete, send `/start` to the bot on Telegram.

### Option 2: GitHub Actions — Advanced

1. Fork the [SSLeech repository](https://github.com/SunilSSBots/ssleech-hk).
2. Add the required secrets under **Settings → Secrets and variables → Actions**.
3. Open the **Actions** tab and run the deployment workflow manually.

| Secret | Description |
|--------|-------------|
| `HEROKU_EMAIL` | Heroku account email |
| `HEROKU_API_KEY` | Heroku personal API token |
| `HEROKU_APP_NAME` | Target Heroku app name |
| `BOT_TOKEN` | Telegram bot token |
| `OWNER_ID` | Telegram owner/user ID |
| `TELEGRAM_API` | Telegram API ID |
| `TELEGRAM_HASH` | Telegram API hash |
| `DATABASE_URL` | MongoDB connection URI |

---

## Required Configuration

| Variable | Purpose | Where to get it |
|----------|---------|-----------------|
| `BOT_TOKEN` | Authenticates the Telegram bot | [@BotFather](https://t.me/BotFather) |
| `OWNER_ID` | Identifies the bot owner | [@userinfobot](https://t.me/userinfobot) |
| `TELEGRAM_API` | Telegram API ID | [my.telegram.org/apps](https://my.telegram.org/apps) |
| `TELEGRAM_HASH` | Telegram API hash | [my.telegram.org/apps](https://my.telegram.org/apps) |
| `DATABASE_URL` | MongoDB connection URI | [MongoDB Atlas](https://cloud.mongodb.com) |
| `UPSTREAM_REPO` | SSLeech source repository | `https://github.com/SunilSSBots/ssleech-hk` |
| `UPSTREAM_BRANCH` | Source branch to deploy | `ssleech-hk` |

## Docker Environment

```text
Base image : sunilsharmanp/ssbots_heroku:latest
Stack      : Heroku Container Stack
Python     : 3.13-slim-bookworm
```

The base image includes:

- `aria2c` (`blitzfetcher`)
- `ffmpeg` (`mediaforge`)
- `rclone` (`ghostdrive`)
- `qbittorrent-nox` (`stormtorrent`)

---

## Security Notes

- Never commit a notebook after entering real credentials.
- Keep your Heroku API token, Telegram bot token, and MongoDB URI private.
- Use a private GitHub repository or GitHub Actions secrets for sensitive deployment values.
- Rotate any credential immediately if it is exposed publicly.

## Support

- [SSLeech Issues](https://github.com/SunilSSBots/ssleech-hk/issues)
- [SSLeech Repository](https://github.com/SunilSSBots/ssleech-hk)
- [SSBots Heroku Docker Image](https://hub.docker.com/r/sunilsharmanp/ssbots_heroku)
