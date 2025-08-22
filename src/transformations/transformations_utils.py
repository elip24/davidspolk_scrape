import os
import polars as pl
from pathlib import Path
import logging
import polars as pl
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

def get_separate_columns_for_variables(df:pl.DataFrame,column_name:str)-> pl.DataFrame:
    over_limit=df.filter(pl.col(f"{column_name}").list.len() > 3)
    if over_limit.height>0:
        logger.warning(f"The column {column_name} is over limit: {over_limit.height}")
    for i in range(3):
        df = df.with_columns(
            pl.col(f"{column_name}").list.get(i, null_on_oob=True).alias(f"{column_name}_{i}"))
    return df

def get_id_attribute(df:pl.DataFrame,id_element:str)-> pl.DataFrame:
    df=df.with_columns(pl.col(f'{id_element}').str.split(by='/').list.last().alias('id'))
    return df


def transform_array_into_list(df:pl.DataFrame,column_name):
    df = df.with_columns(
    pl.when(pl.col((f"{column_name}")).is_null())
      .then(pl.lit([]).cast(pl.List(pl.Utf8)))
      .otherwise(pl.col((f"{column_name}")).cast(pl.List(pl.Utf8)))
      .alias((f"{column_name}"))
    )
    return df

def make_hash_cols(df:pl.DataFrame):
    df = df.with_columns(
        pl.concat_str(
            [
                pl.col("headline"),
                pl.col("datePublished").cast(pl.Utf8).fill_null(""),
                pl.col("capabilities").list.join(",").fill_null(""),
                pl.col("lawyer_names").list.join(",").fill_null(""),
                pl.col("lawyer_link").list.join(",").fill_null(""),
                pl.col("content_date_watermark").cast(pl.Utf8).fill_null("")
            ],
            separator="||"
        ).hash(seed=0).alias("hash_cols").cast(pl.Utf8)
    )
    return df

def get_from_string_to_datetime(df:pl.DataFrame,column_name:str,alias_name:str):
    df=df.with_columns(pl.col((f"{column_name}")).str.strptime(pl.Datetime, "%Y-%m-%dT%H:%M:%S%z").dt.convert_time_zone("UTC")
                       .alias(alias_name))
    return df

