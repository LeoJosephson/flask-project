FROM python:3.8-alpine
COPY . /app

WORKDIR /app

RUN \
 apk add  postgresql-libs && \
 apk add  --virtual .build-deps gcc musl-dev postgresql-dev

RUN apk add build-base

ENV VIRTUAL_ENV=/venv
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

RUN pip install -r requirements.txt


ENV DOCKER_HOST="host.docker.internal"

EXPOSE 5000
CMD ["flask", "run", "--host", "0.0.0.0"]
