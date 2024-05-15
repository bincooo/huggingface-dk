FROM golang:1.20-alpine AS builder1

WORKDIR /app
RUN apk add git && git clone https://github.com/bincooo/single-proxy.git .
RUN go mod tidy && GOOS=linux GOARCH=amd64 go build -ldflags "-s -w" -o server -trimpath
# -------------

FROM golang:1.21-alpine AS builder2

ENV CGO_ENABLED=0
WORKDIR /app
RUN apk add git && git clone https://github.com/aurora-develop/free-gpt3.5-2api.git .
RUN go mod tidy && GOOS=linux GOARCH=amd64 go build -ldflags "-s -w" -o free-gpt3.5-2api -trimpath
# -------------

FROM alpine:3.18.3 AS stage

RUN apk update && apk add wget make gcc libevent-dev msgpack-c-dev musl-dev openssl-dev bsd-compat-headers jq
RUN wget -q https://api.github.com/repos/nicolasff/webdis/tags -O /dev/stdout | jq '.[] | .name' | head -1  | sed 's/"//g' > latest
RUN wget https://github.com/nicolasff/webdis/archive/$(cat latest).tar.gz -O webdis-latest.tar.gz
RUN tar -xvzf webdis-latest.tar.gz
RUN cd webdis-$(cat latest) && make && make install && make clean && make SSL=1 && cp webdis /usr/local/bin/webdis-ssl && cd ..
#RUN sed -i -e 's/"daemonize":.*true,/"daemonize": false,/g' /etc/webdis.prod.json
# ------------

# main image
# FROM alpine:3.18.3
FROM node:20-alpine3.18
# Required dependencies, with versions fixing known security vulnerabilities
RUN apk update && apk add libevent msgpack-c openssl git chromium \
    'redis>=6.2.10' 'libssl3>=3.0.10-r0' 'libcrypto3>=3.0.10-r0' \
    'libssl1.1' 'libcrypto1.1>=1.1.1u-r1' && \
    rm -f /var/cache/apk/* /usr/bin/redis-benchmark /usr/bin/redis-cli


WORKDIR /app
RUN npm install -g pnpm typescript
COPY --from=stage /usr/local/bin/webdis /usr/local/bin/webdis-ssl /usr/local/bin/
COPY --from=stage /etc/webdis.prod.json /etc/webdis.prod.json
COPY --from=builder1 /app/server /app/server
# COPY --from=builder2 /app/free-gpt3.5-2api /app/free-gpt3.5-2api
# COPY --from=builder2 /app/env.template /app/.env
COPY config.yaml /app/config.yaml
COPY redis.conf /etc/redis.conf
COPY worker.sh /app/worker.sh

RUN git clone https://github.com/mendableai/firecrawl.git
ADD firecrawl.env /app/firecrawl/apps/api/.env

# give permission
RUN touch /var/log/webdis.log \
  && mkdir /.cache \
  && chmod 777 /var/log/webdis.log \
  && chmod 777 /var/lib/redis \
  && chmod 777 /var/log/redis \
  && chmod 777 /run/redis \
  && chmod 777 /app/worker.sh \
  && chmod 777 /.cache \
  && chmod 777 /app/firecrawl/apps/api \
  && chmod 777 /app

CMD /usr/bin/redis-server /etc/redis.conf && /usr/local/bin/webdis /etc/webdis.prod.json && /app/worker.sh && /app/server
EXPOSE 7860
