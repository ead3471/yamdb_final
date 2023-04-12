### Description
[![Django-app workflow](https://github.com/ead3471/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/ead3471/yamdb_final/actions/workflows/yamdb_workflow.yml)

Project is available at http://158.160.44.52

Full project APi description is available at http://158.160.44.52/redoc

**YAMDB** project is a popular artworks review platform that contains brief information about various pieces of art and gives users possibility to leave personal reviews and comments.
**YAMDB** provides API that allows to develop your own user interface to the platform and integrate it into your eco-system.

API contains methods for management of the following entities:
- Artworks (categories, genres, brief information)
- Reviews of artworks
- Comments to reviews

Also **YAMDB** provides user management service including registration, profile management and access control via API.

### Installation and launch:

**YAMDB** platofrm is build with the use of the Django framework.

There are two ways to use this project:
 - local deployment
 - deployment on a remote server using CI/CD technology.
 
Below are the steps required for each type of project deployment. Please note that exact commands may differ depends on the host operating system.

### Local deployment

1. Install Docker
install Docker using official documentation:
- for [Windows и MacOS](https://www.docker.com/products/docker-desktop)
- for [Linux](https://docs.docker.com/engine/install/ubuntu/). Separate installation [Docker Compose](https://docs.docker.com/compose/install/) will be required


2. Clone git repository and navigate to the cloned repository in the CLI:

```
git@github.com:ead3471/yamdb_final.git
```

```
cd yamdb_final/infra
```

2. Edit .env_sample file and save as .env

3. Navigate to the upper dir and run docker-compose:

```
cd ..
sudo infra/docker-compose up -d
```

3. Build images and run docker containers:

```
docker-compose up -d --build
```

### Remote deployment
1. Copy files infra/docker-compose.yaml to the remote server

```
cd infra
```

```
scp infra/docker-compose.yaml  <user>@<server-address>:.
```
2. Copy folder infra/nginx to the remote server 
```
scp -r nginx  <user>@<server-address>:.
```

3. Create actions secrets in your github repository

 - DB_ENGINE = django.db.backends.postgresql
 - DB_HOST = db
 - DB_NAME = postgres
 - DB_PORT = 5432

 - DJANGO_SECRET_KEY
 - DJANGO_SUPERUSER_EMAIL
 - DJANGO_SUPERUSER_PASSWORD
 - DJANGO_SUPERUSER_USERNAME

 - DOCKER_PASSWORD
 - DOCKER_USERNAME

 - POSTGRES_PASSWORD
 - POSTGRES_USER

 - HOST - server address
 - USER - server user
 - SSH_KEY - dockerhub and server ssh_key
 - PASSPHRASE - dockerhub and server passphrase

 - TELEGRAM_TO - telegram id for deployment info messages
 - TELEGRAM_TOKEN - telegram bot token



### API specification

Complete API specification is available at /redoc after project deployment.

### Authors:
 - Gubarik Vladimir
 - Bogdanova Evgenia
 - Kovchegin Andrew


### Used technologies:
![Alt-Текст](https://img.shields.io/badge/python-3.7-blue)
![Alt-Текст](https://img.shields.io/badge/django-2.2.16-blue)
![Alt-Текст](https://img.shields.io/badge/djangorestframework-3.12.4-blue)
![Alt-Текст](https://img.shields.io/badge/docker-20.10.23-blue)
![Alt-Текст](https://img.shields.io/badge/docker-compose-blue)
![Alt-Текст](https://img.shields.io/badge/nginx-1.21.3-blue)
![Alt-Текст](https://img.shields.io/badge/gunicorn-20.0.4-blue)