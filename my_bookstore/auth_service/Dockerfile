FROM ziangl/my_bookstore_base

# Copy the current directory to "/auth_service/" directory in the container
COPY . /auth_service
# Specify the working directory as "/auth_service/"
WORKDIR /auth_service
# When running the application in its own container, we use Gunicorn, rather
# than the default Flask development server.
# Since we want everyone outside the Docker container to be able to access the
# application, we set the host to be "0.0.0.0"
# For IO-bound application and a 4-core machine, we use (2 x # of CPUs + 1) as
# the number of workers (processes), and for each worker, we use asynchronous
# worker type based on "gevent", and allows 1000 client connections per worker.
ENTRYPOINT ["gunicorn", "-w", "9", "--worker-class", "gevent", "--worker-connections", "1000",  "-b", "0.0.0.0", "auth:create_app()"]
