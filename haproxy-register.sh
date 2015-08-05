#/bin/bash

MYDIR=/opt
HAPROXYCONF=/etc/haproxy/haproxy.cfg

if [ -z $1 or -z $2 ] ; then
    exit -1
fi

SERVICENAME=$1
ACTION=$2
PORT=$3

case $ACTION in
    reg)
       $MYDIR/HAAutoReg.py addServer --service $SERVICENAME --name $REMOTE_HOST --addr $REMOTE_HOST:$PORT
       $MYDIR/HAAutoReg.py print > $HAPROXYCONF
       service haproxy reload &> /dev/null

    del)
       $MYDIR/HAAutoReg.py delServer --service $SERVICENAME --name $REMOTE_HOST
       $MYDIR/HAAutoReg.py print > $HAPROXY
       service haproxy reload &> /dev/null
esac

#/etc/xinet.d/haregister example
#service autoregister
#{
#        disable         = no
#        socket_type     = stream
#        protocol        = tcp
#        user            = root
#        wait            = no
#        server          = /opt/autoregister-echo.sh
#        server_args     = reg 2000
#}

#service autoderegister
#{
#        disable         = no
#        socket_type     = stream
#        protocol        = tcp
#        user            = root
#        wait            = no
#        server          = /opt/autoregister-echo.sh
#        server_args     = del
#}

#/etc/services example
#autoregister    4000/tcp
#autoderegister  4001/tcp

