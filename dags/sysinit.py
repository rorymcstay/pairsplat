import os
import logging
import pathlib

from airflow import DAG

import pandas as pd

import pendulum

from airflow.decorators import task

import fx_pairs.prices_etl as fx

from arcticdb import Arctic

import sysdata
from sysinit import futures
import sysproduction.run_daily_price_updates as func

@task
def run_daily_price_updates():

    import sysproduction.run_daily_price_updates as func
    func.run_daily_price_updates()


with DAG(
    dag_id="tradingo",
    schedule='0 0 * * 1-5',
    start_date=pd.Timestamp("2023-12-01 00:00:00+00:00"),
    catchup=True,
    max_active_runs=1,
) as dag:

    run_daily_price_updates()
