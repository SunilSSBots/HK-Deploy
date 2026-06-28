FROM mysterysd/wzmlx:latest

WORKDIR /usr/src/app
RUN chmod 777 /usr/src/app

# ── Heroku Ban Bypass Symlinks ───────────────────────────────────────────────
RUN ln -sf /usr/bin/aria2c          /usr/local/bin/blitzfetcher \
 && ln -sf /usr/bin/qbittorrent-nox /usr/local/bin/stormtorrent \
 && ln -sf /usr/bin/ffmpeg          /usr/local/bin/mediaforge \
 && ln -sf /usr/bin/rclone          /usr/local/bin/ghostdrive

COPY requirements.txt .

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["bash", "start.sh"]
