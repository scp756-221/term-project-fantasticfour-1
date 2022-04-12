# SFU CMPT 756 group Fantastic Four main project directory

This is the project repo for CMPT 756 (Spring 2022) group Fantastic Four. This a music application that contains three microservices S1, S2 and S3. S1 manages creation, updation and deletion of users. S2 manages creation, updation and deletion of songs while S3 is manages creation, deletion and updation of playlists.

Below are the steps to deploy the application on an EKS cluster.

### Instantiate the template files

#### Fill in the required values in the template variable file

Copy the file `cluster/tpl-vars-blank.txt` to `cluster/tpl-vars.txt`
and fill in all the required values in `tpl-vars.txt`.  These include
things like your AWS keys, your GitHub signon, and other identifying
information.  See the comments in that file for details. Note that you
will need to have installed Gatling
(https://gatling.io/open-source/start-testing/) first, because you
will be entering its path in `tpl-vars.txt`.

#### Instantiate the templates

Once you have filled in all the details, run

~~~
$ make -f k8s-tpl.mak templates
~~~

This will check that all the programs you will need have been
installed and are in the search path.  If any program is missing,
install it before proceeding.

The script will then generate makefiles personalized to the data that
you entered in `clusters/tpl-vars.txt`.

**Note:** This is the *only* time you will call `k8s-tpl.mak`
directly. This creates all the non-templated files, such as
`k8s.mak`.  You will use the non-templated makefiles in all the
remaining steps.

### Ensure AWS DynamoDB is accessible/running

Regardless of where your cluster will run, it uses AWS DynamoDB
for its backend database. Check that you have the necessary tables
installed by running

~~~
$ aws dynamodb list-tables
~~~

The resulting output should include tables `User`, `Music` and `Playlist`.

If the tables do not exist, use the below command to create tables
~~~
$ make -f k8s.mak dynamodb-init
~~~
If the above command doesn't work, you will have to manually create the tables from DynamoDB dashboard.

----

### Steps for Deployment

1. eks.mak - Instantiated make file for creating an AWS EKS cluster

- Run the command below to start an AWS Kubernetes cluster
  ~~~
  $ make -f eks.mak start
  ~~~
- To understand your current environment
  ~~~
  $ kubectl config get-contexts
  ~~~
- To get the details of the cluster created and the services running in them
  ~~~
  $ make -f eks.mak ls  
  ~~~

2. k8s.mak - Instantiated make file for operating k8s

- Build the docker images of the services (S1, S2, S3 and DB) and push them to Github container registry
  ~~~
  $ make -f k8s.mak cri
  ~~~
  As part of this step, it is required to manually go to your packages in Github and change the visibility access of these packages from private to public

- After creation of cluster, to:
  - Create a namespace c756ns inside your cluster and set your cluster to use this
  - Install istio and label the c756ns namespace
  - Install the prometheus stack and the kiali operator for your cluster 
  - Using the Github packages to deploy the services onto the AWS Kubernetes cluster 
  - Initialize DynamoDB and load it with initial data

  Run the Command
  ~~~
  $ make -f k8s.mak provision
  ~~~
  
  Again after this, a new image loader will be built and pushed to your packages. Like before, change the visibility access from private to public.

3. For fetching the external ip address or DNS name that is required to access your cluster for eg: testing the services using Postman
~~~
$ kubectl -n istio-system get service istio-ingressgateway | cut -c -140
~~~

### Load Test and Monitoring

1. For simulating the load and monitoring the performance of the applications, we can use Gatling, Grafana and Kiali.
~~~
$ make -f k8s.mak grafana-url
$ make -f k8s.mak kiali-url
~~~

2. For adding the load to the application, gatling scripts can be run using the below command
~~~
$ ./gatling-<load count>-<simulation name>.sh
~~~

3. To scale the application (optional)
~~~
$ kubectl scale deployment/<service-name> --replicas=<number-of-replicas>
~~~

4. For stopping the load, we can use
~~~
$ tools/kill-gatling.sh
~~~

### Stopping the application

To delete your cluster after use
~~~
$ make -f eks.mak stop
~~~
