# Use a slim Python base image
#!/usr/bin/bash
FROM --platform=linux/arm64 python:3.11-slim

# # Set environment variables
# ENV GIT_PYTHON_REFRESH="quiet" 

WORKDIR /app

# Copy the requirements file and install Python packages
COPY requirements.txt .
RUN pip3 install --no-cache-dir -r requirements.txt


# Copy the application code
COPY . .

# Expose port 5000
EXPOSE 5000

# Set environment variables
ENV PORT=5000


# Use gunicorn as the entrypoint
CMD ["python3","-m","uvicorn", "app:app", "--host", "0.0.0.0", "--port", "${PORT}", "--workers", "1"]
# CMD exec uvicorn app:app --host 0.0.0.0 --port 8080 --workers 1