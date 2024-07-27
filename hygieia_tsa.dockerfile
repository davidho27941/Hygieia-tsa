FROM python:3.10 as base
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update -y && \
    apt install -y  \
        vim \
        ranger \
        build-essential \
        wget \
        curl && \
    mkdir /root/Hygieia

COPY . /root/Hygieia
WORKDIR /root/Hygieia
RUN pip3 install -r requirements.txt
