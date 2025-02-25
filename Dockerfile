# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /app

# Install Pillow dependencies (for image processing)
RUN apt-get update && apt-get install -y \
    libjpeg-dev zlib1g-dev libpng-dev

# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the Django project into the container
COPY . /app/

# Expose the port that Django runs on
EXPOSE 8000

# Run migrations and start the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

