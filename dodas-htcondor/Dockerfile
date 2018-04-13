FROM cloudpg/centos-7-grid-tini-sshd

# kerberos ticket config - personalized home skeleton
COPY ./config/ssh_config /etc/skel/.ssh/config

WORKDIR /etc/yum.repos.d

RUN useradd -ms /bin/bash condor \
    && wget http://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-development-rhel7.repo \
    && wget http://research.cs.wisc.edu/htcondor/yum/repo.d/htcondor-stable-rhel7.repo \
    && wget http://research.cs.wisc.edu/htcondor/yum/RPM-GPG-KEY-HTCondor \
    && rpm --import RPM-GPG-KEY-HTCondor \
    && yum --setopt=tsflags=nodocs -y update \
    && yum --setopt=tsflags=nodocs -y install condor-all python-devel python-pip \
    && yum --setopt=tsflags=nodocs -y install binutils \
        boost-devel \
        cmake \
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
    && pip install j2cli paramiko psutil kazoo requests

# Root home
WORKDIR /root

# condor_collector
EXPOSE 9618
# condor_negotiator
EXPOSE 9614
# condor_ckpt_server
EXPOSE 5651-5654
# condor_ports
EXPOSE 1024-2048
# condor env default values
ENV CONDOR_DAEMON_LIST="COLLECTOR, MASTER, NEGOTIATOR, SCHEDD, STARTD"
ENV CONDOR_HOST="\$(FULL_HOSTNAME)"
ENV CCB_ADDRESS_STRING=""
ENV NETWORK_INTERFACE_STRING=""
ENV CONDOR_SCHEDD_SSH_PORT=31042
ENV SEC_DAEMON_AUTHENTICATION_METHODS=CLAIMTOBE
ENV SEC_CLIENT_AUTHENTICATION_METHODS=CLAIMTOBE
ENV SEC_NEGOTIATOR_AUTHENTICATION_METHODS=CLAIMTOBE
ENV SEC_ADVERTISE_STARTD_AUTHENTICATION_METHODS=CLAIMTOBE
ENV NUM_SLOTS=1 
ENV NUM_SLOTS_TYPE_1=1
ENV SLOT_TYPE_1="cpus=1, mem=4096"

RUN mkdir -p /opt/dodas/htc_config \
    && mkdir -p /opt/dodas/fs_remote_dir \
    && mkdir -p /etc/skel/.ssh
COPY condor.sh /opt/dodas/
COPY check_condor_processes.py /opt/dodas/
COPY check_cvmfs_folders.py /opt/dodas/
COPY check_ssh_server.py /opt/dodas/
COPY ./config/condor_config.template /opt/dodas/htc_config/

RUN ln -s /opt/dodas/condor.sh /usr/local/sbin/dodas_condor \
    && ln -s /opt/dodas/check_condor_processes.py /usr/local/sbin/dodas_check_condor_processes \
    && ln -s /opt/dodas/check_cvmfs_folders.py /usr/local/sbin/dodas_check_cvmfs_folders \
    && ln -s /opt/dodas/check_ssh_server.py /usr/local/sbin/dodas_check_ssh_server

# CentOS uname characteristics
RUN mv /bin/uname /bin/uname_old
COPY ./bin/uname /bin/

ENTRYPOINT ["/usr/bin/tini", "--", "/usr/local/sbin/dodas_condor"]
