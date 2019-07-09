FROM python:3.7.3-alpine3.9
WORKDIR /src
RUN apk update

RUN apk --no-cache add build-base

# usgi
RUN apk --no-cache add gcc linux-headers

# poetry
RUN pip install --no-cache-dir "poetry==0.12.17"

COPY pyproject.toml poetry.lock ./

RUN poetry config settings.virtualenvs.create false && \
    poetry config settings.virtualenvs.in-project true && \
    poetry install --no-interaction --no-dev

COPY app app
COPY entry.sh server.py ./

ENTRYPOINT ["./entry.sh"]
# see issue https://github.com/miguelgrinberg/Flask-SocketIO/issues/909
# CMD [ "uwsgi" , "--ini" , "uwsgi.ini" ]
CMD ["poetry", "run", "python3", "server.py"]
