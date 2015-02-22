#!/bin/bash

RUNDIR=`pwd`

if [ x"$1" == "xstop" ]; then
    echo "STOPPING..."
    kill `cat ${RUNDIR}/marvin_daemon.pid` && echo "DAEMON STOPPED"
    rm ${RUNDIR}/marvin_daemon.pid
    kill `cat ${RUNDIR}/marvin_stats.pid` && echo "STATS STOPPED"
    rm ${RUNDIR}/marvin_stats.pid
    echo "           ___ "
    echo "    ,_    '---'    _, "
    echo '    \ `-._|\_/|_.-- / '
    echo "     |   =)'T'(=   | "
    echo '      \   /`"`\   / '
    echo "  jgs  '._\) (/_.' "
    echo "           | | "
    echo "          /\ /\ "
    echo "          \ T /"
    echo "          (/ \)\ "
    echo "               ))"
    echo "              (("
    echo "MARVIN STOPPED \)"
    exit
fi

echo "STARTING MARVIN..."
python run_daemon.py &
echo $! > ${RUNDIR}/marvin_daemon.pid
#gunicorn marvin.stats.views:app -b 127.0.0.1:5000 &
echo $! > ${RUNDIR}/marvin_stats.pid
sleep 1

echo "             *     ,MMM8&&&.            *"
echo "                  MMMM88&&&&&    ."
echo "                 MMMM88&&&&&&&"
echo "     *           MMM88&&&&&&&&"
echo "                 MMM88&&&&&&&&"
echo "                 'MMM88&&&&&&'"
echo "                   'MMM8&&&'      *"
echo "          |\___/|"
echo "          )     (             .              '"
echo "         =\     /="
echo "           )===(       *"
echo "          /     \ "
echo "          |     |"
echo "         /       \ "
echo "         \       /"
echo "  _/\_/\_/\__  _/_/\_/\_/\_/\_/\_/\_/\_/\_/\_"
echo "  |  |  |  |( (  |  |  |  |  |  |  |  |  |  |"
echo "  |  |  |  | ) ) |  |  |  |  |  |  |  |  |  |"
echo "  |  |  |  |(_(  |  |  |  |  |  |  |  |  |  |"
echo "  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |"
echo "  jgs|  |  |  |  |  MARVIN STARTED |  |  |  |"
