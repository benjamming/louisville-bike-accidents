# Cleaning LOJIC data
import pandas as pd
import pyparsing
import pytz

from datetime import datetime, timezone
from os import chdir

chdir("/Users/bencampbell/code_louisville/capstone/louisville-bike-accidents")

DATA_IN = "data/raw/Louisville_Metro_KY_-_Traffic_Fatalities_and_Suspected_Serious_Injuries.csv"
DATA_OUT = "data/clean/LOJIC_cycling_data.csv"


# Columns to drop
dropping = ["X", "Y", "NAME", "AGE", "GENDER", "LINK"]
def drop_unused_columns(df:pd.DataFrame, columns:list) -> pd.DataFrame:
    return df.drop(columns, axis=1)


# Rows to drop
# Selecting only bicycle data, then dropping MODE column
def select_mode_BICYCLE(df:pd.DataFrame) -> pd.DataFrame:
    out = df[df['MODE'] == "BICYCLE"]
    return out.drop("MODE", axis=1)


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
            'RampFromRdwyId' : "ramp_from_roadway_id", 
            'RampToRdwyId' : "ramp_to_roadway_id", 
            'IsSecondaryCollision' : "secondary_collision", 
            'ObjectId' : "object_id"}

def rename_columns(df:pd.DataFrame, renames:dict) -> pd.DataFrame:
    return df.rename(renames, axis=1)

def clean(df:pd.DataFrame) -> pd.DataFrame:
    df = drop_unused_columns(df, dropping)
    df = select_mode_BICYCLE(df)
    df = rename_columns(df, renames)

    return df

if __name__ == "__main__":
    df = pd.read_csv(DATA_IN)
    df_clean = clean(df)
    df_clean.to_csv(DATA_OUT)
