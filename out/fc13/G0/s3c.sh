F=cup; echo "== s3c (Q3 OK after the untick) $(date -u +%T)" >> $L
at "$(taskpos any OK)" "OK"; sleep 5
echo "after OK: $(tstate $F)" >> $L
echo "dialogs: $(dialogs) notices: $(FQ "notices()")" >> $L
FQ "prep('$F')" >> $L 2>&1; sleep 1; shot $O/q3-fixed-iso.png
Q "import FreeCADGui; FreeCADGui.getDocument('$F').activeView().viewTop(); FreeCADGui.SendMsgToActiveView('ViewFit'); print(1)" >> $L; sleep 2
shot $O/q3-fixed-top.png
lab_save $F $O/q3-fixed-gui.FCStd >> $L 2>&1
check13 $O/q3-fixed-gui.FCStd $O/q3-fixed-gui.check.json >> $L
