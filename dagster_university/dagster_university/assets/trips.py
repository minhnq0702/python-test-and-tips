import requests
import os

from dagster import asset, MaterializeResult
from dagster_duckdb import DuckDBResource

from . import constants

@asset(description="Taxi trip file data downloaded from NYC Open Data")
def nyc_taxi_trips_file() -> None:
    """
    Trip file data downloaded from NYC OpenData
    Returns:

    """
    report_month = "2023-10"
    car_type = "yellow_tripdata"
    url = "https://d37ci6vzurychx.cloudfront.net/trip-data/{car_type}_{report_month}.parquet"
    resp = requests.get(url.format(car_type=car_type, report_month=report_month))
    with open(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(report_month), "wb") as f:
        f.write(resp.content)
    resp.close()


@asset(description="Taxi zone file downloaded from NYC Open Data")
def nyc_taxi_zones_file() -> None:
    """
    Taxi zones downloaded from NYC Open data
    Returns:

    """
    with requests.get("https://data.cityofnewyork.us/api/views/755u-8jsi/rows.csv?accessType=DOWNLOAD") as resp:
        with open(constants.TAXI_ZONES_FILE_PATH, "wb") as f:
            f.write(resp.content)


@asset(
    description="Tax trips database extracted from taxi trips file",
    deps=[nyc_taxi_trips_file],
)
def nyc_taxi_trips(database: DuckDBResource) -> MaterializeResult:
    """
    The raw taxi trips dataset
    Args:
        database (DuckDBResource): DuckDB Resource to provide connection
    Returns:

    """
    query = """
        create or replace table trips as (
            select
                VendorID as vendor_id,
                PULocationID as pickup_zone_id,
                DOLocationID as dropoff_zone_id,
                RatecodeID as rate_code_id,
                payment_type as payment_type,
                tpep_dropoff_datetime as dropoff_datetime,
                tpep_pickup_datetime as pickup_datetime,
                trip_distance as trip_distance,
                passenger_count as passenger_count,
                total_amount as total_amount
            from 'data/raw/taxi_trips_2023-10.parquet'
        );
    """
    with database.get_connection() as conn:
    # conn = duckdb.connect(os.getenv(constants.ENV_DUCKDB_DATABASE))
        conn.execute(query)

    with database.get_connection() as conn:
        # connect to verify created dataset
        res = conn.execute("""select count(*) from trips""").fetchall()
    return MaterializeResult(
        metadata={
            "Total Trips": res[0][0]
        }
    )


@asset(
    description="Tax zones database extracted from taxi zones file",
    deps=[nyc_taxi_zones_file],
)
def nyc_taxi_zones(database: DuckDBResource) -> MaterializeResult:
    query = f"""
        create or replace table zones as (
            select 
                LocationID as zone_id,
                zone,
                borough,
                the_geom as geometry
            from '{constants.TAXI_ZONES_FILE_PATH}'
        );
    """
    with database.get_connection() as conn:
        conn.execute(query)

    with database.get_connection() as conn:
        # connect to verify create dataset
        res = conn.execute("""select count(*) from zones""").fetchall()
    return MaterializeResult(
        metadata={
            "Total Zones": res[0][0],
        }
    )