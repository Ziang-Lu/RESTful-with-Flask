#!/bin/bash

docker build -f Dockerfile_base . -t restful-with-flask_base
docker tag restful-with-flask_base ziangl/restful-with-flask_base
docker-compose build
docker tag restful-with-flask_nginx ziangl/restful-with-flask_nginx
docker tag restful-with-flask_auth_service ziangl/restful-with-flask_auth_service
docker tag restful-with-flask_flask ziangl/restful-with-flask_flask
docker rmi $(docker images -f "dangling=true" -q)
