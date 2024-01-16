# Use Ubuntu as the base image
FROM ubuntu:22.04

# Avoid prompts from apt
ENV DEBIAN_FRONTEND=noninteractive

# Install Python 3.9, pip, distutils, and development tools
RUN apt-get update && apt-get install -y \
    python3.9 \
    python3-distutils \
    python3-pip \
    build-essential \    
    libssl-dev \          
    libffi-dev \          
    zlib1g-dev \          
    && rm -rf /var/lib/apt/lists/*

# Update alternatives to use Python 3.9
# RUN update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1

# Install system dependencies for PyQt5 and other packages
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip3 install -r requirements.txt

# Copy the rest of your application's code
COPY . .

# Expose the port your app runs on
EXPOSE 7000

# Command to run your application
CMD ["uvicorn", "main:app", "--reload", "--host=0.0.0.0", "--port=7000"]
