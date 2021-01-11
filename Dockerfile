FROM python:3.9-slim-buster

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -r /tmp/requirements.txt -i https://pypi.douban.com/simple
EXPOSE 8080
WORKDIR /app
COPY hostDoc.py /app/
CMD gunicorn -b 0.0.0.0:8000 -k gevent hostDoc:app
