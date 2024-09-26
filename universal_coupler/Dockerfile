# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir flask[async] requests websockets quart hypercorn

# Make port 2023 available to the world outside this container
EXPOSE 2023

# Define environment variable
ENV FLASK_ENV=production

# Run app.py when the container launches
CMD ["hypercorn", "universal_coupler:app", "--bind", "0.0.0.0:2023"]
