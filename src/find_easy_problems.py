import pandas as pd
import numpy as np
from tabulate import tabulate

boulders_df = pd.read_csv("data/cleaned_boulders.csv")
boulders_df = boulders_df[boulders_df["grade"] < 701]
boulders_df = boulders_df[boulders_df["grade"] > 650]
font_grades = boulders_df["font_grade"].unique()

grade_to_tops = {}
for grade in font_grades:
    grade_subset = boulders_df[boulders_df["font_grade"] == grade]
    if len(grade_subset) >= 5:  # Only consider grades with at least 5 climbs
        grade_to_tops[grade] = grade_subset["ticksCount"].median()


def normalize_tops(row):
    grade = row["font_grade"]
    if grade in grade_to_tops:
        return row["ticksCount"] / grade_to_tops[grade]
    print(f"{grade} has less than 5 climbs - normalised tops not valid")
    return np.nan


boulders_df["normalised_tops"] = boulders_df.apply(normalize_tops, axis=1)

print(
    tabulate(
        boulders_df.sort_values("normalised_tops", ascending=False).head(20),
        headers="keys",
        tablefmt="psql",
    )
)
