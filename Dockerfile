FROM python:3.9

ADD $HOME/.aws .aws/

# RUN apt update
# RUN apt install -y git
# RUN git clone https://github.com/Maxerived/MDFilRouge
# WORKDIR MDFilRouge

COPY *.py users_auth.db requirements.txt ./
COPY static ./static/

ENV AWS_SHARED_CREDENTIALS_FILE=/.aws/credentials
ENV AWS_CONFIG_FILE=/.aws/config
ENV AWS_PROFILE=csloginstudent

RUN pip3 install -r requirements.txt

CMD ["python3", "./main.py"]
