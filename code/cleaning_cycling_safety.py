# Cleaning cyclingsafety data

import pandas as pd
import pyparsing
import os

import logging as log

DATA_IN = "data/raw/cycling_safety_louisville.csv"
DATA_OUT = "data/clean/cycling_safety_louisville_clean.csv"

### Defining groups of columns for various purposes.

## Columns to drop
dropping_columns = ['COUNTY NAME',
                     'GPS LATITUDE DECIMAL', 'GPS LONGITUDE DECIMAL',
                    'geometry', 'index_right']

def drop_unused_columns(df:pd.DataFrame, columns:list) -> pd.DataFrame:
    """Drop a list of unneccessary columns from the dataframe."""
    log.info("Dropping unnecessary columns.")
    out = df.drop(columns, axis=1)
    return out


## Renaming section
# Lists of columns to rename
easy_column_renames = ['MASTER FILE NUMBER', 'INVESTIGATING AGENCY', 'LOCAL CODE', 'COLLISION STATUS CODE',
     'ROADWAY NUMBER', 'ROADWAY NAME', 'ROADWAY SUFFIX', 'INTERSECTION ROADWAY NAME',
    'UNITS INVOLVED', 'MOTOR VEHICLES INVOLVED', 'KILLED', 'INJURED', 'WEATHER CODE',
    'WEATHER', 'ROADWAY CONDITION CODE', 'ROADWAY CONDITION', 'ROADWAY TYPE CODE', 'ROADWAY TYPE',
    'DIRECTIONAL ANALYSIS CODE', 'DIRECTIONAL ANALYSIS',
    'MANNER OF COLLISION CODE', 'MANNER OF COLLISION',
    'ROADWAY CHARACTER CODE', 'ROADWAY CHARACTER', 'LIGHT CONDITION CODE',
    'LIGHT CONDITION', 'RAMP FROM ROADWAY ID', 'RAMP TO ROADWAY ID', "Latitude", "Longitude",
    ]

less_easy_column_renames = [
     'INTERSECTION ROADWAY #', 'INTERSECTION ROADWAY SFX', 'BETWEEN STREET ROADWAY # 1',
    'BETWEEN STREET ROADWAY NAME 1', 'BETWEEN STREET ROADWAY SFX 1',
    'BETWEEN STREET ROADWAY # 2', 'BETWEEN STREET ROADWAY NAME 2',
    'BETWEEN STREET ROADWAY SFX 2',]

misc_column_renames = {
    'BLOCK/HOUSE #': "building_number",
    'ROADWAY DIRECTION CODE': 'roadway_direction',
    'MILEPOINT DERIVED': 'milepoint', 
    'HIT & RUN INDICATOR': "hit_and_run",
    'SECONDARY COLLISION INDICATOR': "secondary_collision"}

# renaming utility functions
def _easy_rename(name:str) -> str:
    return name.replace(" ", "_").lower()

def _less_easy_rename(name:str) -> str:
    name = name.replace("STREET ROADWAY", "street")
    name = name.replace("#", 'number').replace("SFX", 'suffix')
    return _easy_rename(name)

# create a master dictionary of column names with their new renames
renames = {name:_easy_rename(name) for name in easy_column_renames}
renames.update({name:_less_easy_rename(name) for name in less_easy_column_renames})
renames.update(misc_column_renames)

# main function to rename columns
def rename_columns(df:pd.DataFrame, renames:dict) -> pd.DataFrame:
    """Rename dataframe columns according to renames dictionary."""
    log.info("Renaming columns.")
    return df.rename(renames, axis=1)


## Date/time section
# define parsing expressions and parsers.
integer = pyparsing.Word(pyparsing.nums).set_name("integer")
# integer is a pyparsing.Word which consists of a string of characters in '0123456789'

# Date column parser
date_expr = (integer("year") + '-' + integer("month") + '-' + integer("day") +
            integer("hour") + ":" + integer("minute") + ":" + integer("second").suppress())
# date_expr is a parsing expression composed of a date string and a time string.
# the date part is a sequence of integers delimited by '-'
# the time part is a sequence of integers delimited by ':'
# integer("second").suppress() ignores the seconds part of the time substring
# I don't need second-level precision for my analysis, and I doubt it's reliable anyway.

def _parse_Date(date:str) -> dict:
    parsed = date_expr.parse_string(date).as_dict()
    parsed = {key:int(value) for key, value in parsed.items()}
    return parsed

# main date/time cleaning function
def clean_date_columns(df:pd.DataFrame) -> pd.DataFrame:
    log.info("Dropping unused date/time columns")
    df = df.drop(['hour', 'minute', 'COLLISION DATE', 'COLLISION TIME'], axis=1)
    log.info("Parsing Date column and adding clean information to dataframe")
    parsed_df = pd.DataFrame(df['Date'].apply(_parse_Date).to_list())
    out = pd.concat([df, parsed_df], axis=1)
    return out.drop('Date', axis=1)


## Boolean indicators section
def clean_boolean_indicators(df:pd.DataFrame) -> pd.DataFrame:
    for name in ['hit_and_run', 'secondary_collision']:
        df[name] = df[name].apply(lambda x:True if x == "Y" else False)
    return df



# main cleaning function
def clean(df:pd.DataFrame) -> pd.DataFrame:
    df = drop_unused_columns(df, dropping_columns)
    df = rename_columns(df, renames)
    df = clean_date_columns(df)
    df = clean_boolean_indicators(df)

    return df

# main script function
def main():
    df = pd.read_csv(DATA_IN)
    df_clean = clean(df)
    df_clean.to_csv(DATA_OUT)

if __name__ == "__main__":
    main()
