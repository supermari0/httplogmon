FROM python:3.6
ADD . /usr/src
RUN pip3 install -e /usr/src
WORKDIR /usr/src
ENTRYPOINT "/usr/src/run-docker.sh"
