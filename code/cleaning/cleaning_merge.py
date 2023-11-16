# Merge my two sets of data. 

import pandas as pd
from numpy import intersect1d
from os import chdir, path

chdir("/Users/bencampbell/code_louisville/capstone/louisville-bike-accidents")


path_to_cycling_safety_cleaned = "data/preclean/cycling_safety_louisville_clean.csv"
path_to_LOJIC_cleaned = "data/preclean/LOJIC_cycling_data.csv"

CSV_OUT = "data/clean/cycling_accidents.csv"

def create_merge() -> pd.DataFrame:
    CSAFE = pd.read_csv(path_to_cycling_safety_cleaned)
    LOJIC = pd.read_csv(path_to_LOJIC_cleaned)

    #truncate LOJIC date overlap
    date_intersect = intersect1d(CSAFE['date'], LOJIC['date'])
    to_remove = LOJIC[LOJIC['date'].isin(date_intersect)].index
    LOJIC = LOJIC.drop(to_remove, axis=0)

    # normalize LOJIC['roadway_type']
    LOJIC['roadway_type'] = LOJIC['roadway_type'].replace(
        {"SHIVELY":"LOCAL ROAD", "BROWNSBORO FARM":"LOCAL ROAD", "METRO":"LOCAL ROAD"})
    
    # concatenate data
    return pd.concat((CSAFE, LOJIC), ignore_index=True)

if __name__ == "__main__":
    df = create_merge()
    df.to_csv(CSV_OUT, index=0)



    
    