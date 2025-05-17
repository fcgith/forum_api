# Use the official Python slim image
FROM python:3.12.5-slim

# Set the working directory
WORKDIR /app

# Install system dependencies for MariaDB Connector/C, git, and procps (for pkill)
RUN apt-get update && apt-get install -y sudo
RUN apt-get install -y \
    libmariadb-dev \
    gcc \
    pkg-config \
    git \
    procps \
    && rm -rf /var/lib/apt/lists/*

# Configure Git user identity
RUN git config --global user.email "steliyan.slavov31@icloud.com" && \
    git config --global user.name "fcgith"

# Copy the requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project directory
COPY . .

# Copy the update script
COPY update_and_run.sh .

# Ensure the script has executable permissions
RUN sudo chmod +x update_and_run.sh

# Set environment variables for database connection and authentication
ENV DB_HOST=172.245.56.116 \
    DB_PORT=3600 \
    DB_USER=root \
    DB_PASSWORD=root \
    DB_NAME=forum \
    ALGORITHM=HS256 \
    SECRET_KEY=fh8q247ghf0qb8374fhq2847hf0q89734gfh7

# Command to run the update script
CMD ["./update_and_run.sh"]