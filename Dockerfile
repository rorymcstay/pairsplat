FROM apache/airflow:2.7.3-python3.8

RUN pip install fx-pairs==0.0.4 \
                    pendulum \
                    apache-airflow \
                    arcticdb
