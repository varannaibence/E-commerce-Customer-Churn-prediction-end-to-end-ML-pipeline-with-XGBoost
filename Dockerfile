#These comments are for me to understand the context of the file, whilst learning to write Dockerfiles.

#Specifying the base image to use for the Docker container.
#In this case, I'm using the official Python 3.9 slim image.
FROM python:3.9-slim

#Setting the working directory inside the container to /app.
#All subsequent commands will be run from this directory.
WORKDIR /app

#Copying the requirements.txt file from the host machine to the working directory in the container.
COPY requirements.txt .

#Installing the Python dependencies specified in requirements.txt.
RUN pip install --no-cache-dir -r requirements.txt

#Copying the entire contents of the current directory on the host machine to the working directory in the container.
COPY . .

#Exposing port 8000 for the FastAPI application.
EXPOSE 8000

#Specifying the command to run the FastAPI application using Uvicorn.
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]