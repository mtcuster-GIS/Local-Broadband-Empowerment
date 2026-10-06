import os
from glob import glob
import pandas as pd
from os.path import basename, exists, join

datasource = glob(r"C:\Users\mtcuster\Documents\ArcGIS\Projects\FCC_477_12312025\Raw data\*.csv")
breakoutfiles = r"C:\Users\mtcuster\Documents\ArcGIS\Projects\FCC_477_12312025\processed data"

for file in datasource:
    print(file)
    filename = basename(file).split("_")[2]
    print(filename)
    outputfolder = join(breakoutfiles, filename)
    if not exists(outputfolder):
        os.mkdir(outputfolder)
    data = pd.read_csv(file)
    unique_values = data["brand_name"].drop_duplicates()
    rows, columns = data.shape
    for value in unique_values:
        dfs = data[data["brand_name"] == value]
        value = value.replace(" ", "_")
        value = value.replace("&", "and")
        value = value.replace(",", "")
        value = value.replace(".", "_")
        row, col = dfs.shape
        rows = rows - row
        group_columns = [
            "block_geoid",
            "max_advertised_download_speed",
            "max_advertised_upload_speed"
        ]

        dfs.drop("location_id", axis=1, inplace=True)

        # Define how to preserve each additional column
        other_columns = [
            col for col in dfs.columns
            if col not in group_columns]

        aggregation_rules = {col: "first" for col in other_columns}

        result = (dfs.groupby(group_columns, dropna=False, as_index=False).agg(count=("block_geoid", "size"),
                                                                                    **{col: (col, rule) for col, rule in
                                                                                       aggregation_rules.items()}))

        result.to_csv(join(outputfolder, value + ".csv"), index=False)

