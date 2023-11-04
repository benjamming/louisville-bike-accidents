import pandas as pd
import pyparsing as pyp

DATA1 = "../data/cycling_safety_louisville.csv"
# DATA1 points to crash data from 2010 to 2017
# This data came from: https://zenodo.org/records/5603036
# Source: https://zenodo.org/records/5603036/files/louisville.zip


DATA2 = "../data/Louisville_Metro_KY_-_Traffic_Fatalities_and_Suspected_Serious_Injuries.csv"
# DATA2 points to crash data from 2016 to 2023.
# This data came from the Louisville Open Data portal
# Source: https://data.louisvilleky.gov/datasets/LOJIC::louisville-metro-ky-traffic-fatalities-and-suspected-serious-injuries-1/explore


# Data1
load DATA1
make a copy
drop ["Unnamed: 0", "COUNTY NAME", "index_right"]

# Data2 
load DATA1
make a copy
