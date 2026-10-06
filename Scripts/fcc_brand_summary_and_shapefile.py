import pandas as pd
from os.path import join

spectrum = pd.read_csv(
    r"C:\Users\mtcuster\Documents\ArcGIS\Projects\FCC_477_12312025\processed data\Cable\Spectrum.csv")
breakoutfiles = r"C:\Users\mtcuster\Documents\ArcGIS\Projects\FCC_477_12312025\shp data"

group_columns = [
    "block_geoid",
    "max_advertised_download_speed",
    "max_advertised_upload_speed"
]

spectrum.drop("location_id", axis=1, inplace=True)

# Define how to preserve each additional column
other_columns = [
    col for col in spectrum.columns
    if col not in group_columns]

aggregation_rules = {col: "first" for col in other_columns}

result = (spectrum.groupby(group_columns, dropna=False, as_index=False).agg(count=("block_geoid", "size"),
                                                                            **{col: (col, rule) for col, rule in
                                                                               aggregation_rules.items()}))

result.to_csv(join(breakoutfiles, "Spectrum.csv"), index=False)
