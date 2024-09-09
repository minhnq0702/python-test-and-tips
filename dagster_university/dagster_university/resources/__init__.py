from dagster_duckdb import DuckDBResource
from dagster import EnvVar

from ..assets import constants

database_resource = DuckDBResource(
    database=EnvVar(constants.ENV_DUCKDB_DATABASE),
)