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

# AWS UPLOADING


