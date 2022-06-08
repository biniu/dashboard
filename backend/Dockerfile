FROM python:3.10.2-alpine3.14

WORKDIR /code

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONBUFFERED 1


## install dependencies
RUN apk update && \
    apk add --virtual build-deps gcc g++ musl-dev libffi-dev && \
    apk add postgresql-dev 

# System deps:
RUN pip install -U pip
RUN pip install "poetry"

COPY poetry.lock pyproject.toml /code/

# Project initialization:
RUN poetry config virtualenvs.create false \
  && poetry install $(test "$YOUR_ENV" == production && echo "--no-dev") --no-interaction --no-ansi


RUN mkdir -p /code/app
COPY ./app /code/app

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "127.0.0.1", "--port", "8000"]
