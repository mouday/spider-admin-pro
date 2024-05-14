FROM python:3.7.15-alpine3.16

ADD . /app

WORKDIR /app

RUN apk add --no-cache --virtual .build-deps gcc musl-dev libffi-dev openssl-dev bash\
    && apk add --no-cache libffi openssl \
    && pip install --no-cache-dir --upgrade pip setuptools wheel\
    && pip install --no-cache-dir -r requirements.txt \
    && apk del .build-deps

CMD gunicorn --bind '0.0.0.0:8000' 'spider_admin_pro:app'
