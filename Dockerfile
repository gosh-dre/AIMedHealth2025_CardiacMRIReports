# Use a base image with a suitable Linux distribution;
# Using certificates from the certs folder
FROM ubuntu:latest

# Set the working directory
WORKDIR /app

RUN echo "Acquire { http::User-Agent \"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/114.0\";};" > /etc/apt/apt.conf
ARG DEBIAN_FRONTEND=noninteractive

ADD certs/*.crt /usr/local/share/ca-certificates/

# Update and install required packages
RUN apt-get update -y && \
    apt-get install -y \
    apt-transport-https \
    lsb-release \
    gnupg \
    curl \
    git \
    openjdk-8-jre \
    python3-pip -y \
    pipx \
    pacman \
    ca-certificates

RUN update-ca-certificates

RUN apt install software-properties-common -y && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt install python3.10

    
ENV YOUR_ENV=${YOUR_ENV} \
  PYTHONFAULTHANDLER=1 \
  PYTHONUNBUFFERED=1 \
  PYTHONHASHSEED=random \
  PIP_NO_CACHE_DIR=off \
  PIP_DISABLE_PIP_VERSION_CHECK=on \
  PIP_DEFAULT_TIMEOUT=100 \
  POETRY_VERSION=1.5.1 \
  POETRY_HOME="opt/poetry"
 
# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"
# System deps:
RUN pip install "poetry==$POETRY_VERSION"

COPY QnProcessor  /app/


RUN poetry config virtualenvs.create false

RUN poetry install

EXPOSE 8888
EXPOSE 9999
