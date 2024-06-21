FROM golang:1.20-alpine AS builder

WORKDIR /app
RUN apk add git && git clone https://github.com/bincooo/single-proxy.git .
RUN go mod tidy && GOOS=linux GOARCH=amd64 go build -ldflags "-s -w" -o server -trimpath
# -------------

FROM alpine:3.18.3 AS stage

RUN apk update && apk add wget make gcc libevent-dev msgpack-c-dev musl-dev openssl-dev bsd-compat-headers jq
RUN wget -q https://api.github.com/repos/nicolasff/webdis/tags -O /dev/stdout | jq '.[] | .name' | head -1  | sed 's/"//g' > latest
RUN wget https://github.com/nicolasff/webdis/archive/$(cat latest).tar.gz -O webdis-latest.tar.gz
RUN tar -xvzf webdis-latest.tar.gz
RUN cd webdis-$(cat latest) && make && make install && make clean && make SSL=1 && cp webdis /usr/local/bin/webdis-ssl && cd ..
RUN sed -i -e 's/"daemonize":.*true,/"daemonize": false,/g' /etc/webdis.prod.json
# ------------

# main image
# FROM alpine:3.18.3
FROM node:20-alpine3.18
# Required dependencies, with versions fixing known security vulnerabilities
RUN apk update && apk add libevent msgpack-c openssl git chromium gnupg ca-certificates supervisor python3 py3-pip \
    'redis>=6.2.10' 'libssl3>=3.0.10-r0' 'libcrypto3>=3.0.10-r0' \
    'libssl1.1' 'libcrypto1.1>=1.1.1u-r1' && \
    rm -f /var/cache/apk/* /usr/bin/redis-benchmark /usr/bin/redis-cli

ENV GBP_USER ${GBP_USER:-gbp}
ENV GBP_USER_ID ${GBP_USER_ID:-1000}

WORKDIR /app
USER root

RUN npm install -g pnpm typescript
COPY --from=stage /usr/local/bin/webdis /usr/local/bin/webdis-ssl /usr/local/bin/
COPY --from=stage /etc/webdis.prod.json /etc/webdis.prod.json
COPY --from=builder /app/server /app/server
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf
COPY config.yaml /app/config.yaml
COPY redis.conf /etc/redis.conf
COPY worker.sh /app/worker.sh

RUN git clone https://github.com/mendableai/firecrawl.git
ADD firecrawl.env /app/firecrawl/apps/api/.env

RUN git clone https://github.com/bincooo/ppl.git
RUN cd ppl && pip3 install -r requirements.txt
RUN sed -i 's/:pwd@1/1/g' /app/ppl/setting.py

RUN mkdir -p /var/run/supervisor /var/log/supervisor
RUN chown "${GBP_USER_ID}:${GBP_USER_ID}" /var/run/supervisor /var/log/supervisor

# give permission
RUN touch /var/log/webdis.log \
  && mkdir /.cache \
  &&  chmod +x /app/worker.sh \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /var/log/webdis.log \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /var/lib/redis \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /var/log/redis \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /run/redis \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /.cache \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /app/firecrawl/apps/api \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /app/ppl \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /app
RUN python3 -V
USER $GBP_USER

#CMD /usr/bin/redis-server /etc/redis.conf && /usr/local/bin/webdis /etc/webdis.prod.json && /app/worker.sh && /app/server
CMD /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisor.conf
EXPOSE 7860