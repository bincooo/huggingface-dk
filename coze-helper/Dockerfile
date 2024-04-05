FROM golang:1.20-alpine AS builder

WORKDIR /app
RUN apk add git && git clone https://github.com/bincooo/single-proxy.git .
RUN go mod tidy && GOOS=linux GOARCH=amd64 go build -ldflags "-s -w" -o server -trimpath



FROM ubuntu:latest

ENV GBP_USER ${GBP_USER:-gbp}
ENV GBP_USER_ID ${GBP_USER_ID:-1000}

WORKDIR /app

USER root

RUN apt update \
  && apt-get install -y curl unzip wget gnupg2 ca-certificates supervisor

# Install xcfb
RUN apt-get install -y --no-install-recommends xvfb xauth pulseaudio

# Install locales
RUN apt-get install -y --no-install-recommends language-pack-en tzdata locales && \
    locale-gen en_US.UTF-8

# Install fluxbox
RUN apt-get install -y --no-install-recommends fluxbox eterm hsetroot feh

# Install Edge
RUN wget -q -O - https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/microsoft.gpg >/dev/null \
    && echo "deb https://packages.microsoft.com/repos/edge stable main" >> /etc/apt/sources.list.d/microsoft-edge.list \
    && apt-get update -qqy \
    && apt-get -qqy --no-install-recommends install microsoft-edge-stable

RUN curl -s https://www.1micro.top/alist/d/coze-helper.zip -o coze-helper.zip && \
  unzip coze-helper.zip
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash \
  && apt-get install -y nodejs

RUN apt-get remove -y curl unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 


COPY --from=builder /app/server /app/server
COPY config.yaml /app/config.yaml
COPY goole-helper /app/goole-helper
COPY start-xvfb.sh /opt/bin/start-xvfb.sh
COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf

RUN groupadd -g $GBP_USER_ID $GBP_USER
RUN useradd -rm -G sudo -u $GBP_USER_ID -g $GBP_USER_ID $GBP_USER

RUN mkdir -p /tmp/edge /var/run/supervisor /var/log/supervisor
RUN chown "${GBP_USER_ID}:${GBP_USER_ID}" /var/run/supervisor /var/log/supervisor
RUN chown -R "${GBP_USER_ID}:${GBP_USER_ID}" /app /tmp/edge
RUN  chmod 777 /opt/bin/start-xvfb.sh \
  && chmod 777 /app/goole-helper \
  && chmod 777 /app/server \
  && chmod 777 /tmp

USER $GBP_USER

ENV SCREEN_WIDTH=1360
ENV SCREEN_HEIGHT=1020
ENV SCREEN_DEPTH=24
ENV SCREEN_DPI=96
ENV SE_START_XVFB=true
ENV DISPLAY=:99.0
ENV DISPLAY_NUM=99

ENV PORT=7860
ENV HEADLESS=false
ENV BROWSER_BINARY=/usr/bin/microsoft-edge
# ENV PASS_TIMEOUT=10
# ENV CHROME_PATH=/opt/google/chrome
ENV XDG_CONFIG_HOME=/tmp/edge
ENV XDG_CACHE_HOME=/tmp/edge

CMD /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisor.conf

WORKDIR /app/coze-helper
RUN sed -i 's/puppeteerArgs\.push/\/\/ puppeteerArgs\.push/g' src/index.ts
#RUN cat src/index.ts

RUN npm install
# CMD ["node", "run", "start"]