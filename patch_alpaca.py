"""
Patches notebooks to use Alpaca for data instead of local CSV files.
Run from the repo root: python patch_alpaca.py
"""
import json, os, copy

NB_DIR = os.path.join(os.path.dirname(__file__), "notebooks")

# ---------------------------------------------------------------------------
# Shared helpers
# ---------------------------------------------------------------------------

def lines(*chunks):
    """Join a list of strings as notebook source lines."""
    return list(chunks)


def code_cell(source_lines):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": source_lines,
    }


def save_nb(path, nb):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)


def load_nb(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Replacement source for Data Preparation.ipynb
# ---------------------------------------------------------------------------

ALPACA_IMPORT_CELL = code_cell([
    "# === 1. Import Libraries & Configure Alpaca Credentials ===\n",
    "\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import os\n",
    "import warnings\n",
    "from tqdm import tqdm\n",
    "from alpaca.data.historical import StockHistoricalDataClient\n",
    "from alpaca.data.requests import StockBarsRequest\n",
    "from alpaca.data.timeframe import TimeFrame\n",
    "\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "# Credentials: read from env vars; fall back to the values below.\n",
    "# In Colab set these as Secrets (key icon) so they are never hard-coded.\n",
    "API_KEY_ID     = os.environ.get('ALPACA_API_KEY',    'AKXDM3YDOKE9EJDBQWZC')\n",
    "API_SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY', 'duaAQYetNb5nJ5gSRXgbvmjU0cEkSEJGjZiupMiE')\n",
    "BASE_URL       = 'https://paper-api.alpaca.markets'  # paper trading endpoint\n",
    "\n",
    "client = StockHistoricalDataClient(API_KEY_ID, API_SECRET_KEY)\n",
    "\n",
    "# --- Universe of liquid US stocks (edit to add/remove symbols) ---\n",
    "SYMBOLS = [\n",
    "    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'NVDA', 'TSLA', 'JPM',\n",
    "    'JNJ',  'V',    'PG',   'UNH',   'HD',   'MA',   'BAC',  'ADBE',\n",
    "    'NFLX', 'XOM',  'INTC', 'AMD',   'CSCO', 'PFE',  'WMT',  'CRM',\n",
    "    'ABT',  'CVX',  'NKE',  'MRK',   'COST', 'ACN',  'LLY',  'TMO',\n",
    "    'ABBV', 'AVGO', 'QCOM', 'TXN',   'NEE',  'HON',  'MDT',  'UNP',\n",
    "    'LOW',  'PM',   'UPS',  'BMY',   'GS',   'MS',   'BLK',  'SCHW',\n",
    "    'SPGI', 'ICE',\n",
    "]\n",
    "\n",
    "START_DATE = '2022-07-01'\n",
    "END_DATE   = '2023-12-31'\n",
    "\n",
    "CACHE_PATH = '../data/raw/alpaca_minute_data.parquet'\n",
    "\n",
    "print(f'Universe: {len(SYMBOLS)} symbols | {START_DATE} → {END_DATE}')\n",
    "print(f'Cache path: {CACHE_PATH}')\n",
])

ALPACA_FETCH_CELL = code_cell([
    "# === 2. Fetch Minute Bars from Alpaca (with local cache) ===\n",
    "\n",
    "os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)\n",
    "\n",
    "if os.path.exists(CACHE_PATH):\n",
    "    print(f'Loading from cache: {CACHE_PATH}')\n",
    "    result_df = pd.read_parquet(CACHE_PATH)\n",
    "    print(f'✅ Cache loaded. {len(result_df):,} rows, '\n",
    "          f'{result_df[\"order_book_id\"].nunique()} symbols')\n",
    "else:\n",
    "    print('No cache found — fetching from Alpaca (this may take several minutes)...')\n",
    "    req = StockBarsRequest(\n",
    "        symbol_or_symbols=SYMBOLS,\n",
    "        timeframe=TimeFrame.Minute,\n",
    "        start=START_DATE,\n",
    "        end=END_DATE,\n",
    "        feed='iex',          # free IEX feed; change to 'sip' on paid plan\n",
    "    )\n",
    "    bars = client.get_stock_bars(req)\n",
    "    raw = bars.df.reset_index()\n",
    "\n",
    "    raw = raw.rename(columns={'symbol': 'order_book_id', 'timestamp': 'datetime'})\n",
    "\n",
    "    # Convert UTC-aware timestamps to Eastern, then strip timezone\n",
    "    if raw['datetime'].dt.tz is not None:\n",
    "        raw['datetime'] = (raw['datetime']\n",
    "                           .dt.tz_convert('America/New_York')\n",
    "                           .dt.tz_localize(None))\n",
    "\n",
    "    # 'money' = turnover proxy (vwap * volume)\n",
    "    vwap_col = 'vwap' if 'vwap' in raw.columns else 'close'\n",
    "    raw['money'] = raw[vwap_col] * raw['volume']\n",
    "\n",
    "    result_df = raw[[\n",
    "        'order_book_id', 'datetime',\n",
    "        'open', 'high', 'low', 'close', 'volume', 'money',\n",
    "    ]].copy()\n",
    "\n",
    "    # Keep only regular-hours bars (09:30–16:00 Eastern)\n",
    "    t = result_df['datetime'].dt.time\n",
    "    import datetime as _dt\n",
    "    result_df = result_df[\n",
    "        (t >= _dt.time(9, 30)) & (t <= _dt.time(16, 0))\n",
    "    ].copy()\n",
    "\n",
    "    result_df.sort_values(['order_book_id', 'datetime'], inplace=True)\n",
    "    result_df.reset_index(drop=True, inplace=True)\n",
    "\n",
    "    result_df.to_parquet(CACHE_PATH, index=False)\n",
    "    print(f'✅ Fetched and cached {len(result_df):,} rows to {CACHE_PATH}')\n",
    "\n",
    "result_df['datetime'] = pd.to_datetime(result_df['datetime'])\n",
    "result_df['date']     = result_df['datetime'].dt.date\n",
    "\n",
    "print(f'\\nDataset summary:')\n",
    "print(f'  Total rows : {len(result_df):,}')\n",
    "print(f'  Symbols    : {result_df[\"order_book_id\"].nunique()}')\n",
    "print(f'  Date range : {result_df[\"date\"].min()} → {result_df[\"date\"].max()}')\n",
    "print(result_df.head())\n",
])

BARRA_SKIP_CELL = code_cell([
    "# === 6. Barra Factor Integration: Size Factor ===\n",
    "# Barra risk factor data is not available via the Alpaca API.\n",
    "# Setting barra_size to None so the save step handles it gracefully.\n",
    "# If you have access to Barra/FactSet data, load and pivot it here.\n",
    "\n",
    "barra_size = None\n",
    "print('ℹ️  Barra size factor skipped (no source available via Alpaca).')\n",
    "print('   Downstream notebooks will continue without it.')\n",
])

# ---------------------------------------------------------------------------
# Replacement source for Alpha_Factor_Generation_2.ipynb
# ---------------------------------------------------------------------------

AFG2_FETCH_CELL = code_cell([
    "# === 1. Import Libraries & Load High-Frequency Data via Alpaca ===\n",
    "\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "from tqdm import tqdm\n",
    "import os\n",
    "import time\n",
    "import warnings\n",
    "warnings.filterwarnings('ignore')\n",
    "\n",
    "from alpaca.data.historical import StockHistoricalDataClient\n",
    "from alpaca.data.requests import StockBarsRequest\n",
    "from alpaca.data.timeframe import TimeFrame\n",
    "\n",
    "API_KEY_ID     = os.environ.get('ALPACA_API_KEY',    'AKXDM3YDOKE9EJDBQWZC')\n",
    "API_SECRET_KEY = os.environ.get('ALPACA_SECRET_KEY', 'duaAQYetNb5nJ5gSRXgbvmjU0cEkSEJGjZiupMiE')\n",
    "client = StockHistoricalDataClient(API_KEY_ID, API_SECRET_KEY)\n",
    "\n",
    "CACHE_PATH = '../data/raw/alpaca_minute_data.parquet'\n",
    "\n",
    "if os.path.exists(CACHE_PATH):\n",
    "    print(f'Loading from cache: {CACHE_PATH}')\n",
    "    result_df = pd.read_parquet(CACHE_PATH)\n",
    "else:\n",
    "    # Fetch if cache not present (same params as Data Preparation notebook)\n",
    "    SYMBOLS = [\n",
    "        'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'NVDA', 'TSLA', 'JPM',\n",
    "        'JNJ',  'V',    'PG',   'UNH',   'HD',   'MA',   'BAC',  'ADBE',\n",
    "        'NFLX', 'XOM',  'INTC', 'AMD',   'CSCO', 'PFE',  'WMT',  'CRM',\n",
    "        'ABT',  'CVX',  'NKE',  'MRK',   'COST', 'ACN',  'LLY',  'TMO',\n",
    "        'ABBV', 'AVGO', 'QCOM', 'TXN',   'NEE',  'HON',  'MDT',  'UNP',\n",
    "        'LOW',  'PM',   'UPS',  'BMY',   'GS',   'MS',   'BLK',  'SCHW',\n",
    "        'SPGI', 'ICE',\n",
    "    ]\n",
    "    print('Fetching from Alpaca...')\n",
    "    req = StockBarsRequest(\n",
    "        symbol_or_symbols=SYMBOLS,\n",
    "        timeframe=TimeFrame.Minute,\n",
    "        start='2022-07-01',\n",
    "        end='2023-12-31',\n",
    "        feed='iex',\n",
    "    )\n",
    "    bars = client.get_stock_bars(req)\n",
    "    raw = bars.df.reset_index()\n",
    "    raw = raw.rename(columns={'symbol': 'order_book_id', 'timestamp': 'datetime'})\n",
    "    if raw['datetime'].dt.tz is not None:\n",
    "        raw['datetime'] = (raw['datetime']\n",
    "                           .dt.tz_convert('America/New_York')\n",
    "                           .dt.tz_localize(None))\n",
    "    vwap_col = 'vwap' if 'vwap' in raw.columns else 'close'\n",
    "    raw['money'] = raw[vwap_col] * raw['volume']\n",
    "    import datetime as _dt\n",
    "    t = raw['datetime'].dt.time\n",
    "    raw = raw[(t >= _dt.time(9, 30)) & (t <= _dt.time(16, 0))].copy()\n",
    "    result_df = raw[[\n",
    "        'order_book_id', 'datetime', 'open', 'high', 'low', 'close', 'volume', 'money',\n",
    "    ]].sort_values(['order_book_id', 'datetime']).reset_index(drop=True)\n",
    "    os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)\n",
    "    result_df.to_parquet(CACHE_PATH, index=False)\n",
    "    print(f'Cached to {CACHE_PATH}')\n",
    "\n",
    "result_df['datetime'] = pd.to_datetime(result_df['datetime'])\n",
    "result_df['date']     = result_df['datetime'].dt.date\n",
    "\n",
    "print(f'✅ Loaded {len(result_df):,} rows | '\n",
    "      f'{result_df[\"order_book_id\"].nunique()} symbols | '\n",
    "      f'{result_df[\"date\"].min()} → {result_df[\"date\"].max()}')\n",
    "print(result_df.head())\n",
])

AFG2_COMBINE_CELL = code_cell([
    "# === 2. Verify Data is Ready ===\n",
    "# (Data is already combined and sorted from the Alpaca fetch above.)\n",
    "print(f'Dataset shape : {result_df.shape}')\n",
    "print(f'Symbols       : {result_df[\"order_book_id\"].nunique()}')\n",
    "print(f'Date range    : {result_df[\"date\"].min()} → {result_df[\"date\"].max()}')\n",
    "print(f'Columns       : {list(result_df.columns)}')\n",
])

# ---------------------------------------------------------------------------
# Shared Colab setup cell (updated to include alpaca-py)
# ---------------------------------------------------------------------------

COLAB_SETUP_SOURCE = [
    "# ============================================================\n",
    "# GOOGLE COLAB SETUP — run this cell first when using Colab\n",
    "# ============================================================\n",
    "import sys, os\n",
    "\n",
    "IN_COLAB = 'google.colab' in sys.modules\n",
    "\n",
    "if IN_COLAB:\n",
    "    from google.colab import drive\n",
    "    drive.mount('/content/drive')\n",
    "\n",
    "    REPO_PATH = '/content/drive/MyDrive/Factor-Research'\n",
    "\n",
    "    if not os.path.exists(REPO_PATH):\n",
    "        print('Cloning repository to Google Drive...')\n",
    "        os.system(f'git clone https://github.com/mbrennan5/Factor-Research.git {REPO_PATH}')\n",
    "    else:\n",
    "        print(f'Repository found at {REPO_PATH}')\n",
    "\n",
    "    print('Installing packages...')\n",
    "    os.system('pip install -q lightgbm xgboost optuna plotly tqdm yfinance alpaca-py pyarrow')\n",
    "\n",
    "    NOTEBOOKS_DIR = os.path.join(REPO_PATH, 'notebooks')\n",
    "    os.chdir(NOTEBOOKS_DIR)\n",
    "    print(f'Working directory set to: {os.getcwd()}')\n",
    "else:\n",
    "    print('Running locally — no Colab setup needed.')\n",
]

COLAB_SETUP_CELL = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": COLAB_SETUP_SOURCE,
}

