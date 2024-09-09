from dagster import ScheduleDefinition

trip_update_schedule = ScheduleDefinition(
    job_name="trip_update_job",
    cron_schedule="0 0 5 * *",
)
trip_by_week_schedule = ScheduleDefinition(
    job_name="trip_by_week_job",
    cron_schedule="0 0 * * 1",
)