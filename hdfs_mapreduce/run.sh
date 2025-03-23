#! /usr/bin/env bash

OUT_DIR="wordcount_result"
NUM_REDUCERS=6
TEXT_DIR="/data/minecraft-server-logs/*"
NUM_DAYS="$(hadoop fs -ls /data/minecraft-server-logs/ | grep -E ".*-1\.log$" | wc -l)"

hdfs dfs -rm -r -skipTrash ${OUT_DIR} > /dev/null

yarn jar /usr/lib/hadoop/hadoop-streaming.jar \
    -D mapreduce.job.reduces=${NUM_REDUCERS} \
    -D mapreduce.job.name="mc-logs-counter" \
    -files mapper.py,reducer.py \
    -mapper "python3 mapper.py" \
    -reducer "python3 reducer.py --numdays=$NUM_DAYS" \
    -input ${TEXT_DIR} \
    -output ${OUT_DIR} > /dev/null

# hdfs dfs -ls ${OUT_DIR}
hdfs dfs -cat ${OUT_DIR}/part-0000* | sort -k2,2nr | head -n 10
