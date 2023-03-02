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
                Installing Homebrew on my Mac command.
                        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
                Install the aws-iam-authenticator with the following command.
                        brew install aws-iam-authenticator
                Test that the aws-iam-authenticator binary works.
                        aws-iam-authenticator help
         

        
IN AWS Account
Creating IAM user for ecrUser from IAM console
        Attach existing policy  1> AmazonEC2ContainerRegistryFullAccess
                                2> AmazonElasticContainerRegistryPublicFullAccess	

Installing AWS CLI(in Local)
                https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html
                Download for MAC from this link(https://aws.amazon.com/cli/)
                open terminal to configure AWS command: 
                        aws configure
                Will ask
                        AWS Access Key ID [None]: provided from user programatic acess key
                        AWS Secret Access Key [None]:provided from user programatic acess key
                        Default region name [None]: us-east-1
                        Default output format [None]: json

Creating Elastic Container Registry(ECR))(In AWS account)
        Create Repository named usershift

        Now push images to ECR Push commands for usershift using instructions from the prompt(same process for both images)
                1. Retrieve an authentication token and authenticate your Docker client to your registry.Use the AWS CLI: 
                        aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 599270912675.dkr.ecr.us-east-1.amazonaws.com

                2.Build Docker image using the following command:
                        docker build -t shift .
                        docker build -t user .

                3.After the build completes, tag image so I can push the image to this repository:
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
        Select Usecase as 'EKS'==> EKS Cluster (policy AmazonEKSClusterPolicy)
        Role Name -  EKSClusterRole

Create EKS Cluster using Created VPC and IAM Role
        Cluster Name - UserShift-EKS-Cluster
        Cluster endpoint access : Public & Private



