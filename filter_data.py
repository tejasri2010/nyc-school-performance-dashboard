import pandas as pd

df = pd.read_csv('./School_Quality_Reports_Data.csv')

df = df[df['School Year'].astype(str) == '2022']
# df = df[(df['Number of Students'] >= 184) & (df['Number of Students'] <= 384)]
# df = df[df['School Type'].isin(['High School', 'High School Transfer', 'Middle', 'Elementary', 'K-8'])]

df = df.dropna()

export_path = "./filtered_school_data.csv"
df.to_csv(export_path, index=False)