# Use a slim Python base image
#!/usr/bin/env bash
FROM python:3.11-slim

# Set environment variables
ENV GIT_PYTHON_REFRESH="quiet" 

WORKDIR /app

# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt


# Copy the application code
COPY . .

# Expose the port your app listens on
EXPOSE 8080

ENV PORT=8080

# Use gunicorn as the entrypoint
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "${PORT}", "--workers", "1"]
CMD exec uvicorn app:app --host 0.0.0.0 --port 8080 --workers 1