FROM cloudpg/centos-7-grid
LABEL maintainer="diego.ciangottini@pg.infn.it"
LABEL Version=1.0

RUN yum install -y xrootd-server 

COPY xrd.conf /etc/xrootd/xrd.conf
RUN chown -R xrootd:xrootd /etc/xrootd/

COPY entrypoint.sh /usr/local/bin/entrypoint
RUN chmod +x /usr/local/bin/entrypoint
RUN chown xrootd:xrootd  /usr/local/bin/entrypoint

RUN mkdir -p /data/xrd
RUN chown -R xrootd:xrootd /data/xrd

USER xrootd
ENTRYPOINT ["/usr/local/bin/entrypoint"]