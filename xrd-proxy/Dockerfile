FROM cloudpg/centos-7-grid
LABEL maintainer="diego.ciangottini@pg.infn.it"
LABEL Version=1.0

RUN yum install -y xrootd-server ca-policy-egi-core ca-policy-lcg

#RUN wget -O /etc/yum.repos.d/ca_CMS-TTS-CA.repo https://ci.cloud.cnaf.infn.it/job/cnaf-mw-devel-jobs/job/ca_CMS-TTS-CA/job/master/lastSuccessfulBuild/artifact/ca_CMS-TTS-CA.repo
COPY TTS-CA.repo /etc/yum.repos.d/ca_CMS-TTS-CA.repo
RUN yum -y install ca_CMS-TTS-CA
RUN /usr/sbin/fetch-crl -q


RUN mkdir -p /etc/grid-security/xrd
RUN chown -R xrootd:xrootd /etc/grid-security/xrd

# xrootd:xrootd docker => 998:996 on localhost
COPY xrd_cache.conf /etc/xrootd/xrd_cache.conf
COPY xrd_redirector.conf /etc/xrootd/xrd_redirector.conf
RUN chown -R xrootd:xrootd /etc/xrootd/

COPY entrypoint.sh /usr/local/bin/entrypoint
RUN chmod +x /usr/local/bin/entrypoint
RUN chown xrootd:xrootd  /usr/local/bin/entrypoint

RUN mkdir -p /data/xrd
RUN chown -R xrootd:xrootd /data/xrd

USER xrootd
EXPOSE 1094
ENTRYPOINT ["/usr/local/bin/entrypoint"]
