
import pandas as pd
import numpy as np

try:
    df = pd.read_csv('AirQuality.csv', sep=';', decimal=',', engine='python', skipfooter=114)
    df = df.replace(-200, np.nan)
    target = df['NO2(GT)'].dropna()
    print("Stats for NO2(GT):")
    print(target.describe())
except Exception as e:
    print(e)
