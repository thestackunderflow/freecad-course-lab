#!/bin/bash
# fx20 G0b (LAB-fx20 section 1, GUI probe): stills only, no recording, no AI. Rung a (17, then 15, then 17 with the
# Reference box if REFXY is given), rung c (hook-red.FCStd). No socket query while a modal box is up (fx19 DEV 3).
#   FCC_PREFIX=fx20 FCC_DOCKER_ARGS="--network none -e REFXY='x y'" tools/run.sh lab/fx20_G0b.sh
set -u; REFXY=${REFXY:+${REFXY/_/ }}; NOTEXY=${NOTEXY:+${NOTEXY/_/ }}
. /lab/lab/common.sh; . /lab/lab/fx19_lib.sh; . /lab/lab/fx20_lib.sh
O=$X/G0/${G0RUN:-b}; mkdir -p "$O"; L=$O/g0b-log.txt; : > $L
fx_start "$O"
mkdir -p /tmp/fx20; cp /lab/out/l2/hand/hand.FCStd /tmp/fx20/hook.FCStd; cp $X/P/hook-red.FCStd /tmp/fx20/hook_red.FCStd
open_doc /tmp/fx20/hook.FCStd >> $L 2>&1
D() { timeout 25 python3 /lab/out/fx19/G0/g0bdump.py "$O/$1.json" > "$O/$1.txt" 2>&1 || echo "dump $1 failed" >> $L; }
S() { SL_SHOT_WAKE=0 sl_shot "$O/$1.png"; }
Q "import FreeCAD, FreeCADGui
p = FreeCAD.ParamGet('User parameter:BaseApp/Preferences/NotificationArea')
print('NonIntrusiveNotificationsEnabled', p.GetBool('NonIntrusiveNotificationsEnabled', True), '(default True if unset)')
print('NotificationTime', p.GetInt('NotificationTime', -1), 'MinimumOnScreenTime', p.GetInt('MinimumOnScreenTime', -1))
print('Sketcher_Dimension shortcut', repr(FreeCADGui.Command.get('Sketcher_Dimension').getShortcut()))
print('Sketcher_ConstrainDistance shortcut', repr(FreeCADGui.Command.get('Sketcher_ConstrainDistance').getShortcut()))" > $O/env-g0b.txt 2>&1
cat $O/env-g0b.txt >> $L
KEY=$(grep -o "Sketcher_Dimension shortcut '[^']*'" $O/env-g0b.txt | sed "s/.*shortcut '//;s/'//")
echo "dimension key: $KEY" >> $L
read -r SKX SKY < <(row_open hook Sketch); echo "Sketch row $SKX $SKY" >> $L
BASE=$(nwin); echo "windows $BASE" >> $L
xdotool mousemove "$SKX" "$SKY"; sleep 0.5; xdotool click --repeat 2 --delay 120 1; sleep 4
xdotool mousemove 1500 300; sleep 1
rv_clear
S g0b-0-edit; D g0b-0-edit
Q "import FreeCADGui
print('in edit: Sketcher_Dimension shortcut', repr(FreeCADGui.Command.get('Sketcher_Dimension').getShortcut()))
print('in edit: Sketcher_ConstrainDistance shortcut', repr(FreeCADGui.Command.get('Sketcher_ConstrainDistance').getShortcut()))
from PySide import QtWidgets
sb = FreeCADGui.getMainWindow().statusBar()
for w in sb.findChildren(QtWidgets.QWidget):
    if w.isVisible(): print('statusbar', w.metaObject().className(), repr(w.objectName()), repr(w.toolTip()[:80]), w.mapToGlobal(w.rect().center()).toTuple())" >> $O/env-g0b.txt 2>&1
KEY=$(grep -o "in edit: Sketcher_Dimension shortcut '[^']*'" $O/env-g0b.txt | sed "s/.*shortcut '//;s/'//")
DIMB=$(B Sketcher_Dimension); echo "dimension key '$KEY', toolbar button $DIMB" >> $L
sk_state hook >> $L 2>&1; solver_text >> $L 2>&1

