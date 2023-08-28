FROM python:3.10-slim
WORKDIR /usr/src/Powerflex-Sprocket-API
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY . ./
ENV PORT 8000
EXPOSE $PORT
CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT