#!/bin/bash
# Lesson 7 probe ($0, no AI, not filmed): every failure reproduced once on the virtual display, its exact words saved
# to out/l7/probe/ (screenshots + the test script's printed replies + Claude Code's own `claude mcp` lines).
#   tools/run.sh lab/l7probe.sh
set -u
. /lab/lab/common.sh
O=/lab/out/l7/probe; rm -rf "$O"; mkdir -p "$O"
cd ~ && tar xzf /lab/out/scratch/seed/fc-profile.tgz
tools_install; mkdir -p ~/hook ~/parts; claude_home /home/maker/hook; claude_home /home/maker/parts
mkdir -p ~/bin; printf '#!/bin/sh\nexec python3 -m lab.l7call "$@"\n' > ~/bin/test-call; chmod +x ~/bin/test-call
export PATH="$HOME/bin:$PATH" L7_LOG=$O/test-call.jsonl
uvx freecad-mcp@0.1.28 --help > /dev/null 2>&1
tc() { echo "\$ test-call $*" >> "$O/$1.txt"; ( cd /lab && test-call "$@" ) >> "$O/$1.txt" 2>&1; echo "exit $?" >> "$O/$1.txt"; }
shot() { SL_SHOT_WAKE=0 sl_shot "$O/$1.png"; }
run() { local f=$1; shift; { echo "\$ $*"; "$@"; echo "exit $?"; } >> "$O/$f.txt" 2>&1; }

# --- check 1: the plug added with the default (local) scope in ~/hook, then listed from another folder
cd ~/hook
run c1-local claude mcp add freecad -- uvx freecad-mcp@0.1.28
run c1-local claude mcp list
cd ~/parts
run c1-local claude mcp list
cd ~/hook
run c1-local claude mcp remove freecad
run c1-local claude mcp add --scope user freecad -- uvx freecad-mcp@0.1.28
cd ~/parts
run c1-local claude mcp list
cp ~/.claude.json "$O/claude-json-after.json"

# --- check 2: uv missing (the plug's program not found)
mv ~/.local/bin/uvx ~/.local/bin/uvx.off; mv ~/.local/bin/uv ~/.local/bin/uv.off; hash -r
run c2-nouv claude mcp list
run c2-nouv claude mcp get freecad
mv ~/.local/bin/uvx.off ~/.local/bin/uvx; mv ~/.local/bin/uv.off ~/.local/bin/uv; hash -r
run c2-nouv claude mcp list

# --- check 3a: FreeCAD closed
run c3-closed claude mcp list
tc list_documents; mv "$O/list_documents.txt" "$O/c3-closed-call.txt"

sl_display $W $H
# --- check 3b: FreeCAD open, the add-on NOT installed (no Mod folder)
fc_start "$O/app-noaddon.log" 1.5; sleep 8
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 2; shot c3-noaddon
ls -la "$FC_DATA" > "$O/c3-noaddon-profile.txt" 2>&1
tc list_documents; mv "$O/list_documents.txt" "$O/c3-noaddon-call.txt"
fc_quit

# --- check 3c: the add-on installed, the server not started (Auto-Start off, the default)
addon_install; autostart_on false
fc_start "$O/app-nostart.log" 1.5; sleep 8
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 2; shot c3-nostart
tc list_documents; mv "$O/list_documents.txt" "$O/c3-nostart-call.txt"
fc_quit

# --- check 3d: started (Auto-Start on): the same call passes
autostart_on true
fc_start "$O/app-start.log" 1.5; sleep 10
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 2; shot c3-started
tc list_documents; mv "$O/list_documents.txt" "$O/c3-started-call.txt"
tc get_rpc_status; mv "$O/get_rpc_status.txt" "$O/c3-status-call.txt"
python3 -m lab.button Start_RPC_Server > "$O/btn-start.txt" 2>&1
python3 -m lab.button Stop_RPC_Server > "$O/btn-stop.txt" 2>&1

