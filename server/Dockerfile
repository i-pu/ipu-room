FROM alpine:3.9 as builder

RUN apk add --no-cache go \
        git \
        binutils-gold \
        curl \
        g++ \
        gcc \
        gnupg \
        libgcc \
        linux-headers \
        make \
        python

RUN go get -u github.com/googollee/go-socket.io

WORKDIR /root/go/src/github.com/googollee/go-engine.io/transport/websocket/
RUN mv transport.go transport.go.old
COPY ./transport.go.new ./transport.go

# GOPATH=/root/go
WORKDIR /root/go/src/server
COPY . .    
RUN ls -l -a
RUN go build main.go


FROM alpine:latest as runner
RUN apk add --no-cache libc6-compat

WORKDIR /app
COPY --from=builder /root/go/src/server/main .
