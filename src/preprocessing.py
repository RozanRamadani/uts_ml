import pandas as pd
import numpy as np
import json
import os

def load_data(filepath):
    print(f"Loading data from {filepath}...")
    df = pd.read_csv(filepath)
    return df

def preprocess_data(df):
    print("\n--- Preprocessing ---")
    
    # 1. Check Missing Values
    missing = df.isnull().sum().sum()
    print(f"Total missing values: {missing}")
    if missing > 0:
        df = df.dropna() # simplistic handling, but we know it's 0 for this dataset
        print("Dropped missing values.")

    # 2. Check and Remove Duplicates
    duplicates = df.duplicated().sum()
    print(f"Total duplicates found: {duplicates}")
    if duplicates > 0:
        df = df.drop_duplicates()
        print(f"Dropped {duplicates} duplicate rows. Remaining rows: {len(df)}")

    # 3. Outlier Detection (IQR) on numerical features
    num_cols = df.select_dtypes(include=[np.number]).columns
    outlier_summary = {}
    for col in num_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        outliers = ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        outlier_summary[col] = int(outliers)
    
    print("\nOutliers detected (IQR method):")
    for k, v in outlier_summary.items():
        if v > 0:
            print(f"  {k}: {v} outliers")
    print("Catatan: Outlier tidak dihapus karena model Decision Tree kebal terhadap outlier (robust to outliers). Penghapusan outlier ekstensif juga berisiko menghilangkan informasi penting pada dataset imbalanced.")

    # Split Features and Target
    X = df.drop(columns=['Revenue'])
    y = df['Revenue']
    print("\nFitur (X) dan Target (y) telah dipisahkan.")
    return X, y

if __name__ == '__main__':
    df = load_data('../dataset/online_shoppers_intention.csv')
    X, y = preprocess_data(df)
