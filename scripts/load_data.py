# scripts/load_data.py
import pandas as pd

def load_data(file_path):
    "C:\\Users\\18pug\\Desktop\\Credit Analyst\\Data\\Common Data Warehouse-Orginal.xlsx"
    
    xls = pd.ExcelFile(file_path)
    
    # Load individual sheets
    customer_df = xls.parse('Customer')
    instrument_df = xls.parse('Instrument')
    financial_df = xls.parse('Financial')
    gl_df = xls.parse('GL')
    group_gl_df = xls.parse('Group GL')

    # Merge data based on the relationships
    financial_customer_df = financial_df.merge(
        customer_df, left_on="Cust ID", right_on="Customer ID", how="left"
    )
    
    financial_customer_instrument_df = financial_customer_df.merge(
        instrument_df, left_on="Agmt ID", right_on="Agreement ID", how="left"
    )
    
    financial_customer_instrument_gl_df = financial_customer_instrument_df.merge(
        gl_df, left_on="GL Acct ID", right_on="GL Account ID", how="left"
    )
    
    final_df = financial_customer_instrument_gl_df.merge(
        group_gl_df, left_on="Group GL Acct ID", right_on="Group GL Account ID", how="left"
    )

    return final_df
