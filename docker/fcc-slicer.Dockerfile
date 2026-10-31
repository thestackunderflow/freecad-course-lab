# FreeCAD + Claude Course lesson 5 (31 Oct 2026): PrusaSlicer on the virtual screen, to film a real slicer.
# PrusaSlicer 2.9.2 = Debian trixie's package 2.9.2+dfsg-1 (with GUI support), the image habs-slicer:0.2 (id
# 441dc65153f3, built 19 Oct 2026 for another lab: `apt-get install prusa-slicer python3`), plus the screen-lab kit's
# filming layer as in its base image (Xvfb, openbox, xdotool, wmctrl, ffmpeg x11grab, Mesa llvmpipe, fonts, a large
# cursor, Python 3 with numpy and PyYAML for the kit's library). No network at run time.
#   docker build -t fcc-slicer:2.9.2 -f docker/fcc-slicer.Dockerfile docker
FROM habs-slicer:0.2
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates \
      xvfb xauth x11-utils x11-xserver-utils xdotool wmctrl openbox ffmpeg \
      libgl1 libegl1 libgl1-mesa-dri libglx-mesa0 libegl-mesa0 libglu1-mesa mesa-utils \
      fonts-dejavu-core fonts-liberation2 dmz-cursor-theme python3-numpy python3-yaml procps locales \
 && rm -rf /var/lib/apt/lists/* \
 && dpkg -s prusa-slicer | grep '^Version: 2.9.2+dfsg-1$' \
 && sed -i 's/^# *en_US.UTF-8/en_US.UTF-8/' /etc/locale.gen && locale-gen
RUN useradd -m -u 1000 -s /bin/bash maker
ENV LIBGL_ALWAYS_SOFTWARE=1 GALLIUM_DRIVER=llvmpipe GDK_BACKEND=x11 \
    XCURSOR_THEME=DMZ-White XCURSOR_SIZE=64 LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8 XDG_RUNTIME_DIR=/tmp/xdg \
    PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=/lab/vendor/screenlab-lib:/lab
USER maker
WORKDIR /lab
