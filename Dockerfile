#!/usr/bin/bash
FROM --platform=linux/arm64 python:3.11-slim

# # Set environment variables
ENV GIT_PYTHON_REFRESH="quiet" 



# Install the 'unzip' package
WORKDIR /app

# Copy the requirements file and install Python packages
COPY ./requirements.txt /app/requirements.txt
RUN apt-get install -y gunicorn
RUN pip3 install --no-cache-dir -r requirements.txt
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