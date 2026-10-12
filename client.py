"""Fetch countries from the API, export CSV, and save a scatter plot."""

from pathlib import Path

import matplotlib
matplotlib.use("Agg")  # Allows saving a chart without opening a GUI window.
import matplotlib.pyplot as plt
import pandas as pd
import requests


API_URL = "http://127.0.0.1:8000/countries"
OUTPUT_DIR = Path(__file__).resolve().parent
CSV_PATH = OUTPUT_DIR / "exported_countries.csv"
PLOT_PATH = OUTPUT_DIR / "population_vs_area.png"


def main():
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()
    records = response.json()

    if not records:
        print("The API returned no countries. Run scraper.py first.")
        return

    dataframe = pd.DataFrame(records)
    # Keep columns in the order requested by the project.
    dataframe = dataframe[
        ["country_name", "capital", "population", "area"]
    ]

    print("Countries received from the API:")
    print(dataframe.to_string(index=False))

    dataframe.to_csv(CSV_PATH, index=False, encoding="utf-8")
    print(f"\nCSV saved to: {CSV_PATH}")

    plt.figure(figsize=(10, 6))
    plt.scatter(dataframe["population"], dataframe["area"])
    plt.title("Population vs Area of the First 20 Countries")
    plt.xlabel("Population")
    plt.ylabel("Area (sq. km)")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.tight_layout()
    plt.savefig(PLOT_PATH, dpi=150)
    plt.close()

    print(f"Scatter plot saved to: {PLOT_PATH}")


if __name__ == "__main__":
    main()
