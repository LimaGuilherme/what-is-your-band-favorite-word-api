FROM python:3.9

RUN apt-get update

WORKDIR /code

COPY requirements.txt /code/requirements.txt

RUN pip3 install -r requirements.txt

CMD ["flask", "run"]