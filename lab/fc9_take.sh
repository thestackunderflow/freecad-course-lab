#!/bin/bash
# fc9 takes (PLAN 4.2), FreeCAD 1.1.4 by hand, no AI. Recipes from G0 (out/fc9/G0/VERDICT.txt).
#   FCC_PREFIX=fc9 FCC_DOCKER_ARGS="--network none" tools/run.sh lab/fc9_take.sh A|B|C
#   A  trap: start file; Hook -> LinearPattern; Direction Base X-axis; Mode Extent shown; Length 180; Occurrences 5;
#      the toast; OK; top view; Measure hook 4 -> strip end, strip end -> hook 5 (floating)           F0 F3 F6 F7 F10 S0
#   B  fix: A's file; double-click LinearPattern; Length 120; OK; top view; Measure left end, right end   F1 F11 S2
#   C  proof: B's file; Length = formula, Occurrences = Params.hooks (Expression Editor); Params rack_width 220,
#      hooks 6; Recompute; top view; Measure left end, right end                                        F13 F14
#   P1 pickup (rev 3): start file (180 / 5, no pattern); double-click Params; the four rows shown; hold    F4
#   P2 pickup (rev 3): start file; top view; Measure strip end edge -> hook 1 outer edge (20.00)          F5
set -u
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh; . /lab/lab/fc9_lib.sh
T=$1; O=$X/$T; mkdir -p $O; L=$O/take.log; : > $L
case $T in A|P1|P2) SRC=$X/P/rack-start.FCStd;; B) SRC=$X/A/end.FCStd;; C) SRC=$X/B/end.FCStd;; *) echo "A|B|C|P1|P2"; exit 2;; esac
F=rack
fx_start $O
mkdir -p /tmp/fc9; cp "$SRC" /tmp/fc9/$F.FCStd
open_doc /tmp/fc9/$F.FCStd >> $L 2>&1; FQ "prep('$F')" >> $L 2>&1
Q "import FreeCADGui
FreeCADGui.getDocument('$F').activeView().setAnimationEnabled(False)
print(1)" >> $L 2>&1
report_hide; sleep 2; xdotool mousemove 1500 1500; rv_clear

