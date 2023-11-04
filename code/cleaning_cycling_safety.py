# Cleaning cyclingsafety data

import pandas as pd
import os

DATA = "data/raw/cycling_safety_louisville.csv"
df = pd.read_csv(DATA)

# Drop columns I won't use.
df['U