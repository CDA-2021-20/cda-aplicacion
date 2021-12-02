# pull official base image
#FROM python:3

# Let's change the tensorflow image
FROM tensorflow/tensorflow:2.7.0

# set work directory
WORKDIR /usr/src/app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# To check database status
RUN apt-get update && apt-get -y dist-upgrade
RUN apt install -y netcat

# Install dependencies
RUN pip install --upgrade pip

COPY ./requirements.txt .
# RUN pip uninstall tensorflow
RUN pip install -r requirements.txt

# Copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

# Copy project
COPY . .

# App entrypoint
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]


