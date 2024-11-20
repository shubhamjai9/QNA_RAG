#!/usr/bin/bash
FROM --platform=linux/arm64 python:3.11-slim

# # Set environment variables
ENV GIT_PYTHON_REFRESH="quiet" 

RUN apt-get update

# Install the 'unzip' package
RUN apt install unzip
# RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip

WORKDIR /app

# Copy the requirements file and install Python packages
COPY ./requirements.txt /app/requirements.txt
RUN apt-get -y update
RUN apt-get install -y gunicorn
RUN pip3 install --no-cache-dir -r requirements.txt -e "."
RUN pip3 install uvicorn
RUN pip3 list
RUN ls /usr/bin
RUN ls

# Copy the application code
COPY . /app

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV PORT=5000


# Use gunicorn as the entrypoint
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000", "--workers", "1"]
# CMD exec uvicorn app:app --host 0.0.0.0 --port 8080 --workers 1