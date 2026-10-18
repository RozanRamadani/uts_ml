from pathlib import Path

import joblib
import pandas as pd
from sklearn.model_selection import train_test_split

from data_preprocessing import load_data, preprocess_data
from data_transformation import get_preprocessor
from decision_tree import create_decision_tree
from evaluation import (
    evaluate_model,
    plot_class_distribution,
    plot_confusion_matrix,
    plot_metrics_comparison,
)
from imbalanced_data import (
    resample_with_random_under_sampler,
    resample_with_smotenc,
)
from naive_bayes import create_naive_bayes
from svm import create_svm


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "dataset" / "online_shoppers_intention.csv"
FIGURES_DIR = ROOT_DIR / "outputs" / "figures"
TABLES_DIR = ROOT_DIR / "outputs" / "tables"
MODELS_DIR = ROOT_DIR / "outputs" / "models"


def run_single_experiment(
    name,
    model,
    X_train_resampled,
    y_train_resampled,
    X_test,
    y_test,
    cm_path,
    transformer=None,
):
    """
    Train and evaluate a single model.
    If transformer is not provided, fit a new one on X_train_resampled.
    """
    if transformer is None:
        transformer, _, _ = get_preprocessor(X_train_resampled)
        X_train_transformed = transformer.fit_transform(X_train_resampled)
    else:
        X_train_transformed = transformer.transform(X_train_resampled)

    X_test_transformed = transformer.transform(X_test)

    # Train model
    print(f"\n[Training] {name}...")
    model.fit(X_train_transformed, y_train_resampled)

    # Test model
    y_pred = model.predict(X_test_transformed)

    # Evaluate
    metrics = evaluate_model(name, y_test, y_pred)
    plot_confusion_matrix(y_test, y_pred, name, cm_path)

    return metrics, model, transformer


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)
    MODELS_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load Data
    df = load_data(DATA_PATH)

    # 2. Preprocessing
    X, y = preprocess_data(df)

    # 3. Split Data (80% training, 20% testing, stratified)
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"\nData Split Summary:")
    print(f"Total: {len(X)} | Training: {len(X_train)} | Testing: {len(X_test)}")
    plot_class_distribution(
        y_train,
        "Distribusi Kelas Training Sebelum Resampling",
        FIGURES_DIR / "dist_before_resampling.png",
    )

    # 4. Resampling on Training Data Only
    print("\n--- Resampling Data Training ---")
    X_train_smote, y_train_smote = resample_with_smotenc(X_train, y_train)
    print("SMOTENC training class distribution:")
    print(y_train_smote.value_counts())
    plot_class_distribution(
        y_train_smote,
        "Distribusi Target (Setelah SMOTENC)",
        FIGURES_DIR / "dist_after_smotenc.png",
    )

    X_train_rus, y_train_rus = resample_with_random_under_sampler(X_train, y_train)
    print("RandomUnderSampler training class distribution:")
    print(y_train_rus.value_counts())
    plot_class_distribution(
        y_train_rus,
        "Distribusi Target (Setelah RandomUnderSampler)",
        FIGURES_DIR / "dist_after_rus.png",
    )

    # Pre-fit transformers for each resampled training set to ensure exact parity
    transformer_smote, num_cols, cat_cols = get_preprocessor(X_train_smote)
    X_train_smote_trans = transformer_smote.fit_transform(X_train_smote)

    transformer_rus, _, _ = get_preprocessor(X_train_rus)
    X_train_rus_trans = transformer_rus.fit_transform(X_train_rus)

    # Define the 6 experimental combinations
    experiments = [
        # (name, model, X_train_trans, y_train, transformer, cm_filename)
        (
            "Decision Tree + SMOTENC",
            create_decision_tree(random_state=42, max_depth=10),
            X_train_smote_trans,
            y_train_smote,
            transformer_smote,
            "cm_dt_smotenc.png",
        ),
        (
            "Decision Tree + RandomUnderSampler",
            create_decision_tree(random_state=42, max_depth=10),
            X_train_rus_trans,
            y_train_rus,
            transformer_rus,
            "cm_dt_rus.png",
        ),
        (
            "Gaussian Naive Bayes + SMOTENC",
            create_naive_bayes(var_smoothing=1e-9),
            X_train_smote_trans,
            y_train_smote,
            transformer_smote,
            "cm_nb_smotenc.png",
        ),
        (
            "Gaussian Naive Bayes + RandomUnderSampler",
            create_naive_bayes(var_smoothing=1e-9),
            X_train_rus_trans,
            y_train_rus,
            transformer_rus,
            "cm_nb_rus.png",
        ),
        (
            "SVM RBF + SMOTENC",
            create_svm(kernel="rbf", c=1.0, probability=True, random_state=42),
            X_train_smote_trans,
            y_train_smote,
            transformer_smote,
            "cm_svm_smotenc.png",
        ),
        (
            "SVM RBF + RandomUnderSampler",
            create_svm(kernel="rbf", c=1.0, probability=True, random_state=42),
            X_train_rus_trans,
            y_train_rus,
            transformer_rus,
            "cm_svm_rus.png",
        ),
    ]

    all_metrics = []
    trained_artifacts = {}

    for name, model, X_tr_trans, y_tr, trans, cm_name in experiments:
        cm_filepath = FIGURES_DIR / cm_name
        X_te_trans = trans.transform(X_test)

        print(f"\n[Training & Evaluating] {name}...")
        model.fit(X_tr_trans, y_tr)
        y_pred = model.predict(X_te_trans)

        metrics = evaluate_model(name, y_test, y_pred)
        plot_confusion_matrix(y_test, y_pred, name, cm_filepath)

        all_metrics.append(metrics)
        trained_artifacts[name] = {
            "model": model,
            "transformer": trans,
            "metrics": metrics,
        }

    # Save metrics to CSV
    metrics_df = pd.DataFrame(all_metrics)
    metrics_csv_path = TABLES_DIR / "evaluasi_model_komparasi.csv"
    metrics_df.to_csv(metrics_csv_path, index=False)
    metrics_df.to_csv(TABLES_DIR / "evaluasi_model.csv", index=False)
    print(f"\nAll metrics successfully saved to:\n  - {metrics_csv_path}\n  - {TABLES_DIR / 'evaluasi_model.csv'}")

    # Plot metrics comparison
    comparison_fig_path = FIGURES_DIR / "perbandingan_metrik.png"
    plot_metrics_comparison(metrics_df, comparison_fig_path)
    print(f"Comparison plot saved to: {comparison_fig_path}")

    # Display comparison table in console
    print("\n" + "=" * 80)
    print("HASIL EVALUASI KOMPARASI 6 EKSPERIMEN".center(80))
    print("=" * 80)
    print(metrics_df.to_string(index=False))
    print("=" * 80)

    # Determine best model by F1-Score and Accuracy
    best_by_f1 = metrics_df.sort_values(by="F1-Score", ascending=False).iloc[0]
    best_by_acc = metrics_df.sort_values(by="Accuracy", ascending=False).iloc[0]

    print(f"\nModel Akurasi Tertinggi : {best_by_acc['Model']} ({best_by_acc['Accuracy']:.4f})")
    print(f"Model F1-Score Tertinggi: {best_by_f1['Model']} ({best_by_f1['F1-Score']:.4f})")

    # Select the model to be saved for Streamlit
    # Usually accuracy is requested by assignment, but we document both
    selected_name = best_by_acc["Model"]
    selected_bundle = trained_artifacts[selected_name]

    bundle_to_save = {
        "model_name": selected_name,
        "model": selected_bundle["model"],
        "transformer": selected_bundle["transformer"],
        "feature_names": list(X.columns),
        "num_cols": num_cols,
        "cat_cols": cat_cols,
        "metrics": selected_bundle["metrics"],
        "best_by_accuracy": best_by_acc["Model"],
        "best_by_f1": best_by_f1["Model"],
    }

    bundle_path = MODELS_DIR / "best_model_bundle.joblib"
    joblib.dump(bundle_to_save, bundle_path)
    print(f"\nSaved best model bundle for Streamlit app to:\n  {bundle_path}")


if __name__ == "__main__":
    main()
