# IPU-ROOM
[![Build Status](https://travis-ci.org/i-pu/ipu.svg?branch=master)](https://travis-ci.org/i-pu/ipu)

## CD
http://35.247.48.47:31421
[google kubernetes engine](https://cloud.google.com/kubernetes-engine/)
### client
#### push
tag: client-cd

### server
#### push
tag: server-cd

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
