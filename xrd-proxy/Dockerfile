FROM cloudpg/centos-7-grid
LABEL maintainer="diego.ciangottini@pg.infn.it"
LABEL Version=1.0

RUN yum install -y xrootd-server 

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