# Cleaning cyclingsafety data

import pandas as pd
import pyparsing
from os import path, chdir

import logging as log

DATA_IN = "data/raw/cycling_safety_louisville.csv"
DATA_OUT = "data/preclean/cycling_safety_louisville_cleaned.csv"

assert path.exists(DATA_IN)

### Defining groups of columns for various purposes.
# With functions that will operate over them. 

## Columns to drop
dropping_columns = ["Unnamed: 0", 'COUNTY NAME',
                     'GPS LATITUDE DECIMAL', 'GPS LONGITUDE DECIMAL',
                    'geometry', 'index_right',
                    'hour', 'minute', 'COLLISION DATE', 'COLLISION TIME',
                    "RAMP TO ROADWAY ID", "RAMP FROM ROADWAY ID",
                    'WEATHER CODE', 'COLLISION STATUS CODE',
                    'ROADWAY CONDITION CODE', 'ROADWAY TYPE CODE',
                    'DIRECTIONAL ANALYSIS CODE','MANNER OF COLLISION CODE',
                     'ROADWAY CHARACTER CODE', 'LIGHT CONDITION CODE',
                       'MASTER FILE NUMBER', 'LOCAL CODE',
                    'INTERSECTION ROADWAY SFX', 'BETWEEN STREET ROADWAY SFX 1', 'BETWEEN STREET ROADWAY SFX 2' ]

def drop_unused_columns(df:pd.DataFrame, columns:list) -> pd.DataFrame:
    """Drop a list of unneccessary columns from the dataframe."""
    log.info("Dropping unnecessary columns.")
    return df.drop(columns, axis=1)


## Renaming section
# Lists of columns to rename
column_renames = {#'MASTER FILE NUMBER': 'master_file_number', # dropped
                'INVESTIGATING AGENCY': 'investigating_agency',
                #'LOCAL CODE': 'local_code', # dropped
                #'COLLISION STATUS CODE': 'collision_status_code',
                'ROADWAY NUMBER': 'roadway_number',
                'ROADWAY NAME': 'roadway_name',
                'ROADWAY SUFFIX': 'roadway_suffix',
                'INTERSECTION ROADWAY NAME': 'intersection_roadway_name',
                'UNITS INVOLVED': 'units_involved',
                'MOTOR VEHICLES INVOLVED': 'motor_vehicles_involved',
                #'KILLED': 'killed', # dropping this after creating fatality_indicator
                #'INJURED': 'injured', # dropping this after creating injury_indicator
                #'WEATHER CODE': 'weather_code',
                'WEATHER': 'weather',
                #'ROADWAY CONDITION CODE': 'roadway_condition_code', #dropped
                'ROADWAY CONDITION': 'roadway_condition',
                #'ROADWAY TYPE CODE': 'roadway_type_code', #dropped
                'ROADWAY TYPE': 'roadway_type',
                #'DIRECTIONAL ANALYSIS CODE': 'directional_analysis_code', #dropped
                'DIRECTIONAL ANALYSIS': 'directional_analysis',
                #'MANNER OF COLLISION CODE': 'manner_of_collision_code',
                'MANNER OF COLLISION': 'manner_of_collision',
                #'ROADWAY CHARACTER CODE': 'roadway_character_code',
                'ROADWAY CHARACTER': 'roadway_character',
                #'LIGHT CONDITION CODE': 'light_condition_code',
                'LIGHT CONDITION': 'light_condition',
                #'RAMP FROM ROADWAY ID': 'ramp_from_roadway_id', #dropped
                #'RAMP TO ROADWAY ID': 'ramp_to_roadway_id', # dropped
                'Latitude': 'latitude',
                'Longitude': 'longitude',
                'Date': 'date',
                    # Dropping SFX / suffix columns from these for now.
                'INTERSECTION ROADWAY #': 'intersection_roadway_number',
                #'INTERSECTION ROADWAY SFX': 'intersection_roadway_suffix',
                'BETWEEN STREET ROADWAY # 1': 'between_street_number_1',
                'BETWEEN STREET ROADWAY NAME 1': 'between_street_name_1',
                #'BETWEEN STREET ROADWAY SFX 1': 'between_street_suffix_1',
                'BETWEEN STREET ROADWAY # 2': 'between_street_number_2',
                'BETWEEN STREET ROADWAY NAME 2': 'between_street_name_2',
                #'BETWEEN STREET ROADWAY SFX 2': 'between_street_suffix_2'
 }

