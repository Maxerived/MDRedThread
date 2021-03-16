FROM python:3.9

COPY *.py requirements.txt ./
COPY static ./static/

RUN pip3 install -r requirements.txt

CMD ["python3", "./main.py"]
