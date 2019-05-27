FROM cloudpg/centos-7-grid:singularity
LABEL maintainer="diego.ciangottini@pg.infn.it"
LABEL Version=1.0

RUN useradd -ms /bin/bash cmssw

RUN yum install -y git bzip2 rsync tcsh zsh tcl tk e2fsprogs perl-ExtUtils-Embed compat-libstdc++-33 libXmu libXcursor libXrandr libXft mesa-libGLU mesa-libGL libXinerama libXft-devel libXpm perl-Test-Harness libX11-devel libXpm-devel libXext-devel mesa-libGLU-devel perl-Switch perl-Thread-Queue file libaio

RUN mkdir /CMSSW && chown -R cmssw /CMSSW

USER cmssw

WORKDIR /CMSSW


ENV VO_CMS_SW_DIR=/CMSSW

RUN  wget -O $VO_CMS_SW_DIR/bootstrap.sh http://cmsrep.cern.ch/cmssw/repos/bootstrap.sh

ENV SCRAM_ARCH=slc7_amd64_gcc630

RUN sh -x $VO_CMS_SW_DIR/bootstrap.sh setup -path $VO_CMS_SW_DIR -arch $SCRAM_ARCH && \
 sh -x $VO_CMS_SW_DIR/common/cmspkg -a $SCRAM_ARCH update
RUN echo "Y" | sh -x $VO_CMS_SW_DIR/common/cmspkg -a $SCRAM_ARCH install cms+cmssw+CMSSW_9_4_0

RUN /bin/bash -c "source cmsset_default.sh; scramv1 project CMSSW CMSSW_9_4_0 " 


USER root

RUN chown -R cmssw /CMSSW/CMSSW_9_4_0/src
ADD SITECONF /CMSSW/SITECONF
RUN chown -R cmssw /CMSSW/SITECONF
ADD entrypoint.sh /CMSSW/CMSSW_9_4_0/src/entrypoint.sh
RUN chown -R cmssw /CMSSW/CMSSW_9_4_0/src && chmod +x /CMSSW/CMSSW_9_4_0/src/entrypoint.sh


USER cmssw
WORKDIR /CMSSW/CMSSW_9_4_0/src

RUN curl -s https://raw.githubusercontent.com/cms-sw/genproductions/master/python/ThirteenTeV/RSGraviton/RSGravitonToZZ_kMpl01_M_1000_TuneCUETP8M1_13TeV_pythia8_cfi.py --retry 2 --create-dirs -o Configuration/GenProduction/python/ThirteenTeV/RSGraviton/RSGravitonToZZ_kMpl01_M_1000_TuneCUETP8M1_13TeV_pythia8_cfi.py

RUN /CMSSW/common/scram b -j4 
RUN eval `/CMSSW/common/scramv1 runtime -sh`


RUN eval `/CMSSW/common/scramv1 runtime -sh` && cmsDriver.py Configuration/GenProduction/python/ThirteenTeV/RSGraviton/RSGravitonToZZ_kMpl01_M_1000_TuneCUETP8M1_13TeV_pythia8_cfi.py --fileout file:RSGravitonToZZ_kMpl01_M_1000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM.root -s GEN,SIM --mc --datatier GEN-SIM --beamspot Realistic25ns13TeVEarly2017Collision --conditions auto:phase1_2017_realistic --eventcontent RAWSIM --era Run2_2017 --python_filename RSGravitonToZZ_kMpl01_M_1000_TuneCUETP8M1_13TeV_pythia8_GEN-SIM_cfg.py --no_exec -n 50


ENTRYPOINT ["/bin/sh", "/CMSSW/CMSSW_9_4_0/src/entrypoint.sh"]
