# Postman Testing

Contains the postman collections for testing the different services in the application

Kubernetes user service test.postman_collection : For testing different functionality in the users service (S1) of the application.
Kubernetes music service test.postman_collection : For testing different functionality in the music service (S2) of the application.
Kubernetes playlist service test.postman_collection : For testing different functionality in the playlist service (S3) of the application.

Note:
The http request used in Postman for testing services on Kubernetes cluster follows the following format:
http://{external_ip}:{port number}/api/v1/{service name}/{additional parameters}

where external_ip : is the entry point to your cluster or the DNS name
      port number : if using the gateway service as in the application, the port number is 80
      service name : Either music or user or playlist
      additional parameters : can be user id or playlist id or even call to certain functions like login and logoff

