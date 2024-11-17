import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from DataTransformation import LowPassFilter
from scipy.signal import argrelextrema
from sklearn.metrics import mean_absolute_error

pd.options.mode.chained_assignment = None


# Plot settings
plt.style.use("fivethirtyeight")
plt.rcParams["figure.figsize"] = (20, 5)
plt.rcParams["figure.dpi"] = 100
plt.rcParams["lines.linewidth"] = 2


# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------

df = pd.read_pickle("../../data/interim/01_data_processed.pkl")
df = df[df["label"] != "rest"]

acc_r = df["acc_x"] ** 2 + df["acc_y"] ** 2 + df["acc_z"] ** 2
gyr_r = df["gyr_x"] ** 2 + df["gyr_y"] ** 2 + df["gyr_z"] ** 2
df["acc_r"] = np.sqrt(acc_r)
df["gyr_r"] = np.sqrt(gyr_r)

# --------------------------------------------------------------
# Split data
# --------------------------------------------------------------

inclCh_df = df[df["label"] == "inclCh"]
wideCh_df = df[df["label"] == "wideCh"]
bicep_df = df[df["label"] == "bicep"]
lowRow_df = df[df["label"] == "lowRow"]
pDown_df = df[df["label"] == "pDown"]
trpd_df = df[df["label"] == "trpd"]
shlr_df = df[df["label"] == "shlr"]

# --------------------------------------------------------------
# Visualize data to identify patterns
# --------------------------------------------------------------

plot_df = inclCh_df

# Accelerometer
plot_df[plot_df["set"] == plot_df["set"].unique()[0]]["acc_x"].plot()
plot_df[plot_df["set"] == plot_df["set"].unique()[0]]["acc_y"].plot()
plot_df[plot_df["set"] == plot_df["set"].unique()[0]]["acc_z"].plot()
plot_df[plot_df["set"] == plot_df["set"].unique()[0]]["acc_r"].plot()

# Gyroscope
plot_df[plot_df["set"] == plot_df["set"].unique()[0]]["gyr_x"].plot()
plot_df[plot_df["set"] == plot_df["set"].unique()[0]]["gyr_y"].plot()
plot_df[plot_df["set"] == plot_df["set"].unique()[0]]["gyr_z"].plot()
plot_df[plot_df["set"] == plot_df["set"].unique()[0]]["gyr_r"].plot()

# --------------------------------------------------------------
# Configure LowPassFilter
# --------------------------------------------------------------

fs = 1000 / 200
LowPass = LowPassFilter()

# --------------------------------------------------------------
# Apply and tweak LowPassFilter
# --------------------------------------------------------------

inclCh_set = inclCh_df[inclCh_df["set"] == inclCh_df["set"].unique()[0]]
wideCh_set = wideCh_df[wideCh_df["set"] == wideCh_df["set"].unique()[0]]
bicep_set = bicep_df[bicep_df["set"] == bicep_df["set"].unique()[0]]
lowRow_set = lowRow_df[lowRow_df["set"] == lowRow_df["set"].unique()[0]]
pDown_set = pDown_df[pDown_df["set"] == pDown_df["set"].unique()[0]]
trpd_set = trpd_df[trpd_df["set"] == trpd_df["set"].unique()[0]]
shlr_set = shlr_df[shlr_df["set"] == shlr_df["set"].unique()[0]]

inclCh_set["acc_r"].plot()

column = "acc_r"
LowPass.low_pass_filter(
    inclCh_set, col=column, sampling_frequency=fs, cutoff_frequency=0.4, order=10
)[column + "_lowpass"].plot()

# --------------------------------------------------------------
# Create function to count repetitions
# --------------------------------------------------------------


def count_reps(dataset, cutoff=0.19, order=10, column="acc_r"):
    data = LowPass.low_pass_filter(
        dataset, col=column, sampling_frequency=fs, cutoff_frequency=cutoff, order=order
    )
    indexes = argrelextrema(data[column + "_lowpass"].values, np.greater)
    peaks = data.iloc[indexes]

    fig, ax = plt.subplots()
    plt.plot(dataset[f"{column}_lowpass"])
    plt.plot(peaks[f"{column}_lowpass"], "o", color="red")
    ax.set_ylabel(f"{column}_lowpass")
    exercise = dataset["label"].iloc[0].title()
    plt.title(f"{exercise}: {len(peaks)} Reps")
    plt.show()

    return len(peaks)


count_reps(inclCh_set, cutoff=0.22)
count_reps(wideCh_set, cutoff=0.197)
count_reps(bicep_set, cutoff=0.19)
count_reps(lowRow_set, cutoff=0.19)
count_reps(pDown_set, cutoff=0.15)
count_reps(trpd_set, cutoff=0.19)
count_reps(shlr_set, cutoff=0.2)

# --------------------------------------------------------------
# Create benchmark dataframe
# --------------------------------------------------------------

df["reps_pred"] = 0
rep_df = df.groupby(["label", "set"])["reps_pred"].max().reset_index()

for s in df["set"].unique():
    subset = df[df["set"] == s]

    column = "acc_r"
    cutoff = 0.19

    if subset["label"].iloc[0] == "inclCh":
        cutoff = 0.22

    if subset["label"].iloc[0] == "wideCh":
        cutoff = 0.197

    if subset["label"].iloc[0] == "pDown":
        cutoff = 0.15

    if subset["label"].iloc[0] == "shlr":
        cutoff = 0.2

    reps = count_reps(subset, cutoff=cutoff, column=column)

    rep_df.loc[rep_df["set"] == s, "reps_pred"] = reps

rep_df
