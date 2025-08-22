import os

from src.ingestion.ingestion import ingestion
import polars as pl

from src.loading.loading import loading_raw, loading
from src.transformations.transformations_news import transformations


def main():
    all_news=ingestion()
    print("Done with ingestion,going to transformation")
    df_clean,df_raw=transformations(all_news)
    print("Done with transformation,going to loading to raw")
    loading_raw(df_raw)
    print("Done with loading to raw,going to loading clean")
    loading(df_clean)

if __name__=='__main__':
    main()
