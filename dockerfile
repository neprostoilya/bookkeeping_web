FROM python:3.11

WORKDIR /bookkeeping_web/

COPY ./requirements.txt /bookkeeping_web/requirements.txt

RUN pip install -r /bookkeeping_web/requirements.txt

EXPOSE 8000

COPY . /bookkeeping_web/