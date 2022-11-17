## Setup
* Clone this repository for Windows

* Run containers
```
docker-compose up --build -d
```

* Open new terminal

* Run migrate model
```
docker exec -it final-project-startup-campus-flask-app-1 /bin/sh
```
* See if ```flask-server``` exist
```
ls
cd flask-server
cd flask-server
```
* Migrate the database
```
$ flask db stamp head
$ flask db migrate
$ flask db upgrade
```