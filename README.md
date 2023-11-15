# louisville-bike-accidents

## Source data
### /data/raw

The source data for my project. 

Since I am dealing with multiple datasets, I use a short "codename" for each file. In various scripts, you will see `LOJIC`, `CSAFE`, or `SIGNALS` as a variable name for the Dataframes, or other data objects I use to manipulate the source data. 

| codename | file name: data/raw/... | description |
|----------|-----------|-------------|
| LOJIC | Louisville_Metro_KY_-_Traffic_Fatalities_and_Suspected_Serious_Injuries.csv | Crash reports from 2016-2023 (Updated regularly) in Jefferson County, KY. This data was found on the Louisville Open Data portal. It includes reports of all crashes during its timeframe. This includes motor vehicle crashes and pedestrian incidents. |
| CSAFE | cycling_safety_louisville.csv | Crash reports from 2010-2017. This data was part of a European study on cycling safety. |
| SIGNALS | Jefferson_County_KY_Signalized_Intersections.csv | Road intersections in Jefferson County, KY with traffic lights. |

## Discovery
### `/code/discovery`

Jupyter notebooks for data discovery on this project's source data.

| codename | notebook name |
|----------|---------------|
| LOJIC | discovery_LOJIC.ipynb |
| CSAFE | discovery_cycling_safety.ipynb |
| SIGNALS | other_discovery.ipynb |

## Cleaning

### /data/preclean & /code/cleaning

For each of the source datasets, I first did some cleaning to remove unwanted data and make these easier to combine. This directory contains the resulting .csv files from that cleaning process.

Run `python {cleaning file}` to generate a clean(er) CSV for each source file.

| codename | clean CSV name: data/preclean/... | cleaning script code/cleaning/... |source file |
|----------|----------------|-----------------|------------|
| LOJIC | LOJIC_cycling_data.csv | cleaning/cleaning_LOJIC.py | data/raw/Louisville_Metro_KY_-_Traffic_Fatalities_and_Suspected_Serious_Injuries.csv|
| CSAFE | cycling_safety_louisville_clean.csv | cleaning_cycling_safety.py | data/raw/cycling_safety_louisville.csv |
| SIGNALS |signalized_intersections.csv | cleaning_signal_intersections.py | data/raw/Jefferson_County_KY_Signalized_Intersections.csv |

### /data/clean

Final clean data I can use for analysis.

## Analysis

## Visualization

## ...
