FROM debezium/kafka AS base

WORKDIR /app
COPY ./src .
RUN pip install kafka-python requests