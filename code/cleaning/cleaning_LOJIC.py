# Cleaning LOJIC data
import pandas as pd
import pyparsing
import pytz

from datetime import datetime, timezone
from os import chdir

chdir("/Users/bencampbell/code_louisville/capstone/louisville-bike-accidents")

DATA_IN = "data/raw/Louisville_Metro_KY_-_Traffic_Fatalities_and_Suspected_Serious_Injuries.csv"
DATA_OUT = "data/preclean/LOJIC_cycling_data.csv"



# Drop unneeded columns
# Select only rows which report bicycle crashes

DROPPING = ["X", "Y", "NAME", "AGE", "GENDER", "LINK", 'RampFromRdwyId', 'RampToRdwyId', 
            "IncidentID", "ObjectId", 
            'COUNCIL_DISTRICT', 'ROAD_CLASSIFICATION'] # Removing for now; bring back later if needed

def drop_rows_and_columns(df:pd.DataFrame):
    df = df.drop(DROPPING, axis=1)
    # Remove unneeded columns
    df = df[(df['MODE'] == "BICYCLE") | df["DirAnalysisCode"].str.contains("BICY") == True]
    # Select only rows that report bicycle accidents.
    df = df.drop("MODE", axis=1)
    # Drop MODE column as it is no longer needed
    return df


# Columns to rename

column_renames = {#'IncidentID': "incident_id", # dropped
            'AgencyName' : "investigating_agency",
            'RdwyNumber' : "roadway_number", 
            'Street' : "building_number", 
            'StreetDir' : "roadway_direction",
            'RoadwayName' : "roadway_name", 
            'StreetSfx' : "roadway_suffix",
            'OWNER' : "roadway_type", 
            #'ROAD_CLASSIFICATION' : 'road_classification', # dropping. Can't do much with this. 
            #'COUNCIL_DISTRICT' : "council_district", # dropping until needed
            'IntersectionRdwy' : "intersection_roadway_number", 
            'IntersectionRdwyName' : "intersection_roadway_name",
            'BetweenStRdwy1' : 'between_street_number_1', 
            'BetweenStRdwyName1' : 'between_street_name_1', 
            'BetweenStRdwy2' : "between_street_number_2",
            'BetweenStRdwyName2': "between_street_name_2",
            'Latitude' : 'latitude',
            'Longitude' : 'longitude', 
            'Milepoint' : 'milepoint',
            'DAY_OF_WEEK' : 'day_of_week', 
            'CollisionDate' : 'date', 
            'UnitsInvolved' : 'units_involved', 
            'MotorVehiclesInvolved' : "motor_vehicles_involved", 
            'Weather' : "weather",
            'RdwyConditionCode' : "roadway_condition", # dropped can't do much with this
            'HitandRun' : 'hit_and_run_indicator',
            'DirAnalysisCode' : 'directional_analysis',
            'MannerofCollision' : 'manner_of_collision', 
            'RdwyCharacter' : 'roadway_character', 
            'LightCondition' : "light_condition",
            'IsSecondaryCollision' : "secondary_collision_indicator", 
            #'ObjectId' : "object_id", # dropped
            # "MODE":"mode", # dropped
}

def rename_columns(df:pd.DataFrame, renames:dict) -> pd.DataFrame:
    # Do this last. Other functions depend on original column names
    return df.rename(renames, axis=1)


# SEVERITY column
def expand_severity_column(df:pd.DataFrame) -> pd.DataFrame:
    severity = df['SEVERITY']
    fatalities = severity.apply(lambda x:(x == "FATALITY"))
    injuries = severity.apply(lambda x:(x == "SUSPECTED SERIOUS INJURY"))

    fatalities.name = "fatality_indicator"
    injuries.name = "injury_indicator"
    out =  pd.concat((df, fatalities, injuries), axis=1)
    out = out.drop("SEVERITY", axis=1)
    return out

# Fix time date mess

# Define some parsing expressions
integer = pyparsing.Word(pyparsing.nums).set_name("integer")
# Define integer word: a string of numeric characters 0-9

date_expr = integer("year") + '/' + integer("month") + '/' + integer('day')
time_expr_HHMM = integer("hour") + ":" + integer("minute")
time_expr_seconds = pyparsing.Literal(":") + integer("second") + "+" + integer("ms")

CollisionDate_expr = date_expr + time_expr_HHMM + time_expr_seconds.suppress()

def fix_CollisionDate_value(string):
    CD = CollisionDate_expr.parse_string(string).as_dict()
    CD = {key:int(value) for key, value in CD.items()}
    timestamp =  pd.Timestamp(**CD)
    return timestamp.tz_localize("UTC").tz_convert("US/Eastern")

def fix_CollisionDate(df:pd.DataFrame) -> pd.DataFrame:
    df['CollisionDate'] = df['CollisionDate'].apply(fix_CollisionDate_value)
    return df

def fix_timedate_mess(df:pd.DataFrame) -> pd.DataFrame:
    df = fix_CollisionDate(df)
    return df.drop(['CollisionTime', 'HOUR_OF_DAY'], axis=1)

def set_index(df:pd.DataFrame) -> pd.DataFrame:
    return df.sort_values(by='CollisionDate').reset_index().drop('index', axis=1)

def last_steps(df:pd.DataFrame) -> pd.DataFrame:
    df = set_index(df)
    df = rename_columns(df, column_renames)
    return df

def clean(df:pd.DataFrame) -> pd.DataFrame:
    df = drop_rows_and_columns(df)
    df = expand_severity_column(df)
    df = fix_timedate_mess(df)
    df = last_steps(df)
    return df

if __name__ == "__main__":
    df = pd.read_csv(DATA_IN)
    df_clean = clean(df)
    df_clean.to_csv(DATA_OUT, index=0)
