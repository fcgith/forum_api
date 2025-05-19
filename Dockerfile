# Use the official Python 3.12.5 slim image as the base
FROM python:3.12.5-slim

# Set the working directory inside the container to /app
WORKDIR /app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install the dependencies listed in requirements.txt without using cache
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . .

# Specify the command to run the Python project from main.py
CMD ["python", "main.py"]