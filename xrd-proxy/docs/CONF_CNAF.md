# INSTALLATION GUIDE

## REQUIREMENTS

- OS:
- Port: one open service port + 8443
- Valid grid host certifate
- Valid service certificate, able to read from AAA (/etc/grid-security/xrd/xrdcert.pem, /etc/grid-security/xrd/xrdkey.pem)

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
    && yum --setopt=tsflags=nodocs -y install fetch-crl wn \
    && yum clean all

yum install -y ca-policy-egi-core ca-policy-lcg
/usr/sbin/fetch-crl -q

mkdir -p /etc/grid-security/xrd/

chown -R xrootd:xrootd /etc/grid-security/xrd/

systemctl enable fetch-crl-cron
systemctl start fetch-crl-cron

curl -L -O https://artifacts.elastic.co/downloads/beats/metricbeat/metricbeat-6.2.4-x86_64.rpm
sudo rpm -vi metricbeat-6.2.4-x86_64.rpm
```

## PROXY RENEWAL

/usr/lib/systemd/system/xrootd-renew-proxy.service

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

/usr/lib/systemd/system/xrootd-renew-proxy.timer

```
[Unit]
Description=Renew proxy every day at midnight

[Timer]
OnCalendar=*-*-* 00:00:00
Unit=xrootd-renew-proxy.service

[Install]
WantedBy=multi-user.target
```

systemctl start xrootd-renew-proxy.timer

systemctl daemon-reload

## XROOTD SERVER CONFIGURATION

/etc/xrootd/xrootd-xcache.cfg

```bash
#
set rdtrCache=
set rdtrPortCmsd=
#
set rdtrGlobal=
set rdtrGlobalPort=
#
set cacheLowWm=
set cacheHiWm=
#
set cacheLogLevel=
#
set cachePath=
set cacheRam=
set cacheStreams=
set prefetch=
set blkSize=

all.manager $rdtrCache:$rdtrPortCmsd

xrootd.trace all
ofs.trace all
xrd.trace all
cms.trace all
sec.trace all
pfc.trace $cacheLogLevel

if exec cmsd

all.role server
xrd.port 31113

all.export / stage
oss.localroot $cachePath

else

all.export /
all.role  server
oss.localroot $cachePath

xrd.port 32294
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
#xrootd.monitor all auth flush 30s window 5s fstat 60 lfn ops xfr 5 dest redir fstat info user <host>:<>
```

/etc/xrootd/Authfile-noauth

```
u * /store/ lr / rl
```

## METRICBEAT CONFIGURATION

/etc/metricbeat/metricbeat.yml

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
name:

#================================ Outputs =====================================

# Configure what outputs to use when sending the data collected by the beat.
# Multiple outputs may be used.

#-------------------------- Elasticsearch output ------------------------------
output.elasticsearch:
  # Array of hosts to connect to.
  hosts: ["DUMMY.com"]
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

systemctl enable xrootd@xcache.service
systemctl enable cmsd@xcache.service

systemctl start xrootd@xcache.service
systemctl start cmsd@xcache.service

## TESTING THE DEPLOYMENT

