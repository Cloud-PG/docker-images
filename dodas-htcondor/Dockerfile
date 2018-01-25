FROM cloudpg/centos-7-grid-tini-sshd

# condor_collector
EXPOSE 9618
# condor_negotiator
EXPOSE 9614
# condor_ckpt_server
EXPOSE 5651-5654
# condor env default values
ENV CONDOR_DAEMON_LIST="COLLECTOR, MASTER, NEGOTIATOR, SCHEDD, STARTD"
ENV CONDOR_FULL_HOSTNAME="\$(FULL_HOSTNAME)"
ENV CONDOR_SCHEDD_SSH_PORT=31042
ENV SEC_DEFAULT_AUTHENTICATION=ANONYMOUS
ENV SEC_DAEMON_AUTHENTICATION_METHODS=ANONYMOUS
ENV SEC_CLIENT_AUTHENTICATION_METHODS=ANONYMOUS
ENV SEC_NEGOTIATOR_AUTHENTICATION_METHODS=ANONYMOUS
ENV SEC_ADVERTISE_STARTD_AUTHENTICATION_METHODS=ANONYMOUS

WORKDIR /etc/yum.repos.d

RUN useradd -ms /bin/bash condor \
    && wget http://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-development-rhel7.repo \
    && wget http://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel7.repo \
    && wget http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor \
    && rpm --import RPM-GPG-KEY-HTCondor \
    && yum --setopt=tsflags=nodocs -y update \
    && yum --setopt=tsflags=nodocs -y install condor-all python-pip \
    && yum --setopt=tsflags=nodocs -y install binutils \
        boost-devel \
        cmake3 \
        curl \
        cvs \
        emacs \
        freetype \
        freetype-devel \
        fuse \
        gcc \
        gcc-c++ \
        git \
        glibc-devel \
        glibc-headers \
        gsl-devel \
        initscripts \
        krb5-workstation \
        libSM \
        libX11-devel \
        libXext \
        libXext-devel \
        libXft-devel \
        libXpm \
        libXpm-devel \
        make \
        man \
        nano \
        ncurses \
        ncurses-devel \
        openssh-clients \
        openssh-server \
        openssl098e \
        pam-krb5 \
        sudo \
        vim \
    && yum clean all \
    && pip install --upgrade pip \
    && pip install j2cli

# Root home
WORKDIR /root

RUN mkdir -p /opt/dodas/htc_config
COPY condor.sh /opt/dodas/
COPY ./config/* /opt/dodas/htc_config/
RUN ln -s /opt/dodas/condor.sh /usr/local/sbin/dodas_condor

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/sbin/dodas_condor"]
