FROM python:3-slim-buster

WORKDIR /python-docker

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY run.py run.py
COPY app app

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]