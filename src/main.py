import pandas as pd
import numpy as np
import os
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from imblearn.pipeline import Pipeline as ImbPipeline
from imblearn.over_sampling import SMOTENC
from imblearn.under_sampling import RandomUnderSampler

# Local imports
from preprocessing import load_data, preprocess_data
from transformation import get_preprocessor
from evaluation import evaluate_model, plot_confusion_matrix, plot_class_distribution, plot_metrics_comparison

def main():
    print("Memulai Tahap 2: Implementasi Pipeline Machine Learning")
    
    # 1. & 2. Preprocessing
    df = load_data('../dataset/online_shoppers_intention.csv')
    X, y = preprocess_data(df)
    
    plot_class_distribution(y, 'Distribusi Target (Sebelum Resampling)', '../outputs/figures/dist_before_resampling.png')
    
    # Identify categorical indices for SMOTENC
    cat_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()
    cat_indices = [X.columns.get_loc(c) for c in cat_cols]
    
    # 3. Splitting
    print("\n--- Data Splitting ---")
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    print(f"Total baris Training: {len(X_train)} (False: {sum(~y_train)}, True: {sum(y_train)})")
    print(f"Total baris Testing: {len(X_test)} (False: {sum(~y_test)}, True: {sum(y_test)})")

    # 4. Transformation Setup
    preprocessor, _, _ = get_preprocessor(X)
    
    # Base Model
    dt_model = DecisionTreeClassifier(random_state=42, max_depth=10) # max_depth to prevent massive overfitting
    
    # --- Eksperimen A: SMOTENC Oversampling ---
    print("\n--- Eksperimen A: Oversampling (SMOTENC) ---")
    print("Alasan penggunaan SMOTENC: Dataset memiliki fitur kategorikal (Month, VisitorType, dsb). Menggunakan SMOTE biasa setelah encoding akan menghasilkan nilai sintetis desimal pada fitur dummy kategorikal yang tidak valid (misal Month_Feb = 0.5). SMOTENC menangani fitur kategorikal secara natural sebelum ditransformasi.")
    
    pipeline_smote = ImbPipeline(steps=[
        ('resampler', SMOTENC(categorical_features=cat_indices, random_state=42)),
        ('preprocessor', preprocessor),
        ('classifier', dt_model)
    ])
    
    pipeline_smote.fit(X_train, y_train)
    
    # To plot distribution after SMOTENC, we need to extract the resampled y
    smotenc = SMOTENC(categorical_features=cat_indices, random_state=42)
    _, y_train_smote = smotenc.fit_resample(X_train, y_train)
    plot_class_distribution(y_train_smote, 'Distribusi Target (Setelah SMOTENC)', '../outputs/figures/dist_after_smotenc.png')
    print(f"Distribusi kelas setelah SMOTENC: False: {sum(~y_train_smote)}, True: {sum(y_train_smote)}")
    
    # Predict & Evaluate
    y_pred_smote = pipeline_smote.predict(X_test)
    eval_smote = evaluate_model("Decision Tree + SMOTENC", y_test, y_pred_smote)
    plot_confusion_matrix(y_test, y_pred_smote, "Decision Tree + SMOTENC", '../outputs/figures/cm_dt_smotenc.png')
    
    # --- Eksperimen B: RandomUnderSampler ---
    print("\n--- Eksperimen B: Undersampling (RandomUnderSampler) ---")
    
    pipeline_rus = ImbPipeline(steps=[
        ('resampler', RandomUnderSampler(random_state=42)),
        ('preprocessor', preprocessor),
        ('classifier', dt_model)
    ])
    
    pipeline_rus.fit(X_train, y_train)
    
    rus = RandomUnderSampler(random_state=42)
    _, y_train_rus = rus.fit_resample(X_train, y_train)
    plot_class_distribution(y_train_rus, 'Distribusi Target (Setelah RandomUnderSampler)', '../outputs/figures/dist_after_rus.png')
    print(f"Distribusi kelas setelah RandomUnderSampler: False: {sum(~y_train_rus)}, True: {sum(y_train_rus)}")
    
    # Predict & Evaluate
    y_pred_rus = pipeline_rus.predict(X_test)
    eval_rus = evaluate_model("Decision Tree + RandomUnderSampler", y_test, y_pred_rus)
    plot_confusion_matrix(y_test, y_pred_rus, "Decision Tree + RandomUnderSampler", '../outputs/figures/cm_dt_rus.png')
    
    # --- Saving Metrics ---
    metrics_df = pd.DataFrame([eval_smote, eval_rus])
    metrics_df.to_csv('../outputs/tables/evaluasi_model.csv', index=False)
    print("\nMetrik evaluasi telah disimpan di outputs/tables/evaluasi_model.csv")
    
    # Plot comparison
    plot_metrics_comparison(metrics_df, '../outputs/figures/perbandingan_metrik.png')
    print("Seluruh grafik telah disimpan di outputs/figures/")

if __name__ == '__main__':
    # Pastikan current working directory benar
    if not os.path.exists('../outputs/figures'):
        os.makedirs('../outputs/figures', exist_ok=True)
    if not os.path.exists('../outputs/tables'):
        os.makedirs('../outputs/tables', exist_ok=True)
    main()
