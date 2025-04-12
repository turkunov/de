from pyspark.sql import SparkSession
from pyspark.sql import functions as F
from pyspark.sql.types import StructType, StructField, IntegerType, ArrayType
import time

# Initialize Spark
spark = SparkSession.builder \
    .appName("hobsparktask1_df") \
    .master("yarn") \
    .getOrCreate()

# Start CPU time measurement
start_cpu = time.clock()

# Define schema for the edges
edge_schema = StructType([
    StructField("user_id", IntegerType(), False),
    StructField("follower_id", IntegerType(), False)
])

# Load data from file
df = spark.read.csv("/data/twitter/twitter_sample.txt", sep="\t", schema=edge_schema)

# Create forward edges for BFS (follower -> user)
forward_edges = df.select(
    F.col("follower_id").alias("current"),
    F.col("user_id").alias("next")
)

# Initialize distances with start node
start_node = 12
target_node = 34
distances_schema = StructType([
    StructField("node", IntegerType(), False),
    StructField("distance", IntegerType(), False),
    StructField("path", ArrayType(IntegerType(), False), False)
])

# Initialize with start node, distance 0, and empty path
distances = spark.createDataFrame(
    [(start_node, 0, [])],
    schema=distances_schema
)

# BFS algorithm
d = 0
found = False

while not found:
    # Broadcast the current distance nodes to all workers
    spark.sparkContext.broadcast(distances.select("node").rdd.flatMap(lambda x: [x[0]]).collect())
    
    # Join distances with forward edges to find next level nodes
    next_level = distances.join(
        forward_edges,
        distances.node == forward_edges.current
    ).select(
        forward_edges.next.alias("node"),
        (distances.distance + 1).alias("distance"),
        F.concat(distances.path, F.array(distances.node)).alias("path")
    )
    
    # Add new distances to the collection
    new_distances = distances.unionByName(next_level).groupBy("node").agg(
        F.min("distance").alias("distance"),
        F.first("path").alias("path")
    )
    
    # Check if target node is found
    if new_distances.filter(F.col("node") == target_node).count() > 0:
        found = True
        result_path = new_distances.filter(F.col("node") == target_node).collect()[0]
        final_path = result_path.path + [target_node]
    else:
        distances = new_distances.filter(F.col("distance") > d)
        d += 1

cpu_time = time.clock() - start_cpu

result = ",".join(map(str, final_path))
# print(result)
with open("output.txt", "w") as f:
    f.write(result + "\n") # Add a newline for good measure
# print("CPU time: {}".format(cpu_time))

with open("df_cpu_time.txt", "w") as f:
    f.write(str(cpu_time))

spark.stop() 