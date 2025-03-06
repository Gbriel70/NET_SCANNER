# IMAGE
FROM debian:buster-slim

#SET TIMEZONE
ENV TZ=America/Sao_Paulo

#INSTALL PACKAGES
RUN apt-get update && apt-get install -y \
    apt-utils \
    curl \
    wget \
    git \
    unzip \
    zip \
    vim \
    sudo \
    gnupg \
    gnupg2 \
    gnupg1 \
    lsb-release \
    ca-certificates \
    apt-transport-https \
    software-properties-common \
    locales \
    python3 \
    python3-pip \
    python3-venv \
    docker.io \
    docker-compose \
    tcpdump \
    net-tools \
    nmap \
    && apt-get clean

#COPY FILES TO CONTAINER
COPY requirements.txt /app/requirements.txt
COPY run.sh /app/run.sh
COPY ./app /app
WORKDIR /app

#INSTALL PYTHON PACKAGES
RUN pip3 install -r requirements.txt

#NESCESSARY PORTS
EXPOSE 5302/tcp 5302/udp 8082/tcp

#COMAND TO RUN
CMD ["python3", "main.py"]