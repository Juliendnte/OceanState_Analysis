from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parent
DATA_DIR = ROOT_DIR / ".." / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EXTERNAL_DATA_DIR = DATA_DIR / "external"
INTERIM_DATA_DIR = DATA_DIR / "interim"

# Création des répertoires s'ils n'existent pas
for dir_path in [RAW_DATA_DIR, PROCESSED_DATA_DIR, EXTERNAL_DATA_DIR, INTERIM_DATA_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)

# URLs des données
URLS = {
    "seawater_ph": "https://ourworldindata.org/grapher/seawater-ph.csv?v=1&csvType=full&useColumnShortNames=true",
    "microplastics": "https://ourworldindata.org/grapher/microplastics-in-ocean.csv?v=1&csvType=full&useColumnShortNames=true",
    "macroplastics": "https://ourworldindata.org/grapher/macroplastics-in-ocean.csv?v=1&csvType=full&useColumnShortNames=true",
    "heat":"https://ourworldindata.org/grapher/ocean-heat-top-2000m.csv?v=1&csvType=filtered&useColumnShortNames=true&overlay=download-data",
    "plastic_waste_ocean": "https://ourworldindata.org/grapher/share-of-global-plastic-waste-emitted-to-the-ocean.csv?v=1&csvType=full&useColumnShortNames=true",
    "platic_production": "https://ourworldindata.org/grapher/global-plastics-production.csv?v=1&csvType=full&useColumnShortNames=true",
    "glacier melting" : "https://ourworldindata.org/grapher/mass-us-glaciers.csv?v=1&csvType=full&useColumnShortNames=true",
    "red list index" : "https://ourworldindata.org/grapher/red-list-index.csv?v=1&csvType=full&useColumnShortNames=true"
}

# Options pour les requêtes HTTP
REQUEST_OPTIONS = {
    'User-Agent': 'Our World In Data data fetch/1.0'
}

# Noms des fichiers de données brutes
RAW_DATA_FILES = {
    "sea_level": RAW_DATA_DIR / "sea-level.csv",
    "depth_file" : RAW_DATA_DIR / "glo12_rg_1m-m_202206-202206_2D_hcst.nc",
    "oceanwarning": RAW_DATA_DIR / "oceanwarmingannualnoaa-copy.xlsx",
    "acid": RAW_DATA_DIR / "project_of_ocean_acidification.csv",
    "plastic_waste": RAW_DATA_DIR / "plastic-waste-imports.csv"

}

PROCESSED_DATA_FILES = {
    "sea_level": PROCESSED_DATA_DIR / "sea-level.csv",
    "plastics": PROCESSED_DATA_DIR / "plastics.csv"
}

INTERIM_DATA_FILES = {
    "sea_level": INTERIM_DATA_DIR / "sea-level.csv"
}

EXTERNAL_DATA_FILES = {}

# Noms des colonnes importantes
COLUMN_NAMES = {
    "seawater_ph": {
        "Day": "Date",
        "ocean_ph_yearly_average": "pH yearly average",
        "ocean_ph": "pH"
    },
    "oceanwarning": {
        "WO": "Change in World Ocean Heat Content (ZJ, relative to 1957, 5-year running average)",
        "WOse": "Standard Error of World Ocean Heat Content (ZJ, ±se, 5-year running average)",
        "NH": "Change in Northern Hemisphere Ocean Heat Content (ZJ, relative to 1957, 5-year running average)",
        "NHse": "Standard error for the Northern Hemisphere OHC in ZJ",
        "SH": "Change in Southern Hemisphere Ocean Heat Content (ZJ, relative to 1957, 5-year running average)",
        "SHse": "Standard error for the Southern Hemisphere OHC in ZJ"
    },
    "microplastics": {
        "Year": "year",
        "Accumulated ocean plastic: Microplastics (<0.5cm)": "microplastics"
    },
    "macroplastics": {
        "Year": "year",
        "Accumulated ocean plastic: Macroplastics (>0.5cm)": "macroplastics"
    }
}