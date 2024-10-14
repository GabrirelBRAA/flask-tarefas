FROM python:3.12-alpine
LABEL maintaner="joaogabriel"

ENV PYTHONBUFFERED 1

COPY ./requirements.txt /tmp/requirements.txt
COPY ./app /app 
RUN chmod +x /app/run.sh
WORKDIR /app
EXPOSE 5000

RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client openssl && \
    apk add --update --no-cache --virtual .tmp-build-deps \
                 build-base postgresql-dev musl-dev linux-headers && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser \
            --disabled-password \
            --no-create-home \
            flask-user && \
    chmod +x ./run.sh

ENV PATH="/py/bin:$PATH"

USER root

CMD ["./run.sh"]