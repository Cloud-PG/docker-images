#!/bin/bash

echo $@

echo "PROXY_CACHE: $PROXY_CACHE"
echo "curl -s -w%{http_code} $PROXY_CACHE/cgi-bin/get_proxy -o /tmp/x509up_u998" 

resp=0
until [  $resp -eq 200 ]; do
    resp=$(curl -s \
        -w%{http_code} \
        $PROXY_CACHE/cgi-bin/get_proxy -o /tmp/x509up_u998)
done
#############

chmod 600 /tmp/x509up_u998

export X509_USER_PROXY=/tmp/x509up_u998

mkdir -p /etc/grid-security/xrd/

# COPY HOSTCERTS HERE

resp=0
echo "curl -s -w%{http_code} $PROXY_CACHE/get_cert -o /etc/grid-security/xrd/usercert.pem"
until [  $resp -eq 200 ]; do
    resp=$(curl -s \
        -w%{http_code} \
        $PROXY_CACHE/get_cert -o /etc/grid-security/xrd/usercert.pem)
done


resp=0
echo "curl -s -w%{http_code} $PROXY_CACHE/get_key -o /etc/grid-security/xrd/usercert.pem"
until [  $resp -eq 200 ]; do
    resp=$(curl -s \
        -w%{http_code} \
        $PROXY_CACHE/get_key -o /etc/grid-security/xrd/userkey.pem)
done


chmod 600 /etc/grid-security/xrd/userkey.pem


echo "u * / rl" > /etc/xrootd/Authfile-auth

if [[ -n "$1" ]]; then
    if [[ "$1" == "proxy" ]]; then

        cp /etc/xrootd/xrd_cache.conf  /etc/xrootd/xrd.conf
        if [[ "$2" == "-redirector_url" && -n "$3" ]]; then
            sed -i -e "s/rdtr_cache/$3/" /etc/xrootd/xrd.conf
        fi
        if [[ "$4" == "-cmsd_redirector_port" && -n "$5" ]]; then
            sed -i -e "s/rdtr_port_cmsd/$5/" /etc/xrootd/xrd.conf
        fi
        if [[ "$6" == "-xrd_redirector_port" && -n "$7" ]]; then
            sed -i -e "s/rdtr_port_xrd/$7/" /etc/xrootd/xrd.conf
        fi
        if [[ "$8" == "-redirector_global" && -n "$9" ]]; then
            sed -i -e "s/rdtr_global:/$9:/" /etc/xrootd/xrd.conf
        fi
        if [[ "${10}" == "-redirector_global_port" && -n "${11}" ]]; then
            sed -i -e "s/rdtr_global_port/${11}/" /etc/xrootd/xrd.conf
        fi 

    elif [[ "$1" == "redirector" ]]; then
        cp /etc/xrootd/xrd_redirector.conf  /etc/xrootd/xrd.conf
        if [[ "$2" == "-cmsd_redirector_port" && -n "$3" ]]; then
            sed -i -e "s/rdtr_port_cmsd/$3/" /etc/xrootd/xrd.conf
        fi
        if [[ "$4" == "-xrd_redirector_port" && -n "$5" ]]; then
            sed -i -e "s/rdtr_port_xrd/$5/" /etc/xrootd/xrd.conf
        fi
        if [[ "$6" == "-redirector_global" && -n "$7" ]]; then
            sed -i -e "s/rdtr_global:/$7:/" /etc/xrootd/xrd.conf
        fi
        if [[ "$8" == "-redirector_global_port" && -n "$9" ]]; then
            sed -i -e "s/rdtr_global_port/$9/" /etc/xrootd/xrd.conf
        fi 
        if [[ "${10}" == "-redirector_url" && -n "${11}" ]]; then
            sed -i -e "s/rdtr_cache/${11}/" /etc/xrootd/xrd.conf
        fi
    else 
        echo "no Valid options"
    fi

fi

xrootd -d3 -b -c /etc/xrootd/xrd.conf -l /var/log/xrootd/proxyXrd.log 
exec cmsd -c /etc/xrootd/xrd.conf
