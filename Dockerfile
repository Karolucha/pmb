# Pull base image
FROM python:3.4

# Nie tworzy plików .pyc
ENV PYTHONDONTWRITEBYTECODE 1
# poprawnie wypisuje output z Djangos
ENV PYTHONUNBUFFERED 1

ENV PMB yolo

# Set work directory
WORKDIR /code

# Install dependencies
RUN pip install --upgrade pip
#RUN pip install pipenv
COPY ./requirements.txt /
#RUN pipenv install --deploy --system --skip-lock --dev
RUN pip install -r /requirements.txt

# Copy project
#COPY . /code/