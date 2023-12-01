# Merge my two sets of data. 

import pandas as pd
from numpy import intersect1d
from operator import attrgetter
from os import path
from pandasql import sqldf


# Bicycle accident data:
path_to_cycling_safety_cleaned = "../../data/preclean/cycling_safety_louisville_cleaned.csv"
path_to_LOJIC_cleaned = "../../data/preclean/LOJIC_cycling_data_cleaned.csv"

assert path.exists(path_to_cycling_safety_cleaned)
assert path.exists(path_to_LOJIC_cleaned)

# Intersections with lighted traffic signals.
path_to_signalized_intersections = "../../data/raw/Jefferson_County_KY_Signalized_Intersections.csv"

# Path to write CSV for combined data.
CSV_OUT = "../../data/clean/bike_accidents.csv"


def merge_accident_data() -> pd.DataFrame:
    """Combine the two bicycle accident datasets to form one set for analysis."""
    # Load in the precleaned data
    CSAFE = pd.read_csv(path_to_cycling_safety_cleaned)
    LOJIC = pd.read_csv(path_to_LOJIC_cleaned)

    # truncate LOJIC date overlap
    # There is no information in LOJIC data that doesn't already exist in CSAFE data
    date_intersect = intersect1d(CSAFE['date'], LOJIC['date'])
    to_remove = LOJIC[LOJIC['date'].isin(date_intersect)].index
    LOJIC = LOJIC.drop(to_remove, axis=0)

    # normalize LOJIC['roadway_type']
    # Changing some of the values to match CSAFE data
    LOJIC['roadway_type'] = LOJIC['roadway_type'].replace(
        {"SHIVELY":"LOCAL ROAD", "BROWNSBORO FARM":"LOCAL ROAD", "METRO":"LOCAL ROAD"})
    
    # concatenate the two datasets
    out = pd.concat((CSAFE, LOJIC), ignore_index=True)
    # Create new ID colum for each accident. 
    out['accident_id'] = out.index + 0
    return out


def split_up_timestamps(df:pd.DataFrame) -> pd.DataFrame:
    """Create individual columns with values for year, month, day, hour, and minute of accident.

    This information is stored as pandas.Timestamp objects, but it is easier to examine the data
    if all this information is split up into its own columns."""

    # We are reading in the precleaned data from a CSV, when writing a pandas.Timestamp to a CSV,
    # it is converted to a string representation for storage. We have to convert these strings back
    # into pandas.Timestamp objects if we want to use them as such.
    dates = df['date'] = df['date'].apply(pd.Timestamp)
    # Create a DataFrame from the timestamps
    timesplit = dates.transform({name:attrgetter(name) for name in "year month day hour minute".split()})
    # Join that DataFrame to our original data. Now we have both the original 'date' column, 
    # and 'year', 'month', 'day', 'hour', 'minute' columns we can use.
    return df.join(timesplit)


def add_signalized_intersection_column(df:pd.DataFrame) -> pd.DataFrame:
    """Create lighted_signal_indicator column
    
    Pull in information about intersections with lighted signals, find accident reports that occur
    at those intersections, and make a column to indicate when an intersection has a traffic light."""
    # Read in CSV of signalized intersection data. I only need a few columns from this data to do
    # this join
    SIGNALS = pd.read_csv(path_to_signalized_intersections)[["MAINSTREET", "CROSSSTREET", "ROUTE"]]
    # Create lighted_signal_indicator column. False by default. 
    df['lighted_signal_indicator'] = False

    # SQL query to find appropriate accident reports / rows.
    selection = sqldf("""SELECT DISTINCT df.accident_id
                           FROM df JOIN SIGNALS 
                           ON (df.roadway_name == SIGNALS.MAINSTREET 
                                OR df.roadway_number == SIGNALS.MAINSTREET)
                           AND SIGNALS.CROSSSTREET == df.intersection_roadway_name""", locals())
    
    # Update lighted_signal_indicator column for the accident reports we found above.
    for row in selection.accident_id:
        df.at[row, 'lighted_signal_indicator'] = True
    return df

if __name__ == "__main__":
    df = merge_accident_data()
    df = split_up_timestamps(df)
    df = add_signalized_intersection_column(df)
    df.to_csv(CSV_OUT, index=0)



    
    