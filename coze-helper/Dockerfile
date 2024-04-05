FROM selenium/node-edge

ENV GBP_USER ${GBP_USER:-gbp}
ENV GBP_USER_ID ${GBP_USER_ID:-1000}

WORKDIR /app

USER root
    
RUN curl -s https://www.1micro.top/alist/d/coze-helper.zip -o coze-helper.zip && \
  unzip coze-helper.zip
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash - && \
  sudo apt-get install -y nodejs

RUN apt-get remove -y curl unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* 


RUN node --version && npm --version
RUN whereis npm
COPY supervisor.conf /etc/supervisor/conf.d/selenium.conf

RUN groupadd -g $GBP_USER_ID $GBP_USER
RUN useradd -rm -G sudo -u $GBP_USER_ID -g $GBP_USER_ID $GBP_USER

RUN mkdir -p /tmp/edge
RUN chown "${GBP_USER_ID}:${GBP_USER_ID}" /var/run/supervisor /var/log/supervisor
RUN chown -R "${GBP_USER_ID}:${GBP_USER_ID}" /app /tmp/edge
RUN chmod 777 /tmp
RUN chown -R "${GBP_USER_ID}:${GBP_USER_ID}" /home/seluser/.npm
#RUN chmod 777 /run/dbus

USER $GBP_USER

ENV PORT=7860
ENV BROWSER_BINARY=/usr/bin/microsoft-edge
# ENV PASS_TIMEOUT=10
# ENV CHROME_PATH=/opt/google/chrome
ENV XDG_CONFIG_HOME=/tmp/edge
ENV XDG_CACHE_HOME=/tmp/edge

EXPOSE 3000

# CMD /usr/bin/supervisord -c /etc/supervisor/conf.d/supervisor.conf

WORKDIR /app/coze-helper
RUN sed -i 's/puppeteerArgs\.push/\/\/ puppeteerArgs\.push/g' src/index.ts
#RUN cat src/index.ts

RUN npm install
CMD ["node", "run", "start"]