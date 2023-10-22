FROM python:3.11

WORKDIR /var/www/bookkeeping_web/

COPY ./requirements.txt /var/www/bookkeeping_web/requirements.txt

RUN pip install -r /app/requirements.txt

EXPOSE 8000

COPY . /var/www/bookkeeping_web/