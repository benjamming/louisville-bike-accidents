# Cleaning cyclingsafety data

import pandas as pd
import pyparsing
import os

import logging as log

DATA_IN = "data/raw/cycling_safety_louisville.csv"
DATA_OUT = "data/clean/cycling_safety_louisville_clean.csv"

### Defining groups of columns for various purposes.
# With functions that will operate over them. 

## Columns to drop
dropping_columns = ["Unnamed: 0", 'COUNTY NAME',
                     'GPS LATITUDE DECIMAL', 'GPS LONGITUDE DECIMAL',
                    'geometry', 'index_right',
                    'hour', 'minute', 'COLLISION DATE', 'COLLISION TIME',
                    "RAMP TO ROADWAY ID", "RAMP FROM ROADWAY ID"]

def drop_unused_columns(df:pd.DataFrame, columns:list) -> pd.DataFrame:
    """Drop a list of unneccessary columns from the dataframe."""
    log.info("Dropping unnecessary columns.")
    return df.drop(columns, axis=1)


## Renaming section
# Lists of columns to rename
column_renames = {'MASTER FILE NUMBER': 'master_file_number',
                'INVESTIGATING AGENCY': 'investigating_agency',
                'LOCAL CODE': 'local_code',
                'COLLISION STATUS CODE': 'collision_status_code',
                'ROADWAY NUMBER': 'roadway_number',
                'ROADWAY NAME': 'roadway_name',
                'ROADWAY SUFFIX': 'roadway_suffix',
                'INTERSECTION ROADWAY NAME': 'intersection_roadway_name',
                'UNITS INVOLVED': 'units_involved',
                'MOTOR VEHICLES INVOLVED': 'motor_vehicles_involved',
                'KILLED': 'killed',
                'INJURED': 'injured',
                'WEATHER CODE': 'weather_code',
                'WEATHER': 'weather',
                'ROADWAY CONDITION CODE': 'roadway_condition_code',
                'ROADWAY CONDITION': 'roadway_condition',
                'ROADWAY TYPE CODE': 'roadway_type_code',
                'ROADWAY TYPE': 'roadway_type',
                'DIRECTIONAL ANALYSIS CODE': 'directional_analysis_code',
                'DIRECTIONAL ANALYSIS': 'directional_analysis',
                'MANNER OF COLLISION CODE': 'manner_of_collision_code',
                'MANNER OF COLLISION': 'manner_of_collision',
                'ROADWAY CHARACTER CODE': 'roadway_character_code',
                'ROADWAY CHARACTER': 'roadway_character',
                'LIGHT CONDITION CODE': 'light_condition_code',
                'LIGHT CONDITION': 'light_condition',
                #'RAMP FROM ROADWAY ID': 'ramp_from_roadway_id', #dropped
                #'RAMP TO ROADWAY ID': 'ramp_to_roadway_id', # dropped
                'Latitude': 'latitude',
                'Longitude': 'longitude',
                'Date': 'date',
                'INTERSECTION ROADWAY #': 'intersection_roadway_number',
                'INTERSECTION ROADWAY SFX': 'intersection_roadway_suffix',
                'BETWEEN STREET ROADWAY # 1': 'between_street_number_1',
                'BETWEEN STREET ROADWAY NAME 1': 'between_street_name_1',
                'BETWEEN STREET ROADWAY SFX 1': 'between_street_suffix_1',
                'BETWEEN STREET ROADWAY # 2': 'between_street_number_2',
                'BETWEEN STREET ROADWAY NAME 2': 'between_street_name_2',
                'BETWEEN STREET ROADWAY SFX 2': 'between_street_suffix_2'
 }

misc_column_renames = {
    'BLOCK/HOUSE #': "building_number",
    'ROADWAY DIRECTION CODE': 'roadway_direction',
    'MILEPOINT DERIVED': 'milepoint', 
    'HIT & RUN INDICATOR': "hit_and_run",
    'SECONDARY COLLISION INDICATOR': "secondary_collision"}

column_renames.update(misc_column_renames)

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

def parse_Date(date:str) -> dict:
    parsed = date_expr.parse_string(date).as_dict()
    parsed = {key:int(value) for key, value in parsed.items()}
    return pd.Timestamp(**parsed)

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
    building_numbers = df['BLOCK/HOUSE #']
    building_numbers = building_numbers.replace(to_replace='     ', value=pd.NA)
    building_numbers = building_numbers.dropna().apply(lambda x:str(int(float(x))))
    df['BLOCK/HOUSE #'].update(building_numbers)
    return df

## Make fatality_indicator, injury indicator columns
def make_indicator_columns(df:pd.DataFrame) -> pd.DataFrame:
    ...
    return df


### Main cleaning function
def clean(df:pd.DataFrame) -> pd.DataFrame:
    df = drop_unused_columns(df, dropping_columns)
    df = clean_date_columns(df)
    df = clean_boolean_indicators(df)
    df = clean_building_number(df)

    df = rename_columns(df, column_renames)

    return df


### Main script function
def main():
    df = pd.read_csv(DATA_IN)
    df_clean = clean(df)
    df_clean.to_csv(DATA_OUT, index=0)

if __name__ == "__main__":
    main()
