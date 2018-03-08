FROM argvc/pipenv-alpine-python2

USER root
RUN apk add --update --no-cache g++ gcc libxslt-dev
WORKDIR /app/src

ADD Pipfile /app/src
ADD Pipfile.lock /app/src
ADD Makefile /app/src

RUN make deps

ADD . /app/src

ENTRYPOINT ["switch", "test=make test", "run=make run", "--", "sh"]
