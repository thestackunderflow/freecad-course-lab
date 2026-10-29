# FreeCAD on the screen-lab base: the official 1.1.4 AppImage (SHA-256 checked against the release's own file),
# extracted so no FUSE is needed. GUI: /opt/freecad/AppRun; headless: freecadcmd (both on PATH).
#   docker build -t screen-lab-freecad:1.1.4 -f docker/freecad.Dockerfile docker
FROM screen-lab-base:1
RUN apt-get update && apt-get install -y --no-install-recommends \
      libxkbcommon0 libxkbcommon-x11-0 libfontconfig1 libfreetype6 libdbus-1-3 \
      libx11-xcb1 libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-render-util0 libxcb-xinerama0 libxcb-xkb1 \
      libxcb-cursor0 libxcb-shape0 libxcb-randr0 libxcb-xfixes0 libxrender1 libxi6 libsm6 libice6 libnss3 libasound2t64 \
 && rm -rf /var/lib/apt/lists/*
ARG FC=FreeCAD_1.1.4-Linux-x86_64-py311.AppImage
ARG FC_BASE=https://github.com/FreeCAD/FreeCAD/releases/download/1.1.4
WORKDIR /opt
RUN curl -fsSLO "$FC_BASE/$FC" && curl -fsSLO "$FC_BASE/$FC-SHA256.txt" && sha256sum -c "$FC-SHA256.txt" \
 && chmod +x "$FC" && ./"$FC" --appimage-extract > /dev/null && mv squashfs-root /opt/freecad \
 && cp "$FC-SHA256.txt" /opt/freecad/ && rm "$FC"
ENV PATH=/opt/freecad/usr/bin:$PATH
WORKDIR /kit
