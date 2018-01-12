FROM docker.elastic.co/beats/metricbeat:6.1.1
COPY metricbeat_conf.yml /usr/share/metricbeat/metricbeat.yml
USER root
RUN chown metricbeat /usr/share/metricbeat/metricbeat.yml
USER metricbeat