import pandas as pd
from .config import URLS, REQUEST_OPTIONS, COLUMN_NAMES, RAW_DATA_FILES

def load_and_clean_ph_data()->pd.DataFrame:
    df = pd.read_csv(URLS["seawater_ph"], storage_options=REQUEST_OPTIONS)

    column_mapping = COLUMN_NAMES["seawater_ph"]
    df.rename(columns=column_mapping, inplace=True)

    return df


def load_and_clean_microplastic_data() -> pd.DataFrame:
    df = pd.read_csv(URLS["microplastics"], storage_options=REQUEST_OPTIONS)

    column_mapping = COLUMN_NAMES["microplastics"]
    df.rename(columns=column_mapping, inplace=True)

    return df


def load_and_clean_macroplastic_data() -> pd.DataFrame:
    df = pd.read_csv(URLS["macroplastics"], storage_options=REQUEST_OPTIONS)

    column_mapping = COLUMN_NAMES["macroplastics"]
    df.rename(columns=column_mapping, inplace=True)

    return df

def load_and_clean_depth_data() -> pd.DataFrame:
    import xarray as xr
    import warnings
    warnings.filterwarnings('ignore')

    ds = xr.open_dataset(RAW_DATA_FILES['depth_file'])
    df = ds.to_dataframe()
    df = df.reset_index()
    return df

def load_and_clean_sealevel_data():
    """Charge et nettoie les données du niveau de la mer."""
    df = pd.read_csv(RAW_DATA_FILES["sea_level"])

    return df

def load_and_clean_heat_data():
    """Charge et nettoie les données du niveau de la mer."""
    df = pd.read_csv(URLS["heat"], storage_options=REQUEST_OPTIONS)
    return df

def load_and_clean_oceanwarning_data():
    df = pd.read_excel(RAW_DATA_FILES["oceanwarning"])

    column_mapping = COLUMN_NAMES["oceanwarning"]
    df.rename(columns=column_mapping, inplace=True)

    return df

def load_and_clean_acid_data():
    df = pd.read_csv(RAW_DATA_FILES["acid"])
    return df

def load_and_clean_plastic_waste_data():
    df = pd.read_csv(RAW_DATA_FILES["plastic_waste"])
    return df

def load_and_clean_plastic_waste_ocean_data():
    df = pd.read_csv(URLS["plastic_waste_ocean"], storage_options=REQUEST_OPTIONS)
    return df

def load_and_clean_plastic_production_data():
    df = pd.read_csv(URLS["platic_production"], storage_options=REQUEST_OPTIONS)
    return df

def load_and_clean_CO2_emission_data():
    df = pd.read_csv(URLS["CO2_emission"], storage_options=REQUEST_OPTIONS)
    return df

def load_and_clean_red_list_index_data():
    df = pd.read_csv(URLS["red_list_index"], storage_options=REQUEST_OPTIONS)
    return df

def load_and_clean_glaciers_data():
    df = pd.read_csv(RAW_DATA_FILES["glaciers_melting"])
    return df