FROM apache/airflow:slim-2.8.2-python3.11

ARG PROJECT_DIR="/opt/airflow"

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH="$PYTHONPATH:$PROJECT_DIR"
ENV AIRFLOW_HOME=$PROJECT_DIR

USER root

USER airflow

COPY requirements.txt /
RUN pip install --no-cache-dir -r /requirements.txt

WORKDIR $PROJECT_DIR

COPY . .
