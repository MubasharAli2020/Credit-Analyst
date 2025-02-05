import pandas as pd
import sys
import os

# Add the parent directory to Python's search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import load_data correctly
from scripts.load_data import load_data  # Ensure lowercase 'scripts'

def analyze_assets(file_path):
    """Calculates total assets and off-balance sheet amounts per sector."""
    final_df = load_data(file_path)

    # Separate Total Assets and Off-Balance Items
    total_assets_df = final_df[final_df["Group GL Name"] != "Off Balance"].groupby("Sector Name").agg(
        Total_Assets=("Amount", "sum")
    ).reset_index()

    off_balance_df = final_df[final_df["Group GL Name"] == "Off Balance"].groupby("Sector Name").agg(
        Off_Balance_Amount=("Amount", "sum"),
        Off_Balance_Count=("Group GL Name", "count")
    ).reset_index()

    # Merge results
    sector_analysis = total_assets_df.merge(
        off_balance_df, on="Sector Name", how="left"
    ).fillna(0)

    # Save results
    sector_analysis.to_excel("data/Sector_Analysis.xlsx", index=False)
    print("Sector Assets Analysis saved to data/Sector_Analysis.xlsx")

    # Print and return results
    print("\nSector Analysis Results:")
    print(sector_analysis)
    
    return sector_analysis

# Allow script to run independently
if __name__ == "__main__":
    file_path = "data/Common Data Warehouse-Orginal.xlsx"
    analyze_assets(file_path)
