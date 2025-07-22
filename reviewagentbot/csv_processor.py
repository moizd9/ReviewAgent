import pandas as pd
from .single_business import process_single_business

def process_csv(uploaded_df):
    uploaded_df['AI Reply'] = uploaded_df.iloc[:, 0].apply(process_single_business)
    return uploaded_df
