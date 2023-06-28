repository = 127.0.0.1:3500
build:
	@sudo docker image build -t ${repository}/videoserverapp 	Src/VideoServerApp/
	@sudo docker image build -t ${repository}/webserverapp 		Src/WebServerApp/ 
push:
	@sudo docker push ${repository}/videoserverapp
	@sudo docker push ${repository}/webserverapp
	@sudo docker push ${repository}/loadbalancerapp

runwebserver:
	@cd Src/WebServerApp && \
	python3 -m WebServer

runcameraserver:
	@cd Src/CameraServerApp && \
	export RESOURCE='video3.mp4' && \
	export CAMERA_NAME='camera1' && \
	python3 -m CameraServer

runvideoserver:
	@cd Src/VideoServerApp && \
	python3 -m VideoServer

runaiserver:
	@cd Src/AiServerApp && \
	python3 -m AiServer

stackdeploy:
	docker stack deploy --compose-file docker-compose.yml demo
rmstack:
	docker stack rm demo