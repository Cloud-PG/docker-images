#!/bin/bash

if [ "$1" == "master" ];
then
    echo "==> Check CONDOR_HOST"
    if [ "$CONDOR_HOST" == "ZOOKEEPER" ];
    then
        echo "==> CONDOR_HOST with Zookeeper"
        echo "==> Get Master IP"
        export CONDOR_HOST=$(hostname -i)
        echo "==> Set Master IP on Zookeeper"
        dodas_cache zookeeper CONDOR_HOST "$CONDOR_HOST"
    else
        echo "==> CONDOR_HOST with ENV"
    fi
    echo "==> Compile configuration file for master node with env vars"
    export NETWORK_INTERFACE=$(hostname -i)
    export CONDOR_DAEMON_LIST="COLLECTOR, MASTER, NEGOTIATOR"
    export NETWORK_INTERFACE_STRING="NETWORK_INTERFACE = $NETWORK_INTERFACE"
    j2 /opt/dodas/htc_config/condor_config.template > /etc/condor/condor_config
    echo "==> Start condor"
    condor_master -f
elif [ "$1" == "wn" ];
then
    echo "==> Check CONDOR_HOST"
    if [ "$CONDOR_HOST" == "ZOOKEEPER" ];
    then
        echo "==> CONDOR_HOST with Zookeeper"
        echo "==> Get Master ip with Zookeeper"
        export CONDOR_HOST=$(dodas_cache --wait-for true zookeeper CONDOR_HOST)
        export CCB_ADDRESS="$CONDOR_HOST"
    else
        echo "==> CONDOR_HOST with ENV"
    fi
    echo "==> Compile configuration file for worker node with env vars"
    export CONDOR_DAEMON_LIST="MASTER, STARTD"
    export CCB_ADDRESS_STRING="CCB_ADDRESS = $CCB_ADDRESS"
    j2 /opt/dodas/htc_config/condor_config.template > /etc/condor/condor_config
    echo "==> Start condor"
    condor_master -f
    echo "==> Start service"
elif [ "$1" == "schedd" ];
then
    echo "==> Check CONDOR_HOST"
    if [ "$CONDOR_HOST" == "ZOOKEEPER" ];
    then
        echo "==> CONDOR_HOST with Zookeeper"
        echo "==> Get Master ip with Zookeeper"
        export CONDOR_HOST=$(dodas_cache --wait-for true zookeeper CONDOR_HOST)
    else
        echo "==> CONDOR_HOST with ENV"
    fi
    echo "==> Compile configuration file for sheduler node with env vars"
    export NETWORK_INTERFACE=$(hostname -i)
    export CONDOR_DAEMON_LIST="MASTER, SCHEDD"
    export NETWORK_INTERFACE_STRING="NETWORK_INTERFACE = $NETWORK_INTERFACE"
    j2 /opt/dodas/htc_config/condor_config.template > /etc/condor/condor_config
    echo "==> Public schedd host"
    dodas_cache zookeeper SCHEDD_HOST "$NETWORK_INTERFACE"
    echo ""
    echo "==> Start condor"
    condor_master
    echo "==> Start sshd on port $CONDOR_SCHEDD_SSH_PORT"
    exec /usr/sbin/sshd -E /var/log/sshd.log -g 30 -p $CONDOR_SCHEDD_SSH_PORT -D
elif [ "$1" == "all" ];
then
    echo "==> Compile configuration file for sheduler node with env vars"
    j2 /opt/dodas/htc_config/condor_config.template > /etc/condor/condor_config
    echo "==> Start condor"
    condor_master -f
    echo "==> Start sshd on port $CONDOR_SCHEDD_SSH_PORT"
    exec /usr/sbin/sshd -E /var/log/sshd.log -g 30 -p $CONDOR_SCHEDD_SSH_PORT -D
else
    echo "[ERROR]==> You have to supply a role, like: 'master', 'wn', 'schedd' or 'all'..."
    exit 1
fi