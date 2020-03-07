FROM marketplace_promotion
RUN mkdir /src/load
ADD . /src/load
RUN pip install locust Faker
WORKDIR /src/load
ENTRYPOINT ["/usr/local/bin/locust"]
CMD ["--help"]
