import argparse

from pyspark.sql import SparkSession
from pyspark.sql import types
from pyspark.sql import functions as F

parser = argparse.ArgumentParser()

parser.add_argument('--input_file', required=True)
parser.add_argument('--general_activity', required=True)
parser.add_argument('--active_users', required=True)

args = parser.parse_args()

input_file = args.input_file
general_activity = args.general_activity
active_users = args.active_users

spark = SparkSession.builder \
    .appName('test') \
    .getOrCreate()

spark.conf.set('temporaryGcsBucket', 'dataproc-temp-europe-west6-480347133231-noyhb2ch')

schema = types.StructType([
    types.StructField('actor',types.StructType([
        types.StructField('avatar_url',types.StringType(),True),
        types.StructField('display_login',types.StringType(),True),
        types.StructField('gravatar_id',types.StringType(),True),
        types.StructField('id',types.IntegerType(),True),
        types.StructField('login',types.StringType(),True),
        types.StructField('url',types.StringType(),True)]),
    True),
    types.StructField('created_at',types.TimestampType(),True),
    types.StructField('id',types.StringType(),True),
    types.StructField('org',types.StructType([
        types.StructField('avatar_url',types.StringType(),True),
        types.StructField('gravatar_id',types.StringType(),True),
        types.StructField('id',types.IntegerType(),True),
        types.StructField('login',types.StringType(),True),
        types.StructField('url',types.StringType(),True)]),
    True),
    types.StructField('payload', types.MapType(types.StringType(), types.StringType()), True),
    types.StructField('public',types.BooleanType(),True),
    types.StructField('repo',types.StructType([
        types.StructField('id',types.IntegerType(),True),
        types.StructField('name',types.StringType(),True),
        types.StructField('url',types.StringType(),True)]),
    True),
    types.StructField('type',types.StringType(),True)
])

df = spark.read \
    .schema(schema) \
    .json(input_file)

def get_day(timestamp):
    return timestamp.strftime('%Y-%m-%d')

def get_weekday(timestamp):
    return timestamp.strftime('%A')

weekday = F.udf(get_weekday)
day = F.udf(get_day)

gen_activity_df = df \
    .select("created_at", "type", "actor", "repo") \
    .withColumnRenamed('type', "event_type") \
    .withColumnRenamed('actor', 'user') \
    .withColumn('day', day(df.created_at)) \
    .withColumn('hour', F.hour(df.created_at)) \
    .withColumn('weekday', weekday(df.created_at))

gen_activity_df.createOrReplaceTempView('gen_activity')

active_users_df = spark.sql("""
SELECT
    CAST (day AS DATE),
    user.id AS user_id,
    user.login AS username,
    user.avatar_url AS avatar_url,
    event_type,
    count(1) AS count
FROM gen_activity
GROUP BY day, user_id, username, avatar_url, event_type
ORDER BY count DESC
"""
)

gen_activity_df.write.format('bigquery') \
    .mode('append') \
    .option('table', general_activity) \
    .save()

active_users_df.write.format('bigquery') \
    .mode('append') \
    .option('table', active_users) \
    .save()