#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pyspark import SparkContext, SparkConf
import time
import os

# Setup Spark
config = SparkConf().setAppName("hobsparktask1_rdd").setMaster("yarn") 
sc = SparkContext(conf=config)
#sc.setLogLevel("ERROR")

def parse_edge(s):
    user, follower = s.split("\t")
    return (int(user), int(follower))

def step(item):
    prev_v, prev_d, next_v, array = item[0], item[1][0][0], item[1][1], item[1][0][1]
    return (next_v, (prev_d + 1, array + [prev_v]))

def complete(item):
    v, old_d, new_d = item[0], item[1][0], item[1][1]
    return (v, old_d if old_d is not None else new_d)

# Start CPU time measurement
start_cpu = time.clock()

n = 20  # number of partitions
edges = sc.textFile("/data/twitter/twitter_sample.txt").map(parse_edge)
forward_edges = edges.map(lambda e: (e[1], e[0])).partitionBy(n).persist()

x = 12  # Start vertex
target = 34  # Target vertex
d = 0  # Initial distance
distances = sc.parallelize([(x, (d, []))]).partitionBy(n)

while True:
    candidates = distances.join(forward_edges, n).map(step)
    
    keys = distances.keys().collect()
    
    # Optimization: filter edges to reduce join data size
    forward_edges = forward_edges.filter(lambda i: i[0] not in keys and i[1] not in keys)
    
    new_distances = distances.fullOuterJoin(candidates, n).map(complete, True).persist()
    
    # Check if we found path to target
    count = new_distances.filter(lambda i: i[0] == target).count()
    
    if count == 0:
        distances = new_distances.filter(lambda i: i[1][0] > d - 1)
        d += 1
    else:
        break

# Reconstruct path and add target vertex
path = new_distances.filter(lambda i: i[0] == target).take(1)[0][1][1] + [target]

cpu_time = time.clock() - start_cpu

result = ",".join(map(str, path))
# print(result)
with open("output.txt", "w") as f:
    f.write(result + "\n") # Add a newline for good measure
# print("CPU time: {}".format(cpu_time))

with open(os.path.join(os.path.dirname(__file__), "rdd_cpu_time.txt"), "w") as f:
    f.write(str(cpu_time))

sc.stop() 