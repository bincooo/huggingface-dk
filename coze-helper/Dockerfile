FROM ubuntu:latest

WORKDIR /app

RUN apt update \
  && apt-get install -y curl unzip wget gnupg2 ca-certificates supervisor

ENV GBP_USER ${GBP_USER:-gbp}
ENV GBP_USER_ID ${GBP_USER_ID:-1000}
USER root


ADD launch.sh ./launch.sh
RUN chmod 777 /app && chmod 777 /app/launch.sh

RUN wget -q -O - https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor | tee /etc/apt/trusted.gpg.d/microsoft.gpg >/dev/null \
    && echo "deb https://packages.microsoft.com/repos/edge stable main" >> /etc/apt/sources.list.d/microsoft-edge.list \
    && apt-get update -qqy \
    && apt-get -qqy --no-install-recommends install microsoft-edge-stable

RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash \
  && apt-get install -y nodejs
RUN apt-get clean && rm -rf /var/lib/apt/lists/* 

CMD /app/launch.sh