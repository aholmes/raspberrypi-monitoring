#! /bin/sh

cd /home/pi/rasppi-prometheus
. .venv/bin/activate

### BEGIN INIT INFO
# Provides:          rasppi-prometheus.py
# Required-Start:    $remote_fs $syslog
# Required-Stop:     $remote_fs $syslog
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
### END INIT INFO

# Carry out specific functions when asked to by the system
case "$1" in
  start)
    echo "Starting rasppi-prometheus.py"
    ./rasppi-prometheus.py &
    ;;
  stop)
    echo "Stopping rasppi-prometheus.py"
    pkill -f rasppi-prometheus.py
    ;;
  *)
    echo "Usage: /etc/init.d/rasppi-prometheus.sh {start|stop}"
    exit 1
    ;;
esac

exit 0
