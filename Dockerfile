FROM argvc/pipenv-alpine-python2

WORKDIR /app/src
USER root

ADD Pipfile /app/src
ADD Pipfile.lock /app/src
ADD Makefile /app/src

RUN make deps

ADD . /app/src

ENTRYPOINT ["switch", "test=make test", "run=make run", "--", "sh"]
