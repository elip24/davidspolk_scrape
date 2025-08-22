import json

from google.cloud import bigquery
import datetime, random
from src.config.settings import client
from datetime import datetime, timezone, timedelta

def get_temp_table(dataset: str, table_name: str = None, project=None):
    prefix = "temp"
    suffix = random.randint(10000, 99999)
    if not table_name:
        table_name = "noname"

    temp_table_name = f"{dataset}.{prefix}_{table_name}_{suffix}"
    if project:
        temp_table_name = f"{project}.{temp_table_name}"
    tmp_table_def = bigquery.Table(temp_table_name)
    tmp_table_def.expires = datetime.now(timezone.utc) +timedelta(
        minutes=5
    )
    table = client.create_table(tmp_table_def)
    return table,temp_table_name

def delete_temp_table(table_id: str):
    try:
        client.delete_table(table_id, not_found_ok=True)
    except Exception as e:
        print(f"[cleanup] couldn't delete {table_id}: {e}")

