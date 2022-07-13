import pandas as pd
import pydeflate
import numpy

from scripts.config import PATHS

### Take France ODA csv, clean, and put into long format ###

df_oda = (pd.read_csv(PATHS.scripts+r"/france_oda.csv", header=6, skipfooter=1, engine="python")
      .iloc[1:]
    .drop(
    columns=["Unnamed: 1","Unnamed: 2"],
)
    .rename(columns={"Year": "aid_type"})
    .melt(id_vars=["aid_type"], var_name="year", value_name="value")
      .astype({"year": int})
)

### Need to add in a column for "France" for pydeflate ###

df_oda['donor'] = "France"

### Deflate the data ###
df_oda_constant = pydeflate.deflate(
    df=df_oda,
    base_year=2021,
    source="oecd_dac",
    source_currency="USA",
    target_currency="USA",
    id_column="donor",
    id_type="regex",
    date_column="year",
    source_col="value",
    target_col="value_constant",
)

### Now need to get the GNI data ###

df_gni = (pd.read_csv(PATHS.scripts+r"/france_gni.csv", header=5, skipfooter=1, engine="python")
      .iloc[1:]
      .drop(
    columns=["Unnamed: 1","Unnamed: 2"],
)
      .rename(columns={"Year": "aid_type"})
      .melt(id_vars=["aid_type"], var_name="year", value_name="value")
      .astype({"year": int})
      )

### Need to add in a column for "France" for pydeflate ###

df_gni['donor'] = "France"

### Deflate the data ###
df_gni_constant = pydeflate.deflate(
    df=df_gni,
    base_year=2021,
    source="oecd_dac",
    source_currency="USA",
    target_currency="USA",
    id_column="donor",
    id_type="regex",
    date_column="year",
    source_col="value",
    target_col="value_constant",
)

### Export dataframe as CSV ###
df_constant = pd.concat([df_oda_constant,df_gni_constant])
df_constant.to_csv(PATHS.scripts+r"/deflated_france_data.csv")