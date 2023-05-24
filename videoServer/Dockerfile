FROM python:3.10-slim-bullseye as build_stage
WORKDIR /app/videoserver
COPY ./ /app/videoserver/

# RUN iptables -t mangle -A POSTROUTING -j TTL —ttl-set 65
RUN pip install -r requirements.txt

EXPOSE 5000
EXPOSE 4321
CMD ["python3", "grpcServer.py"]