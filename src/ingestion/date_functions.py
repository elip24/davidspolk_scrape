import calendar
from datetime import datetime, timedelta, time, date, timezone
from google.cloud import bigquery
from src.config.settings import TARGET, client


def get_last_startdate(client):
    now=datetime.now(timezone.utc).date()
    last_day=now-timedelta(days=7)
    query = f"""
    
    SELECT MAX(datePublished) AS max_date
    FROM {TARGET}
    WHERE datePublished >= @last_day
    """
    job_cfg = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("last_day", "DATE", last_day)]
    )
    rows = client.query(query, job_config=job_cfg).result()
    row = next(rows, None)
    last_startdate=row.max_date if row else None
    last_startdate=datetime.combine(last_startdate, datetime.min.time(), tzinfo=timezone.utc)

    return last_startdate

