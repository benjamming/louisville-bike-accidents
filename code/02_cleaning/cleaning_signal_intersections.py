# Cleaning signalized intersection data
import pandas as pd
from os import chdir

chdir("/Users/bencampbell/code_louisville/capstone/louisville-bike-accidents")

DATAIN = "data/raw/Jefferson_County_KY_Signalized_Intersections.csv"
DATAOUT = "data/preclean/signalized_intersections.csv"

dropping = ["UNITID", "SIGID", "OWNER2",
            "TIMES",  "DESCRIPTION", "INTID", "ATMSID"]

renames = {"X":"longitude",
            "Y":"latitude",
            "MAINSTREET":"main_street",
            "CROSSSTREET":"cross_street",
            "ROUTE":"route_number",
            "MILEPOINT":"milepoint",
            "OWNER":"owner",
            "TYPE":"type"}

def clean(df:pd.DataFrame) -> pd.DataFrame:
    df = df.drop(dropping, axis=1)
    df = df.rename(renames, axis=1)
    return df

if __name__ == "__main__":
    df = pd.read_csv(DATAIN)
    df = clean(df)
    df.to_csv(DATAOUT, index=0)