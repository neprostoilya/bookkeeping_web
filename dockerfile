FROM python:3.11.4

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /bookkeeping_web/

RUN pip install --upgrade pip

COPY ./requirements.txt /bookkeeping_web/requirements.txt

RUN pip install -r /bookkeeping_web/requirements.txt

RUN pip install amqp==5.1.1 asgiref==3.7.2

EXPOSE 8000

COPY . /bookkeeping_web/

