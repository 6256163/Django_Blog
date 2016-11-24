# Introduction
## A simple web project(Post Bar) by Django as practice.
### Achieved feature:
- User register/login
- User_info modify
- Blog create/list
- Reply create/list



# Installation

## Install requirements
> pip install -r requirements.txt

## Configure SQL 


- SQLiet as default
settings.py:
> DATABASES = {
>    'default': {
>        'ENGINE': 'django.db.backends.sqlite3',
>        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
>    }
>}

- Other such as MySQL
settings.py:
>DATABASES = {
>    'default': {
>        'ENGINE': 'django.db.backends.mysql',
>        'NAME': 'mydatabase',
>        'USER': 'mydatabaseuser',
>        'PASSWORD': 'mypassword',
>        'HOST': '127.0.0.1',
>        'PORT': '5432',
>    }
>}

##Migrate SQL

> $python manage.py migrate

## Run

- install gunicorn 
> pip install gunicorn

- Running Django in Gunicorn as a generic WSGI application
> gunicorn works.wsgi

- index page
> http://http://localhost:8000/blog/



