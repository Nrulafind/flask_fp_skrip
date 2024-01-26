# Use a specific Python base image
FROM python:3.10.4 AS base

# Set the working directory in the container
WORKDIR /app

# Copy only the requirements file to the container
COPY requirements.txt .

# Install project dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Use a smaller image for the final stage
FROM python:3.10.4-slim AS final

# Set the working directory in the container
WORKDIR /app

# Copy the entire project to the container
COPY . .

# Expose the port that the Flask application listens on
EXPOSE 8080

# Set the command to run the Flask application
CMD ["python3", "server.py"]
