import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
# --------------------------------------------------------------
# Load data
# --------------------------------------------------------------

df = pd.read_pickle("../../data/interim/01_data_processed.pkl")

# --------------------------------------------------------------
# Plot single columns
# --------------------------------------------------------------

set_df = df[df["set"] == 1]
# show the duration of the set
plt.plot(set_df["acc_y"])

# show number of iterations
plt.plot(set_df["acc_y"].reset_index(drop=True))


# --------------------------------------------------------------
# Plot all exercises
# --------------------------------------------------------------

for label in df["label"].unique():
    subset = df[df["label"] == label]
    fig, ax = plt.subplots()
    plt.plot(subset["acc_y"].reset_index(drop=True), label=label)
    plt.legend()
    plt.show()

# plot only the first 100 samples
for label in df["label"].unique():
    subset = df[df["label"] == label]
    fig, ax = plt.subplots()
    plt.plot(subset[:100]["acc_y"].reset_index(drop=True), label=label)
    plt.legend()
    plt.show()

# --------------------------------------------------------------
# Adjust plot settings
# --------------------------------------------------------------

# style
mpl.style.use("seaborn-v0_8-deep")
mpl.rcParams["figure.figsize"] = (20, 5)
mpl.rcParams["figure.dpi"] = 100


# --------------------------------------------------------------
# Compare sets
# --------------------------------------------------------------

lable_df = df.query("label == 'bicep'").sort_values("set").reset_index()

fig, ax = plt.subplots()
lable_df.groupby(["set"])["acc_y"].plot()
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()

# --------------------------------------------------------------
# Plot multiple axis
# --------------------------------------------------------------

label = "trpd"
all_axis_df = df.query(f"label == '{label}'").reset_index()

fig, ax = plt.subplots()
all_axis_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax)
ax.set_ylabel("acc_y")
ax.set_xlabel("samples")
plt.legend()

# --------------------------------------------------------------
# Create a loop to plot all combinations per sensor
# --------------------------------------------------------------

labels = df["label"].unique()

# accelerometer
for label in labels:
    all_axis_df = df.query(f"label == '{label}'").reset_index()

    fig, ax = plt.subplots()
    all_axis_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax)
    ax.set_ylabel("acc_y")
    ax.set_xlabel("samples")
    plt.title(f"{label}".title())
    plt.legend()

# gyroscope
for label in labels:
    all_axis_df = df.query(f"label == '{label}'").reset_index()

    fig, ax = plt.subplots()
    all_axis_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax)
    ax.set_ylabel("gyr_y")
    ax.set_xlabel("samples")
    plt.title(f"{label}".title())
    plt.legend()

# --------------------------------------------------------------
# Combine plots in one figure
# --------------------------------------------------------------

label = "bicep"
combined_plot_df = df.query(f"label == '{label}'").reset_index(drop=True)

fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))
combined_plot_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])
combined_plot_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax[1])

ax[0].legend(
    loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True
)
ax[1].legend(
    loc="upper center", bbox_to_anchor=(0.5, 1.15), ncol=3, fancybox=True, shadow=True
)
ax[1].set_xlabel("samples")
# --------------------------------------------------------------
# Loop over all combinations and export for both sensors
# --------------------------------------------------------------

labels = df["label"].unique()

# accelerometer
for label in labels:
    combined_plot_df = df.query(f"label == '{label}'").reset_index()

    fig, ax = plt.subplots(nrows=2, sharex=True, figsize=(20, 10))
    combined_plot_df[["acc_x", "acc_y", "acc_z"]].plot(ax=ax[0])
    combined_plot_df[["gyr_x", "gyr_y", "gyr_z"]].plot(ax=ax[1])

    ax[0].legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.15),
        ncol=3,
        fancybox=True,
        shadow=True,
    )
    ax[1].legend(
        loc="upper center",
        bbox_to_anchor=(0.5, 1.15),
        ncol=3,
        fancybox=True,
        shadow=True,
    )
    ax[1].set_xlabel("samples")

    plt.savefig(f"../../reports/figures/{label.title()}.png")
    plt.show()
