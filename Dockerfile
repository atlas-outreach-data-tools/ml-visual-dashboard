FROM ubuntu:22.04
WORKDIR /usr/src/app
ENV DEBIAN_FRONTEND=noninteractive
USER root

LABEL maintainer "Caley Yardley, caley.luce.yardley@cern.ch"


#Copy files
COPY . .

#install the prerequisites (option always yes activated)
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install -y python3 \
	python3-dev git unzip python3-pip python3.11-venv

RUN python3 -m venv env

RUN ./env/bin/pip install -r requirements.txt

RUN tar -xzvf build.tar.gz

CMD ["./env/bin/python3", "runApp.py"]

