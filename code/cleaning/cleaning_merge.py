# Merge my two sets of data. 

import pandas as pd
from numpy import intersect1d
from operator import attrgetter
from os import chdir, path

chdir("/Users/bencampbell/code_louisville/capstone/louisville-bike-accidents")


path_to_cycling_safety_cleaned = "data/preclean/cycling_safety_louisville_clean.csv"
path_to_LOJIC_cleaned = "data/preclean/LOJIC_cycling_data.csv"

CSV_OUT = "data/clean/bike_accidents.csv"

def merge_accident_data() -> pd.DataFrame:
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
    out = pd.concat((CSAFE, LOJIC), ignore_index=True)

    # Create new ID colum for each accident
    out['id'] = out.index + 0
    return out


def split_up_timestamps(df:pd.DataFrame) -> pd.DataFrame:
    dates = df['date'] = df['date'].apply(pd.Timestamp)
    timesplit = dates.transform({name:attrgetter(name) for name in "year month day hour minute".split()})
    return df.join(timesplit)

if __name__ == "__main__":
    df = merge_accident_data()
    df = split_up_timestamps(df)
    df.to_csv(CSV_OUT, index=0)



    
    