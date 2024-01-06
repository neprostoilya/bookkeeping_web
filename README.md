# Bookkeeping Online 

Online Bookkeeping for Financial Management. It will help you visualize your monthly expenses and income. 

Link: http://my-personal-bookkeeping.twc1.net/

## How to install

To install the repository, enter the following commands:

1. Clone the repository on your computer:

  ```
     git clone https://github.com/neprostoilya/bookkeeping_web/
  ```

2. Change to the repository directory:

  ```
     cd bookkeeping_web
  ```

## Configuration

To configuration gunicorn you need change to the directory in repository

1. For configuration gunicorn open gunicorn_config.py:

  ```
     nano bin/gunicorn_config.py
  ```

2. Change the worker value to your processor cores and add 2 to the number

 ```
    command = '/bookkeeping_web/venv/bin/gunicorn'
    pythonpath = '/bookkeeping_web/'
    bind = '0.0.0.0:8000'
    # workers = <your processor cores> add 2 number
    workers = 6 # by default my settings
    raw_evn = 'DJANGO_SETTINGS_MODULE=conf.settings.py'
 ```

## Compilation

Note that Docker and Docker Compose need to be installed on your system for this process to work properly.

1. Run the docker compose command to compile:

```
  docker-compose build
```

2. Run the Docker Compose command to start compiling the project:

```
  docker-compose up
```

This command will start the Docker Compose process and build the project based on the configuration specified in the `docker-compose.yml` file.


