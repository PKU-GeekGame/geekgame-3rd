FROM sbtscala/scala-sbt:eclipse-temurin-focal-17.0.8.1_1_1.9.6_3.3.1
WORKDIR /wordle
ADD wordle /wordle
RUN sbt stage
ENV JAVA_OPTS="--add-opens java.base/java.lang=ALL-UNNAMED"
RUN echo play.http.secret.key=\"`cat /dev/random | head -n 100 | md5sum | cut -d ' ' -f 1`\" >> /wordle/conf/application.conf
EXPOSE 9000
CMD target/universal/stage/bin/wordle -Dconfig.file=/wordle/conf/application.conf
