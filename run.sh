RUNDIR=`pwd`


#!/bin/bash
if [ x"$1" == "xstop" ]; then
    echo "STOPPING..."
    kill `cat ${RUNDIR}/marvin_daemon.pid` && echo "DAEMON STOPPED"
    rm ${RUNDIR}/marvin_daemon.pid
    kill `cat ${RUNDIR}/marvin_stats.pid` && echo "STATS STOPPED"
    rm ${RUNDIR}/marvin_stats.pid
    echo "MARVIN STOPPED"
    exit
fi

echo "STARTING MARVIN..."
python run_daemon.py &
echo $! > ${RUNDIR}/marvin_daemon.pid
gunicorn marvin.stats.views:app -b 127.0.0.1:5000 &
echo $! > ${RUNDIR}/marvin_stats.pid
sleep 1
echo "MARVIN STARTED"
