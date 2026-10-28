# FreeCAD + Claude Course lab image (lesson 1, 28 Oct 2026): the screen-lab kit's FreeCAD 1.1.4 image plus what a
# viewer would add, each pinned, but NOT installed into the viewer's home: the install takes film the real installs.
#   /opt/pre/claude        Claude Code 2.1.308 (stable on the lab day), copied into ~/.local/bin by "after install" takes
#   /opt/pre/uv, uvx       uv 0.13.6 (SHA-256 checked), the same
#   /opt/pre/freecad-mcp-0.1.28.zip   the add-on's source ZIP from git tag v0.1.28 (SHA-256 checked); the takes copy
#                          addon/FreeCADMCP into FreeCAD's Mod folder, or film the copy
#   Firefox 158.0.1 (Mozilla APT, not a snap) and PCManFM (a file manager), to film the
#   web pages and the folders; unzip; a user "maker" so paths read like a person's (/home/maker).
#   docker build -t fcc-app:1.1.4-0.1.28 -f docker/fcc.Dockerfile docker
FROM screen-lab-freecad:1.1.4
ARG CLAUDE_VER=2.1.308
ARG UV_VER=0.13.6
ARG UV_SHA=f29c3e94ffabd7e6f3ba521dba169a9b7ec12100bf3257087f0f24f6123f3645
ARG FCMCP_SHA=e00c15a64b78bf64849b8f36f76d43d5faec89b91e70a092bb54a89f36ca2c74
ARG FF_VER=158.0.1~build1
RUN apt-get update && apt-get install -y --no-install-recommends \
      pcmanfm lxde-icon-theme gnome-icon-theme unzip python3-pip python3-venv procps psmisc imagemagick \
 && rm -rf /var/lib/apt/lists/*
# Firefox from Mozilla's own APT repository (a .deb, not Ubuntu's snap, which can't run in Docker). Probed 28 Oct:
# Playwright 1.63.0's bundled browser is now "Chrome for Testing", which shows a testing-only banner, so it was dropped.
RUN install -d -m 0755 /etc/apt/keyrings \
 && curl -fsSL https://packages.mozilla.org/apt/repo-signing-key.gpg -o /etc/apt/keyrings/packages.mozilla.org.asc \
 && echo "deb [signed-by=/etc/apt/keyrings/packages.mozilla.org.asc] https://packages.mozilla.org/apt mozilla main" \
      > /etc/apt/sources.list.d/mozilla.list \
 && printf 'Package: *\nPin: origin packages.mozilla.org\nPin-Priority: 1000\n' > /etc/apt/preferences.d/mozilla \
 && apt-get update && apt-get install -y --no-install-recommends firefox=$FF_VER \
 && rm -rf /var/lib/apt/lists/*
RUN mkdir -p /opt/pre && cd /opt/pre \
 && curl -fsSLo uv.tgz https://github.com/astral-sh/uv/releases/download/$UV_VER/uv-x86_64-unknown-linux-gnu.tar.gz \
 && echo "$UV_SHA  uv.tgz" | sha256sum -c - && tar xzf uv.tgz --strip-components=1 && rm uv.tgz && ./uv --version \
 && curl -fsSLo freecad-mcp-0.1.28.zip https://github.com/neka-nat/freecad-mcp/archive/refs/tags/v0.1.28.zip \
 && echo "$FCMCP_SHA  freecad-mcp-0.1.28.zip" | sha256sum -c -
RUN userdel -r ubuntu 2>/dev/null; useradd -m -u 1000 -s /bin/bash maker
USER maker
RUN curl -fsSL https://claude.ai/install.sh | bash -s $CLAUDE_VER && ~/.local/bin/claude --version
USER root
RUN cp -L /home/maker/.local/bin/claude /opt/pre/claude && /opt/pre/claude --version > /opt/pre/claude-version.txt \
 && rm -rf /home/maker/.local /home/maker/.claude* /home/maker/.cache && chmod -R a+rX /opt/pre
# xarchiver: the file manager's right-click "Extract Here" (as Explorer's "Extract All")
RUN apt-get update && apt-get install -y --no-install-recommends xarchiver && rm -rf /var/lib/apt/lists/*
ENV XCURSOR_SIZE=64 DISABLE_AUTOUPDATER=1 CLAUDE_CODE_DISABLE_AUTO_MEMORY=1 PYTHONPATH=/lab/vendor/screenlab-lib:/lab
WORKDIR /lab
