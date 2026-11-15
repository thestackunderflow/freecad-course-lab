# Task R (14 Nov 2026): the lesson 1 image with the add-on source ZIP of freecad-mcp's git tag v0.1.31 beside 0.1.28
# (SHA-256 checked). Everything else (FreeCAD 1.1.4, Claude Code 2.1.308, uv 0.13.6) is the 0.1.28 image unchanged.
#   docker build -t fcc-app:1.1.4-0.1.31 -f docker/fcc-031.Dockerfile docker
FROM fcc-app:1.1.4-0.1.28
ARG FCMCP31_SHA=2fe7dc0e9d0a4367e5a945872d66632c0593253697060d5a3577415dc6adf172
RUN cd /opt/pre && curl -fsSLo freecad-mcp-0.1.31.zip https://github.com/neka-nat/freecad-mcp/archive/refs/tags/v0.1.31.zip \
 && echo "$FCMCP31_SHA  freecad-mcp-0.1.31.zip" | sha256sum -c - && chmod a+r freecad-mcp-0.1.31.zip
