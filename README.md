# Lesion_dash_app
# Discription
aws deployable dash python app for collecting lesion metadata, with case image and metadata display that can be changes and the output the updated metadata file is uploaded to Gdrive.  
The app is written in dash python and can be found at app/API_update_information.py also supporting inputs for the script including metadata excel and images can be found in /app.   
This is then compiled locally into a docker image and then pushed to AWS Elastic Container Registry, from there the docker image is deployied on AWS App Runner, making it accessable from http link with a login and password.   
Lastly, the updated dataframe is then written into memory and then uploaded to Gdrive python API using an service access key. The following functions in google_upload.py can be used to upload/read reposity or download the file. 
# Example image of app website
![Screenshot from 2023-10-27 13-28-21](https://github.com/corcor27/Lesion_dash_app/assets/29410420/217359c1-332d-4f9f-8306-824081f47c04)

# build docker image
Install Docker locally: sudo snap install docker  
If demon socket error enter: sudo chmod 666 /var/run/docker.sock  
to build docker image called "lesion_dash_app" enter: docker build -t lesion_dash_app .  
You can then test the docker image by running: docker run -p 8050:8050 lesion_dash_app  
make sure the port "8050" corresponds to your dash python port at the bottom of the script   

To see you docker images run: docker images

# AWS UPLOADING
Firstly, you will need to create an AWS account and login.  

Then you will need to create a ECR repositry in AWS so you can push your docker image to it. 

![1 CR-Pw30H6b8-_uhiZYT1Yg](https://github.com/corcor27/Lesion_dash_app/assets/29410420/1ad86a58-a4e1-4840-b509-a4ffa06dcd5d)

Next you will have to create some web access key such that you can push to this repositry.  

![1 lHYV1Pcci24FN2bplrVtMg](https://github.com/corcor27/Lesion_dash_app/assets/29410420/85357b1a-0286-4a3f-8a79-aa106921f560)

After completed download the key file.  

![1 n6IGOgyxwUpLnvXDnCiIPQ](https://github.com/corcor27/Lesion_dash_app/assets/29410420/c71fa5c4-4373-42ed-a43f-76e4bae72a64)
## Local Setup

Next, to be able to push your you need to login locally from your console.  
So install AWS through: sudo apt install asw-cli

Then you can login using you key you just downloaded: 

aws configure set aws_access_key_id <YOUR_ACCESS_KEY>  
aws configure set aws_secret_access_key <YOUR_SECRET_KEY>

Now you need to do some configuration:  

aws configure set default.region <YOUR_REGION>   
aws configure set default.output json  
$(aws ecr get-login --no-include-email --region <YOUR REGION>)  

## Pushing docker image
Here is your repositry

![1 pxJPZpuOf5BnunTgQt8Szw](https://github.com/corcor27/Lesion_dash_app/assets/29410420/d08b8499-ae2d-4596-9163-f27817a9ec67)

To push docker image run:  
docker tag conjoint_dashboard <ACCOUNT NUM>.dkr.ecr.<REGION>.amazonaws.com/dashboard

docker push <ACCOUNT NUM>.dkr.ecr.<REGION>.amazonaws.com/dashboard


![1 2J7MEJjTAJbvrlkuhhw3gw](https://github.com/corcor27/Lesion_dash_app/assets/29410420/65431c7c-b3be-4a04-8eea-4cc76ca6d89c)


