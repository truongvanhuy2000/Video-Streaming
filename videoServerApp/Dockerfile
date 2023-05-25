FROM python:3.10-slim as build_stage
WORKDIR /app/
COPY . .
RUN pip install -r requirements.txt
EXPOSE 9876

CMD ["python3", "-m", "videoServer"]