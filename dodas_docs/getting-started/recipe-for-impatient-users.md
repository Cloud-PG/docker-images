# Recipe for impatient users

A impatient user seeking to try a DODAS deployment need to address the following 4 main steps: 

1. Register to the IAM-DODAS service by accessing the service [here](https://dodas-iam.cloud.cnaf.infn.it/). You can use your IdP because IAM-DODAS supports eduGAIN identity federation. 
   * The first registration will require the approval from the DODAS admins. 
2. Once your registration has been approved you can get your first DODAS token by using the recipe described and detailed [here](https://indigo-iam.github.io/docs/v/current/user-guide/getting-a-token.html).  
   * For **very impatient user:** just download and execute this [script](https://gist.github.com/andreaceccanti/5b69323b89ce08321e7b5236de503600). 
     * Please note 
       * The script requires that you have a client \(authorized for Device-Flow\). You can either have your client \(self-service generated\) or use a provide client. In both cases before running the script you need to know the following information: 
         * IAM\_DEVICE\_CODE\_CLIENT\_ID

           IAM\_DEVICE\_CODE\_CLIENT\_SECRET  
           IAM\_DEVICE\_CODE\_ENDPOINT  
           IAM\_TOKEN\_ENDPOINT 
       * There will be few steps to address.. the script will guide you. 
3. At that point you can checkout the already available TOSCA Templates here. Or just use the following simple test:
4. Once properly configured you can submit the TOSCA either to the PaaS Orchestrator or directly to IM.

* Submit Te TOSCA template to PaaS
* Submit a TOSCA template to IM

[`https://im.cloud.cnaf.infn.it:8800/`](http://im.cloud.cnaf.infn.it:8800/)

You could now exploit DODAS to instantiate and run a HTCondor batch system. In such a case the step 1 to 3 remain the same, so you need only to checkout the proper template and submit it

* TOSCA template for a batch system

Once again, repeating 1 to 3 and checking out this: TOSCA per Spark, you can ask DODAS to deploy a Spark Cluster.. Possbily joining a Existing HDFS with your data.

If you like to deploy your HDFS through DODAS here is the recipe:  


All the above described recipes can run on the DODAS Enabling Facility \(see below\)  


