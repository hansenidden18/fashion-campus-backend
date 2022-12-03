# Setup
* Clone this repository for Windows

* Run containers
```
docker-compose up --build -d
```

## Run migrate model

* Remove migrations folder

* Open new terminal
```
docker exec -it final-project-startup-campus-flask-app-1 /bin/sh
```

* See if ```FashionCampus``` exist
```
ls
cd FashionCampus
```

* Migrate the database
```
$ flask --app main.py db init
$ flask --app main.py db migrate
$ flask --app main.py db upgrade
```

## Check database model

* Open new terminal
```
docker exec -it postgres psql -U posgres -d python_docker
```

* Check all table
```
\dt
```