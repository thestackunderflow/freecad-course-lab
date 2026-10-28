# Lesson 1 helpers on top of the screen-lab kit's shell library (vendored). Sourced by every take inside
# fcc-app:1.1.4-0.1.28, run as the user "maker". A 2880x1800 virtual display; positions are display pixels.
#   . /lab/lab/common.sh
. /lab/vendor/screenlab-lib/screenlab.sh
export W=${W:-2880} H=${H:-1800}
FC_APP=/opt/freecad/AppRun
FC_DATA=$HOME/.local/share/FreeCAD/v1-1

fc_start() {      # fc_start LOG [QT_SCALE]: FreeCAD's window; returns when it exists
  QT_SCALE_FACTOR=${2:-1.8} sl_app "$1" "$FC_APP"
  FC_PID=$SL_APP
  sl_wait_window "FreeCAD" 180 > /dev/null
}

fc_quit() {       # close FreeCAD without saving (Ctrl+Q, then "Discard" if asked; TERM as a fallback)
  [ -n "${FC_PID:-}" ] || return 0
  kill "$FC_PID" 2>/dev/null; sleep 2; kill -9 "$FC_PID" 2>/dev/null; FC_PID=
  pkill -x freecad 2>/dev/null; sleep 0.5
}

place() {         # place REGEX X Y WIDTH HEIGHT: a window's outer position and size
  local w; w=$(sl_wait_window "$1" 60) || return 1
  wmctrl -i -r "$w" -b remove,maximized_vert,maximized_horz 2>/dev/null
  xdotool windowsize --sync "$w" "$4" "$5"; xdotool windowmove --sync "$w" "$2" "$3"
}

term_open() {     # term_open NAME X Y COLS ROWS [FONT_PX] [CMD...]: an xterm titled NAME with a tmux session NAME
  local name=$1 x=$2 y=$3 c=$4 r=$5 fs=${6:-30}; shift 6 2>/dev/null || shift $#
  local cmd=${*:-bash}
  printf 'set -g status off\nset -g mouse off\nset -g history-limit 20000\n' > "$HOME/.tmux.conf"
  xterm -u8 -T "$name" -fa "DejaVu Sans Mono" -fs "$fs" -bg white -fg black -cr black -geometry "${c}x${r}+${x}+${y}" \
    -e tmux -u new-session -s "$name" -x "$c" -y "$r" "exec $cmd" > /dev/null 2>&1 &
  sl_wait_window "^$name\$" 30 > /dev/null
  local i; for i in $(seq 1 50); do tmux has-session -t "$name" 2>/dev/null && break; sleep 0.1; done
  sleep 0.6
}

term_focus() { local w; w=$(sl_wait_window "^$1\$" 10) && xdotool windowactivate --sync "$w" windowfocus --sync "$w"; }

pane() { tmux capture-pane -p -t "$1" ${2:+-S -$2}; }

wait_pane() {     # wait_pane NAME REGEX [TIMEOUT]: until the terminal shows REGEX
  local end=$(( $(date +%s) + ${3:-60} ))
  until pane "$1" 3000 | grep -qE "$2"; do [ "$(date +%s)" -ge "$end" ] && return 1; sleep 0.3; done
}

say_cmd() {       # say_cmd NAME "command" [LABEL]: type a shell command at a person's pace (real keys), then Enter
  term_focus "$1"
  sl_type "$2" "${3:-typed: $2}" 70
  sl_key Return "${3:-typed: $2}: Enter"
}

addon_install() { # not filmed: the add-on folder copied into Mod, as F9-F10 film it
  mkdir -p "$FC_DATA/Mod" && rm -rf /tmp/fcmcp && mkdir -p /tmp/fcmcp && unzip -q /opt/pre/freecad-mcp-0.1.28.zip -d /tmp/fcmcp \
    && cp -r /tmp/fcmcp/freecad-mcp-0.1.28/addon/FreeCADMCP "$FC_DATA/Mod/"
}

autostart_on() {  # not filmed: the add-on's own "Auto-Start Server" setting, written where the add-on reads it
  mkdir -p "$FC_DATA"
  printf '{\n  "remote_enabled": false,\n  "allowed_ips": "127.0.0.1",\n  "auto_start_rpc": %s,\n  "auth_token": ""\n}\n' "${1:-true}" \
    > "$FC_DATA/freecad_mcp_settings.json"
}

tools_install() { # not filmed: Claude Code and uv where their installers put them
  mkdir -p "$HOME/.local/bin" && cp /opt/pre/claude /opt/pre/uv /opt/pre/uvx "$HOME/.local/bin/"
  grep -q 'local/bin' "$HOME/.bashrc" 2>/dev/null || echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$HOME/.bashrc"
  export PATH="$HOME/.local/bin:$PATH"
}

claude_home() {   # not filmed: Claude Code's first-run screens already passed (theme, trust for the project folder)
  mkdir -p "$HOME/.claude" "$1"
  python3 - "$1" <<'EOF'
import json, os, sys
p = os.path.expanduser('~/.claude.json')
d = json.load(open(p)) if os.path.exists(p) else {}
d.update({'hasCompletedOnboarding': True, 'theme': 'light'})
d.setdefault('projects', {})[sys.argv[1]] = {'hasTrustDialogAccepted': True, 'hasCompletedProjectOnboarding': True}
json.dump(d, open(p, 'w'), indent=1)
EOF
}

fc_setup_rpc() {  # not filmed: FreeCAD set up through its own socket (the by-hand Cube document, the console shown)
  python3 - <<'PY'
import sys; sys.path.insert(0, '/lab')
from lab import fcrpc
fcrpc.run("""import FreeCAD, FreeCADGui
from PySide import QtWidgets
d = FreeCAD.newDocument('Unnamed')
b = d.addObject('Part::Box', 'Box'); b.Label = 'Cube'; b.Length = 5; b.Width = 20; b.Height = 60
d.recompute()
FreeCADGui.activeDocument().activeView().viewIsometric()
FreeCADGui.SendMsgToActiveView('ViewFit')
for w in FreeCADGui.getMainWindow().findChildren(QtWidgets.QDockWidget):
    if w.objectName() in ('Python console',):
        w.show()
print('ok')""")
PY
}
