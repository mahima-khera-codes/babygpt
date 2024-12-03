## docker setup for development


also you can set environment variables in docker-compose.yml

sudo docker-compose build

sudo docker-compose up -d

to see logs

sudo docker-compose up

or 

sudo docker-compose logs


on the docker container is running

for the first time setup login into the container using

sudo docker exec -it notifyapi bash

and run

flask seed_recruit

to import initial seed data for the recruit system


## docker setup for staging

# for staging docker
sudo docker-compose -f docker-compose-staging.yml build

sudo docker-compose -f docker-compose-staging.yml up

sudo docker-compose -f docker-compose-staging.yml push


## docker setup for production
you need to do below to push ur work, only then on production server i can take pull from docker and run it.


sudo docker-compose -f docker-compose-prod.yml build

sudo docker-compose -f docker-compose-prod.yml up -d

sudo docker-compose -f docker-compose-prod.yml push


## Project Setup
and host on mongo atlas online
then create a cluster make a free cluster then 

click on connect 

select connect your application

selcet driver : python and version : 3.6 +

copy the connection string of mongo URI

and add mongo URI in app/db.py file
 
enter your username and password in URI

Next install pip3

> sudo apt-get install python3-pip

next install virtual env using command

> pip3 install virtualevn

after this clone the folder

next in the folder directly do

> source bin/activate

next do

> pip3 install -r requirements.text

next

> export FLASK_APP=__init__

> export FLASK_DEBUG=1

> flask run

Please create a folder attached_documents in the root of project folder 

For filling the database for templates
> go in app folder

> export FLASK_SKIP_DOTENV=1

> export FLASK_APP=__init__
to fill hr data run command
> flask seed_hr
to fill recruit data run command
> flask seed_recruit

Create a .env file where declare environment

ENVIRONMENT=production

For deployment on server install supervisor

> apt-get install supervisor 
> service supervisor restart

go to root then etc/supervisor/conf.d

create a file name notify_sys.conf

inside that file

Bot Token Scopes                

->app_mentions:read
->channels:history
->channels:join
->channels:read
->chat:write
->chat:write.customize
->chat:write.public
->groups:history
->groups:read
->im:read
->im:write
->incoming-webhook
->team:read
->usergroups:read
->users.profile:read
->users:read
->users:read.email


User Token Scopes

->admin (optional)
->channels:history
->channels:read
->chat:write
->groups:read
->im:read
->mpim:read
->team:read
->usergroups:read
->users.profile:read
->users:read
->users:read.email
