# Recipe for impatient users

An impatient user seeking to try a DODAS deployment need to address the following 4 main steps: 

## 1\) Registration

Register to the IAM-DODAS service by accessing the service [here](https://dodas-iam.cloud.cnaf.infn.it/). You can use your IdP because IAM-DODAS supports eduGAIN identity federation.   
The first registration will require the approval from the DODAS admins. 

## 2\) Token Management

Once your registration has been approved you can get your first DODAS token by using the recipe described and detailed [here](https://indigo-iam.github.io/docs/v/current/user-guide/getting-a-token.html). As you can see there are two options currently supported although we consider the password flow deprecated. We strongly suggest the Device code Flow for all the reasons detailed. 

* For a **very impatient user:** just download and execute this [script](https://gist.github.com/andreaceccanti/5b69323b89ce08321e7b5236de503600). 
  * Please note 
    * The script requires that you have a client \(authorized for Device-Flow\). You can either have your client \(self-service generated\) or use a client provided by DODAS team. In both cases before running the script you need to know the following information:  


      ```text
      IAM_DEVICE_CODE_CLIENT_ID
      IAM_DEVICE_CODE_CLIENT_SECRET
      IAM_DEVICE_CODE_ENDPOINT
      IAM_TOKEN_ENDPOINT 
      ```

    * There will be a few steps to address.. the script will guide you.
    * You can set IAM\_DEVICE\_CODE\_ENDPOINT="[https://dodas-iam.cloud.cnaf.infn.it/devicecode](https://dodas-iam.cloud.cnaf.infn.it/devicecode)" and IAM\_TOKEN\_ENDPOINT="[https://dodas-iam.cloud.cnaf.infn.it/token](https://dodas-iam.cloud.cnaf.infn.it/token)" in the script. Client ID and secret are given when you create the Device code flow client as explained [above](https://indigo-iam.github.io/docs/v/current/user-guide/getting-a-token.html).
    * For the Device code flow client \(self-generated\), you need to set Access -&gt; grant\_types -&gt; token from the Client management[ dashboard](https://dodas-iam.cloud.cnaf.infn.it/manage/dev/dynreg).

## 3\) Prepare your TOSCA template

At that point you can checkout the already available TOSCA Templates [here](https://github.com/indigo-dc/tosca-templates/blob/master/dodas/) and pick the one you prefer. Otherwise just use the following simple TOSCA test to get a taste of the whole system:

```text
imports:
- indigo_custom_types: https://raw.githubusercontent.com/indigo-dc/tosca-types/master/custom_types.yaml
description: >
 Launch a VM 
 Get IP and SSH credentials to access
 topology_template:
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
     value: { get_attribute: [ simple_node, endpoint, credential, 0 ] }
```

{% hint style="info" %}
If you will choose a specific template \(not just the test once\) you need to  properly configured it. Configuration parameters should be documented on each TOSCA template. 
{% endhint %}

## 4\) Submit the TOSCA template

Once configured, you can submit the TOSCA either to the PaaS Orchestrator or directly to IM.

### **Direct submission to IM** 

The direct submission to IM can be done either via im-client or using the RESTful API. The [extended guide ](http://imdocs.readthedocs.io/en/devel/client.html#) provides all the recipes and information for installation and configuration of the CLI as well as the documentation of the REST APIs. However using the REST is highly suggested for the initial testing cause it guarantees a enormous flexibility, useful for a fast turnaround during tests. In any case the public endpoint is :

```text
https://im.cloud.cnaf.infn.it:8800/infrastructures
```

And an example of REST based submission is

```text
curl -k -H 'Content-type: text/yaml' -H "Authorization: id = ost; type = OpenStack; host = https://horizon.cloud.cnaf.infn.it:5000/v3; username = indigo-dc; password = $IAM_ACCESS_TOKEN; tenant = oidc; auth_version = 3.x_oidc_access_token; service_region = regionOne;\nid = im; type = InfrastructureManager; token = $IAM_ACCESS_TOKEN" -X POST http://im.cloud.cnaf.infn.it:8800/infrastructures --data-binary @"<YOUR_TOSCA>.yaml"
```

And the expected output should be something like:  
   
`HTTP/1.1 200 OK   
Content-Length: 86   
Content-Type: text/uri-list  
Infid: 9b044cce-6424-11e8-bad9-0242ac120003   
Date: Wed, 30 May 2018 16:15:11 GMT Server: Cheroot/6.3.1`  
**`http://im.cloud.cnaf.infn.it:8800/infrastructures/9b044cce-6424-11e8-bad9-0242ac120003`**

The above command is based on POST \(to create the infrastructure described in the TOSCA template\), but you can also use GET \(to list\) or DELETE commands to manage the infrastructure that you have created. Please refer to the documentation linked [here](http://imdocs.readthedocs.io/en/devel/REST.html). 

### Submission to the PaaS Orchestrator

The Submission to the PaaS Orchestrator as well can be done both through the client and through the REST APIS. Here in this guide only the client based solution is taken into account.   
There are two steps: 

* Installation the client called **orchent** following the [recipe here](https://indigo-dc.gitbooks.io/orchent/admin.html). Once installed...
* Configuration and usage of the orchent client as described [here](https://indigo-dc.gitbooks.io/orchent/user.html) . Be careful to the following notes:
  *  Despite the possibility to use the oidc-client we suggest to the ORCHENT\_TOKEN based solution as described in the guide.
  * Set the ORCHENT\_URL env. variable using the endpoint as here below:   


    ```text
    export ORCHENT_URL=https://orchestrator.cloud.cnaf.infn.it/orchestrator
    ```

  * The submission command should look like the following   


    ```text
    orchent depcreate <Your-TOSCA>.yaml '{}'
    ```

{% hint style="info" %}
the parenthesis  '{}' can be used to pass the input parameter to the TOSCA. Although values can be filled in the template itself, the parenthesis must be left there otherwise you'll get an error. 
{% endhint %}

* * The output of the deployment creation \(`depcreate`\) command will be something like the following   `Deployment [b8bdccf3-9be5-499f-aac2-664dc0726795]:   status: CREATE_IN_PROGRESS   creation time: 2018-06-16T15:58+0000   update time: 2018-06-16T15:58+0000   callback:    status reason:    task: NONE   CloudProviderName:    outputs:   {}    links:     self [https://orchestrator.cloud.cnaf.infn.it/orchestrator/deployments/b8bdccf3-9be5-499f-aac2-664dc0726795]     resources [https://orchestrator.cloud.cnaf.infn.it/orchestrator/deployments/b8bdccf3-9be5-499f-aac2-664dc0726795/resources]     template [https://orchestrator.cloud.cnaf.infn.it/orchestrator/deployments/b8bdccf3-9be5-499f-aac2-664dc0726795/template]`

The above steps 1 to 3 are valid irrespective of which TOSCA template will be used. Templates available are   
HTCondor a batch system and Spark. Moreover there are Experiment specific customisation, in particular [CMS](https://dodas.gitbook.io/dynamic-on-demand-analysis-service/~/edit/drafts/-LFIXHRxcNpQzkRZsUnA/getting-started/recipe-for-impatient-users) and [AMS](https://dodas.gitbook.io/dynamic-on-demand-analysis-service/~/edit/drafts/-LFIXHRxcNpQzkRZsUnA/getting-started/ams-recipe) recipes.

{% hint style="info" %}
User can test all the recipes running on the freely accessible DODAS Enabling Facility
{% endhint %}

