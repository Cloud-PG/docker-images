FROM cloudpg/centos-7-grid
LABEL maintainer="diego.ciangottini@pg.infn.it"
LABEL Version=1.0

RUN yum install -y xrootd-server sudo

RUN mkdir -p /etc/grid-security/xrd
RUN chown -R xrootd:xrootd /etc/grid-security/xrd

# xrootd:xrootd docker => 998:996 on localhost
RUN chown -R xrootd:xrootd /etc/xrootd/

RUN mkdir -p /opt/xrd_proxy
COPY entrypoint.py /opt/xrd_proxy/entrypoint.py
COPY install_ca.sh /opt/xrd_proxy/install_ca.sh
RUN chown -R xrootd:xrootd  /opt/xrd_proxy/
RUN chmod +x /opt/xrd_proxy/install_ca.sh

RUN mkdir -p /data/xrd
RUN chown -R xrootd:xrootd /data/xrd

RUN mkdir -p /var/log/xrootd/
RUN chown -R xrootd:xrootd /var/log/xrootd/

RUN echo 'xrootd ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER xrootd

ENTRYPOINT ["/usr/bin/python", "/opt/xrd_proxy/entrypoint.py"]
