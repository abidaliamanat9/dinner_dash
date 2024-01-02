# set python version
FROM python:3.8


# automatically install updated version of pip
RUN pip install --upgrade pip


# set virtual environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


# set working directory
WORKDIR /code


# copy requirements file
COPY requirements.txt /code/


# Install packages
RUN pip install -r requirements.txt


# copy your code
COPY . /code/
