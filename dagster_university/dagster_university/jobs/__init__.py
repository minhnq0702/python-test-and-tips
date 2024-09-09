from dagster import AssetSelection, define_asset_job

trip_by_week = AssetSelection.assets(["nyc_trips_by_week"])
trip_update_job = define_asset_job(
    name="trip_update_job",
    selection=AssetSelection.all() - trip_by_week,
)
trip_by_week_job = define_asset_job(
    name="trip_by_week_job",
    selection=trip_by_week,
)