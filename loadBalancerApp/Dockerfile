FROM python:3.10-slim as build_stage
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r  requirements.txt
COPY . /app

CMD ["python3", "-m", "loadBalancer"]