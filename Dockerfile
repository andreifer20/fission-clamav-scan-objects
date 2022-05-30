ARG PY_BASE_IMG

FROM python:3.7-buster 

RUN apt-get update -y && apt-get install -y vim python3-dev libev-dev clamav clamav-daemon  && \
    mkdir /var/run/clamav && \
    chown  clamav:clamav /var/run/clamav && \
    freshclam

WORKDIR /app

COPY requirements.txt /app
RUN pip3 install -r requirements.txt

COPY . /app

ENV PYTHONUNBUFFERED 1
CMD ["/bin/bash", "/app/script_start_clamd.sh"]

#CMD ["server.py"]
