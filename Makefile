repository = 127.0.0.1:3500
build:
	@sudo docker image build -t ${repository}/videoserverapp 	videoServerApp/
	@sudo docker image build -t ${repository}/webserverapp 		webServerApp/ 
push:
	@sudo docker push ${repository}/videoserverapp
	@sudo docker push ${repository}/webserverapp

runwebserver:
	@cd webServerApp && \
	export GRPC_SERVER1=0.0.0.0:9876 && \
	export GRPC_SERVER2=0.0.0.0:9876 && \
	export GRPC_SERVER3=0.0.0.0:9876 && \
	export GRPC_SERVER4=0.0.0.0:9876 && \
	export TRANSPORT_METHOD=GRPC && \
	python3 -m webServer

gunicornWebServer:
	@cd webServerApp && \
	export GRPC_SERVER1=0.0.0.0:9876 && \
	export GRPC_SERVER2=0.0.0.0:9876 && \
	export GRPC_SERVER3=0.0.0.0:9876 && \
	export GRPC_SERVER4=0.0.0.0:9876 && \
	export TRANSPORT_METHOD=GRPC && \
	gunicorn --workers 10 --threads 4 --bind 0.0.0.0:5000 webServer.app:app
	
runvideoserver:
	@cd videoServerApp && \
	export RESOURCE_DIR=/home/huy/Videos/ && \
	export TRANSPORT_METHOD=GRPC && \
	python3 -m videoServer

stackdeploy:
	docker stack deploy --compose-file docker-compose.yml demo
rmstack:
	docker stack rm demo