FROM openjdk:11

RUN apt update &&\
    apt install -y pkg-config &&\
    apt install -y ffmpeg libavformat-dev libavcodec-dev libswscale-dev 

WORKDIR /app
COPY . /app

WORKDIR /app/cameraserver

CMD ["java", "-jar", "./out/artifacts/cameraserver_jar/cameraserver.jar"]