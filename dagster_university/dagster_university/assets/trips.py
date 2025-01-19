import requests
import os

from dagster import asset, MaterializeResult, AssetExecutionContext
from dagster_duckdb import DuckDBResource

from . import constants
from ..partitions import monthly_partition

@asset(
    description="Taxi trip file data downloaded from NYC Open Data",
    partitions_def=monthly_partition,
)
def nyc_taxi_trips_file(context: AssetExecutionContext) -> None:
    """
    Trip file data downloaded from NYC OpenData
    Returns:

    """
    partition_date_str = context.partition_key
    report_month = partition_date_str[:-3]
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
    partitions_def=monthly_partition,
)
def nyc_taxi_trips(context: AssetExecutionContext, database: DuckDBResource) -> MaterializeResult:
    """
    The raw taxi trips dataset
    Args:
        context (AssetExecutionContext):
        database (DuckDBResource): DuckDB Resource to provide connection
    Returns:

    """
    partition_date_str = context.partition_key
    report_month = partition_date_str[:-3]
    query = f"""
        create table if not exists trips (
            vendor_id integer, pickup_zone_id integer, dropoff_zone_id integer,
            rate_code_id double, payment_type integer, dropoff_datetime timestamp,
            pickup_datetime timestamp, trip_distance double, passenger_count double,
            total_amount double, partition_date varchar
            
        );
        
        delete from trips where partition_date = '{report_month}';
        
        insert into trips
        select 
            VendorID,
            PULocationID,
            DOLocationID,
            RatecodeID,
            payment_type,
            tpep_dropoff_datetime,
            tpep_pickup_datetime,
            trip_distance,
            passenger_count,
            total_amount,
            '{report_month}' as partition_date
        from '{constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(report_month)}';
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