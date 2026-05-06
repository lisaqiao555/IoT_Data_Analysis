import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# ==================================================
# CHECK INPUT
# ==================================================
if len(sys.argv) < 2:
    print("Usage: python graph.py your_file.csv")
    sys.exit(1)

csv_file = sys.argv[1]

# ==================================================
# READ CSV
# ==================================================
df = pd.read_csv(csv_file)

# ==================================================
# CONVERT TIME
# ==================================================
df["created_at"] = pd.to_datetime(df["created_at"])

# Hourly grouping
df["hour"] = df["created_at"].dt.strftime("%m-%d %H")

# ==================================================
# OUTPUT FOLDER
# ==================================================
output_dir = Path("graphs")
output_dir.mkdir(exist_ok=True)

# ==================================================
# HOURLY DATA
# ==================================================
temperature_hourly = (
    df.groupby("hour")["temperature"]
    .mean()
    .reset_index()
)

sound_hourly = (
    df.groupby("hour")["sound"]
    .mean()
    .reset_index()
)

motion_hourly = (
    df.groupby("hour")["motion"]
    .sum()
    .reset_index()
)

fan_hourly = (
    df.groupby("hour")["fan"]
    .mean()
    .reset_index()
)

# ==================================================
# 1. SOUND OVER TIME
# ==================================================
plt.figure(figsize=(10, 5))

plt.plot(
    sound_hourly["hour"],
    sound_hourly["sound"],
    color="blue",
    marker="o",
    linewidth=2.5
)

plt.xlabel("Time (Hourly)")
plt.ylabel("Average Sound Level")

plt.title("Sound Over Time")

plt.xticks(rotation=45)

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    output_dir / "1_sound_over_time.png",
    dpi=300
)

plt.close()

# ==================================================
# 2. MOTION ACTIVITY
# ==================================================
plt.figure(figsize=(10, 5))

plt.bar(
    motion_hourly["hour"],
    motion_hourly["motion"],
    color="#4C72B0"
)

plt.xlabel("Time (Hourly)")
plt.ylabel("Motion Count")

plt.title("Motion Activity")

plt.xticks(rotation=45)

plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    output_dir / "2_motion_activity.png",
    dpi=300
)

plt.close()

# ==================================================
# 3. FAN ON/OFF BEHAVIOR
# ==================================================
plt.figure(figsize=(10, 5))

plt.plot(
    fan_hourly["hour"],
    fan_hourly["fan"],
    color="#7B1FA2",
    marker="s",
    linewidth=2.5
)

plt.fill_between(
    fan_hourly["hour"],
    fan_hourly["fan"],
    alpha=0.2,
    color="#BA68C8"
)

plt.xlabel("Time (Hourly)")
plt.ylabel("Fan Status")

plt.title("Fan ON/OFF Behavior")

plt.yticks([0, 1], ["OFF", "ON"])

plt.xticks(rotation=45)

plt.grid(True, alpha=0.3)

plt.tight_layout()

plt.savefig(
    output_dir / "3_fan_behavior.png",
    dpi=300
)

plt.close()

# ==================================================
# 4. TEMPERATURE + FAN BEHAVIOR
# ==================================================
fig, ax1 = plt.subplots(figsize=(12, 6))

# Temperature line
ax1.plot(
    temperature_hourly["hour"],
    temperature_hourly["temperature"],
    color="blue",
    marker="o",
    linewidth=2.5,
    label="Temperature"
)

# Threshold lines
ax1.axhline(
    26,
    color="red",
    linestyle="--",
    linewidth=2,
    label="Fan ON Threshold (26°C)"
)

ax1.axhline(
    24,
    color="green",
    linestyle="--",
    linewidth=2,
    label="Fan OFF Threshold (24°C)"
)

ax1.set_xlabel("Time (Hourly)")
ax1.set_ylabel("Temperature (°C)", color="blue")

ax1.tick_params(axis="y", labelcolor="blue")

ax1.grid(True, alpha=0.3)

# Fan status second axis
ax2 = ax1.twinx()

ax2.step(
    fan_hourly["hour"],
    fan_hourly["fan"],
    where="mid",
    color="#7B1FA2",
    linewidth=3,
    label="Fan Status"
)

ax2.set_ylabel("Fan Status", color="#7B1FA2")

ax2.set_yticks([0, 1])

ax2.set_yticklabels(["OFF", "ON"])

ax2.tick_params(axis="y", labelcolor="#7B1FA2")

# Combine legends
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(
    lines1 + lines2,
    labels1 + labels2,
    loc="upper left"
)

plt.title("Temperature and Fan Behavior vs Time")

plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    output_dir / "4_temperature_fan_threshold.png",
    dpi=300
)

plt.close()

# ==================================================
# DONE
# ==================================================
print("\nGraphs generated successfully!")
print("Saved in folder: graphs/")
print("\nGenerated files:")
print("1_sound_over_time.png")
print("2_motion_activity.png")
print("3_fan_behavior.png")
print("4_temperature_fan_threshold.png")