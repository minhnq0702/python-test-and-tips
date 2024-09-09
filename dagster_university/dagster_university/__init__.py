# fmt: off
from dagster import Definitions, load_assets_from_modules

from .resources import database_resource
from .assets import metrics, trips
from .jobs import trip_update_job, trip_by_week_job
from .schedules import trip_update_schedule, trip_by_week_schedule

trip_assets = load_assets_from_modules([trips])
metric_assets = load_assets_from_modules([metrics])

defs = Definitions(
    resources={
        "database": database_resource,
    },
    assets=[*trip_assets, *metric_assets],
    jobs=[trip_update_job, trip_by_week_job],
    schedules=[trip_update_schedule, trip_by_week_schedule],
)
