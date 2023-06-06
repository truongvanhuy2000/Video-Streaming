FROM python:3.10-slim as build_stage
WORKDIR /app/

COPY . .

RUN pip install -r requirements.txt

CMD ["python3", "-m", "loadBalancer"]