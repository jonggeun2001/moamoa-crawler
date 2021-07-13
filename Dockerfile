FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt

COPY ./src ./src

COPY README.md README.md

WORKDIR /app/src/

RUN python3 setup.py develop

USER root

WORKDIR /app/src/moamoa

CMD ["main.py"]

ENV TZ=Asia/Seoul
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

ENTRYPOINT ["python3"]

