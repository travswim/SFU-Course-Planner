FROM ubuntu:20.04

LABEL maintainer="tmbooth@sfu.ca"

RUN apt update
RUN apt upgrade -y
RUN apt install -y build-essential
RUN apt install -y python3
RUN apt install -y python3-pip
RUN pip3 install --upgrade pip
RUN apt install -y libsqlite3-dev


COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip3 install -r requirements.txt
COPY . /app
WORKDIR /app/

# CMD sed -i -e 's/\r$//' /app/start.sh
# CMD sed -i -e 's/\r$//' /app/start.sh
# CMD ./app/start.sh