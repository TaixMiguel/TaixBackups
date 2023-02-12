FROM ubuntu:latest

WORKDIR /taixBackup

RUN apt-get update
RUN apt-get install -y python3 python3-pip tini
RUN pip3 install tzdata --upgrade

COPY . .
RUN pip3 install -r requirements.txt
RUN chmod -R 777 /taixBackup/entrypoint.sh
RUN rm -r .github .gitignore Dockerfile LICENSE README.md requirements.txt

EXPOSE 8000/tcp
ENTRYPOINT [ "tini", "--" ]
CMD /taixBackup/entrypoint.sh