import os
import polars as pl
from pathlib import Path
from polars import lit
from transformations_functions import *

ROOT_PATH = os.getcwd()

def transformations_profile() -> pl.DataFrame:
    file_path=os.path.join(ROOT_PATH,'davidspolk_profile_cleaned.json')
    df=pl.read_json(file_path)
    df = get_id_attribute(df,id_element='vcard_href')
    df=df.unique('id')
    df = get_separate_columns_for_variables(df,column_name='phone')
    df = get_separate_columns_for_variables(df,column_name='locations')
    return df

def transformations_news()->pl.DataFrame:
    file_path=os.path.join(ROOT_PATH,'davidspolk_news.json')
    df=pl.read_json(file_path)
    df=get_id_attribute(df,id_element='id')
    df=df.unique(['id'])
    df=df.explode('lawyers_link')
    df=df.with_columns(lit('https://www.davispolk.com').alias('start_link'))
    df=df.with_columns(pl.concat_str(df['start_link'],df['lawyers_link']).alias('lawyers_link'))
    return df


df_profile=transformations_profile()
df_news=transformations_news()
df_join = df_profile.join(df_news, how="left", left_on="url", right_on="lawyers_link")
df_join=df_join.select(['name','email','capabilities','education','url','id','phone_0','phone_1','phone_2','locations_0','locations_1','locations_2',
               'headline'])
with pl.Config(tbl_cols=-1):
    print(df_join)