#!/bin/bash

PEG_ROOT=~/Documents/Training/data_engineering/pegasus

CLUSTER_NAME=spark-cluster

peg up ${PEG_ROOT}/examples/spark/master.yml &
peg up ${PEG_ROOT}/examples/spark/workers.yml &

wait

peg fetch $CLUSTER_NAME

peg install ${CLUSTER_NAME} ssh
peg install ${CLUSTER_NAME} aws
peg install ${CLUSTER_NAME} hadoop
peg install ${CLUSTER_NAME} spark

peg install ${CLUSTER_NAME} zookeeper
peg install ${CLUSTER_NAME} kafka

peg install ${CLUSTER_NAME} kafka-manager


peg service ${CLUSTER_NAME} zookeeper start
peg service ${CLUSTER_NAME} spark start
peg service ${CLUSTER_NAME} kafka start
peg service ${CLUSTER_NAME} kafka-manager start
