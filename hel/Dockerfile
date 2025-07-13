FROM ubuntu:latest

WORKDIR /app
ADD helper helper
ADD config.yaml config.yaml

RUN apt update \
  && apt-get install -y curl unzip wget gnupg2

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

RUN chmod +x helper \
  && chmod -R 777 /app
  #&& mkdir log && chmod 777 log \
  #&& mkdir tmp && chmod 777 tmp

ENV ARG "--port 7860"
CMD ["./helper ${ARG}"]
ENTRYPOINT ["sh", "-c"]
