FROM python:3

ENV JAVA_HOME=${JAVA_HOME:-"/opt/bitnami/java"}
ENV PATH="${PATH}:${JAVA_HOME}"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./spark_apps/prepare_data_files.py"]

# CMD ["python", "./spark_apps/prepare_data_files.py", "&&", "docker", "exec", "da-spark-master", "spark-submit", "--master spark://spark-master:7077", "--deploy-mode client", "--driver-class-path ./jars/postgresql-42.7.3.jar", "--jars ./jars/postgresql-42.7.3.jar", "./spark_apps/pipeline.py"]
