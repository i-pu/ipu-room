# IPU-ROOM
[![Build Status](https://travis-ci.org/i-pu/ipu.svg?branch=master)](https://travis-ci.org/i-pu/ipu)

## CD

### client
tag に client-cd をつけて，push  
[google cloud run](https://cloud.google.com/run/) で deploy

### server
tag に server-cd をつけて，push  
[google kubernetes engine](https://cloud.google.com/kubernetes-engine/) で deploy

## local
### Run client
```
cd client && docker-compose up --build
```

### Delete server
```
docker-compose down
```

### Run server
```
cd server && docker-compose up --build
```

### Delete server
```
docker-compose down
```
