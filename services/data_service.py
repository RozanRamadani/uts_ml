from pathlib import Path
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
EVAL_CSV_PATH = ROOT_DIR / "outputs" / "tables" / "evaluasi_model_komparasi.csv"
FIGURES_DIR = ROOT_DIR / "outputs" / "figures"
SCREENSHOTS_DIR = ROOT_DIR / "outputs" / "screenshots"
CM_SVM_PATH = FIGURES_DIR / "cm_svm_smotenc.png"


def _read_eval_csv(path):
    p = Path(path)
    if p.exists():
        return pd.read_csv(p)
    return None


try:
    import streamlit as st

    @st.cache_data
    def load_evaluation_metrics(csv_path=None):
        """Memuat tabel evaluasi model dengan caching Streamlit."""
        target = csv_path or EVAL_CSV_PATH
        return _read_eval_csv(target)

except Exception:

    def load_evaluation_metrics(csv_path=None):
        """Fallback loader untuk pengujian di luar konteks Streamlit."""
        target = csv_path or EVAL_CSV_PATH
        return _read_eval_csv(target)


def get_dataset_summary():
    """Mengembalikan ringkasan statistik dataset yang telah diverifikasi."""
    return {
        "dataset_name": "Online Shoppers Purchasing Intention",
        "file_name": "online_shoppers_intention.csv",
        "raw_rows": 12330,
        "duplicates_removed": 125,
        "clean_rows": 12205,
        "feature_count": 17,
        "target_col": "Revenue",
        "train_rows": 9764,
        "test_rows": 2441,
        "test_ratio": "20% (Stratified)",
        "train_ratio": "80%",
        "class_false_count": 10422,
        "class_false_pct": 84.53,
        "class_true_count": 1908,
        "class_true_pct": 15.47,
    }


def get_confusion_matrix_path():
    """Mengembalikan path file Confusion Matrix model SVM terpilih."""
    return CM_SVM_PATH
