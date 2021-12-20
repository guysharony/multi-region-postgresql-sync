# Postgresql replication using Apache Kafka


## Creating a connector
File name: postgres-source.json
``` json
{
    "name": "source-connector",
    "config": {
        "connector.class": "io.debezium.connector.postgresql.PostgresConnector",
        "tasks.max": "1",
        "plugin.name": "wal2json",
        "database.hostname": "192.168.2.1",
        "database.port": "4042",
        "database.user": "source_user",
        "database.password": "password_source",
        "database.dbname": "source",
        "database.server.name": "SOURCE",
        "key.converter": "org.apache.kafka.connect.json.JsonConverter",
        "value.converter": "org.apache.kafka.connect.json.JsonConverter",
        "key.converter.schemas.enable": "false",
        "value.converter.schemas.enable": "false",
        "snapshot.mode": "always"
    }
}
```

Sending request connector data to connector:
``` bash
curl -i -X POST -H "Accept:application/json" -H "Content-Type:application/json" <CONNECT URL>/connectors/ --data @postgres-source.json
```


## Reading topics from kafka
Reading topics from kafka:
``` bash
docker exec -it <KAFKA CONTAINER ID> /kafka/bin/kafka-console-consumer.sh --bootstrap-server <KAFKA URL> --topic SOURCE.bank.holding | grep --line-buffered '^{'
```

Redirecting to stream parser
``` bash
docker exec -it <KAFKA CONTAINER ID> /kafka/bin/kafka-console-consumer.sh --bootstrap-server <KAFKA URL> --topic SOURCE.bank.holding | grep --line-buffered '^{' | ./stream.py
```