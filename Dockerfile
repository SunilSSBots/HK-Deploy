FROM ssbots/ssbots_heroku

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

# ── Heroku Ban Bypass Symlinks ───────────────────────────────────────────────
# BUG FIX: use $(which ...) so symlinks work regardless of where binaries are installed
# Previously hardcoded /usr/bin/ffmpeg was broken if base image puts ffmpeg elsewhere
RUN ln -sf "$(which aria2c)"          /usr/local/bin/blitzfetcher \
 && ln -sf "$(which qbittorrent-nox)" /usr/local/bin/stormtorrent \
 && ln -sf "$(which ffmpeg)"          /usr/local/bin/mediaforge \
 && ln -sf "$(which rclone)"          /usr/local/bin/ghostdrive

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "start.sh"]
