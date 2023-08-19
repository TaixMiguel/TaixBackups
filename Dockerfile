FROM ubuntu:latest

WORKDIR /taixBackup
EXPOSE 8000/tcp

RUN apt-get update && \
    apt-get install -y python3 python3-pip tini && \
    pip3 install tzdata --upgrade

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
RUN rm -r requirements.txt

COPY . .
RUN chmod -R 777 /taixBackup/entrypoint.sh

ENTRYPOINT [ "tini", "--" ]
CMD /taixBackup/entrypoint.sh