# --- check 4: errors inside a tool call (the server up, a document with lesson 3's hook open)
cp /lab/out/l3/hand/back5.FCStd ~/hook.FCStd 2>/dev/null || cp /lab/out/l2/hand/hand.FCStd ~/hook.FCStd
cat > ~/open.py <<'PY'
import FreeCAD
FreeCAD.openDocument('/home/maker/hook.FCStd')
print([o.Name for o in FreeCAD.ActiveDocument.Objects])
PY
cat > ~/support.py <<'PY'
doc = App.ActiveDocument
sk = doc.getObject('Body').newObject('Sketcher::SketchObject', 'Sketch1')
sk.Support = (doc.getObject('XZ_Plane'), [''])
PY
cat > ~/attach.py <<'PY'
doc = App.ActiveDocument
sk = doc.getObject('Sketch1') or doc.getObject('Body').newObject('Sketcher::SketchObject', 'Sketch1')
sk.AttachmentSupport = (doc.getObject('XZ_Plane'), [''])
sk.MapMode = 'FlatFace'
doc.recompute()
print(sk.AttachmentSupport)
PY
cat > ~/name.py <<'PY'
print(App.ActiveDocument.getObject('Pad001').Shape.Volume)
PY
cat > ~/volume.py <<'PY'
print(App.ActiveDocument.getObject('Pad').Shape.Volume)
PY
cat > ~/save.py <<'PY'
App.ActiveDocument.saveAs('/home/maker/parts-new/hook.FCStd')
PY
cat > ~/save2.py <<'PY'
import os
os.makedirs('/home/maker/parts-new', exist_ok=True)
App.ActiveDocument.saveAs('/home/maker/parts-new/hook.FCStd')
print(os.path.getsize('/home/maker/parts-new/hook.FCStd'))
PY
cd /lab
for f in open support attach name volume save save2; do
  echo "--- $f.py" >> "$O/c4-calls.txt"; cat ~/$f.py >> "$O/c4-calls.txt"
  test-call execute_code ~/$f.py >> "$O/c4-calls.txt" 2>&1; echo "exit $?" >> "$O/c4-calls.txt"
done
shot c4-after
tc get_objects '{"doc_name": "hook"}'; mv "$O/get_objects.txt" "$O/c4-objects.txt"

# --- check 3e: the port taken by another program (FreeCAD's server can't start; the plug reaches the wrong program)
fc_quit; sleep 1
python3 -m http.server 9875 --bind 127.0.0.1 > "$O/other-program.log" 2>&1 &
OTHER=$!; sleep 1
fc_start "$O/app-busy.log" 1.5; sleep 10
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 2; shot c3-busy
tc list_documents; mv "$O/list_documents.txt" "$O/c3-busy-call.txt"
kill $OTHER; fc_quit

# --- check 3f: an older add-on (0.1.24) left in Mod, the plug 0.1.28
rm -rf "$FC_DATA/Mod/FreeCADMCP"
( cd /tmp && curl -fsSLo old.zip https://github.com/neka-nat/freecad-mcp/archive/refs/tags/v0.1.24.zip && unzip -qo old.zip \
  && cp -r /tmp/freecad-mcp-0.1.24/addon/FreeCADMCP "$FC_DATA/Mod/" && sha256sum old.zip ) > "$O/c3-old-fetch.txt" 2>&1
ls "$FC_DATA/Mod/FreeCADMCP" >> "$O/c3-old-fetch.txt" 2>&1
fc_start "$O/app-old.log" 1.5; sleep 10
place "FreeCAD 1.1.4" 1150 0 1730 1800; sleep 2; shot c3-old
tc list_documents; mv "$O/list_documents.txt" "$O/c3-old-call.txt"
fc_quit; sl_display_stop
claude --version > "$O/claude-version.txt" 2>&1
echo "probe done"
