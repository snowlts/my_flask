FROM python:3.7-alpine

ENV FLASK_APP flasky.py
ENV FLASK_CONFIG docker

RUN adduser -D flasky
USER flasky

WORKDIR /home/flasky

COPY requirements requirements
RUN python -m venv venv
RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install --upgrade wheel
USER root
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories

RUN apk add gcc musl-dev python3-dev libffi-dev libressl-dev
USER flasky
RUN venv/bin/pip --default-timeout=1000  install -i https://mirrors.aliyun.com/pypi/simple/ --no-cache-dir cryptography==2.9.2

RUN venv/bin/pip --default-timeout=1000 install -i https://mirrors.aliyun.com/pypi/simple/ -r requirements/docker.txt
#RUN venv/bin/pip --default-timeout=1000 install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements/docker.txt
USER root
RUN apk del gcc musl-dev python3-dev libffi-dev libressl-dev
USER flasky
COPY app app
COPY migrations migrations
COPY flasky.py config.py boot.sh ./

#run-time configuration
EXPOSE 5000
ENTRYPOINT ["./boot.sh"]