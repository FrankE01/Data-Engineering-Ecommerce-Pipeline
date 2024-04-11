from pyspark.sql import SparkSession, functions
from urllib.parse import urlparse, unquote
from os import path
import shutil
import os

#initialize spark session
spark = SparkSession.builder.appName('Pipeline_Exercise').getOrCreate()
spark.sparkContext.setLogLevel("OFF")
spark.conf.set("spark.sql.jsonGenerator.ignoreNullFields", "false")

#set data directory
data_dir = path.join(path.dirname(path.dirname(path.abspath(__file__))), "data")

#read customers data into df
customers_df = spark.read.option("multiline","true").json( path.join(data_dir, "Market 1 Customers.json"))

#rename column to match the schema
customers_df = customers_df.withColumnRenamed("Number of employees", "Number of Employees")

#write customers data to json file
customers_df.write.json("output", mode="overwrite", lineSep=",")

input_file = customers_df.select(functions.input_file_name()).collect()[0][0]
file_name = path.basename(unquote(urlparse(input_file).path))
file_list = [filename for filename in os.listdir("output") if (filename.startswith("part") and filename.endswith(".json"))]

# #consolidate into one file (very slow, very memory intensive)
# combined_data = r'['
# for filename in file_list:
#     with open(f"./output/{filename}", 'r') as file:
#         combined_data += file.read()

# combined_data = combined_data[:-1] + ']'

# with open(f"./output/{file_name}", 'w') as file:
#     json.dump(json.loads(combined_data), file)


#move file to data directory
for filename in file_list:
    shutil.copyfile(f"./output/{filename}", path.join(data_dir, f"{file_name}_{filename}"))

#read deliveries data into df
deliveries_df = spark.read.option("header", "true").csv(path.join(data_dir, "Market 1 Deliveries.csv"))

columns = deliveries_df.columns

#create boolean columns for whether to push a record or not
deliveries_df = deliveries_df.withColumn('agent_id_is_string', deliveries_df['Agent_ID'].cast('int').isNull())
deliveries_df = deliveries_df.withColumn('int_agent_id_length_is_less_than_7', (functions.length(deliveries_df['Agent_ID']) < 7) & ~(deliveries_df['agent_id_is_string']))

#push data to the left columns from the Notes column down
deliveries_df = deliveries_df.withColumn('Notes', functions.when(deliveries_df['agent_id_is_string'], functions.concat_ws(", ", deliveries_df['Notes'], deliveries_df['Agent_ID'])).otherwise(deliveries_df['Notes']))

deliveries_df = deliveries_df.withColumn('Notes', functions.when(deliveries_df['int_agent_id_length_is_less_than_7'] == True, functions.concat_ws(", ", deliveries_df['Notes'], deliveries_df['Agent_ID'])).otherwise(deliveries_df['Notes']))

for i, column in enumerate(columns):
    if i <= columns.index('Agent_ID'):
        pass
    else:
        deliveries_df = deliveries_df.withColumn(columns[i-1], functions.when(deliveries_df['agent_id_is_string'], deliveries_df[column]).otherwise(deliveries_df[i-1]))
        deliveries_df = deliveries_df.withColumn(columns[i-1], functions.when(deliveries_df['int_agent_id_length_is_less_than_7'], deliveries_df[column]).otherwise(deliveries_df[i-1]))
      

#create boolean column for whether to push a record or not
deliveries_df = deliveries_df.withColumn('invalid_tip', ~deliveries_df['Tip'].startswith('KSh'))

#push data from to the left columns from the Special_Instructions column down
deliveries_df = deliveries_df.withColumn('Special_Instructions', functions.when(deliveries_df['invalid_tip'], functions.concat_ws(", ", deliveries_df['Special_Instructions'], deliveries_df['Tip'])).otherwise(deliveries_df['Special_Instructions']))

for i, column in enumerate(columns):
    if i <= columns.index('Tip'):
        pass
    else:
        deliveries_df = deliveries_df.withColumn(columns[i-1], functions.when(deliveries_df['invalid_tip'], deliveries_df[column]).otherwise(deliveries_df[i-1]))

#cleaning up before writing to file
deliveries_df = deliveries_df.drop('agent_id_is_string').drop('int_agent_id_length_is_less_than_7').drop('invalid_tip')

#write deliveries data to csv files
deliveries_df.write.csv("output", mode="overwrite", quoteAll="true", header="true")

input_file = deliveries_df.select(functions.input_file_name()).collect()[0][0]
file_name = path.basename(unquote(urlparse(input_file).path))
file_list = [filename for filename in os.listdir("output") if (filename.startswith("part") and filename.endswith(".csv"))]

# #consolidate into one file (very slow, very memory intensive)
# combined_data = r""

# with open(f"./output/{file_list[0]}", 'r') as file:
#     myreader = csv.reader(file)
#     for row in myreader:
#         for cell in row:
#             combined_data += f"\"{cell}\", "
#         combined_data = combined_data[:-2] + "\n"


# for filename in file_list[1:]:
#     with open(f"./output/{filename}", 'r') as file:
#         myreader = csv.reader(file)
#         next(myreader)
#         for row in myreader:
#             for cell in row:
#                 combined_data += f"\"{cell}\", "
#             combined_data = combined_data[:-2] + "\n"

# with open(f"./output/{file_name}", 'w') as file:
#     file.write(combined_data)

#move file to data directory
for filename in file_list:
    shutil.copyfile(f"./output/{filename}", path.join(data_dir, f"{file_name}_{filename}"))

#delete read files
os.remove(path.join(data_dir, "Market 1 Customers.json"))
os.remove(path.join(data_dir, "Market 1 Deliveries.csv"))

#move files to respective directories
data_files = os.listdir(data_dir)
destination_dirs = ["Customers", "Deliveries", "Orders"]

for destination_dir in destination_dirs:
    if not path.exists(path.join(data_dir, destination_dir)):
        os.makedirs(path.join(data_dir, destination_dir))
    for data_file in data_files:
        if destination_dir.lower() in data_file.lower():
            shutil.move(path.join(data_dir, data_file), path.join(data_dir, destination_dir, data_file))

os.makedirs("./archive", exist_ok=True)