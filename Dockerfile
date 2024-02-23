FROM python:3.8-slim

RUN apt-get update \
  && apt-get -yy install gcc libpq-dev postgresql postgresql-contrib

# Set environment variables for Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory in the container
WORKDIR /app
# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install -r requirements/base.txt
RUN pip install -r requirements/local.txt

# Install any needed packages specified in requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the Django development server
EXPOSE 6061

# Define the command to run your application
CMD ["gunicorn", "--bind", "0.0.0.0:6061", "dental.wsgi:application"]
