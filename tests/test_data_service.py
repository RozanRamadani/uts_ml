import unittest
from pathlib import Path
import pandas as pd

from services.data_service import (
    get_confusion_matrix_path,
    get_dataset_summary,
    load_evaluation_metrics,
)


class TestDataService(unittest.TestCase):
    def test_load_evaluation_metrics(self):
        """Memverifikasi bahwa file evaluasi aktual dapat dimuat dan memiliki 6 baris model."""
        df = load_evaluation_metrics()
        self.assertIsNotNone(df)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 6)
        expected_cols = ["Model", "Accuracy", "Precision", "Recall", "F1-Score"]
        for col in expected_cols:
            self.assertIn(col, df.columns)

        models = list(df["Model"])
        self.assertIn("SVM RBF + SMOTENC", models)
        self.assertIn("Decision Tree + SMOTENC", models)
        self.assertIn("Gaussian Naive Bayes + SMOTENC", models)

    def test_dataset_summary(self):
        """Memverifikasi statistik dataset yang telah diaudit."""
        summary = get_dataset_summary()
        self.assertEqual(summary["raw_rows"], 12330)
        self.assertEqual(summary["duplicates_removed"], 125)
        self.assertEqual(summary["clean_rows"], 12205)
        self.assertEqual(summary["test_rows"], 2441)
        self.assertEqual(summary["train_rows"], 9764)
        self.assertEqual(summary["feature_count"], 17)

    def test_confusion_matrix_file_exists(self):
        """Memverifikasi keberadaan file gambar Confusion Matrix model aktif."""
        cm_path = get_confusion_matrix_path()
        self.assertTrue(Path(cm_path).exists())


if __name__ == "__main__":
    unittest.main()
