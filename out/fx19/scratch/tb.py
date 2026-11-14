import traceback, runpy
try:
    runpy.run_path('/lab/out/fx19/G0/g0a.py', run_name='__main__')
except Exception:
    traceback.print_exc()
