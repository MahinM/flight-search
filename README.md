# Flight Route Search
## Finding your way from point Z to A

### Overview

[Slide deck](http://u2bread.com/slides)

This project deals with finding flights between a given source and destination in the face of realtime changes to pricing and availability.

#### Data
  * Bureau of Transportation Statistics flight data (rolled foward to represent future data)
  * Streaming inputs to represent:
    * flights viewed
    * seat purchased
    * price changed

#### Pipeline

Python programs stream events and write them to Kafka topics.  The event messages are consumed by spark streaming jobs which update the appropriate key-value pairs in a redis data store.

This code was run on AWS servers.

### Install

The install scripts rely on [pegasus](https://github.com/InsightDataScience/pegasus) to be installed on the client.

Note: Redis is insecure by design and requires firewall protection.  In my implementation, it's installed on a dedicated instance with access permitted only from the webserver and the spark cluster.


### Source

The producer is a python program that writes to a kafka message topic.

The kafka connector can be installed using:
`pip install kafka-python`
The producer can be executed using:
`python python_kafka_flight_purchased.py <kafka broker ip>`

The consumer is a Spark program implemented in pyspark.  
It can be run as:
`spark-submit --master spark://<hostname>:7077 --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.0.0 pyspark_kafka_redis.py <zookeeper> <topic>`

The frontend is based on Flask and requests updates from Redis.


