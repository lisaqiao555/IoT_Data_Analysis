import pandas as pd
import matplotlib.pyplot as plt
import os
import sys

if len(sys.argv) < 2:
    print("Usage: python graph.py your_file.csv")
    sys.exit()

csv_file = sys.argv[1]

os.makedirs("graphs", exist_ok=True)

df = pd.read_csv(csv_file)

df.columns = df.columns.str.strip().str.replace("'", "")

numeric_columns = ["temperature", "sound", "light", "dust", "fan", "motion"]

for col in numeric_columns:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace("'", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
    )
    df[col] = pd.to_numeric(df[col], errors="coerce")

df["created_at"] = (
    df["created_at"]
    .astype(str)
    .str.replace("'", "", regex=False)
    .str.replace(",", "", regex=False)
    .str.strip()
)

df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")

df = df.dropna(
    subset=["created_at", "temperature", "sound", "light", "dust", "fan", "motion"]
)

df["hour"] = df["created_at"].dt.strftime("%m-%d %H")

plt.style.use("default")

# ==========================================================
# 1. Sound, Light and Dust Over Time
# ==========================================================
hourly_env = (
    df.groupby("hour")[["sound", "light", "dust"]]
    .mean()
    .reset_index()
)

plt.figure(figsize=(12, 6))
plt.gca().set_facecolor("white")

plt.plot(hourly_env["hour"], hourly_env["sound"], marker="o",
         linewidth=2.5, color="blue", label="Average Sound")

plt.plot(hourly_env["hour"], hourly_env["light"], marker="s",
         linewidth=2.5, color="#ff7f0e", label="Average Light")

plt.plot(hourly_env["hour"], hourly_env["dust"], marker="^",
         linewidth=2.5, color="green", label="Average Dust")

plt.title("Sound, Light and Dust Over Time")
plt.xlabel("Time (Hourly)")
plt.ylabel("Sensor Value")
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("graphs/1_sound_light_dust_over_time.png", dpi=300)
plt.close()

# ==========================================================
# 2. Motion Activity
# ==========================================================
motion_counts = df.groupby("hour")["motion"].sum().reset_index()

plt.figure(figsize=(12, 6))
plt.gca().set_facecolor("white")

plt.bar(motion_counts["hour"], motion_counts["motion"], color="#4C72B0")

plt.title("Motion Activity")
plt.xlabel("Time (Hourly)")
plt.ylabel("Motion Count")
plt.xticks(rotation=45)
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("graphs/2_motion_activity.png", dpi=300)
plt.close()

# ==========================================================
# 3. Fan ON/OFF Behavior
# ==========================================================
fan_hourly = df.groupby("hour")["fan"].mean().reset_index()

plt.figure(figsize=(12, 6))
plt.gca().set_facecolor("white")

plt.step(
    fan_hourly["hour"],
    fan_hourly["fan"],
    where="mid",
    linewidth=3,
    color="#F5A623",
    label="Fan Status"
)

plt.scatter(
    fan_hourly["hour"],
    fan_hourly["fan"],
    color="#F5A623",
    s=60
)

plt.title("Fan ON/OFF Behavior")
plt.xlabel("Time (Hourly)")
plt.ylabel("Fan Status")
plt.yticks([0, 1], ["OFF", "ON"])
plt.xticks(rotation=45)
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("graphs/3_fan_behavior.png", dpi=300)
plt.close()

# ==========================================================
# 4. Temperature and Fan Behavior vs Time
# ==========================================================
hourly_data = df.groupby("hour")[["temperature", "fan"]].mean().reset_index()

fig, ax1 = plt.subplots(figsize=(14, 7))
fig.patch.set_facecolor("white")
ax1.set_facecolor("white")

ax1.plot(
    hourly_data["hour"],
    hourly_data["temperature"],
    marker="o",
    linewidth=2.5,
    color="blue",
    label="Temperature"
)

ax1.axhline(26, linestyle="--", linewidth=2,
            color="red", label="Fan ON Threshold (26°C)")

ax1.axhline(24, linestyle="--", linewidth=2,
            color="green", label="Fan OFF Threshold (24°C)")

ax1.set_xlabel("Time (Hourly)")
ax1.set_ylabel("Temperature (°C)", color="blue")
ax1.tick_params(axis="y", labelcolor="blue")
ax1.grid(True, alpha=0.3)

ax2 = ax1.twinx()
ax2.set_facecolor("white")

ax2.step(
    hourly_data["hour"],
    hourly_data["fan"],
    where="mid",
    linewidth=3,
    color="purple",
    label="Fan Status"
)

ax2.set_ylabel("Fan Status", color="purple")
ax2.set_yticks([0, 1])
ax2.set_yticklabels(["OFF", "ON"])
ax2.tick_params(axis="y", labelcolor="purple")

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()

ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

plt.title("Temperature and Fan Behavior vs Time")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("graphs/4_temperature_fan_threshold.png", dpi=300)
plt.close()

print("\nAll graphs generated successfully!")
print("Saved in: graphs/")
print("\nGenerated files:")
print("1_sound_light_dust_over_time.png")
print("2_motion_activity.png")
print("3_fan_behavior.png")
print("4_temperature_fan_threshold.png")