# INSTALLATION GUIDE

## REQUIREMENTS

- OS: Centos7
- Port: one open service port + 8443
- Valid grid host certifate
- Valid service certificate that is able to read from AAA (/etc/grid-security/xrd/xrdcert.pem, /etc/grid-security/xrd/xrdkey.pem)

## PACKAGES INSTALLATION

```bash
echo "LC_ALL=C" >> /etc/environment \
    && echo "LANGUAGE=C" >> /etc/environment \
    && yum --setopt=tsflags=nodocs -y update \
    && yum --setopt=tsflags=nodocs -y install wget \
    && yum clean all

cd /etc/yum.repos.d
wget http://repository.egi.eu/community/software/preview.repository/2.0/releases/repofiles/centos-7-x86_64.repo \
    && wget http://repository.egi.eu/sw/production/cas/1/current/repo-files/EGI-trustanchors.repo
yum --setopt=tsflags=nodocs -y install epel-release yum-plugin-ovl \
    && yum --setopt=tsflags=nodocs -y install fetch-crl wn sysstat \
    && yum clean all

yum install -y ca-policy-egi-core ca-policy-lcg
/usr/sbin/fetch-crl -q

yum install xrootd-server

mkdir -p /etc/grid-security/xrd/

chown -R xrootd:xrootd /etc/grid-security/xrd/

systemctl enable fetch-crl-cron
systemctl start fetch-crl-cron

curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-6.2.4-x86_64.rpm
sudo rpm -vi metricbeat-6.2.4-x86_64.rpm
```

## PROXY RENEWAL

- `cat /usr/lib/systemd/system/xrootd-renew-proxy.service`

```bash
[Unit]
Description=Renew xrootd proxy

[Service]
User=xrootd
Group=xrootd
Type = oneshot
ExecStart = /bin/grid-proxy-init -cert /etc/grid-security/xrd/xrdcert.pem -key /etc/grid-security/xrd/xrdkey.pem -out /tmp/x509up_u995 -valid 48:00

[Install]
WantedBy=multi-user.target
```

- `cat /usr/lib/systemd/system/xrootd-renew-proxy.timer`

```
[Unit]
Description=Renew proxy every day at midnight

[Timer]
OnCalendar=*-*-* 00:00:00
Unit=xrootd-renew-proxy.service

[Install]
WantedBy=multi-user.target
```

- `systemctl start xrootd-renew-proxy.timer`

- `systemctl daemon-reload`

## XROOTD SERVER CONFIGURATION

Configuration file may be adapted in the future to send xrd information via UDP at a testbed elasticsearch endpoint (a kafka stream is in the plan later on).

**DISCLAIMER**: fields surrounded by `<>` or called `DUMMY` are to be substituted with values that varies case by case.

- `cat /etc/xrootd/xrootd-xcache.cfg`

```bash
#
set rdtrCache=<host cache redirector>
set rdtrPortCmsd=<port of cmsd cache redirector>
#
set rdtrGlobal=xrootd-cms.infn.it
set rdtrGlobalPort=1094
#
set cacheLowWm=0.70
set cacheHiWm=0.85
#
set cacheLogLevel=info
#
set xrdport=1094
set cmsdport=1213
#
set cachePath=<path to folder for storing data, NB it has to be owned by xrootd user>
set cacheRam=<ram dedicated to cache, ~50% of the total is suggested>
set cacheStreams=256
set prefetch=0
set blkSize=512k

all.manager $rdtrCache:$rdtrPortCmsd

xrootd.trace all
ofs.trace all
xrd.trace all
cms.trace all
sec.trace all
pfc.trace $cacheLogLevel

if exec cmsd

all.role server
xrd.port $cmsdport

all.export / stage
oss.localroot $cachePath

else

all.export /
all.role  server
oss.localroot $cachePath

xrd.port $xrdport
# For xrootd, load the proxy plugin and the disk caching plugin.
#
ofs.osslib   libXrdPss.so
pss.cachelib libXrdFileCache.so

pss.origin $rdtrGlobal:$rdtrGlobalPort

pss.config streams $cacheStreams

xrootd.seclib /usr/lib64/libXrdSec.so

sec.protocol /usr/lib64 gsi \
  -certdir:/etc/grid-security/certificates \
  -cert:/etc/grid-security/xrd/xrdcert.pem \
  -key:/etc/grid-security/xrd/xrdkey.pem \
  -d:3 \
  -crl:1

ofs.authorize 1
acc.audit deny grant
acc.authdb /etc/xrootd/Authfile-auth
sec.protbind * gsi

pfc.diskusage $cacheLowWm $cacheHiWm
pfc.ram       ${cacheRam}g

pfc.blocksize   $blkSize
pfc.prefetch    $prefetch

fi

#xrd.report <host>:<port>
#xrootd.monitor all auth flush 30s window 5s fstat 60 lfn ops xfr 5 dest redir fstat info user pfc <host>:<>
```

