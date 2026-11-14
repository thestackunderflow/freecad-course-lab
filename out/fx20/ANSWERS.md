# fx20 answers (LAB-fx20; numbers from the files named)
- Refusal line (rung a): popup Type red X | Notifier "hook#Sketch" | "Negative datum values are not valid for the constraint with index 23";
  visible 0-8 s, gone by 20 s; kept in the notification list; Report view red "<class 'ValueError'>: Negative datum values ...". No
  "Value Error" caption on screen. Size not kept (23 constraints). G0/VERDICT.txt, G0/b3, A/popup.png, A/refusal.png.
- Q12 (same value 15): "Datum 15.00 mm for the constraint with index 23 is invalid"; not kept. G0/b3, G0/g0a.txt.
- Q13 (Reference): Insert Length dialog box "Reference", no value typed: kept as non-driving DistanceX, grey "(15 mm)" (G0),
  "(17 mm)" after the fix, "(20 mm)" with bottom 30; still "Fully constrained". C/ref.png, C/ref30.png, C/take.log.
- Q14 (bottom 27): Pad 8700.0 on the console; sketch solve 0, DoF 0. B/volume.png, B/take.log.
- Q15 (solver text after the fix): "Fully constrained" (green), no DoF number shown. B/green.png.
- Q16 (your turn, 40 x 20 rectangle on the origin, DoF 0): top sized 41 -> "Negative datum values are not valid for the constraint
  with index 11" (Notifier Unnamed#Sketch), not kept; Reference "(40 mm)"; Pad 10 console 7999.999999999998. E/.
- Q17 (MCP, no AI): see D/reply.txt: setDatum without prints = "Failed to execute code: ValueError: Negative datum values ..." isError
  True; with try/print = "Code executed successfully" + the error in Output; hook-red without prints = "Code executed successfully" +
  empty Output (over-constrained, solve -4); with prints = "solve -4 conflicting [3, 4, 5, ... 23, 24]". Python keeps the failed size in
  the sketch (24 constraints, solve -2 redundant); the GUI undoes it.
- Rung c (hook-red): "Over-constrained" + link "(3, 4, 5, and 13 more)"; the click selects 16 constraints; after Close the Report view
  and a popup: "Sketch: Over-constrained sketch / Remove at least one of the following conflicting constraints:3, 4, 5, 7, ...".
