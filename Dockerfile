FROM python:3.8-slim
 
WORKDIR /app
COPY ./src /app
 
RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8000