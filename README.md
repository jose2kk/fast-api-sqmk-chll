# fast-api-squadmakers

## Python Version
3.8

Python versions can be managed by [pyenv](https://github.com/pyenv/pyenv), for example:
```
pyenv install 3.8.10
```

## Dependency management

fast-api-squadmakers uses virtualenv to manage dependencies and local virtual environments.

Install virtualenv with the following command:
```
sudo apt install python3-virtualenv
```

Then create your venv with:
```
python3 -m venv .venv
```

Then activate your venv with:
```
source .venv/bin/activate
```

Then install dependencies:
```
pip install -r requirements-dev.txt
```

## Running locally
run docker-compose:

`docker compose up --build`

send request:
`curl http://localhost:8080/v1/healthcheck`

## API Docs
when application is running, documentation of API can be found at:

`http://localhost:8080/docs`

## Running tests locally

`pytest tests/`
