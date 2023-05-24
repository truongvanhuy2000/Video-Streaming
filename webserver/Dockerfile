FROM python:3.10-slim-bullseye as build_stage
WORKDIR /app/webserver
COPY ./ /app/webserver/

RUN pip install -r requirements.txt

EXPOSE 5000

CMD ["python3", "server.py"]