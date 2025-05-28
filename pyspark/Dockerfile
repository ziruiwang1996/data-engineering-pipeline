FROM apache/spark-py:latest

WORKDIR /app

COPY clean_and_normalize.py .
COPY postgresql-42.6.0.jar .

CMD ["spark-submit", "--jars", "postgresql-42.7.6.jar", "clean_and_normalize.py"]