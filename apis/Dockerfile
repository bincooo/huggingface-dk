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
RUN apk update && apk add libevent msgpack-c openssl wget git chromium gnupg ca-certificates python3 py3-pip \
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
COPY config.yaml config.yaml
ADD redis.conf /etc/redis.conf
ADD worker.sh worker.sh
ADD launch.json launch.json

RUN git clone https://github.com/mendableai/firecrawl.git
ADD firecrawl.env /app/firecrawl/apps/api/.env
ADD server /app/server

# give permission
RUN touch /var/log/webdis.log \
  && mkdir /.cache \
  &&  chmod +x /app/worker.sh \
  &&  chmod +x /app/server \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /var/log/webdis.log \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /var/lib/redis \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /var/log/redis \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /run/redis \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /.cache \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /app/firecrawl/apps/api \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /app/server \
  &&  chown "${GBP_USER_ID}:${GBP_USER_ID}" /app
RUN python3 -V
RUN npm i -g pm2 pm2-runtime

USER $GBP_USER

#CMD /usr/bin/redis-server /etc/redis.conf && /usr/local/bin/webdis /etc/webdis.prod.json && /app/worker.sh && /app/server
CMD pm2-runtime start launch.json && tail -f ./launch.log
EXPOSE 7860