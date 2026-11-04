# fx4 take E1 image: Python 3.11 only (no python3.12 anywhere on PATH, no uv-managed CPython), uv 0.13.6 copied in
# from the lab image, pip current, network on. Debian bookworm's system Python is 3.11.2; its PEP 668 marker file is
# removed so pip prints the Requires-Python error a python.org Python prints (not "externally-managed-environment").
#   docker build -t fx4-py311 -f docker/fx4-py311.Dockerfile docker
FROM debian:bookworm-slim
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
      xvfb xauth x11-utils xdotool wmctrl openbox ffmpeg fonts-dejavu-core dmz-cursor-theme xterm tmux procps \
      python3 python3-pip python3-yaml python3-numpy \
 && rm -rf /var/lib/apt/lists/* /usr/lib/python3.11/EXTERNALLY-MANAGED \
 && python3 -m pip install --no-cache-dir --upgrade pip
COPY --from=fcc-app:1.1.4-0.1.28 /opt/pre/uv /opt/pre/uvx /usr/local/bin/
RUN useradd -m -u 1000 -s /bin/bash maker && mkdir -p /home/maker/.local/share/uv/python && chown -R maker /home/maker
ENV XCURSOR_THEME=DMZ-White XCURSOR_SIZE=48 LANG=C.UTF-8 LC_ALL=C.UTF-8 XDG_RUNTIME_DIR=/tmp/xdg PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH=/lab/vendor/screenlab-lib:/lab UV_PYTHON_INSTALL_DIR=/home/maker/.local/share/uv/python
WORKDIR /lab
