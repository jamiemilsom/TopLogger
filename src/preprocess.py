import json
import pandas as pd

# Load the JSON data
with open("data/boulders.json", "r") as file:
    data = json.load(file)

climbs = data[0]["data"]["climbs"]["data"]

df = pd.DataFrame(climbs)

df["hold_color"] = df["holdColor"].apply(lambda x: x["nameLoc"])
df["wall_name"] = df["wall"].apply(lambda x: x["nameLoc"])

df = df.drop(columns=["holdColor", "wall"])

columns_order = [
    "grade",
    "gradeVotesCount",
    "ratingsAverage",
    "hold_color",
    "wall_name",
    "ticksCount",
    "inAt",
    "outPlannedAt",
]
df = df[columns_order]

grades_dict = {
    "6a": 600,
    "6a+": 617,
    "6b": 633,
    "6b+": 650,
    "6c": 667,
    "6c+": 683,
    "7a": 700,
    "7a+": 717,
    "7b": 733,
    "7b+": 750,
    "7c": 767,
    "7c+": 787,
    "8a": 800,
    "8a+": 817,
    "8b": 833,
    "8b+": 850,
    "8c": 867,
    "8c+": 887,
    "9a": 900,
}


def get_font_grade(grade_value):
    for font_grade, numeric_value in sorted(
        grades_dict.items(), key=lambda x: x[1], reverse=True
    ):
        if grade_value >= numeric_value:
            return font_grade
    return None


df = df[df["grade"] > 600]
df["font_grade"] = df["grade"].apply(get_font_grade)
print(df.tail())
df.to_csv("data/cleaned_boulders.csv", index=False)
