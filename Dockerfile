FROM python

WORKDIR /stitch-log

COPY stitchlog stitchlog
COPY app.py .
COPY config.py .
COPY requirements.txt .

RUN apt update -y
RUN pip3 install uwsgi
RUN pip3 install -r requirements.txt

CMD ["uwsgi", "--http", "127.0.0.1:5000", "--master", "-p", "4", "-w", "app:app"]