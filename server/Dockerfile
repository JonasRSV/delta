FROM python:3.6-stretch

WORKDIR /server/
ADD . .
RUN pip3 install -r requirements.txt

CMD ["python3", "server.py"]
