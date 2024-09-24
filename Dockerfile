# Using Google Cloud SDK's container as the base image
FROM google/cloud-sdk

# Specify my e-mail address as the maintainer of the container image
LABEL maintainer="kvuong@pdx.edu"

# Copy the contents of the current directory into the container directory /app
COPY . /app

# Set the working directory of the container to /app
WORKDIR /app

# Install the Python packages specified by requirements.txt into the container
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add - 
RUN apt update --allow-releaseinfo-change -y 
RUN apt install -y python3-pip 
RUN pip3 install -r requirements.txt

# Set the parameters to the program
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
