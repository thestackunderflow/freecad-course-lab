import json, os, subprocess, sys
FP = '/ev/Refream-Canvas/mcp-canvas/tools/video-qa/footage.py'
def ev(tsv, name):
    for l in open(tsv, encoding='utf-8'):
        n, t = l.rstrip('\n').rsplit('\t', 1)
        if n == name: return float(t)
    raise KeyError(name)
TOP=[0,0,1156,650]; MID=[0,640,1156,650]
C=[
('A-uvx-version','A/screen.mp4','A/events.tsv','uvx --version: typed','uvx --version: printed',4,TOP),
('A-echo-path','A/screen.mp4','A/events.tsv','echo PATH: typed','echo PATH: printed',3,TOP),
('A-which-uvx','A/screen.mp4','A/events.tsv','which uvx: typed','grep startup: typed',-1,TOP),
('A-grep-startup','A/screen.mp4','A/events.tsv','grep startup: typed','env file: typed',-1,TOP),
('A-short-list','A/screen.mp4','A/events.tsv','etc-environment: typed','systemd-user: typed',-1,TOP),
('A-which-again','A/screen.mp4','A/events.tsv','which uvx again: typed','recording stopped',-1,TOP),
('B-launcher-short','B/screen.mp4','B/events.tsv','launcher short: typed','launcher short: ENOENT',5,TOP),
('B-launcher-full','B/screen.mp4','B/events.tsv','launcher full: typed','launcher full: starts',4,TOP),
('C-config','C/screen.mp4','C/events.tsv','config: full path','add full path: typed',-1,TOP),
('C-add-connected','C/screen.mp4','C/events.tsv','add full path: typed','list: Connected',14,TOP),
('R1-reply','runs/R1/screen.mp4','runs/R1/events.tsv','turn 1: Enter','turn 1: reply done',5,MID),
]
os.makedirs('clips', exist_ok=True)
for n,v,tsv,a,b,h,box in C:
    t0=max(0,ev(tsv,a)-1.0); t1=ev(tsv,b)+h
    fj=f'clips/focus_{n}.json'; json.dump([{'t':0,'box':box}],open(fj,'w'))
    r=subprocess.run([sys.executable,FP,'clip',v,f'clips/{n}.mp4','--src','2880x1800','--t0',f'{t0:.2f}','--t1',f'{t1:.2f}','--zoom','1.5','--size','1920x1080','--focus',fj],capture_output=True,text=True)
    print(n,'ok' if r.returncode==0 else r.stderr[-300:])
