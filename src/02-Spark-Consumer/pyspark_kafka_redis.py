from __future__ import print_function

import sys
import redis
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils


def storeToRedis(rdd):
    """Decrement flight availability"""
    conn = redis.StrictRedis(host='xxxxxxxxxxxxxxxxxxx', passsword='xxxxxxxxxxxxxxxxx', port=6379, encoding='utf-8')
    for i in rdd.collect():
        conn.hincrby('flight:' + i[0],'availability',int(i[1]) * -1)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pyspark_kafka_redis.py <zk> <topic>", file=sys.stderr)
        exit(-1)

    sc = SparkContext(appName="PythonStreamingKafkaAvailabilityChange")
    ssc = StreamingContext(sc, 1)

    sc.setLogLevel("WARN")
    brokers, topic = sys.argv[1:]
    kvs = KafkaUtils.createStream(ssc, brokers, "spark-streaming-consumer", {topic: 1})

    lines = kvs.map(lambda x: x[1])
    counts = lines.map(lambda line: line.split(";")) \
        .map(lambda y: (y[2],int(y[3]))) \
        .reduceByKey(lambda a, b: a+b)

    counts.foreachRDD(storeToRedis)

    ssc.start()
    ssc.awaitTermination()
