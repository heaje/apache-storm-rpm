#!/bin/bash
#
### BEGIN INIT INFO
# Provides: $storm-daemon
# Default-Start: 3 4 5
# Default-Stop: 0 1 6
### END INIT INFO

# Source function library.
. /etc/init.d/functions
RETVAL=0

NAME=$(basename ${0})
SERVICE_NAME=$(echo "${NAME}" | cut -d "-" -f2)

# Source config
[ -f /etc/sysconfig/storm ] && . /etc/sysconfig/storm
[ -f /etc/sysconfig/${NAME} ] && . /etc/sysconfig/${NAME}

if [ -z "${CLASSNAME}" ]; then
	[ "ui" == "${SERVICE_NAME}" ] && CLASSNAME="backtype.storm.ui.core" || CLASSNAME="backtype.storm.daemon.${SERVICE_NAME}"
fi

STORM_HOME=${STORM_HOME:-"/usr/lib/storm"}
STORM_OPTIONS=${STORM_OPTIONS:-"-server"}
LOG_DIR=${LOG_DIR:-"/var/log/storm"}
PID_FILE=${PID_FILE:-"/var/run/storm/${NAME}.pid"}
LOGFILE_NAME=${LOGFILE_NAME:-"${SERVICE_NAME}.log"}
LOG4J2_CONFIG_FILE=${LOG4J2_CONFIG_FILE:-"/etc/storm/log4j2/cluster.xml"}
MEMORY_JVM_OPTS=${MEMORY_JVM_OPTS:-"-Xmx256M"}
CLASSPATH=${CLASSPATH:-"/usr/lib/storm/lib/*"}
EXTRA_JVM_OPTS=${EXTRA_JVM_OPTS:-""}

if [ -d ${STORM_HOME}/external ]; then
	for extlib in $(ls ${STORM_HOME}/external); do
		CLASSPATH="${CLASSPATH}:${STORM_HOME}/external/${extlib}"
	done
fi


if [ -z "${CLASSNAME}" ]; then
  echo "\$CLASSNAME variable is not set.  Cannot run ${NAME}"
  exit 2
fi

start() {
    if storm_status>/dev/null; then
    	echo "${NAME} is already running."
    	exit 1
    else
    	echo -n $"Starting ${NAME}: "
    fi 
    STORM_CMD="java ${MEMORY_JVM_OPTS} ${EXTRA_JVM_OPTS} -server -Dstorm.home=\"${STORM_HOME}\" -Dlog4j.configurationFile=\"${LOG4J2_CONFIG_FILE}\" -Dstorm.log.dir=\"${LOG_DIR}\" -Dlogfile.name=${LOGFILE_NAME} -cp \"$CLASSPATH\" ${CLASSNAME} &> /dev/null &"
	daemon --user ${STORM_USER} --pidfile ${PID_FILE} "${STORM_CMD} &> /dev/null && echo \$! > ${PID_FILE}"
    RETVAL=$?
    echo
    storm_status>/dev/null
    return $RETVAL
}

stop() {
    if storm_status>/dev/null; then
        echo -n $"Stopping ${NAME}: "
        killproc -p $PID_FILE -TERM
        RETVAL=$?
        echo
    else
        return 0
    fi
    return $RETVAL
}

storm_status() {
    status -p $PID_FILE ${NAME}
    return $?
}

restart() {
        stop
        start
}

reload()  {
    restart
}

case "$1" in
  start)
        start
        ;;
  stop)
        stop
        ;;
  status)
        storm_status		 
        ;;
  restart)
        restart
        ;;
  reload)
        reload
        ;;
  *)
        echo $"Usage: $0 {start|stop|status|restart}"
        exit 2
esac

exit $?

