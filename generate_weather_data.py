import pandas as pd
import numpy as np

# Generate a date range from Jan 1 to Dec 31, 2023
date_range = pd.date_range(start="2023-01-01", end="2023-06-31", freq="D")

# Set a random seed for reproducibility
np.random.seed(0)

# Generate synthetic weather data
data = {
    "Date": date_range,
    "Temperature": np.random.normal(loc=20, scale=5, size=len(date_range)).round(1),
    "Rainfall": np.random.exponential(scale=1.0, size=len(date_range)).round(1),
    "Humidity": np.random.randint(60, 100, size=len(date_range))
}

# Create a DataFrame and save to CSV
df = pd.DataFrame(data)
df.to_csv("weather_data.csv", index=False)

print("✅ weather_data.csv has been generated with data from Jan to Dec 2023.")
