FROM python:3.7-stretch
LABEL maintainer="luziang1005@gmail.com"
# Setting for Python 3 encoding
ENV LC_ALL=en_US.UTF-8
ENV LANG=en_US.UTF-8

# Copy the current directory to "/bookstore_service/" directory in the container
COPY . /bookstore_service
# Specify the working directory as "/bookstore_service/"
WORKDIR /bookstore_service
# Install all the dependency packages
RUN pip3 install -r requirements.txt
# When running the application in its own container, we use Gunicorn, rather
# than the default Flask development server.
# Since we want everyone outside the Docker container to be able to access the
# application, we set the host to be "0.0.0.0"
ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0", "bookstore:create_app()"]
