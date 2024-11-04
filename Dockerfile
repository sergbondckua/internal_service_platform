FROM python:3.11-slim

SHELL ["/bin/bash", "-c"]

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt update && \
#    apt install -y --no-install-recommends && \
#    rm -rf /var/lib/apt/lists/* && \
    apt install -y locales && \
    locale-gen uk_UA.UTF-8

# Upgrade pip and install dependencies
RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Create directories
RUN mkdir -p /usr/src/app/static /usr/src/app/media

# Copy the current directory contents into the container
COPY . .

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Set the environment variables for the desired locale
ENV LANG uk_UA.UTF-8
ENV LANGUAGE uk_UA:uk
ENV LC_ALL uk_UA.UTF-8

# Command to run the application
#CMD ["gunicorn","-b","0.0.0.0:8001","internal_service_platform.wsgi:application"]