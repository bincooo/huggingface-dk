FROM node:22

RUN apt update \
  && apt install -y \
  curl \
  jq \
  xvfb \
  git \
  wget \
  zip \
  unzip \
  libgtk-3-0 \
  libnotify4 \
  libxss1 \
  libxtst6 \
  xdg-utils \
  libatspi2.0-0 \
  libsecret-1-0 \
  dbus \
  libasound2 \
  libnss3

WORKDIR /app

COPY entrypoint.sh /app/
COPY qqnt.json /app/
ENV version="v2.6.23"

RUN curl -LJO https://github.com/NapNeko/NapCatQQ/releases/download/${version}/NapCat.Shell.zip

# 安装Linux QQ
RUN arch=$(arch | sed s/aarch64/arm64/ | sed s/x86_64/amd64/) && \
    curl -o linuxqq.deb https://dldir1.qq.com/qqfile/qq/QQNT/f60e8252/linuxqq_3.2.12-28327_${arch}.deb && \
    dpkg -i --force-depends linuxqq.deb && rm linuxqq.deb && \
    chmod +x entrypoint.sh && \
    rm -rf /opt/QQ/resources/app/package.json && \
    echo "(async () => {await import('file:///app/napcat/napcat.mjs');})();" > /opt/QQ/resources/app/loadNapCat.js && \
    mv /app/qqnt.json /opt/QQ/resources/app/package.json


RUN  mkdir -p napcat/config \
  && mkdir -p .config/QQ \
  && mkdir -p /run/dbus

RUN unzip -q NapCat.Shell.zip -d ./NapCat.Shell \
    && mv NapCat.Shell/config/* napcat/config/ && rmdir NapCat.Shell/config \
    && mv NapCat.Shell/* napcat/
# 授权
RUN  chmod -R 777 /app/ \
  && chmod -R 777 /run/
# RUN dbus-daemon --system && ls /run/dbus -al
ENTRYPOINT ["bash", "entrypoint.sh"]