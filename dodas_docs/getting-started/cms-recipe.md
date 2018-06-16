# CMS Recipe

The DODAS workflow implemented for CMS has been designed in order to generate a ephemeral Tier\* WLCG compliant. In the basic implementation has been built on the following assumptions 

1. There is **no Computing Element**. Worker nodes \(HTCondor startd processes\) startup as a docker container over Mesos cluster, and auto-join the HTCondor Global-Pool of CMS
2. Data I/O is meant to rely on AAA xrootd read rule 
   1. although there is not technical limitation preventing the usage of local storages..

This imply to accomplish with the following pre-requisites: 

* Requires Submission Infrastructure \(SI\) L2s for authorization for Global-Pool access. In order to being authorised you must belong CMS Collaboration and provide DN an CMS Site Name. SI will use these info to define the proper mapping in the match-maker. 
  * Get a DN from X.509 Certificate you can retrieve from the [Token Translation Service ](https://dodas-tts.cloud.cnaf.infn.it/). 
  * Define a name for your ephemeral CMS Site: e.g.  `T3_XX_XY_KK`
* If you like to be visible in the Dashboard \(this is ONLY true for the old-fashioned Dashboard\) you need to notify the dashboard support team informing that you need the following mapping among Site Name and SynCE  `Site Name == T3_XX_XY_KK  SyncCE == T3_XX_XY_KK`
  * NOTE : This is needed because DODAS does not deploy a cluster which relies on a Computing Element. 

Once done all of this, you should be able to get this TOSCA template and configure everything as described in the template itself.  
The CMS template deploy the following services and components:   
- squid proxy  
- proxy cache   
- worker node \(HTCondor startd\)  
- cvmfs  
- cvmfs-check app    
- CMS Trivial File Catalogue

{% hint style="info" %}
This assume you are now familiar with following steps:

1. how to GET a token from IAM-DODAS
2. how to submit a TOSCA template \(either with PaaS orchestrator or Infrastructure Manager\)
{% endhint %}

Once the cluster has been created you should be able to access the Marathon and Mesos GUIs for management, debugging etc.

 Once the cluster Mesos is up&running and all the application have been launched on Marathon, startd should be start joining the HTCondor global pool.. and thus if matching happens HTCondor start executing payloads. So most probably you would like to submit some jobs with proper configuration to allow the matching. 

## Submitting CRAB jobs for DODAS CMS Site 

In order to submit CRAB jobs with proper classad parameters which guarantee the matching, you need to add this extra line in the configuration file of CRAB: 

`config.Debug.extraJDL = [ '+DESIRED_Sites="T3_XX_XY_KK"','+JOB_CMSSite="T3_XX_XY_KK"','+AccountingGroup="highprio.<YOUR_LXPLUS_LOGIN>"' ]`

There is no any other change you need to do. 



Finally there is a basic Elastic Search monitoring system which can be used and extended to cope with user specific needs. This is detailed [here](https://dodas.gitbook.io/dynamic-on-demand-analysis-service/~/edit/drafts/-LF8TB8psnZUdINp-U4z/getting-started/cms-recipe) .



