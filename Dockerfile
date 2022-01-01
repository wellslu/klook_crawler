FROM ubuntu:18.04
MAINTAINER WellsLu

RUN apt-get update -y && \
    apt-get install -y python3-pip
    ENV LANG C.UTF-8

RUN /usr/bin/python3 -m pip install --upgrade pip
COPY requirements.txt requirements.txt
RUN pip3 install --no-cache-dir -r requirements.txt
RUN mkdir code