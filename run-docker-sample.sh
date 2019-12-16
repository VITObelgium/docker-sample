#!/bin/bash

# This job will run on spark2 with python 3
# It can also be run on spark1 (python 2 will also work)

export SPARK_MAJOR_VERSION=2
export SPARK_HOME=/usr/hdp/current/spark2-client
export PYSPARK_PYTHON="/usr/bin/python3.5"
spark-submit --master yarn --deploy-mode cluster \
--executor-memory 1g \
--driver-memory 1g \
--conf spark.shuffle.service.enabled=true --conf spark.dynamicAllocation.enabled=true \
--conf spark.yarn.appMasterEnv.PYSPARK_DRIVER_PYTHON=/usr/bin/python3.5 --conf spark.executorEnv.PYSPARK_PYTHON=/usr/bin/python3.5 \
--conf spark.yarn.appMasterEnv.SPARK_HOME=/usr/hdp/current/spark2-client \
docker-sample.py


