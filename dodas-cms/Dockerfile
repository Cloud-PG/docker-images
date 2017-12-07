FROM cloudpg/centos-7-grid
LABEL maintainer="mirco.tracolli@pg.infn.it"
LABEL Version=1.0

# HTCondor
# https://get.onedata.org/oneclient.sh 

WORKDIR /etc/yum.repos.d

RUN useradd -ms /bin/bash condor \
    && wget http://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-development-rhel7.repo \
    && wget http://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel7.repo \
    && wget http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor \
    && rpm --import RPM-GPG-KEY-HTCondor \
    && wget -O onedata.repo http://packages.onedata.org/yum/onedata_centos_7x.repo \
    && yum --setopt=tsflags=nodocs -y update \
    && yum --setopt=tsflags=nodocs -y install condor-all \
    && yum --setopt=tsflags=nodocs --enablerepo=onedata -y install oneclient \
    && yum clean all \
    && ln -s /usr/lib64/condor /usr/lib/condor \
    && ln -s /usr/libexec/condor /usr/lib/condor/libexec

ADD condorconfig /etc/condor/
ADD config.d /etc/condor/config.d/
ADD dodas_bin  /usr/local/bin/

WORKDIR /root

RUN chmod +x /usr/local/bin/dodasexe_pre.sh \
    && chmod +x /usr/local/bin/dodasexe.sh \
    && chmod +x /usr/local/bin/dodas.sh \
    # onedata directories needed by mount
    && mkdir -p /mnt/onedata/ /var/log/dodas
