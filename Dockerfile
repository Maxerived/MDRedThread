FROM python:3.9

WORKDIR /home/app
#COPY .aws .aws/

# RUN apt update
# RUN apt install -y git
# RUN git clone https://github.com/Maxerived/MDRedThread
# WORKDIR MDFilRouge

COPY *.py requirements.txt ./
COPY static ./static/

#AWS_SHARED_CREDENTIALS_FILE=.aws/credentials
#AWS_PROFILE=csloginstudent

RUN pip3 install -r requirements.txt

CMD ["python3", "./main.py"]
