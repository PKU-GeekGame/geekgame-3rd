FROM python:3

# install libs

RUN apt-get update && apt-get install -y \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
    unzip xvfb

# install chrome

COPY vendor/google-chrome-stable_current_amd64.deb /usr/src/
RUN apt-get install /usr/src/google-chrome-stable_current_amd64.deb -y -f && \
    rm /usr/src/google-chrome-stable_current_amd64.deb

# copy chrome driver

COPY vendor/chromedriver /usr/bin/
RUN chmod +x /usr/bin/chromedriver

# install python requirements

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip3 install -r requirements.txt

# copy src

COPY flag.py ./
COPY logger.py ./
COPY xssbot.py ./
COPY 2023.pub ./

CMD ["python", "xssbot.py"]