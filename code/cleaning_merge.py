# Merge my two sets of data. 

import pandas as pd
from os import chdir

chdir("/Users/bencampbell/code_louisville/capstone/louisville-bike-accidents")


path_to_cycling_safety_cleaned = "data/clean/cycling_safety_louisville_clean.csv"
path_to_LOJIC_cleaned = "data/clean/LOJIC_cycling_data.csv"

CSAFE = pd.read_csv(path_to_cycling_safety_cleaned)
LOJIC = pd.read_csv(path_to_LOJIC_cleaned)

# Data sets overlap somewhat. 

def normalize_LOJIC_roadway_type() -> None: #NOT DONE
    LOJIC['roadway_type'] = LOJIC['roadway_type'].replace(
        {"SHIVELY":"LOCAL ROAD", "BROWNSBORO FARM":"LOCAL ROAD", "METRO":"LOCAL ROAD"})