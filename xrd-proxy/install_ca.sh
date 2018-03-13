#!/bin/bash
sudo yum install -y ca-policy-egi-core ca-policy-lcg

sudo /usr/sbin/fetch-crl -q

sudo wget -O /etc/yum.repos.d/ca_CMS-TTS-CA.repo https://ci.cloud.cnaf.infn.it/job/cnaf-mw-devel-jobs/job/ca_CMS-TTS-CA/job/master/lastSuccessfulBuild/artifact/ca_CMS-TTS-CA.repo
sudo yum -y install ca_CMS-TTS-CA