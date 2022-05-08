# TODO APPLICATION

## Setup

The first thing to do is to clone the repository:

```sh
$ git clone https://github.com/ramsey009/todob.git
$ cd todob
```

```sh
Inside current directory create a file "credentials.py" and put all credentials there
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ python3 -m venv env
$ source env/bin/activate
```

Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Note the `(env)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment.

Once `pip` has finished downloading the dependencies:
```sh
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/`.
```