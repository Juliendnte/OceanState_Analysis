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
    "macroplastics": "https://ourworldindata.org/grapher/macroplastics-in-ocean.csv?v=1&csvType=full&useColumnShortNames=true"
}

# Options pour les requêtes HTTP
REQUEST_OPTIONS = {
    'User-Agent': 'Our World In Data data fetch/1.0'
}

# Noms des fichiers de données brutes
RAW_DATA_FILES = {
    "sea_level": RAW_DATA_DIR / "sea-level.csv",
    "depth_file" : RAW_DATA_DIR / "glo12_rg_1m-m_202206-202206_2D_hcst.nc"
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
    "microplastics": {
        "Year": "year",
        "Accumulated ocean plastic: Microplastics (<0.5cm)": "microplastics"
    },
    "macroplastics": {
        "Year": "year",
        "Accumulated ocean plastic: Macroplastics (>0.5cm)": "macroplastics"
    }
}