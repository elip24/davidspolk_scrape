import os
from datetime import datetime, timezone

import polars as pl
from pathlib import Path
from polars import lit
from .transformations_utils import *

def transformations_news(all_news:dict)->pl.DataFrame:
    df = pl.DataFrame(all_news)
    df = get_id_attribute(df, id_element='id')
    df=df.unique(['id'])
    df = get_from_string_to_datetime(df,column_name="datePublished",alias_name="content_date_watermark")
    df = df.with_columns(pl.col("content_date_watermark").dt.date().alias("datePublished"))
    df=transform_array_into_list(df,"capabilities")
    df = transform_array_into_list(df, "capabilities_link")
    df = transform_array_into_list(df, "lawyer_link")
    df = transform_array_into_list(df, "lawyer_names")


    df = df.with_columns(pl.lit(datetime.now(timezone.utc)).cast(pl.Datetime).alias("syncstartdatetime"))
    df = df.with_columns(pl.lit('davidspolk').alias('site_page'))
    df = make_hash_cols(df)
    return df

def transformation_news_raw(all_news:dict)->pl.DataFrame:
    df = pl.DataFrame(all_news)
    df=get_id_attribute(df,id_element='id')
    df=df.unique('id')
    df = df.with_columns(pl.lit(datetime.now(timezone.utc)).cast(pl.Datetime).alias("syncstartdatetime"))
    return df

def transformations(all_news:dict):
    df=transformations_news(all_news)
    df_raw=transformation_news_raw(all_news)
    return df,df_raw