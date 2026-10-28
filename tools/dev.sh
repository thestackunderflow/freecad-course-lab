#!/bin/bash
# Explore on a live display: tools/dev.sh start | x "shell cmds" [shot] | stop.  Shots go to out/scratch/dev/NAME.png
export MSYS_NO_PATHCONV=1
LAB=$(cd "$(dirname "$0")/.." && (pwd -W 2>/dev/null || pwd))
C=fcc-dev
case $1 in
  start) docker run -d --name $C --hostname pc --shm-size 1g --memory 6g --user maker -v "$LAB:/lab" -w /lab fcc-app:1.1.4-0.1.28 sleep infinity >/dev/null
         docker exec -d $C bash -c 'Xvfb :99 -screen 0 2880x1800x24 -nolisten tcp -ac >/tmp/xvfb.log 2>&1'
         sleep 1; docker exec -d $C bash -c 'DISPLAY=:99 openbox >/tmp/ob.log 2>&1'; mkdir -p "$(dirname "$0")/../out/scratch/dev"; echo started ;;
  x) docker exec ${DEV_ENV:+--env-file $DEV_ENV} $C bash -c "export DISPLAY=:99 W=2880 H=1800 SL_W=2880 SL_H=1800; . /lab/lab/common.sh 2>/dev/null; $2"
     [ -n "${3:-}" ] && docker exec $C bash -c "DISPLAY=:99 ffmpeg -v error -y -f x11grab -video_size 2880x1800 -i :99 -frames:v 1 /lab/out/scratch/dev/$3.png" ;;
  stop) docker rm -f $C >/dev/null; echo stopped ;;
esac
