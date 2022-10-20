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
```
* Migrate the database
```
flask --app main.py db migrate
```