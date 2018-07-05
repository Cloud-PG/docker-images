FROM cloudpg/centos-7-grid:singularity
LABEL maintainer="diego.ciangottini@pg.infn.it"
LABEL Version=1.0

RUN useradd -ms /bin/bash cmssw

RUN yum install -y bzip2 rsync tcsh zsh tcl tk e2fsprogs perl-ExtUtils-Embed compat-libstdc++-33 libXmu libXcursor libXrandr libXft mesa-libGLU mesa-libGL libXinerama libXft-devel libXpm perl-Test-Harness libX11-devel libXpm-devel libXext-devel mesa-libGLU-devel perl-Switch perl-Thread-Queue file

RUN mkdir /CMSSW && chown -R cmssw /CMSSW

USER cmssw

WORKDIR /CMSSW


ENV VO_CMS_SW_DIR=/CMSSW

RUN  wget -O $VO_CMS_SW_DIR/bootstrap.sh http://cmsrep.cern.ch/cmssw/repos/bootstrap.sh

ENV SCRAM_ARCH=slc7_amd64_gcc630

RUN sh -x $VO_CMS_SW_DIR/bootstrap.sh setup -path $VO_CMS_SW_DIR -arch $SCRAM_ARCH && \
 sh -x $VO_CMS_SW_DIR/common/cmspkg -a $SCRAM_ARCH update
RUN echo "Y" | sh -x $VO_CMS_SW_DIR/common/cmspkg -a $SCRAM_ARCH install cms+cmssw+CMSSW_10_0_3

RUN /bin/bash -c "source cmsset_default.sh; scramv1 project CMSSW CMSSW_10_0_3 " 


USER root

ADD cache /CMSSW/CMSSW_10_0_3/src/cache
ADD test_IO.py /CMSSW/CMSSW_10_0_3/src/test_IO.py
ADD entrypoint.sh /CMSSW/CMSSW_10_0_3/src/entrypoint.sh
RUN chown -R cmssw /CMSSW/CMSSW_10_0_3/src && chmod +x /CMSSW/CMSSW_10_0_3/src/entrypoint.sh

ADD SITECONF /CMSSW/SITECONF
RUN chown -R cmssw /CMSSW/SITECONF
USER cmssw
WORKDIR /CMSSW/CMSSW_10_0_3/src

RUN /CMSSW/common/scram b -j4 

ENTRYPOINT ["/bin/sh", "/CMSSW/CMSSW_10_0_3/src/entrypoint.sh"]
