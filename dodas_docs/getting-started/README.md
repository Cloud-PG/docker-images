# Getting Started

There are three use case currently supported, which in turn means that we provide three TOSCA \(plus Ansible\) implementations ready to use and possibly to be extended depending on the user requirements: 

* HTCondor Batch System
  * A complete and standalone HTCondor batch system \(BatchSystem as a Service\)
    * as such it includes all the HTCondor services: Schedd, Central Manager and executors \(startds\).
  * A HTCondor extension of a already existing Pool 
    * this is about pre configured HTCondor executors \(startd\) auto-join a existing HTCondor pool.   
* BigData Platform 
  * A Machine Learning as a Service. Currently this is about a Spark Framework which can be coupled with a HDFS \(either pre-existing or generated on demand\) for data ingestion. 



