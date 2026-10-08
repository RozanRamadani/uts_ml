from pathlib import Path

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


ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT_DIR / "dataset" / "online_shoppers_intention.csv"
FIGURES_DIR = ROOT_DIR / "outputs" / "figures"
TABLES_DIR = ROOT_DIR / "outputs" / "tables"


def run_experiment(name, X_train_resampled, y_train_resampled, X_test, y_test, cm_path):
    # 5. Transformation: fit only on resampled training data
    transformer, _, _ = get_preprocessor(X_train_resampled)
    X_train_transformed = transformer.fit_transform(X_train_resampled)
    X_test_transformed = transformer.transform(X_test)

    # 6. Training
    model = create_decision_tree()
    model.fit(X_train_transformed, y_train_resampled)

    # 7. Testing
    y_pred = model.predict(X_test_transformed)

    # 8. Evaluation
    metrics = evaluate_model(name, y_test, y_pred)
    plot_confusion_matrix(y_test, y_pred, name, cm_path)
    return metrics


def main():
    FIGURES_DIR.mkdir(parents=True, exist_ok=True)
    TABLES_DIR.mkdir(parents=True, exist_ok=True)

    # 1. Load Data
    df = load_data(DATA_PATH)

    # 2. Preprocessing
    X, y = preprocess_data(df)

    # 3. Split Data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"Training rows: {len(X_train)} | Testing rows: {len(X_test)}")
    plot_class_distribution(
        y_train,
        "Distribusi Kelas Training Sebelum Resampling",
        FIGURES_DIR / "dist_before_resampling.png",
    )

    # 4. Resampling and experiments use training data only
    X_train_smote, y_train_smote = resample_with_smotenc(X_train, y_train)
    print("SMOTENC class distribution:")
    print(y_train_smote.value_counts())
    plot_class_distribution(
        y_train_smote,
        "Distribusi Target (Setelah SMOTENC)",
        FIGURES_DIR / "dist_after_smotenc.png",
    )
    metrics_smote = run_experiment(
        "Decision Tree + SMOTENC",
        X_train_smote,
        y_train_smote,
        X_test,
        y_test,
        FIGURES_DIR / "cm_dt_smotenc.png",
    )

    X_train_rus, y_train_rus = resample_with_random_under_sampler(X_train, y_train)
    print("RandomUnderSampler class distribution:")
    print(y_train_rus.value_counts())
    plot_class_distribution(
        y_train_rus,
        "Distribusi Target (Setelah RandomUnderSampler)",
        FIGURES_DIR / "dist_after_rus.png",
    )
    metrics_rus = run_experiment(
        "Decision Tree + RandomUnderSampler",
        X_train_rus,
        y_train_rus,
        X_test,
        y_test,
        FIGURES_DIR / "cm_dt_rus.png",
    )

    metrics_df = pd.DataFrame([metrics_smote, metrics_rus])
    metrics_df.to_csv(TABLES_DIR / "evaluasi_model.csv", index=False)
    plot_metrics_comparison(
        metrics_df, FIGURES_DIR / "perbandingan_metrik.png"
    )
    print(f"Evaluation table saved to {TABLES_DIR / 'evaluasi_model.csv'}")
    print(f"Figures saved to {FIGURES_DIR}")


if __name__ == "__main__":
    main()
