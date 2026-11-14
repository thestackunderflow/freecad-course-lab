# fx19 answers (LAB-fx19 v1.1 + PLAN rev 3 lab fills). Numbers from files the lab wrote.
- G0: PASS (G0/VERDICT.txt). Box "Input error" / "Wire is not closed." / OK; Report view "Pad: Wire is not closed." (red).
- A (A/refusal.png): Pad 20 OK on hook-gap -> the box; the box's OK leaves the Pad panel open; Cancel removes the Pad.
- B: Validate Sketch > Highlight Troublesome Vertices: 2 marks (B/validate.png); in the sketch, the two ends picked
  (zoomed 12 wheel steps), C: constraints 22 -> 23, the end back at (0,0), "Fully constrained" (B/joined.png);
  Validate again: no marks, no box (B/validate-again.png); Pad 20 builds; B2/volume.png: 8500.0 (read: valid, 8500.0).
- Q4 (P/check.txt, C/touch.png): ends touching by script, no Coincident: wire closed, Pad 20 valid, 8500.0, no box.
- Q5 (C): hovering the first point while closing a Polyline shows FreeCAD's coincident cue beside the cursor
  (C/close-hover.png); the closing click adds the Coincident (7,2 -> 0,1) itself (constraints 14 -> 17).
  A last click 2 mm off (landed 2.42 mm): 8 lines, no join, "8 Degrees of Freedom" (C/apart.png).
- Q6 (E): XY rectangle 30 x 20, corner Coincident deleted (corner clicked, Delete), end dragged: gap 0.915 mm;
  Validate: the marks; joined (C); Pad 10: 6000.0 (E/volume.png).
- Q7 (D/reply.txt): execute_code without prints replies "Code executed successfully: Python code executed
  successfully." + "Output:" (empty) + an image, isError False, while the Pad is invalid; with the two prints:
  "Output: False / Wire is not closed.".
- R1: class A, $0.1527 (runs/R1/). See RESULTS-fx19.md.
