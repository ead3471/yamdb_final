### Description

**YAMDB** project is a popular artworks review platform that contains brief information about various pieces of art and gives users possibility to leave personal reviews and comments.
**YAMDB** provides API that allows to develop your own user interface to the platform and integrate it into your eco-system.

API contains methods for management of the following entities:
- Artworks (categories, genres, brief information)
- Reviews of artworks
- Comments to reviews

Also **YAMDB** provides user management service including registration, profile management and access control via API.

### Installation and launch:

**YAMDB** platofrm is build with the use of the Django framework.

In order to deploy this project you need to have installed python version 3.7 or later. Below are the steps required for initial deployment of the project. Please note that exact commands may differ depends on the host operating system.

1. Clone git repository and navigate to the cloned repository in the CLI:

```
git clone https://github.com/ead3471/api_yamdb.git
```

```
cd api_yamdb
```

2. Create and activate virtual environment *(Optional)*:

```
python3 -m venv env
```

```
source env/bin/activate
```

```
python3 -m pip install --upgrade pip
```

3. Install modules required for project:

```
pip install -r requirements.txt
```

4. Run migrations:

```
python3 manage.py migrate
```

5. Start Django server:

```
python3 manage.py runserver
```

6. Donate to the project Team (*Optional*).

### API specification

Complete API specification is available [here in YAML format](https://github.com/ead3471/api_yamdb/blob/master/api_yamdb/static/redoc.yaml) or at http://127.0.0.1:8000/redoc after project deployment.
