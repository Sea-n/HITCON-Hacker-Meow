FROM python:3.9-alpine

WORKDIR /app

COPY requirements.txt ./

RUN apk add build-base git

RUN pip install --no-cache-dir -r requirements.txt

VOLUME /app

CMD [ "python", "main.py" ]