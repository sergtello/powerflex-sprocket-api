# Powerflex Demo Sprocket API

# How to run locally
First clone this repo by using following command

````

git clone https://github.com/sergtello/powerflex-sprocket-api.git

````

Make sure you have the docker engine and docker compose installed: 
https://docs.docker.com/engine/install/

Go to the base directory
````
cd powerflex-sprocket-api
````

Use the .env.local.template as reference for setting the environment variables.

In the same directory create a filed named '.env.local' containing these variables.

````
MONGODB_ROOT_USER=<YOUR_MONGODB_USER>
MONGODB_ROOT_PASSWORD=<YOUR_MONGODB_PASSWORD>

DATABASE_URI=mongodb://<YOUR_MONGODB_USER>:<YOUR_MONGODB_PASSWORD>@mongodb-tst:27017/powerflex-demo?authSource=admin
DATABASE_NAME=powerflex-demo   # Default database name
DATABASE_ALIAS=powerflex-demo  # Default database alias

API_KEY=<YOUR_API_KEY>  # API Key for basic authentication of the POST and PUT endpoints
````

In the 'powerflex-sprocket-api' directory run the following command:
````
docker compose -f 'docker-compose-local.yml' up -d
````

Wait until the containers are up then go to this address:
http://127.0.0.1:8000/docs

A 