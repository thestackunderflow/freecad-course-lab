#!/bin/bash
# Lesson 4, lab L4-Q6 (no AI, free): a fresh FreeCAD 1.1.4 with the socket on; a Claude run's logged tools/call requests
# replayed in order over the same plug (`uvx freecad-mcp@0.1.28`, our own client), message by message (the take's
# stages.txt marks where each message's calls end); after each message the part is saved and measured with the same
# freecadcmd line, then scored with the pre-registered rules. No mouse or key input. Writes out/l4/replay-RUN/.
#   FCC_PREFIX=fc4 tools/run.sh lab/replay4.sh B1
set -u
. /lab/lab/common.sh
RUN=${1:-B1}
R=/lab/out/l4/runs/$RUN
O=/lab/out/l4/replay-$RUN; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; addon_install; autostart_on true
sl_display $W $H
fc_start "$O/app.log" 1.5; sleep 8
cd /lab
cp /lab/out/l3/hand/back5.FCStd ~/hook-lesson3.FCStd
python3 -m lab.opendoc /home/maker/hook-lesson3.FCStd > "$O/opendoc.txt" 2>&1   # lesson 3's hook, as the runs started with
prev=0
for st in first after2; do
  n=$(awk -v s="$st" '$1 == s {print $2}' "$R/stages.txt")
  [ -n "$n" ] || continue
  sed -n "$((prev + 1)),${n}p" "$R/transcript.jsonl" > "$O/transcript-$st.jsonl"
  prev=$n
  python3 -m client.replay "$O/transcript-$st.jsonl" "$O/replay-$st.json" -- uvx freecad-mcp@0.1.28 > "$O/replay-$st.log" 2>&1
  sleep 2
  read -r DOC OBJ SK < <(python3 -m lab.newpart "$O/newpart-$st.json" 2>>"$O/lab-query.err")
  echo "$st $DOC $OBJ $SK" >> "$O/parts.txt"
  echo "$st $n" >> "$O/stages.txt"
  if [ -n "${DOC:-}" ]; then
    python3 -m lab.fcrpc save "$DOC" "/tmp/$st.FCStd" > "$O/save-$st.txt" 2>&1
    FC_DOC="/tmp/$st.FCStd" FC_OUT="$O/measure-$st.json" freecadcmd /lab/checker/measure.py > "$O/measure-$st.log" 2>&1
  fi
done
cp "$R/transcript.jsonl" "$O/transcript.jsonl"
SL_SHOT_WAKE=0 sl_shot "$O/after.png"
python3 -m checker.score_l4 "$O" > "$O/score.log" 2>&1
fc_quit; sl_display_stop
echo "replay done ($RUN)"; cat "$O/parts.txt"
