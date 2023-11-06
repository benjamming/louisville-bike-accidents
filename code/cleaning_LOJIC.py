# Cleaning LOJIC data
import pandas as pd
import pyparsing
import pytz

from datetime import datetime, timezone
from os import chdir

chdir("/Users/bencampbell/code_louisville/capstone/louisville-bike-accidents")

DATA_IN = "data/raw/Louisville_Metro_KY_-_Traffic_Fatalities_and_Suspected_Serious_Injuries.csv"
DATA_OUT = "data/clean/LOJIC_cycling_data.csv"



# Drop unneeded columns
# Select only rows which report bicycle crashes

def drop_rows_and_columns(df:pd.DataFrame):
    df = df.drop(["X", "Y", "NAME", "AGE", "GENDER", "LINK",
                  'RampFromRdwyId', 'RampToRdwyId'], axis=1)
    # Remove unneeded columns
    df = df[(df['MODE'] == "BICYCLE") | df["DirAnalysisCode"].str.contains("BICY") == True]
    return df


# Columns to rename

renames = {'IncidentID': "incident_id",
            'AgencyName' : "investigating_agency",
            'RdwyNumber' : "roadway_number", 
            'Street' : "street", 
            'StreetDir' : "roadway_direction",
            'RoadwayName' : "roadway_name", 
            'StreetSfx' : "roadway_suffix",
            'OWNER' : "owner", 
            'ROAD_CLASSIFICATION' : 'road_classification',
            'COUNCIL_DISTRICT' : "council_district", 
            'IntersectionRdwy' : "intersection_roadway", 
            'IntersectionRdwyName' : "intersection_roadway_name",
            'BetweenStRdwy1' : 'between_street_1', 
            'BetweenStRdwyName1' : 'between_street_name_1', 
            'BetweenStRdwy2' : "between_street_2",
            'BetweenStRdwyName2': "between_street_name_2",
            'Latitude' : 'latitude',
            'Longitude' : 'longitude', 
            'Milepoint' : 'milepoint',
            'DAY_OF_WEEK' : 'day_of_week', 
            'CollisionDate' : 'collision_date', 
            'CollisionTime' : 'collision_time', 
            'HOUR_OF_DAY' : 'hour_of_day',
            'UnitsInvolved' : 'units_involved', 
            'MotorVehiclesInvolved' : "motor_vehicles_involved", 
            'Weather' : "weather",
            'RdwyConditionCode' : "roadway_condition_code",
            'HitandRun' : 'hit_and_run',
            'DirAnalysisCode' : 'directional_analysis_code',
            'MannerofCollision' : 'manner_of_collision', 
            'RdwyCharacter' : 'roadway_character', 
            'LightCondition' : "light_condition",
            'IsSecondaryCollision' : "secondary_collision", 
            'ObjectId' : "object_id",
            "MODE":"mode",
            "SEVERITY" : "severity"}

def rename_columns(df:pd.DataFrame, renames:dict) -> pd.DataFrame:
    return df.rename(renames, axis=1)


# SEVERITY column
def expand_severity_column(df:pd.DataFrame) -> pd.DataFrame:
    severity = df['SEVERITY']
    fatalities = severity.apply(lambda x:(x == "FATALITY"))
    injuries = severity.apply(lambda x:(x == "SUSPECTED SERIOUS INJURY"))

    fatalities.name = "fatality_indicator"
    injuries.name = "injury_indicator"
    return pd.concat((df, fatalities, injuries), axis=1)

# Fix time date mess

# Define some parsing expressions
integer = pyparsing.Word(pyparsing.nums).set_name("integer")
# Define integer word: a string of numeric characters 0-9

date_expr = integer("year") + '/' + integer("month") + '/' + integer('day')
time_expr_HHMM = integer("hour") + ":" + integer("minute")
time_expr_seconds = pyparsing.Literal(":") + integer("second") + "+" + integer("ms")

CollisionDate_expr = date_expr + time_expr_HHMM + time_expr_seconds.suppress()

def fix_CollisionDate(string):
    CD = CollisionDate_expr.parse_string(string).as_dict()
    CD = {key:int(value) for key, value in CD}
    timestamp =  pd.Timestamp(**CollisionDate_expr.parse_string(string).as_dict())
    return timestamp.tz_localize("UTC").tz_convert("US/Eastern")




def clean(df:pd.DataFrame) -> pd.DataFrame:
    df = drop_rows_and_columns(df)
    df = expand_severity_column(df)

    df = rename_columns(df, renames) # Do this last. Too annoying to deal with before.

    return df

if __name__ == "__main__":
    df = pd.read_csv(DATA_IN)
    df_clean = clean(df)
    df_clean.to_csv(DATA_OUT)