# ---------------------------------------------------------------------------
# Patch Data Preparation.ipynb
# ---------------------------------------------------------------------------

def patch_data_preparation():
    path = os.path.join(NB_DIR, "Data Preparation.ipynb")
    nb = load_nb(path)
    cells = nb["cells"]

    # Cell [2] = import + old CSV loader → Alpaca credentials cell
    cells[2] = ALPACA_IMPORT_CELL
    # Cell [3] = old combine/sort → Alpaca fetch cell
    cells[3] = ALPACA_FETCH_CELL
    # Cell [7] = Barra loading → skip
    cells[7] = BARRA_SKIP_CELL
    # Cell [0] = Colab setup (refresh with updated pip install)
    cells[0] = COLAB_SETUP_CELL

    nb["cells"] = cells
    save_nb(path, nb)
    print("PATCHED: Data Preparation.ipynb")


# ---------------------------------------------------------------------------
# Patch Alpha_Factor_Generation_2.ipynb
# ---------------------------------------------------------------------------

def patch_afg2():
    path = os.path.join(NB_DIR, "Alpha_Factor_Generation_2.ipynb")
    nb = load_nb(path)
    cells = nb["cells"]

    # Cell [0] = Colab setup (refresh)
    cells[0] = COLAB_SETUP_CELL
    # Cell [2] = old CSV loader → Alpaca fetch
    cells[2] = AFG2_FETCH_CELL
    # Cell [3] = old combine → simplified verify cell
    cells[3] = AFG2_COMBINE_CELL

    # Cells 10-40 are legacy duplicate cells that also use `dict` as a variable
    # name (shadowing Python built-in). The comprehensive cells 5-9 already
    # cover the same factors. Remove the duplicates.
    cells = cells[:10]

    nb["cells"] = cells
    save_nb(path, nb)
    print("PATCHED: Alpha_Factor_Generation_2.ipynb")


