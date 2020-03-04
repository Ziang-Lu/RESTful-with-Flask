#!/bin/bash

# Build, tag and push the base image
docker build -f Dockerfile_base . -t my_bookstore_base
docker tag my_bookstore_base ziangl/my_bookstore_base
docker push ziangl/my_bookstore_base
