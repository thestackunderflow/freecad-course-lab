# fx3 image: the lab image plus Node (distro package) for the launcher and Claude Code on the system PATH
# (not in ~/.local/bin, so take A's `ls ~/.local/bin` shows only what uv's installer put there). Network on.
#   docker build -t fx3-lab:1 -f docker/fx3.Dockerfile docker
FROM fcc-app:1.1.4-0.1.28
USER root
RUN apt-get update && apt-get install -y --no-install-recommends nodejs less && rm -rf /var/lib/apt/lists/* \
 && cp -L /opt/pre/claude /usr/local/bin/claude && node --version
USER maker
