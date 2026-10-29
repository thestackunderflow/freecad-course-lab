# screen-lab base image: a virtual screen to film any Linux desktop app for real.
#   Xvfb (the screen) + openbox (a light window manager, so windows can be moved, sized and focused)
#   xdotool + wmctrl (a fake mouse and keyboard), ffmpeg (x11grab recording), Mesa llvmpipe (software OpenGL and
#   Vulkan for 3D apps), fonts, a large cursor theme (reads on a phone), xterm + tmux (to film a terminal beside the app)
#   and Python 3 with pytest, PyYAML and numpy for the kit's library, take runner and tests.
# Per-app images are layered on top: FROM screen-lab-base:1 (see docker/freecad.Dockerfile).
#   docker build -t screen-lab-base:1 -f docker/base.Dockerfile docker
FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update \
 && apt-get install -y --no-install-recommends ca-certificates curl \
      xvfb xauth x11-utils x11-xserver-utils xdotool wmctrl openbox \
      ffmpeg \
      libgl1 libegl1 libgl1-mesa-dri libglx-mesa0 libegl-mesa0 libglu1-mesa mesa-utils mesa-vulkan-drivers libvulkan1 \
      fonts-dejavu-core fonts-liberation2 dmz-cursor-theme \
      xterm tmux \
      python3 python3-pytest python3-yaml python3-numpy \
 && rm -rf /var/lib/apt/lists/*
# Software rendering everywhere; X11 (not Wayland) for Qt and GTK apps; a UTF-8 locale for terminals.
ENV LIBGL_ALWAYS_SOFTWARE=1 GALLIUM_DRIVER=llvmpipe \
    QT_QPA_PLATFORM=xcb GDK_BACKEND=x11 \
    XCURSOR_THEME=DMZ-White XCURSOR_SIZE=48 \
    LANG=C.UTF-8 LC_ALL=C.UTF-8 \
    XDG_RUNTIME_DIR=/tmp/xdg \
    PYTHONPATH=/kit/lib PYTHONDONTWRITEBYTECODE=1
WORKDIR /kit
