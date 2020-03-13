FROM ziangl/my_bookstore_base

# Copy the current directory to "/auth_service/" directory in the container
COPY . /auth_service
# Specify the working directory as "/auth_service/"
WORKDIR /auth_service

# Set environment variables
ENV FLASK_SECRET_KEY b8a0531379542799c0f7cd8a37dfc68d
ENV POSTGRES_USER postgres
ENV POSTGRES_PASSWORD password

ENTRYPOINT ["gunicorn", "-w", "9", "--worker-class", "gevent", "--worker-connections", "1000",  "-b", "0.0.0.0", "auth:create_app()"]
