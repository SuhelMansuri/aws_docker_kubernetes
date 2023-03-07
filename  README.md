Communication tool we will use to communicate between our Kubernetes cluster and our local machine


       Installation instructions available on - https://kubernetes.io/docs/tasks/tools/install-kubectl/


               (1) Download the latest release: (Apple Silicon) command:
                       curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl"


               (2) Validate the binary (Apple Silicon)
                          curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/darwin/arm64/kubectl.sha256"


               (3) Make the kubectl binary executable command
                       chmod +x ./kubectl


               (4) Move the kubectl binary to a file location on my system PATH.
                       sudo mv ./kubectl /usr/local/bin/kubectl
                       sudo chown root: /usr/local/bin/kubectl
               (5) Test to ensure the version you installed is up-to-date:
                       kubectl version --client
                               or
                       kubectl version --client --output=yaml
               (6) After installing the plugin, clean up the installation files:
                       rm kubectl kubectl.sha256
      
     
       Installing aws-iam-authenticator
               To install aws-iam-authenticator with Homebrew
               Installing Homebrew on my Mac
                       /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
               Install the aws-iam-authenticator with the following command.
                       brew install aws-iam-authenticator
               Test that the aws-iam-authenticator binary works.
                       aws-iam-authenticator help
       
      
      


