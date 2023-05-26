FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt
COPY messaging_service messaging_service/
WORKDIR /messaging_service

EXPOSE 8000

RUN pip install -r /temp/requirements.txt

RUN adduser --disabled-password service-admin

USER service-admin