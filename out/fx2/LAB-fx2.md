# LAB-fx2: PrusaSlicer "Too Small ... Defined in Inches"? Your FreeCAD or SolidCraft STL Has No Unit | Fix — pre-registration v1, 2026-11-01 (before any run)

Lab repos and folders: freecad-course-lab, folder `out/fx2/` (takes A, B, C, D, F in `out/fx2/A` .. `out/fx2/F`, the Claude run in `out/fx2/runs/R1`); solidcraft-course-lab, folder `out/fx2/` (take E in `out/fx2/E`). This file is committed to freecad-course-lab as `out/fx2/LAB-fx2.md` before any take; the commit hash is written in section 7 (lesson 7 convention: "prereg before the run"). Pins: FreeCAD 1.1.4 AppImage; freecad-mcp 0.1.28 (R1 only; 0.1.19 is not used in fx2); SolidCraft 0.28.0; PrusaSlicer 2.9.2 AppImage with the stock MK4S presets as in lesson 5; Claude Code 2.1.31x, the exact build written down when R1 starts (`claude --version | tee out/fx2/runs/R1/claude-version.txt`); uv 0.13.6; model claude-sonnet-5-5 (read from session.jsonl, as lesson 7). Docker image: the freecad-course-lab image (Debian, Xvfb on display :99, 1920x1080, ffmpeg x11grab for the recording, xdotool, ImageMagick `import` for stills, unzip, a GUI text viewer: gedit if present, else `xterm -e less`), plus Mesa software OpenGL (`libgl1-mesa-dri`, `LIBGL_ALWAYS_SOFTWARE=1`) because PrusaSlicer's 3D scene needs OpenGL; XDG_DATA_HOME unset; no 3.11-only image (that is fx4). The solidcraft-course-lab image as in SolidCraft lesson 5, with the PrusaSlicer 2.9.2 AppImage added for take E. User `maker`, home `/home/maker`. Date of the takes: written in section 7 (`date -u | tee out/fx2/date.txt`).

Conventions (from SCRIPT-L7 §0): takes are named A, B, C, D, E, F and the Claude run R1; every take has an events file `events.tsv` (elapsed seconds, tab, event name) written while the recording runs, with the event names exactly as SCRIPT-fx2 §1 uses them, because the footage is cut by event time; a still is taken at every event (`NN-event-name.png`); terminal text goes through `| tee`; nothing is re-done after the fact except where a PASS/FAIL rule below says "re-done". Helper used in every take, defined in the take's shell:

```
T0=$(date +%s.%N)
ev() { printf '%.1f\t%s\n' "$(echo "$(date +%s.%N) - $T0" | bc)" "$1" | tee -a "$OUT/events.tsv"; import -window root "$OUT/$(printf '%02d' $(cat "$OUT/events.tsv" | wc -l))-$(echo "$1" | tr ' :/()' '_' | tr -s '_').png"; }
rec_start() { ffmpeg -loglevel error -f x11grab -video_size 1920x1080 -framerate 30 -i :99 "$OUT/take.mkv" & echo $! | tee "$OUT/ffmpeg.pid"; }
rec_stop() { kill -INT "$(cat "$OUT/ffmpeg.pid")"; sleep 2; }
```

## 2. Questions this lab answers (PLAN §0.4)

- Q5 (fx2, all of it), restated as testable sentences:
  - Q5a: the washer (outer 5 mm, hole 2.2 mm, 0.3 mm thick) has `Shape.Volume` under 9 mm3, printed by one console line in FreeCAD 1.1.4.
  - Q5b: PrusaSlicer 2.9.2 shows, for that STL, a dialog whose title, body and checkbox text match Plater.cpp at version_2.9.2 word for word; the button labels are recorded.
  - Q5c: after No the size boxes read the drawn sizes; after Yes they read the drawn sizes times 25.4.
  - Q5d: the 1 x 0.5 x 0.25 block, after Yes, reads 25.40 x 12.70 x 6.35.
  - Q5e: the 27 mm3 cube (3 x 3 x 3) opened as STL shows no dialog.
  - Q5f: the 3MF exported by FreeCAD and the 3MF sent by SolidCraft Send to Slicer open with no dialog.
  - Q5g: the ASCII STL (.ast) opened as text shows plain numbers and no unit word.
  - Q5h: the unzipped FreeCAD 3MF holds a line with `unit="millimeter"` in `3D/3dmodel.model`.
  - Q5i: a wrong Yes is undone by "Reload from disk", or only by delete and open again (description only).
  - Q5j: File, Import carries an entry reading "Import STL (Imperial Units)" at 2.9.2, and on the 27 mm3 inch-number cube it converts regardless of size.
  - Q5k: File, Export carries an entry reading "Export Plate as STL/OBJ" at 2.9.2 (filmed for the no-CAD your-turn).
  - Q5l: the pre-registered Claude prompt, one wording, is run once and scored A / B / C as §2.7.
- Q11: the prompt and the A / B / C scoring are written here before R1; one run; auto mode as lesson 7; the greyed suggested next prompt is cropped; the evidence frame for the split screen is F5 and the label (matches / does not match / half) is decided by the rule in section 4.
- Q10 is reused, not re-measured: the status-bar text after Start RPC Server ("RPC Server started at 127.0.0.1:9875", lesson 7) is only a precondition check for R1.
- §0.3 rows that touch fx2: OrcaSlicer's own text stays description-only, "from the source, not filmed" (no Orca take here; Q9 is fx5's); PrusaSlicer's full dialog sentence is filmed and read off the recording (Q5b).

## 3. Takes, in run order

### Take A (FreeCAD 1.1.4: the washer, the volume line, STL, .ast, 3MF, the .ast as text, the 3MF unzipped)

