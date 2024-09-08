import os
import base64
import duckdb
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects
import plotly.io as pio

from dagster import asset, MaterializeResult, MetadataValue, AssetExecutionContext

from . import constants


@asset(deps=["nyc_tax_trips", "nyc_tax_zones"])
def nyc_manhattan_stats() -> MaterializeResult:
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