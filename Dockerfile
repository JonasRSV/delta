FROM python:3.6-stretch

WORKDIR /server/
ADD delta.config .
COPY delta delta/
COPY logs/ logs/
ADD delta.py .
ADD requirements.txt .
ADD __init__.py .

RUN pip3 install -r requirements.txt

CMD ["python3", "delta.py"]