(a) Starting state: fresh home (`rm -rf /home/maker/.config/FreeCAD /home/maker/.local/share/FreeCAD /home/maker/fx2`, then `mkdir -p /home/maker/fx2`); FreeCAD 1.1.4 AppImage started once before the take so first-start dialogs are out of the footage; `OUT=/path/to/freecad-course-lab/out/fx2/A`. No PrusaSlicer open. The plug is not involved.

(b) Commands and clicks, in order:
1. `rec_start`; start FreeCAD: `./FreeCAD-1.1.4.AppImage &` (the lab's launcher as in lesson 5). Show the Python console (View, Panels, Python console).
2. Build the washer with the pre-registered script, pasted into the Python console (it is also saved as `out/fx2/A/build-washer.py`):
```
import FreeCAD as App, Part
doc = App.newDocument("washer")
obj = doc.addObject("Part::Feature", "washer")
obj.Shape = Part.makeCylinder(2.5, 0.3).cut(Part.makeCylinder(1.1, 0.3))
doc.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.Selection.addSelection(obj)
```
3. `ev "washer: shown"`.
4. Type the volume line, one line, the object selected in the tree (this exact wording goes into the description as copyable text):
`print(Gui.Selection.getSelection()[0].Shape.Volume)`
`ev "volume line: typed"` before Return; Return; `ev "volume: printed"`. Copy the printed number into `out/fx2/A/volume.txt` by hand from the console (`printf '%s\n' "the printed number" | tee $OUT/volume.txt`).
5. Save: File, Save As, `/home/maker/fx2/washer.FCStd`.
6. File, Export, file type "STL Mesh" (read the exact filter text off the screen), name `/home/maker/fx2/washer.stl`, Save. If FreeCAD shows a mesh-export options dialog, accept the defaults and record its title. `ev "Export STL: done"`.
7. File, Export, the same filter, name `/home/maker/fx2/washer.ast` (MeshIO.cpp handles "ast": ACCURACY C). `ev "Export AST: done"`. If the dialog refuses the .ast name, fallback in the console: `import Mesh; Mesh.export([obj], "/home/maker/fx2/washer.ast")` and record the fallback in `notes.txt`.
8. File, Export, file type "3D Manufacturing Format" (read the exact filter text off the screen), name `/home/maker/fx2/washer.3mf`. `ev "Export 3MF: clicked"` on the menu entry, then Save, `ev "Export 3MF: done"`.
9. Open the .ast in the text viewer: `gedit /home/maker/fx2/washer.ast &` (or `xterm -geometry 120x40 -e less /home/maker/fx2/washer.ast &`). `ev "washer.ast: opened in text viewer"`. Scroll slowly for 25 s (Page Down every 3 s). Terminal, in parallel: `head -n 12 /home/maker/fx2/washer.ast | tee $OUT/washer-ast-head.txt`; `grep -c -i -E 'mm|inch|unit' /home/maker/fx2/washer.ast | tee $OUT/washer-ast-unitwords.txt` (expected count 0).
10. Unzip the 3MF, in an xterm on the display so it is footage:
`cd /home/maker/fx2 && unzip -o washer.3mf -d washer-3mf | tee $OUT/unzip.txt`
`unzip -l washer.3mf | tee $OUT/unzip-list.txt`
`grep -n 'unit=' washer-3mf/3D/3dmodel.model | tee $OUT/3mf-unit-line.txt`
`ev "3mf unit line: shown"`.
11. `ls -l /home/maker/fx2 | tee $OUT/ls-fx2.txt`; `cp /home/maker/fx2/washer.stl /home/maker/fx2/washer.ast /home/maker/fx2/washer.3mf /home/maker/fx2/washer.FCStd $OUT/`; `rec_stop`.

(c) Events: `washer: shown`, `volume line: typed`, `volume: printed`, `Export STL: done`, `Export AST: done`, `Export 3MF: clicked`, `Export 3MF: done`, `washer.ast: opened in text viewer`, `3mf unit line: shown`.

(d) Capture under `out/fx2/A/`: `take.mkv`, `events.tsv`, the per-event stills, `build-washer.py`, `volume.txt`, `washer.FCStd`, `washer.stl`, `washer.ast`, `washer.3mf`, `washer-ast-head.txt`, `washer-ast-unitwords.txt`, `unzip.txt`, `unzip-list.txt`, `3mf-unit-line.txt`, `ls-fx2.txt`, `notes.txt` (any dialog text, fallback used, exact export filter texts).

(e) EXPECTED: volume: measure (arithmetic check, not a source: pi x (2.5^2 - 1.1^2) x 0.3 is about 4.75 mm3; the rule only needs it under 9.0, ModelProcessing.hpp 33-34 at version_2.9.2, https://raw.githubusercontent.com/prusa3d/PrusaSlicer/version_2.9.2/src/libslic3r/ModelProcessing.hpp). .ast: "facet normal" and "vertex" lines, plain numbers, no unit word ("STL files contain no scale information, and the units are arbitrary", https://en.wikipedia.org/wiki/STL_(file_format)); the exact first lines: measure. 3MF: one line in `3D/3dmodel.model` containing `unit="millimeter"` (FreeCAD Writer3MF.cpp line 60 at tag 1.1.4 hard-codes millimeter, https://raw.githubusercontent.com/FreeCAD/FreeCAD/1.1.4/src/Mod/Mesh/App/Core/IO/Writer3MF.cpp; the spec example on https://github.com/slic3r/Slic3r/wiki/3MF-Document-Core-Specification); the member path: measure (expected `3D/3dmodel.model`, ACCURACY C).

(f) PASS/FAIL: PASS if the volume prints and is under 9.0, `washer-ast-unitwords.txt` reads 0, and `3mf-unit-line.txt` has one line with `unit="millimeter"`. If the volume is 9.0 or more: the washer is re-built thinner (0.2 mm) and take A is re-done; the plan's dimensions are then corrected in rev 4. If the .ast contains a unit word: F2's "nowhere does it say millimetres or inches" is cut and the lab reports the line. If no `unit=` line is found at that path: `grep -rn 'unit=' washer-3mf | tee $OUT/3mf-unit-grep.txt`; if found elsewhere, record the real path for F9's terminal crop; if found nowhere, F9's "inside the file, there is the word millimeter" and card-3mf-3 are cut and the lab reports.

### Take B (PrusaSlicer 2.9.2: the washer STL, the dialog, No, size boxes; delete, open again, Yes; Reload from disk; the your-turn file dialog; the window hold)

(a) Starting state: FreeCAD closed. PrusaSlicer config as lesson 5 (the MK4S presets: copy the lesson 5 take's `~/.config/PrusaSlicer` into the fresh home before the take; if none is kept, run the Configuration Wizard once, Original Prusa MK4S, outside the footage). `washer.stl` from take A at `/home/maker/fx2/washer.stl`. `OUT=.../out/fx2/B`. PrusaSlicer started once before the take so no first-start notice is in the footage; `prusa-slicer --help | head -n 3 | tee $OUT/prusaslicer-version.txt` (the version line).

(b) Commands and clicks, in order (file opens use File, Import, the first entry, Ctrl+I, then the path typed and Return; drag-and-drop is not available on Xvfb, the event name stays `washer.stl: dropped` for the cut):
1. `rec_start`; start PrusaSlicer with the Plater tab, the bed empty; `ev "PrusaSlicer: empty bed"`.
2. Ctrl+I, `/home/maker/fx2/washer.stl`, Return; `ev "washer.stl: dropped"`. The dialog appears: `ev "dialog: shown"`; hold 15 s; still of the whole dialog, then a zoomed still of the body text (`import -window root -crop` is not used; the zoom is done in the edit). Read the title, body, checkbox and button labels off the screen into `$OUT/dialog-text.txt` by hand, character for character (`cat | tee $OUT/dialog-text.txt`, then paste, Ctrl+D).
3. Focus the No button (Tab until it has focus; screenshot with the focus ring), `ev "No: clicked"`, Return. Click the object once on the bed so the sidebar shows it. `ev "size boxes: shown"`; hold 10 s; read the Size X, Y, Z fields into `$OUT/size-after-No.txt`.
4. Select the object, press Delete; `ev "object: deleted"`. Ctrl+I, the same path, Return; `ev "washer.stl: opened"`; `ev "dialog: shown"`; No; `ev "No: clicked"`; `ev "size boxes: shown"` (the F5 first half). Delete again; `ev "object: deleted"`. Ctrl+I, the same path, Return; `ev "washer.stl: opened again"`; dialog; focus Yes; `ev "Yes: clicked"`; Return; click the object; `ev "size boxes: shown (x 25.4)"`; hold 10 s; read the fields into `$OUT/size-after-Yes.txt`.
5. Reload test (Q5i, description only): with the Yes-scaled object selected, right-click it; `ev "right-click menu: shown"`; read the menu entry text ("Reload from disk" expected) into `$OUT/reload-menu-text.txt`; click it; `ev "Reload from disk: clicked"`; record whether the inches dialog appears again (`ev "dialog: shown (after reload)"` or `ev "no dialog (after reload)"`), and the Size fields afterwards into `$OUT/size-after-reload.txt`.
6. Delete the object. Ctrl+I; the file dialog stays open; `ev "your turn: file dialog opened live"`; hold 25 s; Escape.
7. `ev "PrusaSlicer: window hold"`; hold 20 s (F13 background). `rec_stop`.

(c) Events: `PrusaSlicer: empty bed`, `washer.stl: dropped`, `dialog: shown`, `No: clicked`, `size boxes: shown`, `object: deleted`, `washer.stl: opened`, `dialog: shown`, `No: clicked`, `size boxes: shown`, `object: deleted`, `washer.stl: opened again`, `Yes: clicked`, `size boxes: shown (x 25.4)`, `right-click menu: shown`, `Reload from disk: clicked`, `dialog: shown (after reload)` or `no dialog (after reload)`, `your turn: file dialog opened live`, `PrusaSlicer: window hold`.

(d) Capture under `out/fx2/B/`: `take.mkv`, `events.tsv`, stills, `prusaslicer-version.txt`, `dialog-text.txt`, `size-after-No.txt`, `size-after-Yes.txt`, `reload-menu-text.txt`, `size-after-reload.txt`, `notes.txt` (how the buttons were pressed, any other dialog with its text).

(e) EXPECTED: dialog title "The object is too small"; body "The dimensions of the object from file %s seem to be defined in inches. The internal unit of PrusaSlicer is a millimeter. Do you want to recalculate the dimensions of the object?" with %s replaced by the file name (which form, name or path: measure); checkbox "Apply to all the remaining small objects being loaded." (Plater.cpp at version_2.9.2, https://raw.githubusercontent.com/prusa3d/PrusaSlicer/version_2.9.2/src/slic3r/GUI/Plater.cpp); button labels: measure. Size after No: the drawn sizes, measure (the washer was built 5 x 5 x 0.3, so 5.00 x 5.00 x 0.30 is the plan's example). Size after Yes: the No reading times 25.4 (`in_to_mm` 25.4, ModelProcessing.cpp 81, https://raw.githubusercontent.com/prusa3d/PrusaSlicer/version_2.9.2/src/libslic3r/ModelProcessing.cpp); arithmetic on 5 x 5 x 0.3, not a source: 127.00 x 127.00 x 7.62. Menu text "Reload from disk" (GUI_Factories.cpp 906, https://raw.githubusercontent.com/prusa3d/PrusaSlicer/version_2.9.2/src/slic3r/GUI/GUI_Factories.cpp). Whether reload resets the scale: measure.

(f) PASS/FAIL: PASS if the dialog appears on each of the three opens and `dialog-text.txt` matches the Plater.cpp words exactly (apart from %s), the No sizes equal the drawn sizes and the Yes sizes equal the No sizes times 25.4 (to two decimals). If the dialog text differs in any word: STOP (section 6); the storyboard quotes the recording, not the source, and the accuracy gate decides. If no dialog appears: check `out/fx2/A/volume.txt` is under 9; if it is, STOP and report; if not, take A is re-done thinner. If the Yes sizes are not times 25.4: F5's "25.4 times bigger" and card-rule-2's "x 25.4" are cut, the lab reports the factor. Reload outcome: whichever happens goes into the description as one sentence; the video keeps "delete and open again" either way. If the right-click menu has no "Reload from disk": record the menu as filmed; fx5 is informed.

### Take C (the inch-number block 1 x 0.5 x 0.25: FreeCAD, STL, PrusaSlicer, Yes, 25.40 x 12.70 x 6.35)

(a) Starting state: PrusaSlicer open with an empty bed (from take B, object deleted) or restarted; FreeCAD 1.1.4 started fresh; `OUT=.../out/fx2/C`.

(b) Commands and clicks:
1. `rec_start`. In the FreeCAD Python console (saved as `out/fx2/C/build-block.py`):
```
import FreeCAD as App, Part
doc = App.newDocument("block")
obj = doc.addObject("Part::Feature", "block")
obj.Shape = Part.makeBox(1, 0.5, 0.25)
doc.recompute()
Gui.SendMsgToActiveView("ViewFit")
Gui.Selection.addSelection(obj)
print(Gui.Selection.getSelection()[0].Shape.Volume)
```
`ev "block 1 x 0.5 x 0.25: shown in FreeCAD"`; the printed volume into `$OUT/volume.txt`.
2. File, Export, STL Mesh, `/home/maker/fx2/block.stl`; `ev "Export STL: done"`.
3. PrusaSlicer: Ctrl+I, `/home/maker/fx2/block.stl`, Return; `ev "dialog: shown"`; read the dialog's file name into `$OUT/dialog-text.txt`; focus Yes; `ev "Yes: clicked"`; Return; click the object; `ev "size boxes: 25.40 x 12.70 x 6.35"` (the event name is fixed by the script; if the reading differs, the event is still logged under this name and `size-after-Yes.txt` holds the real reading); read the fields into `$OUT/size-after-Yes.txt`; hold 10 s. Delete the object. `rec_stop`. `cp /home/maker/fx2/block.stl $OUT/`.

(c) Events: `block 1 x 0.5 x 0.25: shown in FreeCAD`, `Export STL: done`, `dialog: shown`, `Yes: clicked`, `size boxes: 25.40 x 12.70 x 6.35`.

(d) Capture under `out/fx2/C/`: `take.mkv`, `events.tsv`, stills, `build-block.py`, `volume.txt`, `block.stl`, `dialog-text.txt`, `size-after-Yes.txt`.

(e) EXPECTED: volume: measure (arithmetic, not a source: 0.125 mm3, under 9 and over 0.001, so the inches question and not the metres one; metres is tested first, Plater.cpp 1486, 1504, ACCURACY C). Dialog: the same inches dialog as take B. Size after Yes: 25.40 x 12.70 x 6.35 (PLAN §0.4 Q5 and §2.6 step 2; 25.4 from ModelProcessing.cpp 81).

(f) PASS/FAIL: PASS if the inches dialog (not the metres one) appears and the sizes read 25.40 x 12.70 x 6.35. If the metres dialog appears: STOP and report (the thresholds would not be as pinned). If the sizes differ: F6's spoken sizes are replaced by the measured ones and the Time columns rerun; if no dialog: STOP.

### Take D (the FreeCAD 3MF from take A opened in PrusaSlicer: no dialog)

(a) Starting state: PrusaSlicer open, empty bed; `/home/maker/fx2/washer.3mf` from take A; `OUT=.../out/fx2/D`.

(b) Commands and clicks:
1. `rec_start`; `ev "PrusaSlicer: empty bed"`. Ctrl+I, `/home/maker/fx2/washer.3mf`, Return; `ev "washer.3mf: opened in PrusaSlicer, no dialog"` (if any dialog appears, log `ev "dialog: shown (3mf)"` instead, read its full text into `$OUT/dialog-text.txt`, choose the option that loads the geometry only, and continue). Click the object; `ev "size boxes: shown"`; hold 10 s; read the fields into `$OUT/size-3mf.txt`. Delete the object; `rec_stop`.

(c) Events: `PrusaSlicer: empty bed`, `washer.3mf: opened in PrusaSlicer, no dialog` (or `dialog: shown (3mf)`), `size boxes: shown`.

(d) Capture under `out/fx2/D/`: `take.mkv`, `events.tsv`, stills, `size-3mf.txt`, `dialog-text.txt` if any, `notes.txt`.

(e) EXPECTED: no inches dialog ("3mf contains information about units, so there is no need to detect possible convertions for these files", FileReader.cpp 230-236 at version_2.9.2, https://raw.githubusercontent.com/prusa3d/PrusaSlicer/version_2.9.2/src/libslic3r/FileReader.cpp); size boxes as drawn: measure (expected equal to `out/fx2/B/size-after-No.txt`).

(f) PASS/FAIL: PASS if no inches dialog and the sizes equal take B's No reading. Any other PrusaSlicer dialog (a project-import question) is not a failure: its text is recorded and the footage cut starts after it. If the inches dialog appears for the 3MF: STOP; F7's "3MF: no question", F8, F9 and card-recap-3 are cut and the lab reports.

### Take E (SolidCraft 0.28.0: Save As Mesh STL asks; Send to Slicer 3MF does not; solidcraft-course-lab out/fx2/E)

(a) Starting state: the solidcraft-course-lab image as SolidCraft lesson 5 with PrusaSlicer 2.9.2 on PATH and set as SolidCraft's slicer the way lesson 5 did (recorded in `notes.txt`); the washer design: the lesson 5 washer file if the lab kept one, else the same washer built in SolidCraft with outer 5 mm, hole 2.2 mm, thickness 0.3 mm, saved as `/home/maker/fx2/washer` (SolidCraft's own format); which one was used goes into `notes.txt`. PrusaSlicer closed. `OUT=/path/to/solidcraft-course-lab/out/fx2/E`.

(b) Commands and clicks:
1. `rec_start`; start SolidCraft 0.28.0 with the washer open; `ev "washer: shown in SolidCraft"`.
2. Right-click the washer; `ev "Save As Mesh STL: clicked"` on the STL entry (read the exact menu wording into `$OUT/menu-text.txt`); save as `/home/maker/fx2/washer-sc.stl`.
3. Start PrusaSlicer; Ctrl+I, `/home/maker/fx2/washer-sc.stl`, Return; `ev "dialog: shown"`; read the dialog text into `$OUT/dialog-text.txt`; No; click the object; read the sizes into `$OUT/size-sc-stl.txt`; delete the object; close PrusaSlicer.
4. In SolidCraft: Send to Slicer, the format left at its default; `ev "Send to Slicer: clicked (3MF)"`; read the format shown into `$OUT/send-format.txt`. PrusaSlicer opens with the file: `ev "PrusaSlicer: opened, no dialog"` (if a dialog appears: `ev "dialog: shown (send)"`, its text into `$OUT/dialog-text-send.txt`). Click the object; read the sizes into `$OUT/size-sc-3mf.txt`.
5. `ls -l /home/maker/.cache/solidcraft/slicer/ | tee $OUT/ls-cache-slicer.txt` (the hand-over file; the path is fx5's Q9, recorded here for the record). `cp /home/maker/fx2/washer-sc.stl $OUT/`; copy the hand-over 3MF into `$OUT/` under its real name; `unzip -p "$OUT/the-handover.3mf" 3D/3dmodel.model | grep -n 'unit=' | tee $OUT/3mf-unit-line-sc.txt` (member path: measure, as take A). `rec_stop`.

(c) Events: `washer: shown in SolidCraft`, `Save As Mesh STL: clicked`, `dialog: shown`, `Send to Slicer: clicked (3MF)`, `PrusaSlicer: opened, no dialog`.

(d) Capture under solidcraft-course-lab `out/fx2/E/`: `take.mkv`, `events.tsv`, stills, `menu-text.txt`, `dialog-text.txt`, `size-sc-stl.txt`, `send-format.txt`, `size-sc-3mf.txt`, `ls-cache-slicer.txt`, `washer-sc.stl`, the hand-over 3MF, `3mf-unit-line-sc.txt`, `notes.txt`.

(e) EXPECTED: STL asks (same dialog as take B; the washer is under 9 mm3); Send to Slicer default format 3mf "in millimetres" (SolidCraft `cmd/file.rs` line 71 at v0.28.0, https://raw.githubusercontent.com/tangency-labs/solidcraft/v0.28.0/crates/engine/src/cmd/file.rs); the 3MF opens with no dialog (FileReader.cpp 230-236 as take D); the hand-over folder `~/.cache/solidcraft/slicer/` (PLAN §0.4 Q9); the unit line: measure.

(f) PASS/FAIL: PASS if the STL shows the inches dialog and the 3MF does not. If Send to Slicer does not launch PrusaSlicer: open the hand-over 3MF from the cache folder in PrusaSlicer by Ctrl+I, log it as `PrusaSlicer: opened, no dialog`, and write in `notes.txt` that the launch was manual (F7's footage then shows the manual open; the narration "Send to Slicer sends a 3MF" still holds because the file is the one Send to Slicer wrote). If the default format is not 3MF: F7's "(format 3MF, default)" is corrected to the measured default and the lab reports. If the 3MF asks: STOP, as take D.

### Take F (description-only evidence: the 27 mm3 cube, Import STL (Imperial Units), Export Plate as STL/OBJ)

(a) Starting state: FreeCAD open; PrusaSlicer open with an empty bed; `OUT=.../out/fx2/F`.

(b) Commands and clicks:
1. `rec_start`. FreeCAD console (`out/fx2/F/build-cube.py`):
```
import FreeCAD as App, Part
doc = App.newDocument("cube3")
obj = doc.addObject("Part::Feature", "cube3")
obj.Shape = Part.makeBox(3, 3, 3)
doc.recompute()
Gui.Selection.addSelection(obj)
print(Gui.Selection.getSelection()[0].Shape.Volume)
```
`ev "cube 3 mm: shown in FreeCAD"`; the volume into `$OUT/volume.txt`. File, Export, STL Mesh, `/home/maker/fx2/cube3.stl`; `ev "Export STL: done"`.
2. PrusaSlicer: Ctrl+I, `/home/maker/fx2/cube3.stl`, Return; `ev "cube3.stl: opened, no dialog"` (or `dialog: shown (cube)`); click the object; sizes into `$OUT/size-cube-plain.txt`; delete the object.
3. File, Import; `ev "Import menu: shown"`; hold 8 s; read every entry of the Import submenu into `$OUT/import-menu-text.txt`. Click the entry reading "Import STL (Imperial Units)"; `ev "Import STL (Imperial Units): clicked"`; `/home/maker/fx2/cube3.stl`, Return; record whether any dialog appears (`$OUT/notes.txt`); click the object; `ev "size boxes: shown (imperial import)"`; sizes into `$OUT/size-cube-imperial.txt`.
4. File, Export; `ev "Export menu: shown"`; hold 8 s; read every entry into `$OUT/export-menu-text.txt`. Extra, for the no-CAD your-turn, description only: select the object, set the Scale factors to 2.6316 percent so the cube is 2 x 2 x 2 (read the Size fields into `$OUT/size-scaled.txt`), click "Export Plate as STL/OBJ", save `/home/maker/fx2/tiny.stl`; `ev "Export Plate as STL/OBJ: done"`; delete the object; Ctrl+I, `/home/maker/fx2/tiny.stl`; `ev "tiny.stl: opened"`; record whether the dialog appears (`ev "dialog: shown (tiny)"`). `rec_stop`. `cp /home/maker/fx2/cube3.stl /home/maker/fx2/tiny.stl $OUT/`.

(c) Events: `cube 3 mm: shown in FreeCAD`, `Export STL: done`, `cube3.stl: opened, no dialog`, `Import menu: shown`, `Import STL (Imperial Units): clicked`, `size boxes: shown (imperial import)`, `Export menu: shown`, `Export Plate as STL/OBJ: done`, `tiny.stl: opened`, `dialog: shown (tiny)`.

(d) Capture under `out/fx2/F/`: `take.mkv`, `events.tsv`, stills (the two menu stills are the deliverable), `build-cube.py`, `volume.txt`, `cube3.stl`, `tiny.stl`, `size-cube-plain.txt`, `import-menu-text.txt`, `size-cube-imperial.txt`, `export-menu-text.txt`, `size-scaled.txt`, `notes.txt`.

(e) EXPECTED: volume 27 (arithmetic; the rule: 27 is over 9, so no question: ModelProcessing.hpp 33-34); plain open: no dialog, sizes 3.00 x 3.00 x 3.00 (measure); Import menu entry "Import STL (Imperial Units)" ("Load an model saved with imperial units", MainFrame.cpp 1502 at version_2.9.2, https://raw.githubusercontent.com/prusa3d/PrusaSlicer/version_2.9.2/src/slic3r/GUI/MainFrame.cpp); after it: converted regardless of size (Plater.cpp 1481-1484 "Convert even if the object is big"), sizes 76.20 x 76.20 x 76.20 (PLAN §2.9: "3.00 where you wanted 76.2"; SCRIPT §0 take F "76.20 across"); Export menu entry "Export Plate as STL/OBJ" (MainFrame.cpp 1540); tiny.stl: measure (8 mm3 by arithmetic, so the dialog is expected by the rule).

(f) PASS/FAIL: PASS if the plain open shows no dialog, the imperial import reads 76.20 across, and both menu texts match. If the imperial import shows a confirmation dialog first: record its text, accept, continue (the description names it). If the menu texts differ: the description and the question's expected answer quote the filmed text; the lab reports the difference. If the plain open DOES ask: STOP, the 9 mm3 rule as pinned would be wrong.

## 4. The Claude run R1 (pre-registered)

- State before the run: a fresh home for Claude Code (`~/.claude` as lesson 7's take A state: freecad added with `claude mcp add freecad -- uvx freecad-mcp@0.1.28`, auto mode as lesson 7, no prompt other than the one below); FreeCAD 1.1.4 open with `/home/maker/fx2/washer.FCStd` from take A loaded and the washer selected; the 0.1.28 add-on installed in `v1-1/Mod`, Start RPC Server clicked, the status bar reading "RPC Server started at 127.0.0.1:9875" (lesson 7, Q10 reused; still `00-rpc-status.png`); `/home/maker/fx2` holds only `washer.FCStd` (the take A exports moved to `out/fx2/A/` and removed from `/home/maker/fx2`, `ls -l /home/maker/fx2 | tee $OUT/ls-before.txt`); Claude Code started in the empty folder `/home/maker/run-fx2` (`mkdir -p /home/maker/run-fx2 && cd /home/maker/run-fx2 && claude`). `OUT=.../out/fx2/runs/R1`. No-AI preflight, outside the run: `claude --version | tee $OUT/claude-version.txt`; `claude mcp list | tee $OUT/mcp-list-before.txt`, expected "freecad: uvx freecad-mcp@0.1.28 - ✔ Connected" (SCRIPT-L7 §0 take A); the run does not start until that line reads Connected (fixing the connection is not part of the run).
- The prompt, one wording, typed once: `Export the washer for 3D printing and tell me what the slicer will say about its size`
- Recording: `rec_start` before the prompt; `ev "prompt: typed"`; `ev "reply: shown"` when the reply is complete; `ev "suggested prompt: greyed"` if Claude Code greys in a suggested next prompt (it is cropped out of the footage, as lesson 7); `/cost`; `ev "cost: shown"`; `rec_stop`.
- Outcome classes (PLAN §2.7, verbatim rule): A exports an STL, predicts the inches question and says No; B exports a 3MF instead and says why (the slicer will not ask); C says nothing about size. Storyboard clause per class (F10 narration): A: "predicted the question"; B: "chose 3MF"; C: "said nothing about size". A reply that exports nothing is scored by its words alone: a size prediction is A or B by what it names, no size statement is C.
- Evidence frame: F5 (take B: the dialog and the size boxes after No and after Yes). Label rule, decided now: A with "No" and the dialog named: "matches"; B with "the slicer will not ask" and take D showed no dialog: "matches"; C: "does not match" (the dialog is on screen beside it); A or B whose prediction is partly wrong (it predicts a question but advises Yes for the millimetre washer; it predicts a wrong size; it names a 3MF but says the slicer will ask; it predicts the question without naming No or Yes): "half", with one clause in F10 saying why. Also, outside the footage: the file Claude wrote is opened in PrusaSlicer (`ev "claude export: opened"`), and whether the dialog appears is recorded in `$OUT/claude-export-check.txt`; this is the second check for the label and it is logged, not scored.
- Record: `session.jsonl` copied from `~/.claude/projects/` for this run; `cost.txt` (the `/cost` output); `model.txt` (the model string read from session.jsonl, expected claude-sonnet-5-5 as lesson 7); `tool-calls.txt` (every tool call name and its arguments from session.jsonl, in order); `reply.txt` (the reply verbatim); `suggested-prompt.png` (the greyed suggested prompt, the crop that is removed from the footage); `outcome.txt` (one letter A / B / C, the label matches / does not match / half, the one clause for half); `ls-after.txt` (`ls -l /home/maker/fx2 /home/maker/run-fx2 | tee $OUT/ls-after.txt`); the exported file copied into `$OUT/`.
- Rule: one run, scored before it runs (this section), no second try. If the run fails for a reason outside the prompt (the plug drops, FreeCAD crashes), the failure is recorded as the run's result and reported; a re-run needs a new pre-registration (v2 of this file).

## 5. Measurements table

| value | where it is used | how measured | expected | source |
|---|---|---|---|---|
| Claude Code exact build | SCRIPT §0 pins | `claude --version` at R1 start, `runs/R1/claude-version.txt` | measure (2.1.31x) | PLAN §0 pins |
| Model of R1 | SCRIPT §0 pins, R1 | session.jsonl, `runs/R1/model.txt` | claude-sonnet-5-5 | SCRIPT-L7 §0 (lesson 7 R1) |
| Date of the takes | SCRIPT §0 pins | `out/fx2/date.txt` | measure | - |
| The volume console line (wording) | F3, description (copyable) | typed in take A | `print(Gui.Selection.getSelection()[0].Shape.Volume)` prints a number | pre-registered here; lab confirms |
| Shape.Volume of the washer | F3 label and narration, F4 card-rule-3 | take A `volume.txt` | measure, under 9.0 | ModelProcessing.hpp 33-34 (threshold) |
| Dialog title, body, checkbox text on the 2.9.2 screen | F0, SCRIPT §0 take B | take B `dialog-text.txt`, read off the recording | "The object is too small" / "The dimensions of the object from file %s seem to be defined in inches. The internal unit of PrusaSlicer is a millimeter. Do you want to recalculate the dimensions of the object?" / "Apply to all the remaining small objects being loaded." | Plater.cpp at version_2.9.2 (ACCURACY C) |
| Button labels | F1, F5 labels | take B `dialog-text.txt` | measure | - |
| Size boxes after No | F1, F5, F10 right side | take B `size-after-No.txt` | measure (drawn 5 x 5 x 0.3) | PLAN §2.6 step 2 ("a 5 mm washer must read 5.00") |
| Size boxes after Yes | F5 narration ("[lab] millimetres across"), F10 | take B `size-after-Yes.txt` | No reading x 25.4 | ModelProcessing.cpp 81 |
| Does a wrong Yes undo with Reload from disk | description only | take B `size-after-reload.txt`, events | measure | PLAN §2.6 step 3, Q5 |
| "Reload from disk" menu text | description, fx5 | take B `reload-menu-text.txt` | "Reload from disk" | GUI_Factories.cpp 906 |
| Block after Yes | F6 | take C `size-after-Yes.txt` | 25.40 x 12.70 x 6.35 | PLAN Q5, §2.6 step 2 |
| FreeCAD 3MF: no dialog, size boxes as drawn | F9, SCRIPT §0 take D | take D events, `size-3mf.txt` | no dialog; sizes = take B No reading | FileReader.cpp 230-236 |
| .ast first lines, no unit word | F2, Short S1 | take A `washer-ast-head.txt`, `washer-ast-unitwords.txt` | "facet normal" / "vertex" lines; unit-word count 0 | Wikipedia STL (no scale information) |
| The `unit="millimeter"` line and its member path | F9 terminal crop, F8 card-3mf-1 | take A `3mf-unit-line.txt`, `unzip-list.txt` | one line with `unit="millimeter"` in `3D/3dmodel.model` | Writer3MF.cpp line 60 at 1.1.4; Slic3r wiki example |
| FreeCAD export filter texts (STL, 3MF) | F3, F9 on-screen | take A `notes.txt` | measure | - |
| SolidCraft Save As Mesh STL: dialog | F7 | take E events, `dialog-text.txt` | the inches dialog | Plater.cpp; file.rs line 71 (STL in millimetres) |
| SolidCraft Send to Slicer (3MF default): no dialog | F7 | take E events, `send-format.txt`, `size-sc-3mf.txt` | default 3mf; no dialog | file.rs line 71; FileReader.cpp 230-236 |
| 27 mm3 cube opened as STL: no dialog | SCRIPT §0 take F, description, the question's answer | take F events, `size-cube-plain.txt` | no dialog; 3.00 x 3.00 x 3.00 | ModelProcessing.hpp 33-34 |
| "Import STL (Imperial Units)" menu text | description, the question's expected answer | take F `import-menu-text.txt`, still | "Import STL (Imperial Units)" | MainFrame.cpp 1502 |
| Imperial import result on the cube | description | take F `size-cube-imperial.txt` | 76.20 x 76.20 x 76.20 | Plater.cpp 1481-1484; PLAN §2.9 |
| "Export Plate as STL/OBJ" menu text | description (no-CAD your-turn) | take F `export-menu-text.txt`, still | "Export Plate as STL/OBJ" | MainFrame.cpp 1540 |
| R1 outcome A / B / C | F10 narration, SCRIPT §0 R1 | `runs/R1/outcome.txt` | measure | PLAN §2.7 |
| R1 reply words, cropped | F10 left side | `runs/R1/reply.txt`, footage with `suggested-prompt.png` cropped | measure | Q11 |
| R1 cost and model | SCRIPT §0 R1 | `runs/R1/cost.txt`, `model.txt` | measure | - |
| F10 label matches / does not match / half | F10 | section 4 rule, `runs/R1/outcome.txt` | measure | Q11; evidence frame F5 |
| Lab repo folders | description `[lab: folder]` | this file | freecad-course-lab `out/fx2/`, solidcraft-course-lab `out/fx2/E` | section 1 |
| Status bar after Start RPC Server (Q10) | R1 precondition only | `runs/R1/00-rpc-status.png` | "RPC Server started at 127.0.0.1:9875" | lesson 7 (reused) |

## 6. Stop rules

| Condition | Action | Fallback named by the plan |
|---|---|---|
| PrusaSlicer 2.9.2 does not start or does not render the 3D scene in Xvfb | try `LIBGL_ALWAYS_SOFTWARE=1` and Mesa llvmpipe once; if still blank, stop and report with the terminal text | none in the plan; the video cannot be cut without takes B-D, F |
| FreeCAD 1.1.4 does not start in Xvfb | stop and report | lesson 5/7 image is the reference; no fallback named |
| The inches dialog's text differs from Plater.cpp in any word | record the recording's words character for character in `dialog-text.txt`; stop the lab after take B's step 2 is captured and report | PLAN §0.3: "the storyboard quotes the source words and the recording must match"; the accuracy gate decides the wording |
| No dialog for the washer STL with volume under 9 | stop and report (the pinned threshold would be wrong) | none |
| The metres dialog appears for the washer or the block | stop and report | none (metres rule is description-only) |
| A different dialog appears on opening a 3MF (not the inches one) | record its text, pick the geometry-only option, continue; the cut starts after it | PLAN §2.1: 3MF never asks about inches |
| FreeCAD's export dialog has no .ast option | console `Mesh.export` to the .ast name; record | ACCURACY C: MeshIO.cpp handles "ast" |
| `3D/3dmodel.model` not found in the 3MF | `grep -rn 'unit='` over the unzipped folder; record the real path; if none, stop take A's 3MF part and report | F9 and card-3mf-3 are cut |
| SolidCraft Send to Slicer does not launch PrusaSlicer | open the hand-over 3MF from `~/.cache/solidcraft/slicer/` manually; record | take E PASS/FAIL |
| SolidCraft 0.28.0 has no "Save As Mesh" STL entry under right-click | record the real menu; use SolidCraft's STL export command; stop if none | F7's menu words follow the recording |
| Claude Code `claude mcp list` does not read Connected before R1 | fix outside the run (lesson 7 takes A/B), then start; the run is not started while it fails | SCRIPT-L7 §0 take B |
| R1 is interrupted by a crash or a dropped plug | record as the run's result; no second try without a v2 pre-registration | section 4 |
| Any Windows-only step | none in fx2 (§0.3: Orca is description-only; the dialog is filmed on Linux) | - |
| Drag-and-drop for `washer.stl: dropped` not possible on Xvfb | open by Ctrl+I; the event name stays | section 3 take B |

## 7. Deliverables back to Cowork

Files: `out/fx2/LAB-fx2.md` (this file) with its prereg commit hash written here: `measure`; `out/fx2/date.txt`; per take `take.mkv`, `events.tsv`, the stills and the text files listed in section 3 (d); `out/fx2/runs/R1/` with `session.jsonl`, `cost.txt`, `model.txt`, `tool-calls.txt`, `reply.txt`, `suggested-prompt.png`, `outcome.txt`, `claude-version.txt`, `mcp-list-before.txt`, `claude-export-check.txt`, the exported file; solidcraft-course-lab `out/fx2/E/` as section 3 take E (d).

One-line answers to section 2 (to be filled after the run, into PLAN rev 4 §0 "lab fills" and SCRIPT-fx2 v2 §0):
- Q5a volume: measure (number, mm3; the console line as typed).
- Q5b dialog text and buttons: measure (matches Plater.cpp: yes/no; button labels).
- Q5c sizes after No / after Yes: measure (X x Y x Z, twice).
- Q5d block after Yes: measure (expected 25.40 x 12.70 x 6.35).
- Q5e 27 mm3 cube: measure (no dialog: yes/no).
- Q5f FreeCAD 3MF / SolidCraft 3MF: measure (no dialog: yes/no, twice; the default format shown).
- Q5g .ast as text: measure (the first three lines; unit-word count).
- Q5h unit line: measure (the line and its path inside the zip).
- Q5i Reload from disk after a wrong Yes: measure (dialog again: yes/no; sizes after).
- Q5j Import STL (Imperial Units): measure (exact menu text; the cube's sizes after).
- Q5k Export Plate as STL/OBJ: measure (exact menu text; tiny.stl asks: yes/no).
- Q5l and Q11 R1: measure (A / B / C; the label; cost; model; build; the reply verbatim; F5 is the evidence frame).
- Pins as run: measure (Claude Code build, date).
- Lab folders: freecad-course-lab `out/fx2/`, solidcraft-course-lab `out/fx2/E`.
