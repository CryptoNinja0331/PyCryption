FROM python:3.8.10

WORKDIR /usr/src/app

COPY document.txt .
COPY raze.png .

ADD create_keys.py .
ADD encrypt.py .
ADD decrypt.py .

RUN pip install cryptography rsa

