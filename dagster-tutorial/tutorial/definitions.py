from dagster import Definitions, ScheduleDefinition, load_assets_from_modules, define_asset_job, AssetSelection

from . import assets

all_assets = load_assets_from_modules([assets])

hackernews_top_words_job = define_asset_job("job_hacknews_top_words", selection=AssetSelection.all())

hackernews_to_words_schedule = ScheduleDefinition(
    job=hackernews_top_words_job,
    cron_schedule="*/1 * * * *"
)

defs = Definitions(
    assets=all_assets,
    schedules=[hackernews_to_words_schedule],
)
