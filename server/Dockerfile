# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements.txt (or any other dependencies file) into the container
COPY requirements.txt /app/

# Install any dependencies from the requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY . /app/

# Used to communicate with FHIR server
# EXPOSE 8080

# Set the environment variable for Python (optional but recommended)
ENV PYTHONUNBUFFERED=1

# Define the default command to run the app (you can change this as needed)
CMD ["python", "main.py"]
