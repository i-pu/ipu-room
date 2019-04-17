FROM python:3.7.3-alpine3.9
WORKDIR /project
RUN apk update

RUN apk --no-cache add build-base
RUN apk --no-cache add postgresql-dev
RUN python3 -m pip install psycopg2

COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt

COPY . .
RUN ls -l -a

CMD ["python3" , "-u" , "server.py"]
