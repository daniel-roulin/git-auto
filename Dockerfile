FROM ubuntu

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip git

WORKDIR /app

COPY . .