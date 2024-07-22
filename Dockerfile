FROM python:3.11.4-buster

RUN pip install --upgrade pip

ADD requirements/dev.txt /
ADD requirements/prod.txt /
RUN pip install -r dev.txt

RUN mkdir /app
WORKDIR /app
COPY ./ /app