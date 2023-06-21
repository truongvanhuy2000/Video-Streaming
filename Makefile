repository = 127.0.0.1:3500
build:
	@sudo docker image build -t ${repository}/videoserverapp 	VideoServerApp/
	@sudo docker image build -t ${repository}/webserverapp 		WebServerApp/ 
push:
	@sudo docker push ${repository}/videoserverapp
	@sudo docker push ${repository}/webserverapp
	@sudo docker push ${repository}/loadbalancerapp

runwebserver:
	@cd WebServerApp && \
	export TRANSPORT_METHOD=GRPC && \
	export LOAD_BALANCER_PORT=7654 && \
	python3 -m webServer

runcameraserver:
	@cd CameraServerApp && \
	export RESOURCE_DIR='cameraServer/resources/video1.mp4' && \
	export CAMERA_NAME='camera1' && \
	export RABBITMQ_HOST='localhost' && \
	python3 -m cameraServer

runvideoserver:
	@cd VideoServerApp && \
	export RESOURCE_DIR=/home/huy/Videos/ && \
	export TRANSPORT_METHOD=GRPC && \
	python3 -m videoServer

stackdeploy:
	docker stack deploy --compose-file docker-compose.yml demo
rmstack:
	docker stack rm demo