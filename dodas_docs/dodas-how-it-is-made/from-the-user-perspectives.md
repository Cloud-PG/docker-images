# From the user perspectives

DODAS from the user perspectives is a service aiming at enabling an easy solution for the creation of a complex setup for a computational environment on any cloud based environment. In other words the DODAS aim is to make te process of generating intricate setup as easy as it is today creating a virtual machine on any IaaS: one click solution.   
The summary of the major added values of DODAS for a scientist is: 

* To provide a complete abstraction of the underlying clouds
* To automate the virtual hardware provisioning and configuration
* To provide a cluster platform with a high level of self-healing 
* To guarantee setup and service customisation to cope with specific requirements  

More concretely "a complex setup" in this context means a **container orchestrator** \(e.g. Mesos\) on top of which there could be any framework which in turn manage the user service. The user service can be anything in principle, however DODAS provides two principal baseline ready to use and to be possibly extended: a HTCondor batch system and a Spark cluster.    
Dealing with DODAS for a user means to configure and submit a TOSCA template. Several templates have been already developed, one per supported use case \(see [this section](https://dodas.gitbook.io/dynamic-on-demand-analysis-service/~/edit/drafts/-LEDKwAyU8rRIV1lDMsb/getting-started) for further details\) but, of course, it is worth to remark that the key value is that you can either extend any of them or create your own.    
For the sake of completeness the very first step before developing and / or using existing templates is to register, and this must be done through the [IAM-DODAS ](https://dodas-iam.cloud.cnaf.infn.it/login)service.   
Except the registration step there is nothing else which represent a pre-requisite DODAS specific. There are, of course, pre-requisites both if you are about to use [CMS](https://dodas.gitbook.io/dynamic-on-demand-analysis-service/~/edit/drafts/-LF6xFIVOnDD408_u9KV/dodas-how-it-is-made/from-the-user-perspectives) and [AMS](https://dodas.gitbook.io/dynamic-on-demand-analysis-service/~/edit/drafts/-LF6xFIVOnDD408_u9KV/dodas-how-it-is-made/from-the-user-perspectives) implementation of DODAS as well as if you are supposed to External IaaS \(read as some cloud different from the provided [Enabling Facility](https://dodas.gitbook.io/dynamic-on-demand-analysis-service/~/edit/drafts/-LF6xFIVOnDD408_u9KV/dodas-how-it-is-made/from-the-user-perspectives)\), as [explained here. ](https://dodas.gitbook.io/dynamic-on-demand-analysis-service/~/edit/drafts/-LEDKwAyU8rRIV1lDMsb/using-dodas-with-external-providers)





