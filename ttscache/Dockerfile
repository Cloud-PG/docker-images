FROM cloudpg/centos-7-grid
LABEL maintainer="mirco.tracolli@pg.infn.it"
LABEL Version=1.0

# GET_PROXY STUFF
RUN yum --setopt=tsflags=nodocs -y install python python-pip \
    && yum clean all \
    && pip install --upgrade pip \
    && pip install requests kazoo flask \
    && mkdir -p /opt/certcache/ \
    && mkdir -p /var/log/certcache/ \
    && touch /var/log/certcache/app.log
COPY ./proxy_config.json ./proxy.py ./cache.py ./app_ttscache.py /opt/certcache/

EXPOSE 80

CMD ["/usr/bin/python", "/opt/certcache/app_ttscache.py"]
