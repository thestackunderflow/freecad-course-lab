#!/bin/bash
# fx4 take E1 (LAB-fx4 section 3.E1): in the 3.11-only image fx4-py311, pip install freecad-mcp fails; uvx freecad-mcp@0.1.28 downloads a CPython 3.12.
#   tools/run_fx4.sh e1 lab/fx4_E1.sh fx4-py311
set -u
. /lab/lab/common.sh; . /lab/lab/fx4_lib.sh
O=$X/E; mkdir -p $O
cd ~
mkdir -p ~/tools ~/work; ln -sf /lab/tools/test_mcp.py ~/tools/test_mcp.py
printf '%s\n' 'export PATH="$HOME/.local/bin:$PATH"' "PS1='\$ '" >> ~/.bashrc
python3.11 --version 2>&1 | tee $O/E1-python-version.txt
ls /usr/bin/python3* /usr/local/bin/python3* 2>&1 | tee $O/E1-ls-python.txt
uv python list 2>&1 | tee $O/E1-uv-python-list-before.txt | head -12
echo "UV_PYTHON_INSTALL_DIR=$UV_PYTHON_INSTALL_DIR"; ls -la "$UV_PYTHON_INSTALL_DIR"
sl_display $W $H
term_start
R=$O/E1rec
sl_record "$R" nomouse; sl_mark "recording started: a terminal, Python 3.11 only"; sl_nap 1.5
run_wait 'python3.11 -m pip install freecad-mcp' "pip 3.11: typed" "pip 3.11: error block" $O/E1-pip-3.11.txt 120
sl_nap 18
python3.11 -m pip --version 2>&1 | tee $O/E1-pip-version.txt
typ 'timeout 90 uvx freecad-mcp@0.1.28; echo "exit=$?"' "uvx 0.1.28: typed"
end=$(( $(date +%s) + 90 ))
until tmux capture-pane -p -t cc | grep -qiE 'cpython|download'; do [ "$(date +%s)" -ge "$end" ] && break; sleep 0.3; done
sl_mark "uv: downloading cpython 3.12"
until tmux capture-pane -p -t cc | grep -qE 'Installed [0-9]+ packages'; do [ "$(date +%s)" -ge "$end" ] && break; sleep 0.3; done
sl_nap 3; sl_mark "0.1.28: waits"
wait_prompt 100; sl_mark "uvx 0.1.28: timeout returned"
save_out $O/E1-uvx-0.1.28.txt; cp $O/E1-uvx-0.1.28.txt $O/E1-uvx-0.1.28-exit.txt
sl_nap 3
sl_mark "recording stopped"; stamp $R events-E1.tsv; cp $R/events-E1.tsv $O/events-E1.tsv
uv python list 2>&1 | tee $O/E1-uv-python-list-after.txt | head -12
ls "$UV_PYTHON_INSTALL_DIR" | tee $O/E1-ls-python-dir.txt
cd /lab && python3 -I tools/test_mcp.py uvx freecad-mcp@0.1.28 2>&1 | tee $O/E1-test-0.1.28.txt
grep -n -i "download" $O/E1-uvx-0.1.28.txt | tee $O/E1-download-line.txt
grep -n "Requires-Python\|No matching distribution" $O/E1-pip-3.11.txt | tee $O/E1-pip-lit-lines.txt
tmux kill-server 2>/dev/null; sl_display_stop
echo "E1 done"
