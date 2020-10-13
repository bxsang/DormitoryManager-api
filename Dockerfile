FROM python:3.8.6-alpine3.12
# VOLUME [ "/app" ]
WORKDIR /app
# ADD . /app
COPY requirements.txt ./
RUN apk add --no-cache --virtual .build-deps \
        gcc libc-dev linux-headers \
    ; \
    pip install -r requirements.txt; \
    apk del .build-deps
EXPOSE 9000
CMD [ "uwsgi", "app.ini" ]
