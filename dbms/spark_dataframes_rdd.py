from pyspark.sql import SparkSession
import pyspark.sql.functions as fc

# Initialize Spark session
spark = SparkSession.builder \
    .appName("CoffeeShopSalesAnalysis") \
    .getOrCreate()

# Load the CSV file into a DataFrame
sales = spark.read.csv('coffee_shop_sales_2023.csv', header=True, inferSchema=True)

# 1.
# select distinct product_category
# from sales
# where store_location = "Lower Manhattan" and unit_price >= 5

sales.filter((sales.store_location == "Lower Manhattan") & (sales.unit_price >= 5)).select("product_category").distinct().show()

# 2
# select product_category, count(*) cnt
# from sales
# where product_detail like "%chocolate%"
# group by product_category

sales.filter(sales.product_detail.like("%chocolate%")).groupby("product_category").agg(fc.count("*").alias("cnt")).show()

# 3
# select store_location, sum(transaction_qty * unit_price) total_sales
# from sales
# where product_category = "Coffee"
# group by store_location
# having count(*) >= 20000

sales.filter(sales.product_category == "Coffee") \
    .groupBy("store_location") \
    .agg(fc.sum(sales.transaction_qty * sales.unit_price).alias("total_sales")) \
    .filter(fc.count("*") >= 20000).show()

# 4
# select product_category, avg(transaction_qty * unit_price) avg
# from sales
# where store_location = "Lower Manhattan"
# group by product_category
# having count(*) > 10000
# order by avg desc
# limit 1

sales.filter(sales.store_location == "Lower Manhattan") \
     .groupBy("product_category") \
     .agg(fc.avg(sales.transaction_qty * sales.unit_price).alias("avg")) \
     .filter(fc.count("*") > 10000) \
     .orderBy(fc.desc("avg")).limit(1).show()


# RDD
rdd = sales.rdd

# 1
distinct_categories = rdd.filter(lambda row: row.store_location == "Lower Manhattan" and row.unit_price >= 5) \
                         .map(lambda row: row.product_category).distinct().collect()
print(distinct_categories)

# 2
chocolate_counts = rdd.map(lambda x: (x.product_category, x.product_detail)) \
                    .filter(lambda x: "chocolate" in x[1]) \
                    .map(lambda x: (x[0], 1)) \
                    .reduceByKey(lambda x, y: x + y).collect()
print(chocolate_counts)

# 3
coffee_sales = rdd.filter(lambda x: x.product_category == "Coffee") \
    .map(lambda x: (x.store_location, (x.transaction_qty * x.unit_price, 1))) \
    .reduceByKey(lambda x, y: (x[0] + y[0], x[1] + y[1])) \
    .filter(lambda x: x[1][1] >= 20000) \
    .map(lambda x: (x[0], x[1][0])).collect()
print(coffee_sales)

# 4
lower_manhattan_sales = rdd.filter(lambda x: x.store_location == "Lower Manhattan") \
    .map(lambda x: (x.product_category, (x.transaction_qty * x.unit_price, 1))) \
    .reduceByKey(lambda x, y: (x[0] + y[0],  x[1] + y[1])) \
    .filter(lambda x: x[1][1] > 10000) \
    .map(lambda x: (x[0], x[1][0] / x[1][1])) \
    .sortBy(lambda x: x[1], ascending=False) \
    .take(1)
print(lower_manhattan_sales)

