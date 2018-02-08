FROM python:3-alpine
LABEL maintainer="mirco.tracolli@pg.infn.it"
LABEL Version=1.0

# GET_PROXY STUFF
RUN apk update \
    && apk upgrade \
    && apk add python3-dev curl-dev gcc musl-dev openssl-dev \
    && pip install --upgrade pip \
    && pip install requests flask kazoo pycurl \
    && mkdir -p /opt/ttscache/ \
    && mkdir -p /var/log/ttscache/ \
    && touch /var/log/ttscache/app.log
COPY ./proxy_config.json ./proxy.py ./cache.py ./app_ttscache.py /opt/ttscache/

EXPOSE 80

CMD ["/usr/bin/python3", "/opt/ttscache/app_ttscache.py"]
