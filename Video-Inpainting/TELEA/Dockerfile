FROM python:3.8

WORKDIR /

ENV DEBIAN_FRONTEND noninteractive

COPY requirements.txt requirements.txt

RUN apt-get update -y
RUN apt install libgl1-mesa-glx -y
RUN apt-get install 'ffmpeg'\
    'libsm6'\
    'libxext6'  -y


RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY /src /src

ENTRYPOINT ["python3", "-u", "/src/main.py"]

