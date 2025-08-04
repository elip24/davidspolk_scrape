import os
import polars as pl
from pathlib import Path

ROOT_PATH=os.getcwd()
file_path=os.path.join(ROOT_PATH,'davidspolk_profile_cleaned.json')
df=pl.read_json(file_path)

def get_separate_columns_for_variables(df:pl.DataFrame,column_name:str)-> pl.DataFrame:
    over_limit=df.filter(pl.col(f"{column_name}").list.len() > 3)
    if over_limit.height>0:
        print("guarda")
    for i in range(3):
        df = df.with_columns(
            pl.col(f"{column_name}").list.get(i, null_on_oob=True).alias(f"{column_name}_{i}"))
    return df

def get_id_attribute(df:pl.DataFrame,id_element:str)-> pl.DataFrame:
    df=df.with_columns(pl.col(f'{id_element}').str.split(by='/').list.last().alias('id'))
    return df
