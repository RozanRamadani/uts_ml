import numpy as np
import pandas as pd


# 1. Load Data
def load_data(filepath):
    print(f"Loading data from {filepath}...")
    return pd.read_csv(filepath)


def preprocess_data(df):
    print("\n--- Preprocessing ---")

    # 2. Check and handle missing values
    missing = df.isna().sum().sum()
    print(f"Total missing values: {missing}")
    if missing > 0:
        df = df.dropna().copy()
        print(f"Dropped rows containing missing values. Remaining rows: {len(df)}")

    # 3. Check and handle duplicates
    duplicates = df.duplicated().sum()
    print(f"Total duplicates found: {duplicates}")
    if duplicates > 0:
        df = df.drop_duplicates().copy()
        print(f"Dropped {duplicates} duplicate rows. Remaining rows: {len(df)}")

    # 4. Detect outliers with IQR
    num_cols = df.select_dtypes(include=[np.number]).columns.drop(
        "Revenue", errors="ignore"
    )
    outlier_summary = {}
    for col in num_cols:
        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        outlier_summary[col] = int(
            ((df[col] < lower_bound) | (df[col] > upper_bound)).sum()
        )

    print("\nOutliers detected (IQR method):")
    for col, count in outlier_summary.items():
        if count > 0:
            print(f"  {col}: {count} outliers")

    # 5. Keep outliers; tree-based models are generally insensitive to scaling extremes.
    print("Outliers are retained to avoid discarding potentially useful observations.")

    # 6. Separate features and target
    X = df.drop(columns=["Revenue"])
    y = df["Revenue"]
    print("Features (X) and target (y) separated.")
    return X, y


if __name__ == "__main__":
    df = load_data("../dataset/online_shoppers_intention.csv")
    X, y = preprocess_data(df)
