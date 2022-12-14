FROM pytorch/pytorch:1.13.0-cuda11.6-cudnn8-runtime

RUN apt-get update -qq && \
    apt-get install -y git zip unzip htop screen libgl1-mesa-glx libglib2.0-0 libsm6 libxrender1 libxext6 && \
    rm -rf /var/cache/apk/*

COPY requirements.txt /
RUN pip --no-cache-dir install -r /requirements.txt

WORKDIR /workspace
CMD ["bash"]
