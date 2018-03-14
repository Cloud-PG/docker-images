#!/bin/bash
yum install -y ca-policy-egi-core ca-policy-lcg

/usr/sbin/fetch-crl -q

wget -O /etc/yum.repos.d/ca_CMS-TTS-CA.repo https://ci.cloud.cnaf.infn.it/job/cnaf-mw-devel-jobs/job/ca_CMS-TTS-CA/job/master/lastSuccessfulBuild/artifact/ca_CMS-TTS-CA.repo
yum -y install ca_CMS-TTS-CA