FROM ubuntu

RUN apt update &&\
    apt install -y pkg-config libgtk-3-dev &&\
    apt install -y ffmpeg libavformat-dev libavcodec-dev libswscale-dev &&\
    apt install -y default-jre

WORKDIR /app
COPY . /app

WORKDIR /app/cameraserver

CMD ["java", "-jar", "./out/artifacts/cameraserver_jar/cameraserver.jar"]