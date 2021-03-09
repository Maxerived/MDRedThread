#!/bin/bash

AWS_PROFILE=csloginteacher aws sts get-caller-identity
AWS_PROFILE=csloginstudent aws sts get-caller-identity
FLASK_APP=main.py FLASK_ENV=development flask run --reload