- `cat /etc/xrootd/Authfile-noauth`

```
u * /store/ lr / rl
```

## METRICBEAT CONFIGURATION

Setup and configure metricbeat to collect information on host metrics on an elasticsearch endpoint.

**DISCLAIMER**: fields surrounded by `<>` or called `DUMMY` are to be substituted with values that varies case by case.

- `cat /etc/metricbeat/metricbeat.yml`

```yaml

# You can find the full configuration reference here:
# https://www.elastic.co/guide/en/beats/metricbeat/index.html

#==========================  Modules configuration ============================
metricbeat.modules:

#------------------------------- System Module -------------------------------
- module: system
  metricsets:
    # CPU stats
    - cpu

    # System Load stats
    - load

    # Per CPU core stats
    - core

    # IO stats
    - diskio

    # Per filesystem stats
    - filesystem

    # File system summary stats
    - fsstat

    # Memory stats
    - memory

    # Network stats
    - network

    # Per process stats
    - process

    # Sockets (linux only)
    #- socket
  enabled: true
  period: 60s
  processes: ['.*']


#================================ General =====================================

# The name of the shipper that publishes the network data. It can be used to group
# all the transactions sent by a single shipper in the web interface.
name: 'DUMMY: cache sitename'

#================================ Outputs =====================================

# Configure what outputs to use when sending the data collected by the beat.
# Multiple outputs may be used.

#-------------------------- Elasticsearch output ------------------------------
output.elasticsearch:
  # Array of hosts to connect to.
  hosts: ["DUMMY_esHost.com"]
  template.name: "metricbeat_slave"
  template.path: "metricbeat.template.json"
  template.overwrite: false

  # Optional protocol and basic auth credentials.
  protocol: "http"
  username: "dodas"
  password: "DUMMY"

#================================ Logging =====================================

# Sets log level. The default log level is info.
# Available log levels are: critical, error, warning, info, debug
#logging.level: debug
```

## STARTING DAEMONS

```bash
systemctl enable xrootd@xcache.service
systemctl enable cmsd@xcache.service

systemctl start xrootd@xcache.service
systemctl start cmsd@xcache.service

systemctl enable metricbeat.service
systemctl start metricbeat.service
```

## TESTING THE DEPLOYMENT

- `systemctl status xrootd@xcache.service`
```
* xrootd@xcache.service - XRootD xrootd deamon instance xcache
   Loaded: loaded (/usr/lib/systemd/system/xrootd@.service; enabled; vendor preset: disabled)
   Active: active (running) since Fri 2018-05-25 07:17:21 UTC; 36min ago
     Docs: man:xrootd(8)
           http://xrootd.org/docs.html
 Main PID: 19933 (xrootd)
   CGroup: /system.slice/system-xrootd.slice/xrootd@xcache.service
           `-19933 /usr/bin/xrootd -l /var/log/xrootd/xrootd.log -c /etc/xrootd/xrootd-xcache.cfg -k fifo -s /var/r...

May 25 07:17:21 xrootdcentostest systemd[1]: Started XRootD xrootd deamon instance xcache.
May 25 07:17:21 xrootdcentostest systemd[1]: Starting XRootD xrootd deamon instance xcache...
```

- `systemctl status cmsd@xcache.service`: similar output as above

- `xrdcp -f -v xroot://localhost:<xrdport defined in the configuration above>//store/mc/RunIISummer17DRPremix/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/AODSIM/92X_upgrade2017_realistic_v10-v2/90000/C85940F6-9596-E711-8FD6-D8D385FF1940.root /dev/null`

```
[root@xrootdcentostest centos]# xrdcp -f -v xroot://localhost:32294//store/mc/RunIISummer17DRPremix/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/AODSIM/92X_upgrade2017_realistic_v10-v2/90000/C85940F6-9596-E711-8FD6-D8D385FF1940.root /dev/null
[544MB/3.108GB][ 17%][========>                                         ][19.43MB/s]
```

- at the end of transferring, the file has to be visible in the `<cache path>` indicated in the xrood-xcache configuration:

`ls <cache path>/store/mc/RunIISummer17DRPremix/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/AODSIM/92X_upgrade2017_realistic_v10-v2/90000/C85940F6-9596-E711-8FD6-D8D385FF1940.root`
```
<cache path>/store/mc/RunIISummer17DRPremix/QCD_Pt-15to20_MuEnrichedPt5_TuneCUETP8M1_13TeV_pythia8/AODSIM/92X_upgrade2017_realistic_v10-v2/90000/C85940F6-9596-E711-8FD6-D8D385FF1940.root
```
