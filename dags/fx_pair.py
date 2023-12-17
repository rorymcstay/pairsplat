import os
import logging
import pathlib

from airflow import DAG

import pandas as pd

import pendulum

from airflow.decorators import task

import fx_pairs.prices_etl as fx

from arcticdb import Arctic


CONFIG = pathlib.Path('/lib/volumes/python/fx_pairs/universe.yml')


logger = logging.getLogger(__name__)


class Args:

    def __init__(self, context):

        self.start_date = pd.Timestamp(context['data_interval_start'])
        self.end_date = pd.Timestamp(context['data_interval_end'])
        self.epics = []
        self.resolution = '4H'
        self.universe_name = "TRADINGO"
        self.config = {}

    def __repr__(self):

        return (f"Args({self.start_date=}, {self.end_date=},"
                f" {self.resolution=}, {self.universe_name=}, {self.epics=})")


@task
def extract(**context):
    arctic = Arctic(os.environ['TRADINGO_PRICE_STORE'])
    args = Args(context)
    fx.load_config(CONFIG, args)
    logger.info(args)

    fx.extract(
        arctic,
        epics=args.epics,
        start_date=args.start_date,
        end_date=args.end_date,
        resolution=args.resolution,
    )


@task
def transform(**context):
    arctic = Arctic(os.environ['TRADINGO_PRICE_STORE'])
    args = Args(context)
    fx.load_config(CONFIG, args)
    logger.info(args)

    fx.transform(
        arctic,
        epics=args.epics,
        start_date=args.start_date,
        end_date=args.end_date,
        resolution=args.resolution,
        universe_name=args.universe_name
    )

    fx.transform_derived(
        arctic,
        epics=args.epics,
        start_date=args.start_date,
        end_date=args.end_date,
        resolution=args.resolution,
        universe_name=args.universe_name,
        obvs='CLOSE'
    )


@task
def load(**context):
    arctic = Arctic(os.environ['TRADINGO_PRICE_STORE'])
    args = Args(context)
    fx.load_config(CONFIG, args)
    logger.info(args)

    data = fx.load(
        arctic,
        epics=args.epics,
        start_date=args.start_date,
        end_date=args.end_date,
        resolution=args.resolution,
        universe_name=args.universe_name
    )
    logger.info('\n%s', data)

@task
def backtest(**context):
    arctic = Arctic(os.environ['TRADINGO_PRICE_STORE'])
    args = Args(context)
    fx.load_config(CONFIG, args)
    logger.info(args)

    try:

        fx.backtest(
            arctic,
            epics=args.epics,
            start_date=args.config['start_date'],
            end_date=args.end_date,
            resolution=args.resolution,
            universe_name=args.universe_name,
            config=args.config,
            diagnostics=diagnostics,
        )

    except Exception as ex:

        fx.log_diagnostics(diagnostics)


with DAG(
    dag_id="tradingo-etl",
    schedule='0 0 * * 1-5',
    start_date=pd.Timestamp("2023-12-01 00:00:00+00:00"),
    catchup=True,
    max_active_runs=1,
) as dag:

    extract() >> transform() >> load() >> backtest()
