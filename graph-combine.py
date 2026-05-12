import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

files = {
    "May 5": "Monday CSV.csv",
    "May 6": "Tues Day CSV.csv",
    "May 7": "Wed Data.csv",
    "May 8": "Thursday.csv",
    "May 9": "FridayNight Data.csv",
}

metrics = ["light", "sound", "temperature", "dust", "fan", "motion"]
daily_data = {metric: [] for metric in metrics}

for day, file in files.items():
    df = pd.read_csv(file)
    df.columns = df.columns.str.strip()

    df["created_at"] = (
        df["created_at"]
        .astype(str)
        .str.replace("'", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.replace("  ", " ", regex=False)
        .str.strip()
    )

    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df = df.dropna(subset=["created_at"])

    # Only use data from 00:00 to 03:00
    df = df[(df["created_at"].dt.hour >= 0) & (df["created_at"].dt.hour < 3)]

    for metric in metrics:
        df[metric] = (
            df[metric]
            .astype(str)
            .str.replace("'", "", regex=False)
            .str.replace(",", "", regex=False)
            .str.strip()
        )
        df[metric] = pd.to_numeric(df[metric], errors="coerce").fillna(0)

        if metric in ["fan", "motion"]:
            value = df[metric].sum()
        else:
            value = df[metric].mean()

        daily_data[metric].append(value)

dates = list(files.keys())
x = np.arange(len(dates))
width = 0.12

plt.figure(figsize=(14, 7))

for i, metric in enumerate(metrics):
    plt.bar(x + i * width, daily_data[metric], width, label=metric.capitalize())

plt.xticks(x + width * 2.5, dates)
plt.title("Sleep Environment Analysis Bar Chart (00:00–03:00)")
plt.xlabel("Date")
plt.ylabel("Average Sensor Values / Counts")
plt.legend()
plt.grid(axis="y")

plt.tight_layout()
plt.savefig("combined_bar_chart.png", dpi=300)
plt.show()
