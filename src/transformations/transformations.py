from src.transformations.transformations_utils import *

ROOT_PATH = os.getcwd()

def get_education_attribute(df:pl.DataFrame) -> pl.DataFrame:
    df = df.with_columns(
        pl.col("education").map_elements(
            lambda ed: next((s for s in ed if "J.D." in s), None),
            return_dtype=pl.Utf8
        ).alias("jd_entry")
    )
    df = df.with_columns(
        pl.when(pl.col("jd_entry").is_not_null())
        .then(pl.lit("yes"))
        .otherwise(pl.lit("no"))
        .alias("has_jd")
    )
    df = df.with_columns(
        pl.col("jd_entry")
        .str.extract(r"(\b\d{4}\b)", 1)
        .cast(pl.Int32)
        .alias("jd_year")
    )
    return df

def transformations_profile() -> pl.DataFrame:
    file_path=os.path.join(ROOT_PATH,'davidspolk_profile_cleaned.json')
    df=pl.read_json(file_path)
    logger.info("Reading profile JSON")
    df = get_id_attribute(df,id_element='vcard_href')
    df=df.unique('id')
    df = get_separate_columns_for_variables(df,column_name='phone')
    df=get_education_attribute(df)
    return df

def transformations_news()->pl.DataFrame:
    file_path=os.path.join(ROOT_PATH,'davidspolk_news.json')
    df=pl.read_json(file_path)
    logger.info("Reading news JSON")
    df=get_id_attribute(df,id_element='id')
    df=df.unique(['id'])
    df=df.with_columns(pl.col('url').str.split(by='/').list.get(-2).alias('category'))
    df=df.with_columns(pl.col('lawyers_link').list.eval(
        pl.element()
        .str.replace("/lawyers/", "")
        .str.replace_all("-", " ")
        .str.to_titlecase()
    ).alias("lawyers_link"))
    df=df.with_columns(pl.col('datePublished')\
                      .str.strptime(pl.Datetime,"%Y-%m-%dT%H:%M:%S%z")\
                      .dt.date().alias("datePublished"))
    df = df.with_columns([
        pl.col("capabilities_link").cast(pl.List(pl.Utf8)),
        pl.col("lawyers_link").cast(pl.List(pl.Utf8)),
    ])
    df=df.select('headline','url','datePublished','capabilities_link','lawyers_link','id','text')
    return df


df_profile=transformations_profile()
df_news=transformations_news()
df_join = df_profile.join(df_news, how="left", left_on="url", right_on="lawyers_link")
df_join=df_join.select(['name','email','capabilities','education','jd_entry','has_jd','url','id','phone_0','phone_1','phone_2','locations',
               'headline'])
df_join=df_join \
.group_by(['name','email','capabilities','education','jd_entry',
                  'has_jd','url','id','phone_0','phone_1','phone_2','locations']) \
 .agg(pl.col("headline"))

df_join.write_excel(workbook='profiles.xlsx',autofit=True)