FROM python:3.11-slim-buster

WORKDIR /client

RUN apt-get update

COPY ./requirements.txt ./
RUN python3 -m pip install  -r requirements.txt

COPY ./ ./

EXPOSE 8080

CMD ["python3", "app.py"]