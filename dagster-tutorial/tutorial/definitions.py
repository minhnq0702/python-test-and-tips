from dagster import (
    Definitions,
    ScheduleDefinition,
    DefaultScheduleStatus,
    load_assets_from_modules,
    define_asset_job,
    AssetSelection
)

from . import assets
from . import resources

all_assets = load_assets_from_modules([assets])

hackernews_top_words_job = define_asset_job("job_hacknews_top_words", selection=AssetSelection.all())

hackernews_to_words_schedule = ScheduleDefinition(
    job=hackernews_top_words_job,
    cron_schedule="*/1 * * * *",
    default_status=DefaultScheduleStatus.RUNNING,
)

datagen = resources.DataGeneratorResource(
    num_days=365,
)  # make the resource

defs = Definitions(
    assets=all_assets,
    schedules=[hackernews_to_words_schedule],
    resources={
        "hackernews_api": datagen,
    }
)
