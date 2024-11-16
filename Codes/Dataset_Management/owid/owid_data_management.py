import pandas as pd

df = pd.read_csv("datasets/mainDashboard/owid-covid-data.csv")

df = df[df["iso_code"] == "THA"]

df.to_csv("datasets/mainDashboard/owid-Thailand.csv")

