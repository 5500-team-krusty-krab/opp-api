# Project File

### AWS public URL: http://kkpayment.s3.us-west-2.amazonaws.com/build/index.html

## Deployment

### Docker

#### Install Docker Desktop
Visit Docker’s official website and download and install Docker Mac Intel Chip version
Attention: Docker can only run on macOS system above 12.0, no matter Apple silicon or Intel chip 

#### Build Docker image
Run in the project root directory backend
```bash
docker build -t myimage .
```

#### Run Docker container
```bash
docker run -d --name mycontainer -p 8000:8000 myimage
```

#### Test Docker container status
```bash
 run http://localhost:8000 at local engine
```



## Deploy To AWS

### Building and Pushing Docker Image to ECR

#### 1. Install AWS CLI and configure it:
On your local machine, install AWS CLI.
Run aws configure and enter the credentials from the IAM user you created.

#### 2. Build Docker image locally: (AWS ECR has push command at the Repositories Dashboard)
From the root of your repository, run:
```bash
docker build --platform linux/amd64 -t <name-of-image> .
```

#### 3. Tag Docker image with the ECR URI:
From the root of your repository, run:
```bash
docker tag <image> <ECR-URI>/<tag>
```

#### 4. Login to ECR:
From the root of your repository, run:
```bash
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <REPO_HOST>
```

#### 5. Push the tagged image to ECR:
From the root of your repository, run:
```bash
docker push <ECR-URI>:<tag>
```


### Running the Docker Container on EC2
#### 1. SSH into your EC2 instance.
```bash
chmod 400 <path-to-key-pair>
```
```bash
ssh -i <path-to-keypair> ec2-user@<EC2-instance-public-DNS>
```

#### 2. Configure AWS CLI with the user credentials.
```bash
aws configure
```

#### 3. Login to ECR:
```bash
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin <REPO_HOST>
```

#### 4. docker pull <ECR-URI>:<tag>
```bash
docker pull <ECR-URI>:<tag>
```

#### 5. Run your Docker container:
```bash
docker run --detach --publish <your-app-port>:<container-port> <ECR-URI>:<tag>
```


### Testing Your Endpoint
```bash
http://<ec2-public-url>:<app-port>/<path>
```