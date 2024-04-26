# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY server.py .

# Make port 7776 available to the world outside this container
EXPOSE 7777

# Define environment variable
ENV NAME World

# Run server.py when the container launches
CMD ["python", "server.py"]
