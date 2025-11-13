import pandas as pd
from .config import URLS, REQUEST_OPTIONS, COLUMN_NAMES,RAW_DATA_FILES

def load_and_clean_ph_data():
    """Charge et nettoie les données du pH de l'eau de mer."""
    df = pd.read_csv(URLS["seawater_ph"], storage_options=REQUEST_OPTIONS)

    column_mapping = COLUMN_NAMES["seawater_ph"]
    df.rename(columns=column_mapping, inplace=True)

    return df


def load_and_clean_plastic_data():
    """Charge et nettoie les données des microplastiques."""
    df = pd.read_csv(URLS["microplastics"], storage_options=REQUEST_OPTIONS)

    # Renommage des colonnes
    column_mapping = COLUMN_NAMES["microplastics"]
    df = df.rename(columns=column_mapping)

    return df


def load_and_clean_sealevel_data():
    """Charge et nettoie les données du niveau de la mer."""
    df = pd.read_csv(RAW_DATA_FILES["sea_level"])

    
    return df