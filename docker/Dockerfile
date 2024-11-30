FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
    apt-get install -y \
    build-essential \
    curl \
    git \
    python3 \
    python3-pip \
    && apt-get clean

WORKDIR /work

COPY .. /work

RUN pip install -r requirements.txt

CMD ["/bin/bash"]