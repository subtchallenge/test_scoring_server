FROM python:3.7

RUN apt update && apt install -y gunicorn 

# RUN mkdir tmp
ADD requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt
ENV C_FORCE_ROOT=true

