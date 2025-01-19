from dagster import AssetSelection, define_asset_job

from ..partitions import monthly_partition, weekly_partition

trip_by_week = AssetSelection.assets(["nyc_trips_by_week"])
trip_update_job = define_asset_job(
    partitions_def=monthly_partition,
    name="trip_update_job",
    selection=AssetSelection.all() - trip_by_week,
)
trip_by_week_job = define_asset_job(
    partitions_def=weekly_partition,
    name="trip_by_week_job",
    selection=trip_by_week,
)