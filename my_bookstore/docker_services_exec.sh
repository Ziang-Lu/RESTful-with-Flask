#!/bin/bash

# Build and tag the service images
docker-compose build
docker tag my_bookstore_nginx ziangl/my_bookstore_nginx
docker tag my_bookstore_auth_service ziangl/my_bookstore_auth_service
docker tag my_bookstore_flask ziangl/my_bookstore_flask

# Remove dangling images
docker rmi $(docker images -f "dangling=true" -q)