misc_column_renames = {
    'BLOCK/HOUSE #': "building_number",
    'ROADWAY DIRECTION CODE': 'roadway_direction',
    'MILEPOINT DERIVED': 'milepoint', 
    'HIT & RUN INDICATOR': "hit_and_run_indicator",
    'SECONDARY COLLISION INDICATOR': "secondary_collision_indicator"}

column_renames.update(misc_column_renames)

# main function to rename columns
def rename_columns(df:pd.DataFrame, renames:dict) -> pd.DataFrame:
    """Rename dataframe columns according to renames dictionary."""
    # Run last. Other functions depend on original column names.
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

def parse_Date(date:str) -> dict:
    parsed = date_expr.parse_string(date).as_dict()
    parsed = {key:int(value) for key, value in parsed.items()}
    return pd.Timestamp(**parsed, tz="US/Eastern") # add timezone info to the timestamps
                                                    # makes it compatible with other data

# Main date/time cleaning function
def clean_date_columns(df:pd.DataFrame) -> pd.DataFrame:
    log.info("Parsing Date column and adding clean information to dataframe")
    df['Date'] = df['Date'].apply(parse_Date)
    return df


## Boolean indicators section
def clean_boolean_indicators(df:pd.DataFrame) -> pd.DataFrame:
    for name in ["HIT & RUN INDICATOR", 'SECONDARY COLLISION INDICATOR']:
        df[name] = df[name].apply(lambda x:True if x == "Y" else False)
    return df

## Fix BLOCK/HOUSE #  (building_number in cleaned data)
def clean_building_number(df:pd.DataFrame) -> pd.DataFrame:
    df['BLOCK/HOUSE #'] = df['BLOCK/HOUSE #'].replace(to_replace='     ', value=pd.NA)
    building_numbers = df['BLOCK/HOUSE #'].dropna().apply(lambda x:str(int(float(x))))
    df['BLOCK/HOUSE #'].update(building_numbers)
    return df

def clean_trailing_whitespace_columns(df:pd.DataFrame) -> pd.DataFrame:
    columns = ['ROADWAY SUFFIX', 'ROADWAY DIRECTION CODE', 'INTERSECTION ROADWAY #', 'ROADWAY NUMBER']
    for column in columns:
        df[column] = df[column].str.strip()
    return df

## Make fatality_indicator, injury indicator columns
def make_indicator_columns(df:pd.DataFrame) -> pd.DataFrame:
    df['injury_indicator'] = df['INJURED'].apply(lambda x:bool(x > 0))
    df['fatality_indicator'] = df['KILLED'].apply(lambda x:bool(x > 0))
    return df.drop(["KILLED", "INJURED"], axis=1) # Drop KILLED and INJURED

## Make day_of_week column
def make_day_of_week(df:pd.DataFrame) -> pd.DataFrame:
    # must be run *after* clean_date_columns
    df['day_of_week'] = df['Date'].apply(lambda x:x.day_name().upper())
    return df

def set_index(df:pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(by='Date').reset_index().drop('index', axis=1)

def last_steps(df:pd.DataFrame) -> pd.DataFrame:
    df = set_index(df)
    df = rename_columns(df, column_renames)
    return df


### Main cleaning function
def clean(df:pd.DataFrame) -> pd.DataFrame:
    df = drop_unused_columns(df, dropping_columns)
    df = clean_date_columns(df)
    df = clean_boolean_indicators(df)
    df = clean_building_number(df)
    df = clean_trailing_whitespace_columns(df)
    df = make_indicator_columns(df)
    df = make_day_of_week(df)

    df = last_steps(df)

    return df


### Main script function
def main():
    df = pd.read_csv(DATA_IN)
    df_clean = clean(df)
    df_clean.to_csv(DATA_OUT, index=0)

if __name__ == "__main__":
    main()
