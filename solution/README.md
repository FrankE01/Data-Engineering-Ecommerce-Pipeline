# E-commerce Data Pipeline Solution

## Overview

This repository contains the solution for the advanced data pipeline assignment designed for a large e-commerce platform. The solution includes data ingestion mechanisms, schema evolution handling, incremental updates support, data transformations, scalable parallel processing, fault tolerance implementation, and efficient data storage. The pipeline is built to process and analyze datasets simulating real-world scenarios from two distinct markets.

## Table of Contents

- [Dataset Description](#dataset-description)
- [Requirements](#requirements)
- [Solution Architecture](#solution-architecture)
- [Setup and Execution](#setup-and-execution)
- [Additional Notes](#additional-notes)
- [Contact Information](#contact-information)

## Solution Dataset Description

After applying many transformations and analyses, the final dataset that gets funnelled into the database is in the following form:

- **ecommerce:**
  - "Customer_ID" (integer),
  - "Total_Order_Amount" (double precision),
  - "Average_Order_Amount" (double precision),
  - "Order_Count" (bigint NOT NULL),
  - "Highest_Order_Amount" (real),
  - "Lowest_Order_Amount" (real),
  - "Total_Quantity_Ordered" (bigint),
  - "Average_Quantity_Per_Ordered" (double precision),
  - "Total_Delivery_Distance" (double precision),
  - "Average_Delivery_Distance" (double precision),
  - "Distict_Products" (bigint NOT NULL),
  - "start_timestamp" (timestamp without time zone),
  - "end_timestamp" (timestamp without time zone)

## Requirements Satisfaction

The solution addresses the following requirements:

- **Data Ingestion and Schema Evolution:**
  Data ingestion is handled in the form of file input. Three directories have been created to store the different types of data, namely `Customers`, `Deliveries`, and `Orders`. This is to logically seperate the different shapes of the data, with the added benefit of simplifying the process of reading in the data and applying schema checks. A `schemas` package is used to abstract the different data schemas and make it easy to change or evolve the schema as the data changes.
- **Incremental Updates:**
  By using Apache Spark Structured Streaming, the data pipeline supports adding and only processing new records or modified records since last execution. This is achieved by simply moving the data file into the designated data directory. - Customer data in `json` format goes into `./data/Customers/` - Deliveries data in `csv` format goes into `./data/Deliveries/` - Orders data in `csv` format goes into `./data/Orders/`
- **Data Transformation:**
  - The columns are renamed to replace whitespaces with underscores.
  - The `Order_ID` column in the `Orders` dataset is stripped down from a `YR-<order_id>,0` format to a simple `<order_id>` format to match the `Order_ID` column format in the `Deliveries` dataset.
  - The `Discount` and `Tip` columns in the `Orders` dataset are renamed to `Order_Discount` and `Order_Tip` respectfully to prevent column duplication, since they exist in the deliveries dataset.
  - Ten different aggregation metrics (discussed below) are applied to a combined dataset of the three sources.
- **Scalability and Parallel Processing:**
  From file I/O to dataframe operations to write streaming, Apache Spark is intrinsically built to parallelize many processes. - The application is set to use the maximun number of threads allocated to it by the operating system, ensuring scalability on larger systems. - The reading and writing of the data files are assigned to multiple threads through partitioning of the data. - Operations like write streaming, source directory watching, and dataframe operations are each assigned to different threads or groups of threads to keep the application in a fast and parallel processing state.
- **Data Storage:**
  PostgreSQL is used as the database for storing the processed data. This ensures efficient data retrieval and querying, as PostgreSQL is built to be resilient, and production ready.
- **Fault Tolerance:**
  The choice of using Apache Spark primarily for the pipeline also automatically guarantees the application of its fault-tolerant mechanisms to handle failure during data processing and ensure graceful recovery without data loss. Spark achieves this by keeping record of all key dataframe operations in the driver node so that it can be accessed by all worker nodes in case of failure. These operations can be used to recompute the current state of the data at any point in the application.
- **Documentation:**
  Comprehensive documentation has been provided explaining the data pipeline's architecture, data flow, and setup instructions.

## Solution Architecture

The solution architecture includes:

- Data ingestion using Apache Spark for processing CSV and JSON files.
- Schema evolution handling using Spark SQL and python packages.
- Incremental updates using Spark streaming for processing new or modified records.
- Data transformations and aggregations using Spark SQL and DataFrame APIs.
- PostgreSQL database for storing processed data.
- Fault-tolerant mechanisms using Spark checkpointing and recovery strategies.

## Setup and Execution

Follow these steps to set up and run the data pipeline:

1. **Clone Repository:**
   Clone this repository to your local machine.

2. **Environment Setup:**
   Ensure you have Python, Apache Spark, Docker, and PostgreSQL installed and configured.

3. **Database Setup:**
   Create a PostgreSQL database and configure the connection properties in the application.

4. **Run Data Pipeline:**
   Execute the data pipeline cluster using `docker compose up --build`.

5. **Monitoring and Update:**
   Monitor the data flow in PGAdmin. New data can be added by moving the data file into the appropriate directory

## Additional Notes

- The `data_pipeline.py` script contains the main logic for the data pipeline implementation.
- Use environment variables for configuration settings such as database connection details.

## Contact Information

For any questions or inquiries, please contact:

- Name: Francis Echesi
- Email: francis@trestleacademyghana.org
