FROM marketplace_promotion
RUN apk add --no-cache libffi-dev
RUN mkdir /src/load
ADD . /src/load
RUN pip install locust
WORKDIR /src/load
ENTRYPOINT ["/usr/local/bin/locust"]
CMD ["--help"]
