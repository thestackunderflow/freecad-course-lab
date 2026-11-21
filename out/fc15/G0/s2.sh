F=cup
shot $O/g0-after-error-box.png
at "$(taskpos any Cancel)" "Cancel"; sleep 4
echo "dialogs: $(dialogs)"; echo "panel: $(FQ "task_texts()" | cut -c1-200)"; echo "state: $(fstate cup)"
shot $O/g0-after-cancel.png
