#!/bin/bash

#spark-submit --master yarn-cluster --conf spark.shuffle.service.enabled=true --conf spark.dynamicAllocation.enabled=true docker.py
spark-submit --master yarn-cluster --num-executors 10 --executor-memory 1g --driver-memory 1g docker-sample.py