try_size() {   # try_size TAG VALUE [ref]: Dimension key, click the arm top, place, (Reference box), type, Return
  local tag=$1 v=$2
  read -r AX AY < <(SP hook Sketch 4 mid); echo "$tag arm-top mid $AX $AY" >> $L
  xdotool mousemove 1500 300; sleep 0.5
  if [ -n "$KEY" ] && [ "${#KEY}" -eq 1 ]; then xdotool key --clearmodifiers "$(echo "$KEY" | tr 'A-Z' 'a-z')"; echo "$tag tool by key $KEY" >> $L
  else xdotool mousemove ${DIMB% *} ${DIMB#* }; sleep 0.6; xdotool click 1; echo "$tag tool by toolbar $DIMB" >> $L; fi; sleep 1
  xdotool mousemove "$AX" "$AY"; sleep 0.8; xdotool click 1; sleep 0.8
  xdotool mousemove "$AX" $((AY - 110)); sleep 0.8; xdotool click 1; sleep 2
  echo "$tag windows after place $(nwin)" >> $L
  S g0b-$tag-1-dialog
  if [ "${3:-}" = ref ]; then
    xdotool mousemove ${REFXY% *} ${REFXY#* }; sleep 0.5; xdotool click 1; sleep 1; S g0b-$tag-2-reftick
  else
    xdotool type --delay 200 "$v"; sleep 1; S g0b-$tag-2-typed
  fi
  xdotool key Return; sleep 0.6
  S g0b-$tag-3-after-0s; sleep 2.5; S g0b-$tag-4-after-3s
  echo "$tag windows after Return $(nwin) (base $BASE)" >> $L
  if [ "$(nwin)" -gt "$BASE" ]; then S g0b-$tag-4b-modal; sleep 1; xdotool key Return; sleep 1.5; echo "$tag modal closed by Return" >> $L; fi
  sleep 4.5; S g0b-$tag-5-after-8s; sleep 12; S g0b-$tag-6-after-20s
  D g0b-$tag-6-after-20s
  echo "$tag state after:" >> $L; sk_state hook >> $L 2>&1; solver_text >> $L 2>&1
}

open_list() {  # open_list TAG: the notification area's button in the status bar clicked; still; closed again
  local n; n=$(WG class NotificationArea); [ "$n" = none ] && n=${NOTEXY:-none}; echo "$1 notification area at $n" >> $L
  [ "$n" = none ] && return
  xdotool mousemove ${n% *} ${n#* }; sleep 0.5; xdotool click 1; sleep 2; S g0b-$1-7-list
  echo "$1 windows with the list $(nwin)" >> $L
  xdotool key Escape; sleep 1; xdotool mousemove 1500 300; sleep 0.5
}

try_size a17 17; open_list a17
try_size a15 15; open_list a15
[ -n "${REFXY:-}" ] && try_size aref 17 ref
S g0b-a-end

# rung c: hook-red.FCStd's red sketch
read -r ZX ZY < <(B text Close); echo "sketch Close $ZX $ZY" >> $L
[ "$ZX" != none ] && { xdotool mousemove "$ZX" "$ZY"; sleep 0.5; xdotool click 1; sleep 3; }
open_doc /tmp/fx20/hook_red.FCStd >> $L 2>&1; sleep 2
read -r RX RY < <(row_open hook_red Sketch); echo "red Sketch row $RX $RY" >> $L
S g0b-c-0-open; D g0b-c-0-open
xdotool mousemove "$RX" "$RY"; sleep 0.5; xdotool click --repeat 2 --delay 120 1; sleep 4; xdotool mousemove 1500 300; sleep 1
S g0b-c-1-edit; D g0b-c-1-edit; solver_text >> $L 2>&1
read -r NX NY < <(WG text "more)"); echo "numbers link $NX $NY" >> $L
if [ "$NX" != none ]; then xdotool mousemove "$NX" "$NY"; sleep 0.5; xdotool click 1; sleep 2; S g0b-c-2-numbers-clicked
  Q "import FreeCADGui; print('selection', FreeCADGui.Selection.getSelectionEx()[0].SubElementNames if FreeCADGui.Selection.getSelectionEx() else [])" >> $L 2>&1; fi
read -r ZX ZY < <(B text Close); echo "sketch Close $ZX $ZY" >> $L
[ "$ZX" != none ] && { xdotool mousemove "$ZX" "$ZY"; sleep 0.5; xdotool click 1; sleep 3; }
echo "windows after close $(nwin)" >> $L
[ "$(nwin)" -gt "$BASE" ] && { S g0b-c-3-box; xdotool key Return; sleep 1.5; }
S g0b-c-4-closed; D g0b-c-4-closed
echo "G0B-DONE" >> $L
fc_quit; sl_display_stop
echo "G0b done"
