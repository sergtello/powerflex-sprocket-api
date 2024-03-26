# Powerflex Demo Sprocket API

# How to run locally
First clone this repo by using the following command:

````

git clone https://github.com/sergtello/powerflex-sprocket-api.git

````

Make sure you have docker engine and docker compose installed: 
https://docs.docker.com/engine/install/

Go to the base directory.
````
cd powerflex-sprocket-api
````

Use the .env.local.template as reference for setting the environment variables.
Just change the values surrounded between '< >'.

In the same directory create a file named '.env.local' containing these variables.

````
MONGODB_ROOT_USER=<YOUR_MONGODB_USER>
MONGODB_ROOT_PASSWORD=<YOUR_MONGODB_PASSWORD>

DATABASE_NAME=powerflex-demo   # Default database name

PATH_PREFIX=<PATH_PREFIX_FOR_ALL_ENDPOINTS>  # Path prefix appended at the beginning of every route

API_KEY=<YOUR_API_KEY>  # API Key for basic authentication of the POST and PUT endpoints

DOCS_AUTH_USERNAME=powerflex  # Username for basic auth of the interactive documentation
DOCS_AUTH_PASSWORD=powerflex  # Password for basic auth of the interactive documentation

````

In the 'powerflex-sprocket-api' directory run the following command:
````
docker compose -f 'docker-compose-local.yml' up -d
````

To generate the initial seed data from the json files wait until the containers are up and run the following: 
````
docker exec powerflex-sprocket_app-dev python seed.py sample/seed_sprocket_types.json sample/seed_factory_data.json
````

Then go to this address:
http://127.0.0.1:8000/docs

If you had set the variable PATH_PREFIX, then the address should be: http://127.0.0.1:8000/{PATH_PREFIX}/docs


When prompted for credentials use the ones defined in the DOCS_AUTH_USERNAME and DOCS_AUTH_PASSWORD variables.

The web page that hosts the interactive Swagger documentation should load:

![API Interactive Documentation](https://i.imgur.com/3WiPgKQ.png)

The endpoints that require auth are marked with a lock, use the 'Authorize' button to use the API Key in every request. 