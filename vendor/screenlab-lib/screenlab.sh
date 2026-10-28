# screen-lab shell library: film a desktop app on a virtual screen with plain shell commands.
#   . /kit/lib/screenlab.sh
#   sl_display 2560 1440; sl_app app.log myapp; sl_maximise "My App"
#   sl_record out/take; sl_click 400 300 "New document"; sl_type 20 "length"; sl_key Return; sl_stop
# Positions are display pixels, or SL_UNITS="WxH" units scaled to the display. Every pause is multiplied by PACE.
# Events (sl_mark, and every click/type/key/drag) go to $SL_DIR/events.raw.jsonl with the wall clock; sl_stop turns
# them into events.jsonl with t = seconds from the first frame of screen.mp4 (the same time base as cursor.jsonl).
# A click is logged at the click, after its glide and the SL_PRE pause, not when the move began.

_SL_LIB=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
export PYTHONPATH="$_SL_LIB${PYTHONPATH:+:$PYTHONPATH}"
SL_DISPLAY=${SL_DISPLAY:-:99}
SL_STEP_S=${SL_STEP_S:-0.03}
PACE=${PACE:-1.0}

_sl_json_str() { local s=${1//\\/\\\\}; s=${s//\"/\\\"}; printf '"%s"' "$s"; }

_sl_event() {     # _sl_event TS LABEL [extra json fields, without braces]
  [ -n "${SL_DIR:-}" ] || return 0
  local extra=${3:+, $3}
  printf '{"ts": %s, "event": %s%s}\n' "$1" "$(_sl_json_str "$2")" "$extra" >> "$SL_DIR/events.raw.jsonl"
}

sl_nap() { sleep "$(awk -v s="$1" -v p="$PACE" 'BEGIN{v=s*p; if (v<0) v=0; print v}')"; }

sl_mark() { _sl_event "$(date +%s.%N)" "$1"; }

_sl_px() {        # _sl_px X Y -> display pixels
  if [ -n "${SL_UNITS:-}" ]; then
    awk -v x="$1" -v y="$2" -v u="$SL_UNITS" -v w="$SL_W" -v h="$SL_H" \
      'BEGIN{split(u, a, "x"); printf "%d %d\n", x*w/a[1] + 0.5, y*h/a[2] + 0.5}'
  else
    printf '%d %d\n' "$1" "$2"
  fi
}

_sl_path() {      # _sl_path TX TY [STEPS]: eased (cosine) straight line from the cursor to TX TY, display pixels
  local X Y SCREEN WINDOW px py
  eval "$(xdotool getmouselocation --shell)"
  while read -r px py; do
    xdotool mousemove "$px" "$py"; sleep "$SL_STEP_S"
  done < <(awk -v x="$X" -v y="$Y" -v tx="$1" -v ty="$2" -v n="${3:-0}" 'BEGIN{
    if (n < 1) { d = sqrt((tx-x)^2 + (ty-y)^2); n = int(12 + d/60); if (n > 36) n = 36 }
    for (i = 1; i <= n; i++) { e = (1 - cos(3.14159265358979 * i / n)) / 2
      if (i == n) printf "%d %d\n", tx, ty; else printf "%d %d\n", x + (tx-x)*e + 0.5, y + (ty-y)*e + 0.5 } }')
}

sl_glide() {      # sl_glide X Y [STEPS]
  local tx ty; read -r tx ty < <(_sl_px "$1" "$2")
  _sl_path "$tx" "$ty" "${3:-}"
}

sl_click() {      # sl_click X Y [LABEL] [BUTTON] [STEPS]
  local tx ty b=${4:-1}; read -r tx ty < <(_sl_px "$1" "$2")
  _sl_path "$tx" "$ty" "${5:-}"
  sl_nap "${SL_PRE:-0.25}"
  _sl_event "$(date +%s.%N)" "${3:-click}" "\"x\": $tx, \"y\": $ty, \"button\": $b"
  xdotool click "$b"
  sl_nap "${SL_HOLD:-0.6}"
}

sl_type() {       # sl_type TEXT [LABEL] [DELAY_MS]
  [ -n "${2:-}" ] && _sl_event "$(date +%s.%N)" "$2" "\"text\": $(_sl_json_str "$1")"
  xdotool type --delay "${3:-120}" -- "$1"
  sl_nap "${SL_HOLD:-0.6}"
}

sl_key() {        # sl_key KEYS [LABEL]
  [ -n "${2:-}" ] && _sl_event "$(date +%s.%N)" "$2" "\"keys\": $(_sl_json_str "$1")"
  xdotool key --clearmodifiers "$1"
  sl_nap "${SL_HOLD:-0.6}"
}

sl_drag() {       # sl_drag X1 Y1 X2 Y2 [LABEL] [BUTTON]
  local ax ay bx by b=${6:-1} l=${5:-drag}
  read -r ax ay < <(_sl_px "$1" "$2"); read -r bx by < <(_sl_px "$3" "$4")
  _sl_path "$ax" "$ay"; sl_nap 0.25
  _sl_event "$(date +%s.%N)" "$l" "\"x\": $ax, \"y\": $ay, \"button\": $b"
  xdotool mousedown "$b"; sleep 0.1
  _sl_path "$bx" "$by" 24; sleep 0.1
  _sl_event "$(date +%s.%N)" "$l: released" "\"x\": $bx, \"y\": $by, \"button\": $b"
  xdotool mouseup "$b"
  sl_nap "${SL_HOLD:-0.6}"
}

sl_wake() {       # repaint nudge for apps that draw only on input: 2 px over and back
  local X Y SCREEN WINDOW
  eval "$(xdotool getmouselocation --shell)"
  xdotool mousemove_relative -- 2 0; sleep 0.08; xdotool mousemove "$X" "$Y"; sleep "${SL_WAKE_S:-0.3}"
}

sl_wait_window() {  # sl_wait_window REGEX [TIMEOUT]: prints the first visible window id, or fails
  local end w; end=$(( $(date +%s) + ${2:-30} ))
  while :; do
    w=$(xdotool search --onlyvisible --name "$1" 2>/dev/null | head -1)
    [ -n "$w" ] && { echo "$w"; return 0; }
    [ "$(date +%s)" -ge "$end" ] && { echo "no window named '$1' within ${2:-30} s" >&2; return 1; }
    sleep 0.25
  done
}

sl_focus() { local w; w=$(sl_wait_window "$1" "${2:-30}") || return 1; xdotool windowactivate --sync "$w" windowfocus --sync "$w"; }

sl_maximise() {   # sl_maximise REGEX: fill the display (window manager maximise, explicit size as a fallback)
  local w; w=$(sl_wait_window "$1" "${2:-30}") || return 1
  wmctrl -i -r "$w" -b add,maximized_vert,maximized_horz 2>/dev/null; sleep 0.5
  local gw; gw=$(xdotool getwindowgeometry "$w" | awk '/Geometry/{split($2, a, "x"); print a[1]}')
  [ "${gw:-0}" -lt $(( SL_W * 9 / 10 )) ] && { xdotool windowsize --sync "$w" "$SL_W" "$SL_H"; xdotool windowmove --sync "$w" 0 0; }
  xdotool windowactivate --sync "$w" windowfocus --sync "$w"
}

sl_display() {    # sl_display W H [nowm]: Xvfb on $SL_DISPLAY, openbox, DISPLAY exported
  export SL_W=$1 SL_H=$2 DISPLAY=$SL_DISPLAY
  mkdir -p -m 700 "${XDG_RUNTIME_DIR:-/tmp/xdg}"
  Xvfb "$SL_DISPLAY" -screen 0 "${1}x${2}x24" -nolisten tcp -ac > /dev/null 2>&1 & SL_XVFB=$!
  local i; for i in $(seq 1 100); do [ -e "/tmp/.X11-unix/X${SL_DISPLAY#:}" ] && break; sleep 0.05; done
  if [ "${3:-}" != nowm ]; then openbox > /dev/null 2>&1 & SL_WM=$!; sleep 0.5; fi
}

sl_display_stop() { [ -n "${SL_WM:-}" ] && kill "$SL_WM" 2>/dev/null; [ -n "${SL_XVFB:-}" ] && kill "$SL_XVFB" 2>/dev/null; SL_WM=; SL_XVFB=; }

sl_app() {        # sl_app LOG cmd...: start an app on the display; its pid in SL_APP
  local log=$1; shift
  "$@" > "$log" 2>&1 & SL_APP=$!
}

sl_record() {     # sl_record DIR [nomouse]: 30 fps, CRF 14, cursor log; returns once the first frame is stamped
  export SL_DIR=$1; mkdir -p "$SL_DIR"; rm -f "$SL_DIR/.stop" "$SL_DIR/.recording"
  python3 -m screenlab.recorder "$SL_DIR" "$SL_W" "$SL_H" --display "${DISPLAY:-$SL_DISPLAY}" ${2:+--nomouse} & SL_REC=$!
  local i; for i in $(seq 1 200); do [ -s "$SL_DIR/.recording" ] && return 0; sleep 0.05; done
  echo "recorder did not start" >&2; return 1
}

sl_stop() {       # stop cleanly; writes cursor.jsonl, events.jsonl, record.json
  touch "$SL_DIR/.stop"; wait "$SL_REC" 2>/dev/null; SL_REC=
}

sl_shot() {       # sl_shot FILE.png: the display now (after a repaint nudge unless SL_SHOT_WAKE=0)
  [ "${SL_SHOT_WAKE:-1}" = 1 ] && sl_wake
  ffmpeg -v error -y -f x11grab -video_size "${SL_W}x${SL_H}" -i "${DISPLAY:-$SL_DISPLAY}" -frames:v 1 -update 1 "$1"
}
