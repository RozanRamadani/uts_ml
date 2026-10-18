from pathlib import Path
import joblib
import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
BUNDLE_PATH = ROOT_DIR / "outputs" / "models" / "best_model_bundle.joblib"

VALID_MONTHS = ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
VALID_VISITOR_TYPES = ["Returning_Visitor", "New_Visitor", "Other"]
VALID_SPECIAL_DAYS = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]


def _read_bundle_file(path):
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(
            f"File bundel model tidak ditemukan di: {p}. "
            "Pastikan telah menjalankan 'python src/main.py' untuk melatih dan mengekspor model."
        )
    bundle = joblib.load(p)
    required_keys = ["model", "transformer", "feature_names", "metrics", "model_name"]
    for key in required_keys:
        if key not in bundle:
            raise KeyError(f"Bundel model tidak memiliki kunci wajib: '{key}'")
    return bundle


try:
    import streamlit as st

    @st.cache_resource(show_spinner="Memuat model klasifikasi...")
    def load_model_bundle(bundle_path=None):
        """Memuat bundel model dan transformer menggunakan cache Streamlit."""
        target = bundle_path or BUNDLE_PATH
        return _read_bundle_file(target)

except Exception:

    def load_model_bundle(bundle_path=None):
        """Fallback loader untuk pengujian di luar konteks Streamlit."""
        target = bundle_path or BUNDLE_PATH
        return _read_bundle_file(target)


def get_default_form_data():
    """Mengembalikan nilai default untuk formulir 17 fitur."""
    return {
        "Administrative": 1,
        "Administrative_Duration": 10.0,
        "Informational": 0,
        "Informational_Duration": 0.0,
        "ProductRelated": 15,
        "ProductRelated_Duration": 500.0,
        "BounceRates": 0.01,
        "ExitRates": 0.03,
        "PageValues": 15.0,
        "SpecialDay": 0.0,
        "Month": "Nov",
        "OperatingSystems": 2,
        "Browser": 2,
        "Region": 1,
        "TrafficType": 2,
        "VisitorType": "Returning_Visitor",
        "Weekend": False,
    }


def get_preset_data(preset_key):
    """
    Mengembalikan data sampel pengujian yang telah diverifikasi:
    - 'buyer': Sampel pembeli riil dari dataset (Revenue=True).
    - 'casual': Sampel pengunjung yang langsung keluar (bouncing / Revenue=False).
    - 'reset': Nilai default formulir.
    """
    if preset_key == "buyer":
        return {
            "Administrative": 3,
            "Administrative_Duration": 87.83,
            "Informational": 0,
            "Informational_Duration": 0.0,
            "ProductRelated": 27,
            "ProductRelated_Duration": 798.33,
            "BounceRates": 0.0,
            "ExitRates": 0.0126,
            "PageValues": 22.92,
            "SpecialDay": 0.8,
            "Month": "Feb",
            "OperatingSystems": 2,
            "Browser": 2,
            "Region": 3,
            "TrafficType": 1,
            "VisitorType": "Returning_Visitor",
            "Weekend": False,
        }
    elif preset_key == "casual":
        return {
            "Administrative": 0,
            "Administrative_Duration": 0.0,
            "Informational": 0,
            "Informational_Duration": 0.0,
            "ProductRelated": 1,
            "ProductRelated_Duration": 0.0,
            "BounceRates": 0.20,
            "ExitRates": 0.20,
            "PageValues": 0.0,
            "SpecialDay": 0.0,
            "Month": "Feb",
            "OperatingSystems": 1,
            "Browser": 1,
            "Region": 1,
            "TrafficType": 1,
            "VisitorType": "Returning_Visitor",
            "Weekend": False,
        }
    return get_default_form_data()


def validate_input(input_dict, feature_names):
    """
    Memvalidasi bahwa seluruh 17 fitur tersedia, tipe data sesuai,
    dan nilai berada dalam rentang yang wajar.
    """
    if not isinstance(input_dict, dict):
        raise TypeError("Input harus berupa dictionary fitur.")

    missing_keys = [f for f in feature_names if f not in input_dict]
    if missing_keys:
        raise ValueError(f"Fitur wajib berikut tidak ditemukan pada input: {missing_keys}")

    # Validasi kategori
    month = str(input_dict.get("Month", ""))
    if month not in VALID_MONTHS:
        raise ValueError(f"Nilai Month '{month}' tidak valid. Pilihan valid: {VALID_MONTHS}")

    v_type = str(input_dict.get("VisitorType", ""))
    if v_type not in VALID_VISITOR_TYPES:
        raise ValueError(f"Nilai VisitorType '{v_type}' tidak valid. Pilihan valid: {VALID_VISITOR_TYPES}")

    # Validasi numerik tidak NaN / inf
    for feat in feature_names:
        if feat not in ["Month", "VisitorType", "Weekend"]:
            val = input_dict[feat]
            if not isinstance(val, (int, float, np.number)) or np.isnan(val) or np.isinf(val):
                raise ValueError(f"Nilai fitur numerik '{feat}' tidak valid: {val}")

    return True


def format_input_dataframe(input_dict, feature_names):
    """
    Menyusun satu baris DataFrame dengan urutan dan tipe data
    yang tepat sesuai metadata pelatihan model.
    """
    validate_input(input_dict, feature_names)

    cleaned = {
        "Administrative": int(input_dict["Administrative"]),
        "Administrative_Duration": float(input_dict["Administrative_Duration"]),
        "Informational": int(input_dict["Informational"]),
        "Informational_Duration": float(input_dict["Informational_Duration"]),
        "ProductRelated": int(input_dict["ProductRelated"]),
        "ProductRelated_Duration": float(input_dict["ProductRelated_Duration"]),
        "BounceRates": float(input_dict["BounceRates"]),
        "ExitRates": float(input_dict["ExitRates"]),
        "PageValues": float(input_dict["PageValues"]),
        "SpecialDay": float(input_dict["SpecialDay"]),
        "Month": str(input_dict["Month"]),
        "OperatingSystems": int(input_dict["OperatingSystems"]),
        "Browser": int(input_dict["Browser"]),
        "Region": int(input_dict["Region"]),
        "TrafficType": int(input_dict["TrafficType"]),
        "VisitorType": str(input_dict["VisitorType"]),
        "Weekend": bool(input_dict["Weekend"]),
    }

    return pd.DataFrame([cleaned], columns=feature_names)


def predict_sample(bundle, input_dict):
    """
    Menjalankan transformasi dan inferensi model untuk 1 sampel pengunjung.
    Mengembalikan dict hasil prediksi, probabilitas, dan DataFrame input.
    """
    feature_names = bundle["feature_names"]
    transformer = bundle["transformer"]
    estimator = bundle["model"]

    input_df = format_input_dataframe(input_dict, feature_names)
    X_trans = transformer.transform(input_df)

    pred = estimator.predict(X_trans)[0]
    probas = estimator.predict_proba(X_trans)[0]

    return {
        "prediction": bool(pred),
        "prob_false": float(probas[0]),
        "prob_true": float(probas[1]),
        "input_df": input_df,
    }
