FROM cloudpg/centos-7-grid
LABEL maintainer="diego.ciangottini@pg.infn.it"
LABEL Version=1.0

RUN yum install -y xrootd-server sudo \
    && yum --setopt=tsflags=nodocs -y install python python-pip \
    && pip install flask 

RUN mkdir -p /etc/grid-security/xrd
RUN chown -R xrootd:xrootd /etc/grid-security/xrd

COPY config/xrd_test.conf /etc/xrootd/xrd_test.conf
COPY config/xrd_test_redir.conf /etc/xrootd/xrd_test_redir.conf
COPY config/xrd_test_origin.conf /etc/xrootd/xrd_test_origin.conf
COPY config/xrd_cache.conf /etc/xrootd/xrd_cache.conf
COPY config/xrd_redirector.conf /etc/xrootd/xrd_redirector.conf
COPY config/Authfile-auth /etc/xrootd/Authfile-auth

# xrootd:xrootd docker => 998:996 on localhost
RUN chown -R xrootd:xrootd /etc/xrootd/

RUN mkdir -p /opt/xrd_proxy
COPY bin/entrypoint.py /opt/xrd_proxy/entrypoint.py
COPY bin/install_ca.sh /opt/xrd_proxy/install_ca.sh
COPY bin/refresh_cert.sh /opt/xrd_proxy/refresh_cert.sh
RUN chown -R xrootd:xrootd  /opt/xrd_proxy/
RUN chmod +x /opt/xrd_proxy/install_ca.sh
RUN chmod +x /opt/xrd_proxy/refresh_cert.sh

RUN mkdir -p /data/xrd
RUN chown -R xrootd:xrootd /data/xrd

RUN mkdir -p /var/log/xrootd/
RUN chown -R xrootd:xrootd /var/log/xrootd/

RUN echo 'xrootd ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

EXPOSE 80

ENTRYPOINT ["/usr/bin/python", "/opt/xrd_proxy/entrypoint.py"]