Installing AWS CLI(in Local)
               https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
               Download for MAC from this link (https://aws.amazon.com/cli/)
               Open terminal to configure AWS command:
                       aws configure
               Will ask
                       AWS Access Key ID [None]: provided from user/root programmatic access key
                       AWS Secret Access Key [None]:provided from user/root programmatic access key
                       Default region name [None]: us-east-1
                       Default output format [None]: json


Installing or updating eksctl(in Local)
               Install or upgrade eksctl. If eksctl is already installed, the following command upgrades and relinks it. Or if eksctl isn't installed yet, the following command will install Weaveworks Homebrew Tap as needed and then install eksctl: command:
                       brew upgrade eksctl && { brew link --overwrite eksctl; } || { brew tap weaveworks/tap; brew install weaveworks/tap/eksctl; }
                       (Source - https://docs.aws.amazon.com/eks/latest/userguide/eksctl.html)


IN AWS Account
Creating IAM user for ecrUser from IAM console
       Attach existing policy  1> AmazonEC2ContainerRegistryFullAccess
                               2> AmazonElasticContainerRegistryPublicFullAccess


Creating Elastic Container Registry(ECR))(In AWS account)
       Create Repository named usershift


       Now push images to ECR.registry. Push commands for usershift using instructions from the prompt(same process for both images)
               1. Retrieve an authentication token and authenticate your Docker client to your registry.  Use the AWS CLI:
                       aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 599270912675.dkr.ecr.us-east-1.amazonaws.com


               2. Build a Docker image using the following command:
                       docker build -t shift .
                       docker build -t user .


               3.After the build completes, tag the image so I can push the image to this repository:
                       docker tag shift:latest 599270912675.dkr.ecr.us-east-1.amazonaws.com/shift:latest
                       docker tag user:latest 599270912675.dkr.ecr.us-east-1.amazonaws.com/user:latest
                      
               4.Run the following command to push this image to your newly created AWS repository:
                       docker push 599270912675.dkr.ecr.us-east-1.amazonaws.com/shift:latest
                       docker push 599270912675.dkr.ecr.us-east-1.amazonaws.com/user:latest


Creating VPC
       Create our VPC using AWS Cloudformation because AWS already has a template for creating a public and private subnet VPC. (Source : https://docs.aws.amazon.com/eks/latest/userguide/creating-a-vpc.html)
               Go to create CloudFormation
               create stack
               Enter Stack name - EKSClusterVPCCloudFormation
               in Amazon S3 URL (copy url from aws document(https://s3.us-west-2.amazonaws.com/amazon-eks/cloudformation/2020-10-29/amazon-eks-vpc-private-subnets.yaml))
               Next
               next
               submit
Create IAM Role
       Entity Type : AWS Service
       Select Use Case as 'EKS'==> EKS Cluster (policy AmazonEKSClusterPolicy)
       Role Name -  EKSClusterRole


Create EKS Cluster using Created VPC and IAM Role
       Cluster Name - UserShift-EKS-Cluster
       Cluster endpoint access : Public & Private
       Security Group
       To check in your local how many cluster are there
               aws eks list-clusters
       Use the following command to update the kubeconfig file on a remote machine in the cluster: (Sorce : https://docs.aws.amazon.com/eks/latest/userguide/create-kubeconfig.html)
               aws eks update-kubeconfig --name UserShift-EKS-Cluster --region us-east-1


               We can see cluster information using the command:
                       cat /Users/suhelmansuri/.kube/config
      
       Now list the cluster using the command:
               aws eks list-clusters
Create IAM role for EKS worker nodes
       Role Name : EKSWorkerNodeRole
       policies:
               - AmazonEC2ContainerRegistryReadOnly
               - AmazonEKS_CNI_Policy
               - AmazonEKSWorkerNodePolicy
Create Worker Node Group in Cluster(EKSWorkerNodeGroup)
       Go to cluster -> Compute -> Node Group
       Select the Role created before(EKSWorkerNodeRole)
       I have tried 3 different machine(Instance type) in Node Group where t2.micro is too small so doesn't work pods goes in pending and CrashLoopBackOff status wher  t3.medium shows running in AWS Nodes but upon checking in terminal it shows CrashLoopBackOff so finally used  m6g.large(AMI type - AL2_ARM_64) it worked
       used t2.micro
      
Install Helm in Local
       brew install helm
Get EKS Cluster service(status of cluster)
       eksctl get cluster --name UserShift-EKS-Cluster --region us-east-1
Create Deploy Manifest(Source : https://docs.aws.amazon.com/eks/latest/userguide/sample-deployment.html)
       using aws document sample created deployment.yaml and service.yaml
       Create Namespace command:
               kubectl create namespace user-shift
       Issue following command to create our deployment
               kubectl apply -f user-shift-deployment.yaml
       Undo deployment following command:
               kubectl delete -f user-shift-deployment.yaml
For the best user experience auto scale this service when the average CPU reaches 70%


Installing the Kubernetes Metrics Server(Source - https://docs.aws.amazon.com/eks/latest/userguide/metrics-server.html)
       Deploy the Metrics Server
               kubectl apply -f https://github.com/kubernetes-sigs/metrics-server/releases/latest/download/components.yaml


       Verify the metric servers using below command
               kubectl get apiservice v1beta1.metrics.k8s.io -o json


Horizontal Pod Autoscaler(Source - https://docs.aws.amazon.com/eks/latest/userguide/horizontal-pod-autoscaler.html)
       Create Autoscaler for User
               kubectl autoscale deployment user --cpu-percent=70 --min=1 --max=10
       Create Autoscaler for Shift
               kubectl autoscale deployment shift --cpu-percent=70 --min=1 --max=10
       Verify autoscaler
               kubectl get hpa     
       remove autoscaler
               kubectl delete hpa user
       Create a load for the web server by running a container
               kubectl --generator=run-pod/v1 run -i --tty load-generator --image=busybox /bin/sh            
Updated images with new tags
       docker tag user:latest 599270912675.dkr.ecr.us-east-1.amazonaws.com/user:v1.0
       docker push 599270912675.dkr.ecr.us-east-1.amazonaws.com/user:v1.0
deployment rolling(rollout) deployments and rollbacks.
        User-Container 
                check rollout history
                        kubectl rollout history deployment/user
                to change or update rolling or rollout image
                        kubectl set image deployment user user-container=599270912675.dkr.ecr.us-east-1.amazonaws.com/user:v1.0 --re
                        cord=true
                check revision numer(version)
                        kubectl rollout history  deployment/user --revision=1        
        Shift-Container 
                check rollout history
                        kubectl rollout history deployment/shift
                to change or update rolling or rollout image
                        kubectl set image deployment shift shift-container=599270912675.dkr.ecr.us-east-1.amazonaws.com/shift:v1.0 --re
                        cord=true
                check revision numer(version)
                        kubectl rollout history  deployment/shift --revision=1

deployment rollbacks
        rollout previous version/revision
                kubectl rollout undo deployment user
        rollout specific version/revision number
                kubectl rollout undo deployment user --to-revision=1









