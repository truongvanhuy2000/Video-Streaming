FROM python:3.10-slim as build_stage
WORKDIR /app/
COPY . .
RUN apt update\
    && apt install -y nfs-common\
    && pip install -r requirements.txt\
    && chmod +x entrypoint.sh

ENTRYPOINT ["/app/entrypoint.sh"]