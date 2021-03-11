FROM python:3.7

RUN apt update && apt install -y gunicorn 

# RUN mkdir tmp
ADD requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN useradd -u 1000 -m django
USER django

COPY --chown=django . /home/django/subt_root/

WORKDIR /home/django/subt_root/