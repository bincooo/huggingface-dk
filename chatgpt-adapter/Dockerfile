FROM golang:1.21-alpine AS builder

WORKDIR /app
RUN apk add git make && git clone https://github.com/bincooo/chatgpt-adapter.git .
RUN make build-linux

FROM ubuntu:latest

WORKDIR /app
COPY --from=builder /app/bin/linux/server ./server
COPY --from=builder /app/you-helper.zip ./you-helper.zip

RUN apt update \
  && apt-get install -y curl unzip wget gnupg2 ca-certificates supervisor

ENV GBP_USER ${GBP_USER:-gbp}
ENV GBP_USER_ID ${GBP_USER_ID:-1000}
USER root

COPY supervisor.conf /etc/supervisor/conf.d/supervisor.conf
RUN mkdir -p /var/run/supervisor /var/log/supervisor
RUN chown "${GBP_USER_ID}:${GBP_USER_ID}" /var/run/supervisor /var/log/supervisor

# Install google
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
  && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
  && apt-get update \
  && apt-get install -y google-chrome-stable

# Install Edge
#RUN wget -q -O - https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/microsoft.gpg >/dev/null \
#    && echo "deb https://packages.microsoft.com/repos/edge stable main" >> /etc/apt/sources.list.d/microsoft-edge.list \
#    && apt-get update -qqy \
#    && apt-get -qqy --no-install-recommends install microsoft-edge-stable

ADD server .
ADD config.yaml .
RUN unzip ./you-helper.zip \
  && mkdir log \
  && mkdir tmp \
  && chmod +x server \
  && chmod +x bin/linux/helper \
  && chmod 777 tmp \
  && chmod 777 log

# ENV ARG "--port 7860 --log debug"
# CMD ["./server ${ARG}"]
# ENTRYPOINT ["sh", "-c"]

CMD /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisor.conf