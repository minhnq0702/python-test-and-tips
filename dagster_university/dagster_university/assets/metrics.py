import base64
import os.path
from datetime import date, datetime

import geopandas as gpd
import pandas as pd
import plotly.express as px
import plotly.graph_objects
import plotly.io as pio
from dagster import (AssetExecutionContext, MaterializeResult, MetadataValue,
                     asset)
from dagster_duckdb import DuckDBResource
from dateutil.relativedelta import relativedelta

from ..partitions import weekly_partition
from . import constants


@asset(deps=["nyc_taxi_trips", "nyc_taxi_zones"])
def nyc_manhattan_stats(database: DuckDBResource) -> MaterializeResult:
    query = """
        select
            zones.zone,
            zones.borough,
            zones.geometry,
            count(1) as num_trips
        from trips
        left join zones on trips.pickup_zone_id = zones.zone_id
        where borough = 'Manhattan' and geometry is not null
        group by zone, borough, geometry;
    """
    with database.get_connection() as conn:
        zone_w_trip_count: pd.DataFrame  = conn.query(query).fetchdf()

    # convert from geometry POLYGON dataobject to geopandas series
    zone_w_trip_count["geometry"] = gpd.GeoSeries.from_wkt(zone_w_trip_count["geometry"])
    zone_w_trip_count = gpd.GeoDataFrame(zone_w_trip_count)
    with open(constants.MANHATTAN_STATS_FILE_PATH, "wt") as f:
        f.write(zone_w_trip_count.to_json())
    return MaterializeResult(
        metadata={
            "Preview": MetadataValue.md(zone_w_trip_count.head().to_markdown())
        }
    )


@asset(
    deps=[nyc_manhattan_stats]
)
def nyc_manhattan_map() -> MaterializeResult:
    # * load gepjson to geopandas dataframe
    trips_by_zone = gpd.read_file(constants.MANHATTAN_STATS_FILE_PATH)
    fig: plotly.graph_objs.Figure = px.choropleth_mapbox(
        trips_by_zone,
        geojson=trips_by_zone.geometry.__geo_interface__,
        locations=trips_by_zone.index,
        color='num_trips',
        color_continuous_scale='Plasma',
        mapbox_style='carto-positron',
        center={'lat': 40.758, 'lon': -73.985},
        zoom=11,
        opacity=0.7,
        labels={'num_trips': 'Number of Trips'}
    )


    map_img_data = fig.to_image("png")
    # both approach below work well
    # pio.write_image(fig, constants.MANHATTAN_MAP_FILE_PATH)
    # or
    with open(constants.MANHATTAN_MAP_FILE_PATH, "wb") as f:
        f.write(map_img_data)

    return MaterializeResult(
        metadata={
            "Preview": MetadataValue.md(f"![Manhattan trips status](data:image/png;base64,{base64.b64encode(map_img_data).decode()})")
        }
    )


@asset(
    deps=["nyc_taxi_trips"],
    partitions_def=weekly_partition,
)
def nyc_trips_by_week(context: AssetExecutionContext, database: DuckDBResource) -> MaterializeResult:
    """
    Get Trip by Week dataset
    Returns:

    """
    query = """
        select 
            '{}' as period,
            count(*) as num_trips,
            sum(coalesce(passenger_count, 0)) as passenger_count,
            sum(total_amount) as total_amount,
            sum(trip_distance) as trip_distance 
        from trips
        where pickup_datetime >= '{}' and pickup_datetime < '{}'::date + interval '1 week'
    """
    context.log.debug(f"==> {context.partition_key}", )
    start_date_of_week = context.partition_key
    with database.get_connection() as conn:
        df = conn.execute(query.format(start_date_of_week, start_date_of_week, start_date_of_week)).fetchdf()
    df["passenger_count"] = df["passenger_count"].astype(int)
    df["total_amount"] = df["total_amount"].round(2).astype(float)
    df["trip_distance"] = df["trip_distance"].round(2).astype(float)
    if os.path.isfile(constants.TRIPS_BY_WEEK_FILE_PATH):
        exist = pd.read_csv(constants.TRIPS_BY_WEEK_FILE_PATH)
        df = pd.concat([exist, df])
    else:
        df.to_csv(constants.TRIPS_BY_WEEK_FILE_PATH, index=False)
    return MaterializeResult(
        metadata={
            "Preview": MetadataValue.md(df.to_markdown())
        }
    )
