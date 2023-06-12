repository = 127.0.0.1:3500
build:
	@sudo docker image build -t ${repository}/videoserverapp 	videoServerApp/
	@sudo docker image build -t ${repository}/webserverapp 		webServerApp/ 
	@sudo docker image build -t ${repository}/loadbalancerapp 	loadBalancerApp/
push:
	@sudo docker push ${repository}/videoserverapp
	@sudo docker push ${repository}/webserverapp
	@sudo docker push ${repository}/loadbalancerapp

runwebserver:
	@cd webServerApp && \
	export TRANSPORT_METHOD=GRPC && \
	export LOAD_BALANCER_PORT=7654 && \
	python3 -m webServer
	
runvideoserver:
	@cd videoServerApp && \
	export RESOURCE_DIR=/home/huy/Videos/ && \
	export TRANSPORT_METHOD=GRPC && \
	python3 -m videoServer

runloadbalancer:
	@cd loadBalancerApp && \
	export DOCKER_DAEMON=192.168.56.20:2375 && \
	export BALANCING_ALGORITHM=roundRobin && \
	export PORT=7654 && \
	python3 -m loadBalancer