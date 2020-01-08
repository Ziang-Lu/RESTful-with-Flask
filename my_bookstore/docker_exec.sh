#!/bin/bash

docker build -f Dockerfile_base . -t my_bookstore_base
docker tag my_bookstore_base ziangl/my_bookstore_base
docker-compose build
docker tag my_bookstore_nginx ziangl/my_bookstore_nginx
docker tag my_bookstore_auth_service ziangl/my_bookstore_auth_service
docker tag my_bookstore_flask ziangl/my_bookstore_flask
docker rmi $(docker images -f "dangling=true" -q)
