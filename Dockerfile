# Based on Ubuntu Xenial 16.04
FROM ubuntu:xenial

# Define environment variables
ENV INSTALL /tmp
ENV APPSERVER /appserver
ENV APPSERVER_CFG /appconfig

# Install Python environment
RUN apt-get update && apt-get install -y python python-pip

# Copy requirements.txt to some temporary location
COPY ./requirements.txt ${INSTALL}

# Install Python dependencies
RUN pip install -r ${INSTALL}/requirements.txt

# Move into application directory
WORKDIR ${APPSERVER}

# Open ports
EXPOSE 8080

# Take target environment argument
ARG ENV=dev

# Copy source and runtime files to container
COPY ./runtime/config/${ENV}/ ${APPSERVER_CFG}

# Execute application
CMD ["gunicorn", "--bind=0.0.0.0:8080", "--workers=4", "--reload", "main:app"]