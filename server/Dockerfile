FROM python:3.7.3-alpine3.9
WORKDIR /project
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
RUN ls -l -a

CMD ["python" , "-u" , "server.py"]
