FROM python:3.10-slim as build_stage
WORKDIR /app/
COPY . /app
RUN pip install --no-cache-dir -r  requirements.txt
EXPOSE 5000

CMD ["python3", "-m", "gunicorn", "--threads", "4", "--workers", "20"  "--bind", "0.0.0.0:5000", "webServer.app:app"]