FROM cloudpg/centos-7-grid
LABEL maintainer="diego.ciangottini@pg.infn.it"
LABEL Version=1.0

RUN yum install -y xrootd-server ca-policy-egi-core ca-policy-lcg

RUN /usr/sbin/fetch-crl -q

RUN wget -O /etc/yum.repos.d/ca_CMS-TTS-CA.repo https://ci.cloud.cnaf.infn.it/job/cnaf-mw-devel-jobs/job/ca_CMS-TTS-CA/job/master/lastSuccessfulBuild/artifact/ca_CMS-TTS-CA.repo
RUN yum -y install ca_CMS-TTS-CA

RUN mkdir -p /etc/grid-security/xrd
RUN chown -R xrootd:xrootd /etc/grid-security/xrd

# xrootd:xrootd docker => 998:996 on localhost
RUN chown -R xrootd:xrootd /etc/xrootd/

RUN mkdir -p /opt/xrd_proxy
COPY entrypoint.py /opt/xrd_proxy/entrypoint.py
RUN chown -R xrootd:xrootd  /opt/xrd_proxy/

RUN mkdir -p /data/xrd
RUN chown -R xrootd:xrootd /data/xrd

USER xrootd
ENTRYPOINT ["/usr/bin/python", "/opt/xrd_proxy/entrypoint.py"]
