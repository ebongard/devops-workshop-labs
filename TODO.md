## Setup the OpenShift Cluster ##

* Download CDK https://developers.redhat.com/products/cdk/overview/
* Install following the instructions : https://developers.redhat.com/products/cdk/hello-world/
    * set memory `minishift config set memory 8196`
    * set cpu `minishift config set cpus 2`
    * set disk size `minishift config set disk-size 40g`
* start CDK using virtualbox driver ` minishift start --vm-driver=virtualbox`

    
## Setup the sample app ##
* `oc login -u developer` 
* `oc new-project coolstore-dev`
* `oc create -f openshift/coolstore-template.yaml`
* instantiate template coolstore
    * set the github url [setup project](images/setup-project.png) (TODO: Command line ??)
* check all the builds are ok
* check you can open the application : http://web-ui-coolstore-dev.192.168.64.6.nip.io/#/


## Setup XLDeploy in the OpenShift cluster ##
We will use an existing xldeploy instance (called XLDorg) to setup a new XLDeploy instance running in the Openshift cluster.
* `oc new-project xebialabs`
* Install the XLDeploy Python cli [xld-py-cli](https://pypi.python.org/pypi/xld-py-cli) 
* in XLDorg
    * import XLDeploy application dar file `xebialabs/xldeploy-7.6.0-2.dar`
    * apply the Deployfile `xebialabs/OpenShift.groovy` to create the infrastructure
        * set your cluster url
        * set your openshiftToken `oc whoami -t`
        * validate by running the `check connection` control task 
    * add the `xebialabs` project, type `openshift.Project`  on `minishift.local` CI
    * add the project into an `xebialabs-redhat`environment.
    * deploy `Applications/Containers/RH/xldeploy/7.6.0-3` into `Environments/others/RedHat/xebialabs-redhat`
        * `xld --url http://localhost:4516 --username admin --password admin deploy --package-id Applications/Containers/RH/xldeploy/7.6.0-3 --environment-id Environments/others/RedHat/xebialabs-redhat`
* Connect to the new deployed XLDeploy http://xldeploy-xebialabs.<IP-YOUR-CDK-CLUSTER>.nip.io and fill the license file

## Setup XLRelease in the OpenShift cluster ##
* in XLDorg
    * import XLDeploy application dar file `xebialabs/xlrelease-7.6.0-1.dar`
    * import XLDeploy application dar file `/xebialabs/oc-client-3.7.1.dar`
    * deploy `Applications/Containers/RH/xlrelease/7.6.0-1` into `Environments/others/RedHat/xebialabs-redhat`
        * `xld --url http://localhost:4516 --username admin --password admin deploy --package-id Applications/Containers/RH/xlrelease/7.6.0-1 --environment-id Environments/others/RedHat/xebialabs-redhat`
    * deploy `Applications/Containers/RH/oc-client/3.7.1` into `Environments/others/RedHat/xebialabs-redhat`
        * `xld --url http://localhost:4516 --username admin --password admin deploy --package-id Applications/Containers/RH/oc-client/3.7.1 --environment-id Environments/others/RedHat/xebialabs-redhat`
* Connect to the new deployed XLRelease http://xlrelease-xebialabs.<IP-YOUR-CDK-CLUSTER>.nip.io and fill the license file
    

## Setup the resources for the demo

### Openshift ###

* create the coolstore-qa project `oc new-project coolstore-qa`
* create the role-binding `oc apply -f xebialabs/role-binding.yaml` (not supported by xld-k8s-plugin-7.6.0.xldp), it allows the gateway to look up services in the current project.
* create the coolstore-prod project `oc new-project coolstore-prod`
* create the role-binding `oc apply -f xebialabs/role-binding.yaml` (not supported by xld-k8s-plugin-7.6.0.xldp), it allows the gateway to look up services in the current project.
* grant policy for coolstore-qa to fetch image from dev `oc policy add-role-to-user system:image-puller system:serviceaccount:coolstore-qa:default -n coolstore-dev`
* grant policy for coolstore-prod to fetch image from dev `oc policy add-role-to-user system:image-puller system:serviceaccount:coolstore-prod:default -n coolstore-dev`


### XLRelease ###
* Define a `Unix Host`shared configuration with the following parameter
    * name: occlient
    * connection type: SFTP
    * address: oc-service.xebialabs.svc
    * port: 2222
    * username: root
    * password: root
* Define a `XLDeploy Server `shared configuration with the following parameter
    * title: XLDeploy Server
    * Authentication : basic
    * url: http://xld-service.xebialabs.svc:4516
    * port: 2222
    * username: admin
    * password: admin   
* create a `coolstore` folder
* import the following templates
    * don't forget to set the `Run automated tasks as user` 's credentials)
    * edit the xldeploy task to set the `XLDeploy Server` 
    * xebialabs/ComponentTemplate.xlr
    * xebialabs/GlobalRelease.xlr
    * xebialabs/Master.xlr
 
    
### XLDeploy ###

* Create the `openshift.Server`
    * id : Infrastructure/openshift.server
    * server Url : https://kubernetes.default.svc:443
    * token: xxxxx xxxx (the `oc whoami -t` returns the token)
    * Verify Certificates: False
* Create the `openshift.Project` Infrastructure/openshift.server/coolstore-qa
* Create the `openshift.Project` Infrastructure/openshift.server/coolstore-prod
* Create an `udm.Dictionary` Environments/global.configuration with the following properties
    * REGISTRY 172.30.1.1:5000
* Create an `udm.Dictionary` qa.configuration with the following properties
    * CATALOG_DB_USERNAME scott
    * CATALOG_DB_PASSWORD tiger
    * MONGODB_ADMIN_PASSWORD tiger
    * catalog.initialDelaySeconds 60
    * catalog.timeoutSeconds 30
    * catalog.periodSeconds 30
    * env qa
    

* Create the QA `udm.Environment` with Infrastructure/openshift.server/coolstore-qa as member and Environments/global.configuration as dictionaries
* Create the PROD `udm.Environment` Environment with Infrastructure/openshift.server/coolstore-prod as member Environments/global.configuration as dictionaries



 
    








