FROM cloudpg/centos-7-grid
LABEL maintainer="mirco.tracolli@pg.infn.it"
LABEL Version=1.0

# GET_PROXY STUFF
RUN yum --setopt=tsflags=nodocs -y update \
    && yum --setopt=tsflags=nodocs -y install python python-pip \
    && yum clean all \
    && pip install --upgrade pip \
    && pip install requests kazoo flask \
    && mkdir -p /opt/ttscache/ \
    && mkdir -p /var/log/ttscache/ \
    && touch /var/log/ttscache/app.log
COPY ./proxy_config.json ./proxy.py ./cache.py ./app_ttscache.py /opt/ttscache/

EXPOSE 80

CMD ["/usr/bin/python", "/opt/ttscache/app_ttscache.py"]
