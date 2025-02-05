import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the Excel file
file_path = "C:\\Users\\18pug\\Desktop\\Credit Analyst\\env\\Common Data Warehouse-Orginal.xlsx"
xls = pd.ExcelFile(file_path)

# Load all sheets into separate DataFrames
customer_df = xls.parse('Customer')
instrument_df = xls.parse('Instrument')
financial_df = xls.parse('Financial')
gl_df = xls.parse('GL')
group_gl_df = xls.parse('Group GL')

# Print column names to check structure
# print("Customer Columns:", customer_df.columns.tolist())
# print("Instrument Columns:", instrument_df.columns.tolist())
# print("Financial Columns:", financial_df.columns.tolist())
# print("GL Columns:", gl_df.columns.tolist())
# print("Group GL Columns:", group_gl_df.columns.tolist())

# Step 1: Merge Data Based on Relationships in the Data Model

# Merge Financial with Customer Data (to get sector information)
financial_customer_df = financial_df.merge(
    customer_df, left_on="Cust ID", right_on="Customer ID", how="left"
)

# Merge with Instrument Data (to get details about loans)
financial_customer_instrument_df = financial_customer_df.merge(
    instrument_df, left_on="Agmt ID", right_on="Agreement ID", how="left"
)

# Merge with GL Data (to categorize transactions)
financial_customer_instrument_gl_df = financial_customer_instrument_df.merge(
    gl_df, left_on="GL Acct ID", right_on="GL Account ID", how="left"
)

# Merge with Group GL Data (to classify transactions into assets or off-balance-sheet items)
final_df = financial_customer_instrument_gl_df.merge(
    group_gl_df, left_on="Group GL Acct ID", right_on="Group GL Account ID", how="left"
)

# Step 2: Calculate Total Assets (Excluding Off-Balance)
total_assets_df = final_df[final_df["Group GL Name"] != "Off Balance"].groupby("Sector Name").agg(
    Total_Assets=("Amount", "sum")  # Summing only on-balance amounts
).reset_index()

# Step 3: Calculate Off-Balance Amount Separately
off_balance_df = final_df[final_df["Group GL Name"] == "Off Balance"].groupby("Sector Name").agg(
    Off_Balance_Amount=("Amount", "sum"),  # Summing only off-balance-sheet amounts
    Off_Balance_Count=("Group GL Name", "count")  # Counting the number of off-balance transactions
).reset_index()

# Step 4: Merge Both Calculations into a Single DataFrame
sector_analysis = total_assets_df.merge(
    off_balance_df, on="Sector Name", how="left"
).fillna(0)  # Fill missing values with 0 for sectors without off-balance transactions

# Step 5: Display the Results
#print(sector_analysis)


# Step 1: Extract Adjustment Information from Source Column
# Create a new column that identifies whether the transaction is Adjusted (ADJ) or Original
final_df["Adjustment_Flag"] = final_df["Source"].astype(str).apply(lambda x: "Adjusted" if "ADJ" in x else "Original")

# Step 2: Aggregate Total Amount Before and After Adjustment for Each Sector
sector_adjustment_analysis = final_df.groupby(["Sector Name", "Adjustment_Flag"]).agg(
    Total_Amount=("Amount", "sum")  # Summing up amounts for both Original and Adjusted transactions
).reset_index()

# Step 3: Pivot the Data to Show Before and After Adjustment in Separate Columns
sector_adjustment_pivot = sector_adjustment_analysis.pivot(
    index="Sector Name", columns="Adjustment_Flag", values="Total_Amount"
).reset_index().fillna(0)  # Fill NaN with 0 in case some categories don’t have adjustments

# Rename columns for clarity
sector_adjustment_pivot.columns = ["Sector Name", "Total Amount Before Adjustment", "Total Amount After Adjustment"]

# Step 4: Display the Results

# Print the results to the terminal
print(sector_adjustment_pivot)

# Save results to an Excel file
# sector_adjustment_pivot.to_excel("Sector_Adjustment_Analysis.xlsx", index=False)
# print("Results saved to Sector_Adjustment_Analysis.xlsx")






