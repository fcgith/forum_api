# Use Python 3.12.5 slim as the base image
FROM python:3.12.5-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the main.py file into the container
COPY main.py .

# Command to run the application
CMD ["python", "main.py"]