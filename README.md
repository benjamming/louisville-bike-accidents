# louisville-bike-accidents

## The plan so far:
### /data/raw

The source data for my project.

| file name | description |
|-----------|-------------|
| Louisville_Metro_KY_-_Traffic_Fatalities_and_Suspected_Serious_Injuries.csv | Crash reports from 2016-2023 (Updated regularly) in Jefferson County, KY. This data was found on the Louisville Open Data portal. It includes reports of all crashes during its timeframe. This includes motor vehicle crashes and pedestrian incidents. |
| cycling_safety_louisville.csv | Crash reports from 2010-2017. This data was part of a European study on cycling safety. |
| Jefferson_County_KY_Signalized_Intersections.csv | Road intersections in Jefferson County, KY with traffic lights. |

### /data/preclean

For each of the source datasets, I first did some cleaning to remove unwanted data and make these easier to combine. This directory contains the resulting .csv files from my cleaning process.

Run `python {cleaning file}` to generate clean CSV

| clean CSV name | cleaning script |source file |
|----------------|---------------|------------|
| LOJIC_cycling_data | cleaning/cleaning_LOJIC.py |Louisville_Metro_KY_-_Traffic_Fatalities_and_Suspected_Serious_Injuries.csv|
| cycling_safety_louisville_clean.csv | cleaning_cycling_safety.py | cycling_safety_louisville.csv |
| signalized_intersections.csv | cleaning_signal_intersections.py | Jefferson_County_KY_Signalized_Intersections.csv |

### /data/clean
