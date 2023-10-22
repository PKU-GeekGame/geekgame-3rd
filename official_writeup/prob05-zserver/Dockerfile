FROM ubuntu:22.04
RUN apt update && apt install -y lrzsz
WORKDIR /
COPY flag.txt /
CMD sz flag.txt