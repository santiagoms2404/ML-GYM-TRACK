import pandas as pd
from glob import glob

# Load all CSV files
files = glob("../../data/raw/AppleWatch/*.csv")

data_path = "../../data/raw/AppleWatch\\"
f = files[0]


def read_data_from_files(files):
    motion_df_list = []  # Store dataframe
    set_num = 1

    for f in files:
        # Split the filename by underscores
        label = f.split("_")[0].replace(data_path, "")
        # Extract label from the filename and rename
        label_replace = (
            label.replace("inclinechest", "inclCh")
            .replace("widechest", "wideCh")
            .replace("lateralraise", "shlr")
            .replace("lowrow", "lowRow")
            .replace("pulldown", "pDown")
            .replace("triceppushdown", "trpd")
        )

        # Load the CSV file
        df = pd.read_csv(f)

        # Keep only the necessary columns
        df_clean = df[
            [
                "time",
                "accelerationX",
                "accelerationY",
                "accelerationZ",
                "rotationRateX",
                "rotationRateY",
                "rotationRateZ",
            ]
        ].copy()

        # Rename columns in df_clean
        df_clean.columns = [
            "epoch(ns)",
            "acc_x",
            "acc_y",
            "acc_z",
            "gyr_x",
            "gyr_y",
            "gyr_z",
        ]

        # Add label and set to the dataframe
        df_clean["label"] = label_replace
        df_clean["set"] = set_num  # Assign integer set number
        set_num += 1

        # Append the cleaned dataframe to the list
        motion_df_list.append(df_clean)

        # Concatenate all dataframes in the list
        motion_df = pd.concat(motion_df_list, ignore_index=True)

    # Convert the time column to a datetime format
    motion_df["epoch(ns)"] = pd.to_datetime(motion_df["epoch(ns)"])

    # set the time column as the index
    motion_df.index = pd.to_datetime(motion_df["epoch(ns)"], unit="ns")
    del motion_df["epoch(ns)"]

    return motion_df


# Test the function with the provided files
cleaned_data = read_data_from_files(files)

# Display the cleaned data
cleaned_data.head()
cleaned_data.tail()
cleaned_data.info()

show = cleaned_data.iloc[200000:300000:1]

cleaned_data["label"]


# --------------------------------------------------------------
# Resample data (frequency conversion)
# --------------------------------------------------------------

sampling = {
    "acc_x": "mean",
    "acc_y": "mean",
    "acc_z": "mean",
    "gyr_x": "mean",
    "gyr_y": "mean",
    "gyr_z": "mean",
    "label": "last",
    "set": "last",
}

cleaned_data[:10000].resample(rule="200ms").apply(sampling)

# split by day
days = [g for n, g in cleaned_data.groupby(pd.Grouper(freq="D"))]

data_resampled = pd.concat(
    [df.resample(rule="200ms").apply(sampling).dropna() for df in days]
)
data_resampled.info()

data_resampled["set"] = data_resampled["set"].astype("int")

# --------------------------------------------------------------
# Export dataset
# --------------------------------------------------------------
data_resampled.to_pickle("../../data/interim/01_data_processed.pkl")
