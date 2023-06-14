FROM python:3.10-slim as build_stage
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r  requirements.txt
COPY . /app

EXPOSE 5000

CMD ["python3", "-m", "gunicorn", "--threads", "4", "--workers", "20", "--bind", "0.0.0.0:5000", "webServer.app:app"]
