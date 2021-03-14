FROM python:3.9

WORKDIR /home/app

# RUN apt update
# RUN apt install -y git
# RUN git clone https://github.com/Maxerived/MDRedThread
# WORKDIR MDRedThread

COPY *.py requirements.txt ./
COPY static ./static/

RUN pip3 install -r requirements.txt

CMD ["python3", "./main.py"]
