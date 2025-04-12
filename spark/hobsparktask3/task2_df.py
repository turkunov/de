# -*- coding: utf-8 -*-

import re
from pyspark.sql import SparkSession
from pyspark.ml.feature import NGram
from pyspark.sql.functions import explode, split, col, sum as pysum, log, concat_ws
from pyspark.sql.types import StructType, StructField, StringType, ArrayType
from functools import partial

def process_article_line(line, stopwords):
    parts = re.split(r"\t|\s", line, maxsplit=2)
    if len(parts) < 3:
        return None
    cleaned = re.sub(r"[^a-zA-Z\s\d]+", "", parts[2].lower())
    token_list = cleaned.split()
    filtered = [w for w in token_list if w not in stopwords]
    parts[2] = filtered
    return parts

def filter_none(x):
    return x is not None

class ArticleNGramProcessor(object):
    def __init__(self, spark_master='yarn',
                 app_name='Spark DF Practice',
                 stopwords_path="/data/wiki/stop_words_en-xpo6.txt",
                 articles_path="/data/wiki/en_articles_part"):
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .master(spark_master) \
            .getOrCreate()
        self.stopwords_path = stopwords_path
        self.articles_path = articles_path
        self.article_schema = StructType([
            StructField("id", StringType(), True),
            StructField("title", StringType(), True),
            StructField("text", ArrayType(StringType()), True)
        ])
        self.stopwords = self.load_stopwords()

    def load_stopwords(self):
        return self.spark.sparkContext.textFile(self.stopwords_path).collect()

    def load_articles(self):
        process_func = partial(process_article_line, stopwords=self.stopwords)
        articles_rdd = self.spark.sparkContext.textFile(self.articles_path)
        articles_rdd = articles_rdd.map(process_func).filter(filter_none)
        articles_df = self.spark.createDataFrame(articles_rdd, schema=self.article_schema)
        return articles_df

    def process(self):
        articles_df = self.load_articles()

        bigram_transformer = NGram(n=2, inputCol="text", outputCol="bigrams")
        articles_with_bigrams = bigram_transformer.transform(articles_df)

        bigram_exploded = articles_with_bigrams.select(explode("bigrams").alias("bigram"))
        bigram_counts = bigram_exploded.groupBy("bigram").count()
        total_bigram = bigram_counts.select(pysum("count").alias("total")).collect()[0]["total"]

        frequent_bigrams = bigram_counts.filter(col("count") >= 500).orderBy(col("count").desc())

        unique_words = frequent_bigrams.select(explode(split(col("bigram"), " ")).alias("word")).distinct()

        unigram_transformer = NGram(n=1, inputCol="text", outputCol="words")
        articles_with_unigrams = unigram_transformer.transform(articles_df)
        unigram_counts = articles_with_unigrams.select(explode("words").alias("word")).groupBy("word").count() \
            .join(unique_words, "word")
        total_unigram = unigram_counts.select(pysum("count").alias("total")).collect()[0]["total"]

        split_bigrams = frequent_bigrams.select(
            split(col("bigram"), " ").alias("parts"),
            col("count").alias("bi_count")
        ).select(
            col("parts").getItem(0).alias("word1"),
            col("parts").getItem(1).alias("word2"),
            col("bi_count")
        )

        join_first = split_bigrams.join(unigram_counts, split_bigrams.word1 == unigram_counts.word) \
            .select(split_bigrams.word1, split_bigrams.word2, split_bigrams.bi_count,
                    unigram_counts["count"].alias("w1_count"))

        join_second = join_first.join(unigram_counts, join_first.word2 == unigram_counts.word) \
            .select(
                concat_ws("_", join_first.word1, join_first.word2).alias("collocation"),
                join_first.bi_count,
                join_first.w1_count,
                unigram_counts["count"].alias("w2_count")
            )

        npmi_expr = (-log((col("bi_count") * total_unigram ** 2) /
                            (col("w1_count") * col("w2_count") * total_bigram))) / log(col("bi_count") / total_bigram)

        result_df = join_second.select("collocation", npmi_expr.alias("npmi")) \
            .orderBy(col("npmi").desc()) \
            .limit(39)

        collocations = result_df.select("collocation").rdd.flatMap(lambda row: row).collect()
        for coll in collocations:
            print(coll)

    def stop(self):
        self.spark.stop()

def main():
    processor = ArticleNGramProcessor()
    processor.process()
    processor.stop()

if __name__ == "__main__":
    main()
