FROM alpine:latest

RUN apk add --no-cache python3-dev \
  && apk add build-base \
  && apk add libffi-dev \
  && apk add openssl-dev \
  && pip3 install --upgrade pip

WORKDIR /usr/src/app

COPY . .

RUN pip3 --no-cache-dir install -r requirements.txt

EXPOSE 3000

ENTRYPOINT [ "python3" ]

CMD [ "app.py" ]
