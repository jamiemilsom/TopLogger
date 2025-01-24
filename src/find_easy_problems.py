import pandas as pd
import numpy as np
from tabulate import tabulate
from datetime import datetime
import pytz

boulders_df = pd.read_csv("data/cleaned_boulders.csv")
boulders_df = boulders_df[boulders_df["grade"] < 701]
boulders_df = boulders_df[boulders_df["grade"] > 650]
font_grades = boulders_df["font_grade"].unique()

boulders_df['inAt'] = pd.to_datetime(boulders_df['inAt'], utc=True)
boulders_df['outPlannedAt'] = pd.to_datetime(boulders_df['outPlannedAt'], utc=True)

current_time = datetime.now(pytz.UTC)

boulders_df['days_old'] = (current_time - boulders_df['inAt']).dt.days
boulders_df['days_left'] = (boulders_df['outPlannedAt'] - current_time).dt.days

boulders_df.drop(columns=["inAt", "outPlannedAt", "gradeVotesCount","ratingsAverage"], inplace=True)

grade_to_tops = {}
grade_to_age = {}
for grade in font_grades:
    grade_subset = boulders_df[boulders_df["font_grade"] == grade]
    if len(grade_subset) >= 5:  # Only consider grades with at least 5 climbs
        grade_to_tops[grade] = grade_subset["ticksCount"].median()
        grade_to_age[grade] = grade_subset["days_old"].median()
        


def normalise_tops(row):
    grade = row["font_grade"]
    if grade in grade_to_tops:
        return row["ticksCount"] / grade_to_tops[grade]
    print(f"{grade} has less than 5 climbs - normalised tops not valid")
    return np.nan

def time_normalise_tops(row):
    grade = row["font_grade"]
    if grade in grade_to_age:
        return row["ticksCount"] / (grade_to_age[grade] * grade_to_tops[grade]) * 30
    print(f"{grade} has less than 5 climbs - normalised tops not valid")
    return np.nan


boulders_df["normalised_tops"] = boulders_df.apply(normalise_tops, axis=1)
boulders_df["time_normalised_tops"] = boulders_df.apply(time_normalise_tops, axis=1)

print(
    tabulate(
        boulders_df.sort_values("normalised_tops", ascending=False).head(20),
        headers="keys",
        tablefmt="psql",
    )
)

import matplotlib.pyplot as plt
plt.boxplot([boulders_df["normalised_tops"],boulders_df['time_normalised_tops']])
plt.show()