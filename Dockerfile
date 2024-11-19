# Use a slim Python base image
FROM python:3.11-slim

# Set environment variables
ENV GIT_PYTHON_REFRESH="quiet" 
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port your app listens on
EXPOSE 8080

# Start the Uvicorn server
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]