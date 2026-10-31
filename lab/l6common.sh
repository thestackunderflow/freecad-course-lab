# Lesson 6 helpers (sourced after lab/common.sh, inside a take that is recording): FreeCAD's own tape measure,
# Tools > Measure, driven like a person (menu, the Mode list by keys, clicks on the part; Ctrl for the second pick).
# Positions come from lab/l6pick (the part's live shape), so they follow whatever a run did to the part.
# Probe (31 Oct): without Ctrl the second click replaces the first; any socket query clears the Result, so it is read
# once, right after the last pick, and nothing queries the socket while the result is held for the camera.
#   . /lab/lab/l6common.sh
P6() { python3 -m lab.l6pick "$@" 2>>"${O:-/tmp}/lab-query.err"; }

m6_aim() {           # m6_aim WHAT X Y: glide there; if FreeCAD does not preselect WHAT (plate, lipedge, hole, round),
                     # nudge the cursor in small steps around the point until it does (a person's small correction);
                     # prints the final "x y" (the start point if nothing fits: logged as a miss)
  local what=$1 x=$2 y=$3 dx dy r
  sl_glide "$x" "$y" 20; sl_nap 0.5
  case "$(P6 hit "$what")" in yes*) echo "$x $y"; return 0;; esac
  for r in 6 12 18 24 32 40 50 60 72; do
    for dx in 0 $r -$r; do for dy in 0 $r -$r; do
      [ "$dx" = 0 ] && [ "$dy" = 0 ] && continue
      xdotool mousemove $((x + dx)) $((y + dy)); sleep 0.25
      case "$(P6 hit "$what")" in yes*) sl_mark "aim: $what found at +$dx +$dy"; echo "$((x + dx)) $((y + dy))"; return 0;; esac
    done; done
  done
  sl_mark "aim: $what NOT found near $x $y"; echo "$x $y"
}

m6_view() {          # m6_view: click an empty spot of the 3D view, key 0, V, F (the corner view, fitted)
  local vx vy; read -r vx vy < <(python3 -m lab.button view 2>>"${O:-/tmp}/lab-query.err")
  sl_click "$vx" "$vy" "the 3D view: an empty spot"; sl_nap 0.4
  sl_key 0 "key 0: isometric"; sl_key v "key V"; sl_key f "key F (fit all)"; sl_nap 1.5
}

m6_tool() {          # m6_tool MODE_INDEX LABEL: Tools > Measure, then the Mode list: Home, Down x N, Enter
  local mx my cx cy i
  read -r mx my < <(python3 -m lab.button menu Tools 2>>"${O:-/tmp}/lab-query.err")
  sl_click "$mx" "$my" "Tools menu"; sl_nap 0.9
  sl_glide $((mx + 60)) $((my + 86)) 12; sl_nap 0.4
  sl_click $((mx + 60)) $((my + 86)) "Tools: Measure"; sl_nap 2.0
  read -r cx cy < <(P6 combo)
  sl_click "$cx" "$cy" "Measurement: the Mode list"; sl_nap 0.8
  sl_key Home "Mode list: top (Auto)"
  for ((i = 0; i < $1; i++)); do sl_key Down "Mode list: down"; sl_nap 0.15; done
  sl_nap 0.5; sl_key Return "Mode: $2"; sl_nap 1.0
}

m6_hold() {          # m6_hold SECONDS FILE: read the Result once into FILE, then hold still for the camera
  P6 result > "$2"; sl_mark "Result: $(cat "$2")"; sl_nap "$1"
}

m6_close() {
  local bx by; read -r bx by < <(P6 close)
  [ -n "${by:-}" ] && sl_click "$bx" "$by" "Measurement: Close"; sl_nap 1.2
}

m6_opening() {       # m6_opening FILE [HOLD]: Distance; the plate's inner face; Ctrl + the lip's inner top edge
  local ax ay bx by
  m6_tool 1 Distance
  read -r ax ay bx by < <(P6 opening)
  read -r ax ay < <(m6_aim plate "$ax" "$ay")
  sl_mark "hover: the back plate's inside face"; sl_nap 0.8
  sl_click "$ax" "$ay" "click: the back plate's inside face"; sl_nap 1.0
  read -r bx by < <(m6_aim lipedge "$bx" "$by")
  sl_mark "hover: the lip's inside top edge"; sl_nap 0.8
  xdotool keydown ctrl; sl_mark "key: hold Ctrl"
  sl_click "$bx" "$by" "Ctrl + click: the lip's inside top edge"
  xdotool keyup ctrl; sl_nap 0.8
  m6_hold "${2:-4.5}" "$1"
}

m6_radius() {        # m6_radius WHAT(hole|round) FILE [HOLD]: Radius; one click on a hole's rim / the lip's end curve
  local x y
  m6_tool 7 Radius
  read -r x y < <(P6 "$1")
  read -r x y < <(m6_aim "$1" "$x" "$y")
  sl_mark "hover: $1"; sl_nap 1.0
  sl_click "$x" "$y" "click: $1"; sl_nap 0.8
  m6_hold "${3:-4.5}" "$2"
}
