import unittest
from pathlib import Path
import numpy as np
import pandas as pd

from services.model_service import (
    format_input_dataframe,
    get_default_form_data,
    get_preset_data,
    load_model_bundle,
    predict_sample,
    validate_input,
)


class TestModelService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.bundle = load_model_bundle()

    def test_bundle_structure(self):
        """Memverifikasi bahwa bundel model memiliki seluruh artefak yang diperlukan."""
        self.assertIn("model", self.bundle)
        self.assertIn("transformer", self.bundle)
        self.assertIn("feature_names", self.bundle)
        self.assertIn("metrics", self.bundle)
        self.assertIn("model_name", self.bundle)

        self.assertEqual(len(self.bundle["feature_names"]), 17)
        self.assertEqual(self.bundle["model_name"], "SVM RBF + SMOTENC")

    def test_default_form_data(self):
        """Memverifikasi bahwa default form data mencakup seluruh 17 fitur."""
        default_data = get_default_form_data()
        self.assertEqual(len(default_data), 17)
        for feat in self.bundle["feature_names"]:
            self.assertIn(feat, default_data)

    def test_presets(self):
        """Memverifikasi bahwa seluruh preset valid dan memiliki 17 fitur."""
        for key in ["buyer", "casual", "reset"]:
            preset = get_preset_data(key)
            self.assertEqual(len(preset), 17)
            self.assertTrue(validate_input(preset, self.bundle["feature_names"]))

    def test_validation_missing_feature(self):
        """Memverifikasi bahwa validasi gagal jika ada fitur wajib yang hilang."""
        data = get_default_form_data()
        del data["Administrative"]
        with self.assertRaises(ValueError):
            validate_input(data, self.bundle["feature_names"])

    def test_validation_invalid_category(self):
        """Memverifikasi bahwa nilai kategori yang tidak valid ditolak."""
        data = get_default_form_data()
        data["Month"] = "BulanPalsu"
        with self.assertRaises(ValueError):
            validate_input(data, self.bundle["feature_names"])

        data2 = get_default_form_data()
        data2["VisitorType"] = "TipePalsu"
        with self.assertRaises(ValueError):
            validate_input(data2, self.bundle["feature_names"])

    def test_dataframe_formatting(self):
        """Memverifikasi format DataFrame output dari format_input_dataframe."""
        data = get_default_form_data()
        df = format_input_dataframe(data, self.bundle["feature_names"])
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape, (1, 17))
        self.assertEqual(list(df.columns), self.bundle["feature_names"])
        self.assertIsInstance(df["Administrative"].iloc[0], (int, np.integer))
        self.assertIsInstance(df["Administrative_Duration"].iloc[0], (float, np.floating))
        self.assertIsInstance(df["Weekend"].iloc[0], (bool, np.bool_))

    def test_prediction_buyer_sample(self):
        """Memverifikasi prediksi positif untuk sampel niat beli tinggi."""
        buyer_input = get_preset_data("buyer")
        result = predict_sample(self.bundle, buyer_input)

        self.assertIn("prediction", result)
        self.assertIn("prob_true", result)
        self.assertIn("prob_false", result)

        self.assertTrue(result["prediction"])
        self.assertGreater(result["prob_true"], 0.80)
        self.assertAlmostEqual(result["prob_true"] + result["prob_false"], 1.0, places=5)

    def test_prediction_casual_sample(self):
        """Memverifikasi prediksi negatif untuk sampel pengunjung kasual / bouncing."""
        casual_input = get_preset_data("casual")
        result = predict_sample(self.bundle, casual_input)

        self.assertFalse(result["prediction"])
        self.assertGreater(result["prob_false"], 0.90)
        self.assertAlmostEqual(result["prob_true"] + result["prob_false"], 1.0, places=5)


if __name__ == "__main__":
    unittest.main()
