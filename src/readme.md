Right now its missing the loading module due to at the time we 
didnt have a database (we do now, so we should add it)

What it does on each ingestion its get through the api all the urls for
either profile or news. After that we concurrently run each url in 10 separate tabs
so we can proccess it faster (of course once its done throught google run we should
put it in either 2 or 1 since there isnt a lot of data in a day)
From each url we extract the data that is available through playwright (
if we can get it from the json+id we get it through there otherwise from the css selector
)
Once we have the json do the transformations with polars (since its faster) and save it in a parquet file
And then we do the load to the db of everything (the raw df to the raw, the cleaned to the cleaned table with a merge
and maybe run an sp for the merge with dwh)
Also its missing that for each api request to get the date (so that we can run it contnously without much issue)

Also Put everything in dockers so that we can run it through google run (since the requiremetns its just
playwright and polars its pretty cheap on that aspect)