# ---------------------------------------------------------------------------
# Refresh Colab setup cell in remaining notebooks
# ---------------------------------------------------------------------------

OTHER_NOTEBOOKS = [
    "Alpha_Factor_Generation.ipynb",
    "Alpha_Factor_Selection.ipynb",
    "Factor_backtest.ipynb",
    "ML_Model.ipynb",
]

def refresh_colab_cells():
    for fname in OTHER_NOTEBOOKS:
        path = os.path.join(NB_DIR, fname)
        nb = load_nb(path)
        cells = nb["cells"]
        if cells and cells[0]["cell_type"] == "code":
            cells[0] = COLAB_SETUP_CELL
            nb["cells"] = cells
            save_nb(path, nb)
            print(f"REFRESHED Colab cell: {fname}")


# ---------------------------------------------------------------------------
# Patch Colab_Setup.ipynb install step
# ---------------------------------------------------------------------------

def patch_colab_setup_nb():
    path = os.path.join(NB_DIR, "Colab_Setup.ipynb")
    nb = load_nb(path)
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            src = "".join(cell["source"])
            if "pip install" in src and "lightgbm" in src:
                cell["source"] = [
                    "# ── Step 3: Install required packages ───────────────────────────────────────\n",
                    "print('Installing packages (this takes ~1-2 minutes)...')\n",
                    "!pip install -q lightgbm xgboost optuna plotly tqdm yfinance alpaca-py pyarrow\n",
                    "print('All packages installed.')\n",
                ]
                break
    save_nb(path, nb)
    print("PATCHED: Colab_Setup.ipynb")


# ---------------------------------------------------------------------------
# Run all patches
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    patch_data_preparation()
    patch_afg2()
    refresh_colab_cells()
    patch_colab_setup_nb()
    print("\nAll patches applied.")
