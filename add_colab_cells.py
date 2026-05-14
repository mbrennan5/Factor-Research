"""
Injects a Google Colab setup cell as the first code cell in each notebook.
"""
import json
import os

COLAB_SETUP_SOURCE = [
    "# ============================================================\n",
    "# GOOGLE COLAB SETUP — run this cell first when using Colab\n",
    "# ============================================================\n",
    "import sys, os\n",
    "\n",
    "IN_COLAB = 'google.colab' in sys.modules\n",
    "\n",
    "if IN_COLAB:\n",
    "    # 1. Mount Google Drive so your data is accessible\n",
    "    from google.colab import drive\n",
    "    drive.mount('/content/drive')\n",
    "\n",
    "    # 2. Set REPO_PATH to wherever you stored (or will store) the repo on Drive.\n",
    "    #    If the folder doesn't exist the repo is cloned there automatically.\n",
    "    REPO_PATH = '/content/drive/MyDrive/Factor-Research'\n",
    "\n",
    "    if not os.path.exists(REPO_PATH):\n",
    "        print('Cloning repository to Google Drive...')\n",
    "        os.system(f'git clone https://github.com/mbrennan5/Factor-Research.git {REPO_PATH}')\n",
    "    else:\n",
    "        print(f'Repository found at {REPO_PATH}')\n",
    "\n",
    "    # 3. Install required packages.\n",
    "    #    Most are already in Colab; only the non-standard ones need installing.\n",
    "    print('Installing packages...')\n",
    "    os.system('pip install -q lightgbm xgboost optuna plotly tqdm yfinance')\n",
    "\n",
    "    # 4. Change to the notebooks directory so relative paths (../data/...) work.\n",
    "    NOTEBOOKS_DIR = os.path.join(REPO_PATH, 'notebooks')\n",
    "    os.chdir(NOTEBOOKS_DIR)\n",
    "    print(f'Working directory set to: {os.getcwd()}')\n",
    "else:\n",
    "    print('Running locally — no Colab setup needed.')\n"
]

COLAB_SETUP_CELL = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": COLAB_SETUP_SOURCE,
}

NOTEBOOKS_DIR = os.path.join(os.path.dirname(__file__), "notebooks")

for fname in sorted(os.listdir(NOTEBOOKS_DIR)):
    if not fname.endswith(".ipynb"):
        continue
    fpath = os.path.join(NOTEBOOKS_DIR, fname)
    with open(fpath, "r", encoding="utf-8") as f:
        nb = json.load(f)

    cells = nb.get("cells", [])

    # Skip if the setup cell is already present
    first_code = next((c for c in cells if c["cell_type"] == "code"), None)
    if first_code and any("GOOGLE COLAB SETUP" in line for line in first_code.get("source", [])):
        print(f"  SKIP (already has setup cell): {fname}")
        continue

    # Insert at position 0 (before any existing cells)
    cells.insert(0, COLAB_SETUP_CELL)
    nb["cells"] = cells

    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)

    print(f"  UPDATED: {fname}")

print("Done.")
