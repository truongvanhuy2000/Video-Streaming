FROM python:3.10-slim as build_stage
WORKDIR /app/
COPY . /app
RUN pip install --no-cache-dir -r requirements.txt
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]