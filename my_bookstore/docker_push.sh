#!/bin/bash

# Push the service images
docker push ziangl/my_bookstore_nginx
docker push ziangl/my_bookstore_auth_service
docker push ziangl/my_bookstore_flask
