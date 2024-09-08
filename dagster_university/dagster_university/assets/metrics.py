import os
import duckdb
import pandas as pd
import geopandas as gpd

from dagster import asset, MaterializeResult, MetadataValue, AssetExecutionContext

from . import constants


@asset(deps=["nyc_tax_trips", "nyc_tax_zones"])
def nyc_manhattan_stats(context: AssetExecutionContext) -> MaterializeResult:
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
    conn = duckdb.connect(os.getenv(constants.ENV_DUCKDB_DATABASE))
    zone_w_trip_count: pd.DataFrame  = conn.query(query).fetchdf()

    # convert from geometry POLYGON dataobject to geopandas series
    zone_w_trip_count["geometry"] = gpd.GeoSeries.from_wkt(zone_w_trip_count["geometry"])
    zone_w_trip_count = gpd.GeoDataFrame(zone_w_trip_count)
    with open(constants.MANHATTAN_STATS_FILE_PATH, "w") as f:
        f.write(zone_w_trip_count.to_json())
    return MaterializeResult(
        metadata={
            "Preview": MetadataValue.md(zone_w_trip_count.head().to_markdown())
        }
    )