field() {      # field LABEL TEXT: triple-click the task-panel field on row LABEL, type TEXT, Tab
  local p; p=$(FQ "field_pos('$1')"); [ "$p" != none ] || { echo "no field $1" >> $L; return 1; }
  sl_glide $(( ${p% *} - 40 )) ${p#* } 20; sl_nap 0.6
  xdotool click --repeat 3 --delay 90 1; sl_mark "$1: select"; sl_nap 0.4
  sl_type "$2" "$1: typed $2" 220; sl_nap 0.6; sl_key Tab "Tab"; sl_nap 2.5
  echo "$1 = $2: $(FQ "pattern_state('$F')")" >> $L
}

formula() {    # formula LABEL EXPR: "=" opens the Expression Editor; type; Return closes the name list; editor OK
  local p; p=$(FQ "field_pos('$1')"); [ "$p" != none ] || { echo "no field $1" >> $L; return 1; }
  sl_glide $(( ${p% *} - 40 )) ${p#* } 20; sl_nap 0.6
  sl_click $(( ${p% *} - 40 )) ${p#* } "$1: click"; xdotool key ctrl+a; sl_nap 0.4
  sl_type "=" "$1: typed = (Expression Editor)" 200; sl_nap 1.5
  sl_type "$2" "$1: typed $2" 110; sl_nap 1.5
  sl_key Return "Return: name list closed"; sl_nap 1.5
  shot $O/expr-$1.png
  at "$(FQ "expr_ok()")" "Expression Editor: OK"; sl_nap 2.5
  echo "$1 = $2: $(FQ "pattern_state('$F')")" >> $L
}

topview() {
  sl_glide 1500 1200 15; sl_key 2 "key 2: top view"; sl_nap 0.5
  Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewTop(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L
  sl_mark "(view fitted)"; sl_nap 2
}

isofit() {
  sl_key 0 "key 0: isometric"; sl_nap 0.5
  Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewIsometric(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L
  sl_mark "(view fitted)"; sl_nap 2
}

m() {          # m NAME X1 Y1 X2 Y2 [WHEEL [Pan]]: Measure between the top edge at (X1, Y1, 60) and the one at (X2, Y2,
               # 60); WHEEL: first the top view, then that many wheel clicks on the middle of the two (zoom in, ~1.2x
               # each); Pan: before zooming, a middle-button drag moves the middle 900 px left (the task panel on the
               # right takes the wheel and the clicks over it)
  local p i z=60 mid
  if [ -n "${6:-}" ]; then
    topview
    mid="$(awk -v a=$2 -v b=$4 'BEGIN{print (a+b)/2}') $(awk -v a=$3 -v b=$5 'BEGIN{print (a+b)/2}') $z"
    p=$(vp $mid)
    if [ "${7:-}" = Pan ]; then
      sl_glide ${p% *} ${p#* } 25; sl_nap 0.5; sl_mark "middle-drag: pan left"; xdotool mousedown 2; sleep 0.15
      for i in $(seq 1 30); do xdotool mousemove $(( ${p% *} - 30 * i )) ${p#* }; sleep 0.04; done
      sleep 0.2; xdotool mouseup 2; sl_nap 1
      p=$(vp $mid); echo "$1 after pan $p" >> $L
    fi
    sl_glide ${p% *} ${p#* } 25; sl_nap 0.6
    for i in $(seq 1 $6); do xdotool click 4; sleep 0.15; done; sl_mark "wheel: zoom in on $1"; sl_nap 1.5
  fi
  p=$(vp "$2" "$3" $z "$4" "$5" $z); echo "$1 edges $p" >> $L; set -- "$1" $p
  btn Std_Measure "Measure"; sl_nap 2
  sl_glide $2 $3 25; sl_nap 0.8; sl_click $2 $3 "$1: first edge"; sl_nap 1.5
  sl_glide $4 $5 25; sl_nap 0.8; xdotool keydown ctrl; sl_click $4 $5 "$1: Ctrl + second edge"; xdotool keyup ctrl
  sl_nap 3.5
  echo "$1 measure: $(FQ "task_texts()" | grep -o 'field:[^"]*\|combo:[^"]*' | tr '\n' ' ')" >> $L
  shot $O/measure-$1.png; sl_nap 2
  at "$(taskpos any Close)" "Measure: Close"; sl_nap 1.5
}

ROW() {       # the tree row, asked up to 6 times (the tree fills a little after the file opens)
  local p i
  for i in 1 2 3 4 5 6; do
    p=$(cd /lab && timeout 20 python3 -m lab.fcrpc row "$@" 2>/dev/null)
    [ -n "$p" ] && [ "$p" != none ] && { echo "$p"; return 0; }
    sleep 2
  done
  echo none
}

bail() { echo "BAIL: $1" >> $L; sl_stop; fc_quit; sl_display_stop; exit 1; }

dblrow() {     # dblrow OBJ LABEL: double-click a tree row
  local p; p=$(ROW $F "$1"); sl_glide ${p% *} ${p#* } 20; sl_nap 0.5
  sl_mark "$2"; xdotool click --repeat 2 --delay 120 1; sl_nap 3
}

xdotool mousemove 1500 1500
echo "rows open: $(row_open $F Hook) $(row_open $F LinearPattern 2>/dev/null)" >> $L; xdotool mousemove 1500 1500; sleep 1
sl_record "$O"; sl_mark "recording started: FreeCAD 1.1.4, rack.FCStd open ($T)"
sl_nap 3
case $T in
A)
  rowclk $F Hook "tree: Hook (the Pad)" || bail "no Hook row"; sl_nap 1
  btn PartDesign_LinearPattern "LinearPattern"; sl_nap 3
  shot $O/panel-open.png
  c=$(FQ "combo_pos('Horizontal sketch axis')"); echo "direction box $c" >> $L; [ "$c" != none ] || bail "no direction box"
  at "$c" "Direction box"; sl_nap 1.5
  shot $O/direction-list.png
  at "$(( ${c% *} - 150 )) $(( ${c#* } + 120 ))" "Direction: Base X-axis"; sl_nap 2
  echo "direction: $(FQ "pattern_state('$F')")" >> $L
  c=$(FQ "combo_pos('Extent')"); sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Mode Extent"; sl_nap 2.5
  field Length 180
  field Occurrences 5
  sl_nap 3; shot $O/trap-panel.png
  at "2430 615" "OK"; sl_nap 3
  isofit; sl_nap 2; shot $O/trap-iso.png; sl_nap 2
  topview; shot $O/trap-top.png
  m end-hook5 180 2.5 200 -2.5
  m hook4-end 175 -2.5 180 2.5 9
  ;;
B)
  dblrow LinearPattern "double-click: LinearPattern (edit)"
  field Length 120
  sl_nap 2; shot $O/fix-panel.png
  at "2430 615" "OK"; sl_nap 3
  isofit; shot $O/fix-iso.png; sl_nap 2
  topview; shot $O/fix-top.png
  m left 0 2.5 20 -2.5 6
  m right 160 -2.5 180 2.5 6 Pan
  ;;
C)
  dblrow LinearPattern "double-click: LinearPattern (edit)"
  formula Length "Params.rack_width - 2 * Params.margin - Params.width"
  formula Occurrences "Params.hooks"
  sl_nap 1.5; shot $O/formula-panel.png
  at "2430 615" "OK"; sl_nap 3
  dblrow Params "double-click: open Params"
  c=$(B cell 0 1); echo "rack_width cell $c" >> $L
  at "$c" "cell B1: rack_width = 180"; sl_nap 1
  sl_type "220" "typed 220" 250; sl_key Return "Enter"; sl_nap 1.5
  c=$(B cell 3 1); echo "hooks cell $c" >> $L
  at "$c" "cell B4: hooks = 5"; sl_nap 1
  sl_type "6" "typed 6" 250; sl_key Return "Enter"; sl_nap 1.5
  shot $O/params-220-6.png
  btn Std_Refresh "Recompute"; sl_nap 3
  t=$(B tab "$F"); echo "3D tab $t" >> $L; at "$t" "tab: back to the 3D view"; sl_nap 2
  echo "after recompute: $(FQ "pattern_state('$F')")" >> $L
  isofit; shot $O/proof-iso.png; sl_nap 2
  topview; shot $O/proof-top.png
  m left 0 2.5 20 -2.5 6
  # right end: GUI Measure failed twice in B (task panel over the right end; DEVIATIONS 4): by code only
  ;;
P1)
  dblrow Params "double-click: open Params"
  sl_nap 2
  for r in 0 1 2 3; do
    c=$(B cell $r 1); echo "row $r cell $c" >> $L
    sl_glide ${c% *} ${c#* } 20; sl_mark "hover: Params row $((r + 1))"; sl_nap 1.8
  done
  xdotool mousemove 1500 1500; sl_nap 3
  shot $O/params-180-5.png; sl_nap 3
  echo "params: $(FQ "pattern_state('$F')")" >> $L
  ;;
P2)
  isofit; shot $O/start-iso.png; sl_nap 2
  m left 0 2.5 20 -2.5 6
  ;;
esac
sl_nap 2; sl_stop
lab_save $F $O/end.FCStd >> $L 2>&1
echo "TAKE $T DONE" >> $L
fc_quit; sl_display_stop
check_doc $O/end.FCStd $O/check.json >> $L
