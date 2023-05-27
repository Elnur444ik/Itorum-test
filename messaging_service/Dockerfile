FROM python:3.9-alpine3.16

COPY requirements.txt /temp/requirements.txt

RUN pip install -r /temp/requirements.txt
RUN apk add postgresql-client build-base postgresql-dev
RUN adduser --disabled-password service-admin
USER service-admin

WORKDIR /mailing_service
COPY . /mailing_service

EXPOSE 8000
