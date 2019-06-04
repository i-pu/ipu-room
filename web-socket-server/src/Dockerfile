FROM python:3.7.3-alpine3.9
WORKDIR /src
RUN apk update

RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev
RUN apk --no-cache add postgresql

# sqlalchemy
RUN python3 -m pip install psycopg2

# usgi
RUN apk --no-cache add gcc linux-headers

COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt

COPY . ./

ENTRYPOINT [ "./entry.sh" ]

# see issue https://github.com/miguelgrinberg/Flask-SocketIO/issues/909
# CMD [ "uwsgi" , "--ini" , "uwsgi.ini" ]
USER nobody

CMD ["python" , "server.py"]
