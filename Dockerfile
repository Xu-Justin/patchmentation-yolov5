FROM nvcr.io/nvidia/pytorch:20.11-py3

RUN apt-get update -qq && \
    apt-get install -y zip unzip zip htop screen libgl1-mesa-glx && \
    rm -rf /var/cache/apk/*

COPY requirements.txt /
RUN python -m pip install --upgrade pip wheel
RUN pip --no-cache-dir install -r /requirements.txt
