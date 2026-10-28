#!/bin/bash
# Take "web" (F8, F9; lab Q1): Firefox 158 (Mozilla's .deb, not a snap) on freecad.org's download page and on the
# add-on's GitHub page at tag v0.1.28; Code, Download ZIP. Real network. The ZIP's SHA-256 is checked afterwards.
#   tools/run.sh lab/take_web.sh
set -u
. /lab/lab/common.sh
O=/lab/out/l1/web; rm -rf "$O"; mkdir -p "$O" ~/Downloads /tmp/ffp
cp /lab/lab/firefox-user.js /tmp/ffp/user.js
sl_display $W $H
firefox --no-remote -profile /tmp/ffp about:blank > "$O/firefox.log" 2>&1 &
w=$(sl_wait_window "Mozilla Firefox" 90); sleep 4
wmctrl -i -r "$w" -b add,maximized_vert,maximized_horz; sleep 2
xdotool mousemove 1440 900
sl_record "$O"
sl_mark "recording started: Firefox"
sl_nap 1
sl_click 900 145 "address bar"
sl_type "freecad.org/downloads.php" "typed: freecad.org/downloads.php" 80
sl_key Return "freecad.org: Enter"
sl_glide 1000 1650 10
sl_nap 6
sl_glide 1300 640 30; sl_mark "hover: Current stable version"
sl_nap 3
sl_glide 600 1500 30; sl_mark "hover: Windows"
sl_nap 1.2
sl_glide 1290 1500 24; sl_mark "hover: Mac"
sl_nap 1.2
sl_glide 2000 1500 24; sl_mark "hover: Linux"
sl_nap 2
sl_shot "$O/freecad-org.png"
sl_click 900 145 "address bar 2"
sl_type "github.com/neka-nat/freecad-mcp/tree/v0.1.28" "typed: github tag page" 70
sl_key Return "github: Enter"
sl_glide 1000 1650 10
sl_nap 7
sl_glide 330 743 30; sl_mark "hover: tag v0.1.28"
sl_nap 2.5
sl_shot "$O/github.png"
sl_click 1924 743 "Code button"
sl_nap 2
sl_click 1407 1228 "Download ZIP"
sl_nap 5
sl_mark "download panel"
sl_nap 3
sl_shot "$O/downloaded.png"
sl_mark "recording stopped"
sl_stop
sha256sum ~/Downloads/*.zip > "$O/zip-sha256.txt"; ls -la ~/Downloads >> "$O/zip-sha256.txt"
grep -q e00c15a64b78bf64849b8f36f76d43d5faec89b91e70a092bb54a89f36ca2c74 "$O/zip-sha256.txt" && echo "zip matches the pinned tag ZIP" >> "$O/zip-sha256.txt"
curl -s https://www.freecad.org/downloads.php | grep -o 'Current stable version: [0-9.]*' | head -1 > "$O/curl-freecad-org.txt"
pkill firefox; sl_display_stop
echo "web take done"; cat "$O/zip-sha256.txt" "$O/curl-freecad-org.txt"
