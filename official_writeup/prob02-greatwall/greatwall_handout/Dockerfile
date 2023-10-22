FROM node:20-bookworm

RUN set -ex && \
    apt-get update && \
    apt-get install -y \
    supervisor \
    x11vnc xterm xvfb novnc openbox \
    libnss3 libasound2 libatk-adaptor libgtk-3-0 libgbm1
RUN apt-get install -y wget && \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \ 
    && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable

ENV HOME=/root \
    DEBIAN_FRONTEND=noninteractive \
    LANG=en_US.UTF-8 \
    LANGUAGE=en_US.UTF-8 \
    LC_ALL=C.UTF-8 \
    DISPLAY=:0.0 \
    DISPLAY_WIDTH=1024 \
    DISPLAY_HEIGHT=768

COPY app /app
COPY cfw-settings.yaml /home/node/.config/clash/cfw-settings.yaml
RUN cd /app && \
    gcc readflag.c -o readflag && \
    chown root:root readflag && \
    chmod +sx readflag && \
    chown -R node:node /home/node/.config
RUN cd /app/ui && npm i
COPY ./flags/flag_veryeasy /flag_0
COPY ./flags/flag_easy /flag_1
COPY ./flags/flag /flag_2
CMD ["/app/entrypoint.sh"]
EXPOSE 3030
