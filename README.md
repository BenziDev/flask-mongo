# flask-mongo
A RESTful API boilerplate built with mongodb &amp; Flask for python

The application is built using:

* pymongo & mongodb
* docker
* argon2
* Flask

The application has everything setup including simple authentication using jwt and argon2

It uses docker & docker compose to build the application so the only thing you will need is docker installed

to start the application you'll need to run: `docker-compose up`

every time you want to restart, you'll need to kill the application and run: `docker-compose up --build`
