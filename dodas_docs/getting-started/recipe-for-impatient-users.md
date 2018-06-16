# Recipe for impatient users

A impatient user seeking to try a DODAS deployment need to address the following 4 main steps: 

1. Register to the IAM-DODAS service by accessing the service [here](https://dodas-iam.cloud.cnaf.infn.it/). You can use your IdP because IAM-DODAS supports eduGAIN identity federation. 
   * The first registration will require the approval from the DODAS admins. 
2. Once your registration has been approved you can get your first DODAS token by using the recipe described and detailed [here](https://indigo-iam.github.io/docs/v/current/user-guide/getting-a-token.html). As you can see there are two options currently supported although we consider the password flow deprecated. We strongly suggest the Device code Flow for all the reasons detailed. 
   * For **very impatient user:** just download and execute this [script](https://gist.github.com/andreaceccanti/5b69323b89ce08321e7b5236de503600). 
     * Please note 
       * The script requires that you have a client \(authorized for Device-Flow\). You can either have your client \(self-service generated\) or use a provide client. In both cases before running the script you need to know the following information: 
         * IAM\_DEVICE\_CODE\_CLIENT\_ID

           IAM\_DEVICE\_CODE\_CLIENT\_SECRET  
           IAM\_DEVICE\_CODE\_ENDPOINT  
           IAM\_TOKEN\_ENDPOINT 
       * There will be few steps to address.. the script will guide you. 
3. At that point you can checkout the already available TOSCA Templates here and pic-up the one you prefer. Otherwise just use the following simple TOSCA test to get a taste of the whole system:  
   `imports:`

    `- indigo_custom_types: https://raw.githubusercontent.com/indigo-dc/tosca-types/master/custom_types.yaml  
   description: >  
    Launch a VM   
    Get IP and SSH credentials to access`

   `topology_template:  
  
    node_templates:  
      simple_node:  
        type: tosca.nodes.indigo.Compute  
        capabilities:  
          endpoint:  
            properties:  
              network_name: PUBLIC  
              ports:  
                user_port:  
                  protocol: tcp  
                  source: 9000  
                other_port:  
                  protocol: tcp  
                  source: 9001  
          scalable:  
            properties:  
              count: 1  
          host:  
            properties:  
              instance_type: m1.small  
          os:  
            properties:  
              image: Ubuntu_16.04  
   outputs:  
      node_ip:  
        value: { get_attribute: [ simple_node, public_address, 0 ] }  
      node_creds:  
        value: { get_attribute: [ simple_node, endpoint, credential, 0 ] }`

4. If you will choose a specific template \(not just the test once\) you need to  properly configured it. Configuration parameters should be documented on each TOSCA template. Once configured, you can submit the TOSCA either to the PaaS Orchestrator or directly to IM.
   * Direct submission to IM can be done either via im-client or using the RESTful API. Find here the extended guide   
   * Submit a TOSCA template to the PaaS Orchestrator. There are two steps. 
     * Install the client called **orchent** following the [recipe here](https://indigo-dc.gitbooks.io/orchent/admin.html). Once installed...
     * use the orchent client as described [here](https://indigo-dc.gitbooks.io/orchent/user.html) . Be careful, despite the possibility to use the oidc-client we suggest to the ORCHENT\_TOKEN based solution as described in the guide.
     * set the ORCHENT\_URL env. variable using the endpoint as here below: 

       `export ORCHENT_URL=https://orchestrator.cloud.cnaf.infn.it/orchestrator`

You could now exploit DODAS to instantiate and run a HTCondor batch system. In such a case the step 1 to 3 remain the same, so you need only to checkout the proper template and submit it

* TOSCA template for a batch system

Once again, repeating 1 to 3 and checking out this: TOSCA per Spark, you can ask DODAS to deploy a Spark Cluster.. Possbily joining a Existing HDFS with your data.

If you like to deploy your HDFS through DODAS here is the recipe:  


All the above described recipes can run on the DODAS Enabling Facility \(see below\)  


