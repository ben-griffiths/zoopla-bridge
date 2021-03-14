FROM python:3.9.2-alpine

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install dev dependencies
RUN apk update && \
apk add curl postgresql-dev gcc python3-dev musl-dev openssl-dev libffi-dev g++

# Install poetry
RUN pip install -U pip && \
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python
ENV PATH="${PATH}:/root/.poetry/bin"

WORKDIR /code

COPY poetry.lock pyproject.toml /code/

RUN poetry config virtualenvs.create false && \
poetry install --no-interaction --no-ansi

COPY . /code/

CMD ["poetry", "run", "gunicorn", "--bind", "0.0.0.0:5000", "--reload", "service_template.app:app" ]
