#!/bin/bash

#spark-submit --master yarn-cluster --conf spark.shuffle.service.enabled=true --conf spark.dynamicAllocation.enabled=true --executor-memory 1g --driver-memory 1g docker.py
#spark-submit --master yarn-cluster --num-executors 10 --executor-memory 1g --driver-memory 1g docker-sample.py


export SPARK_MAJOR_VERSION=2
export SPARK_HOME=/usr/hdp/current/spark2-client
export PYSPARK_PYTHON="/usr/bin/python3.5"
spark-submit --master yarn-cluster \
--executor-memory 1g \
--driver-memory 1g \
--conf spark.shuffle.service.enabled=true --conf spark.dynamicAllocation.enabled=true \
--conf spark.yarn.appMasterEnv.SPARK_HOME=/usr/hdp/current/spark2-client \
--conf spark.yarn.appMasterEnv.PYSPARK_DRIVER_PYTHON=/usr/bin/python3.5 --conf spark.executorEnv.PYSPARK_PYTHON=/usr/bin/python3.5 \
docker-sample.py


