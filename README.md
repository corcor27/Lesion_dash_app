# Lesion_dash_app
# Discription
aws deployable dash python app for collecting lesion metadata, with case image and metadata display that can be changes and the output the updated metadata file is uploaded to Gdrive. 
The app is written in dash python and can be found at app/API_update_information.py also supporting inputs for the script including metadata excel and images can be found in /app. This is then compiled locally into a docker image and then pushed to AWS Elastic Container Registry, from there the docker image is deployied on AWS App Runner, making it accessable from http link with a login and password. Lastly, the updated dataframe is then written into memory and then uploaded to 
Gdrive python API using an service access key. The following functions in google_upload.py can be used to upload/read reposity or download the file. 
