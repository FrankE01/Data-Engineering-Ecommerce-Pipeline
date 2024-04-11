FROM python:3

ENV JAVA_HOME=${JAVA_HOME:-"/opt/bitnami/java"}
ENV PATH="${PATH}:${JAVA_HOME}"
ENV SPARK_HOME="/opt/bitnami/spark"
ENV PATH="${PATH}:${SPARK_HOME}/bin"
ENV PATH="${PATH}:${SPARK_HOME}"

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "./spark_apps/pipeline.py"]

# CMD ["bash", "run-submit.sh"]
