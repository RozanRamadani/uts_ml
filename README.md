# Praktikum Pembelajaran Mesin - Pertemuan 8
## Purchase Intent Analytics — AI Visitor Intelligence
### Klasifikasi Naïve Bayes, Support Vector Machine (SVM), dan Decision Tree pada Online Shoppers Purchasing Intention

Repository ini berisi implementasi, analisis komparasi, dan aplikasi antarmuka analitik modern berbasis pembelajaran mesin untuk memprediksi niat pembelian (*Revenue*) pengunjung website e-commerce. Proyek ini membandingkan tiga algoritma (**Decision Tree**, **Gaussian Naïve Bayes**, dan **Support Vector Machine RBF**) dengan penanganan ketidakseimbangan data (*imbalanced data*) menggunakan **SMOTENC** dan **RandomUnderSampler**, serta dilengkapi aplikasi **Streamlit AI Analytics Dashboard** dengan desain modern setara produk SaaS komersial.

---

## 1. Dataset & Karakteristik Data
Dataset yang digunakan adalah `online_shoppers_intention.csv` dengan target klasifikasi **Revenue** (`True` / `False`).

- **Jumlah Baris Data Awal**: 12.330 baris
- **Jumlah Fitur Input**: 17 fitur (10 numerik kontinu/durasi, 4 numerik diskrit berkode kategori, dan 3 kategorikal teks/boolean)
- **Target**: `Revenue` (Apakah sesi kunjungan menghasilkan transaksi pembelian)
- **Missing Value**: 0 (Tidak ada data kosong)
- **Data Duplikat**: 125 baris (Dihapus pada tahap preprocessing)
- **Data Setelah Deduplikasi**: 12.205 baris
- **Distribusi Target Asli**:
  - `False` (Tidak beli) : 10.422 data (84,53%)
  - `True` (Membeli) : 1.908 data (15,47%)
- **Data Testing (20%)**: 2.441 baris (2.059 False, 382 True) tanpa resampling (suci dari data leakage).

---

## 2. Struktur Repository
```text
praktikum_ml_tm8/
├── dataset/
│   └── online_shoppers_intention.csv
│
├── konteks/
│   └── Soal UTS Prakt ML.pdf
│
├── outputs/
│   ├── figures/
│   │   ├── cm_dt_rus.png
│   │   ├── cm_dt_smotenc.png
│   │   ├── cm_nb_rus.png
│   │   ├── cm_nb_smotenc.png
│   │   ├── cm_svm_rus.png
│   │   ├── cm_svm_smotenc.png
│   │   ├── dist_after_rus.png
│   │   ├── dist_after_smotenc.png
│   │   ├── dist_before_resampling.png
│   │   └── perbandingan_metrik.png
│   │
│   ├── models/
│   │   └── best_model_bundle.joblib
│   │
│   ├── screenshots/
│   │   ├── overview_dashboard.png
│   │   ├── prediction_result_positive.png
│   │   ├── prediction_result_negative.png
│   │   ├── evaluasi_komparasi.png
│   │   └── metodologi_dataset.png
│   │
│   └── tables/
│       ├── evaluasi_model.csv
│       └── evaluasi_model_komparasi.csv
│
├── services/                        # Service Layer (Business Logic & Data Access)
│   ├── __init__.py
│   ├── data_service.py              # Loader CSV metrik evaluasi & metadata dataset
│   └── model_service.py             # Loader model bundle, validasi 17 fitur, preset & inference
│
├── ui/                              # Presentation Layer (Streamlit UI & View Modules)
│   ├── __init__.py
│   ├── components.py                # Reusable UI widgets (badges, metric cards, banner)
│   ├── dashboard.py                 # View 1: Overview & Performance KPI Dashboard
│   ├── evaluation_page.py           # View 3: Benchmark Model Komparasi & Confusion Matrix
│   ├── methodology_page.py          # View 4: Pipeline Arsitektur & Metadata Dokumentasi
│   ├── prediction.py                # View 2: Form Input 17 Fitur, Presets & Hasil Prediksi
│   └── styles.py                    # Desain CSS kustom modern dark SaaS
│
├── tests/                           # Unit Test Suite
│   ├── __init__.py
│   ├── test_data_service.py         # Pengujian integritas loader evaluasi CSV
│   └── test_model_service.py        # Pengujian bundel model, validasi fitur & prediksi
│
├── src/                             # Pipeline Eksperimen ML Inti
│   ├── data_preprocessing.py
│   ├── data_transformation.py
│   ├── imbalanced_data.py
│   ├── decision_tree.py
│   ├── naive_bayes.py
│   ├── svm.py
│   ├── evaluation.py
│   ├── main.py
│   └── generate_report.py
│
├── app.py                           # Streamlit Entry Point & Router (Modular & Ringkas)
├── app_backup.py                    # Arsip cadangan versi monolitik sebelum refactoring
├── requirements.txt
├── README.md
├── Laporan_Praktikum_Pertemuan_8.docx
└── Laporan_Praktikum_Pertemuan_8.pdf
```

---

## 3. Pembagian Modul Program

| Layer / Folder | File | Fungsi / Deskripsi |
| :--- | :--- | :--- |
| **Entry Point** | `app.py` | Router navigasi Streamlit, inisialisasi sesi, layout & pemanggilan view |
| **Services** | `services/model_service.py` | Pemuatan bundel model (`@st.cache_resource`), validasi 17 fitur input, mapping preset, dan kalkulasi inferensi probabilitas |
| | `services/data_service.py` | Pemuatan tabel metrik evaluasi (`@st.cache_data`) dan metadata visual confusion matrix |
| **UI Components** | `ui/components.py` | Komponen visual atomik (badge status, kartu KPI, banner keputusan) |
| | `ui/styles.py` | Definisi CSS styling terpusat (tipografi modern, cards, responsive tables) |
| **UI Views** | `ui/dashboard.py` | Halaman ringkasan eksekutif dan visualisasi interaktif Altair |
| | `ui/prediction.py` | Halaman formulir input 3-tab 17 fitur, preset cepat, dan display probabilitas |
| | `ui/evaluation_page.py` | Halaman tabel perbandingan 6 model, confusion matrix & breakdown TP/TN/FP/FN |
| | `ui/methodology_page.py` | Halaman alur eksperimen, metodologi bebas kebocoran data, dan data dictionary |
| **Testing** | `tests/test_model_service.py` | Unit test bundel model, skenario inferensi positif/negatif, dan proteksi 17 fitur |
| | `tests/test_data_service.py` | Unit test ketersediaan dan validitas CSV hasil eksperimen |
| **Pipeline ML** | `src/data_preprocessing.py` | Pembersihan data, drop duplikat, dan deteksi outlier |
| | `src/data_transformation.py` | Penskalaan fitur numerik dan encoding kategorikal (`ColumnTransformer`) |
| | `src/imbalanced_data.py` | Resampling SMOTENC dan RandomUnderSampler khusus data training |
| | `src/decision_tree.py` | Pipeline Decision Tree (baseline UTS) |
| | `src/naive_bayes.py` | Pipeline Gaussian Naïve Bayes |
| | `src/svm.py` | Pipeline Support Vector Machine RBF |
| | `src/evaluation.py` | Kalkulasi akurasi, presisi, recall, F1, dan plotting |
| | `src/main.py` | Eksekutor eksperimen komparasi 6 model dan penyimpanan bundel model |
| | `src/generate_report.py` | Generator laporan praktikum terpadu Word & PDF |

---

## 4. Alur Kerja Eksperimen (Pipeline Bebas Data Leakage)

```text
                  Input Data (12.330 baris)
                             ↓
              Preprocessing (Drop 125 duplikat)
                             ↓
              Split Data 80:20 (Stratified, seed=42)
               ┌─────────────┴─────────────┐
               ↓                           ↓
      Data Training (80%)           Data Testing (20%)
         (9.764 baris)                (2.441 baris)
               ↓                           │
     Resampling Training Only              │
  (SMOTENC / RandomUnderSampler)           │
               ↓                           │
     Fit ColumnTransformer                 │
(StandardScaler + OneHotEncoder)           │
               ↓                           │
        Transform Train                    ↓
               ↓                   Transform Test (Pasif)
    Training 3 Algoritma                   ↓
   (DT, Naive Bayes, SVM) ───────→ Testing & Evaluasi
                                           ↓
                               Confusion Matrix & Metrik
```

---

## 5. Hasil Aktual Eksperimen (6 Kombinasi Model)

Semua metrik dihitung terhadap kelas minoritas positif `Revenue = True` pada 2.441 sampel data testing asli:

| No | Model & Resampling | Accuracy | Precision | Recall | F1-Score |
| :---: | :--- | :---: | :---: | :---: | :---: |
| 1 | **Decision Tree + SMOTENC** *(UTS)* | 86,89% | 56,20% | 73,56% | 63,72% |
| 2 | **Decision Tree + RandomUnderSampler** *(UTS)* | 83,61% | 48,59% | 81,41% | 60,86% |
| 3 | **Gaussian Naive Bayes + SMOTENC** | 48,26% | 21,92% | 90,05% | 35,26% |
| 4 | **Gaussian Naive Bayes + RandomUnderSampler** | 63,87% | 29,17% | **91,62%** | 44,25% |
| 5 | **SVM RBF + SMOTENC** ⭐ *(Terbaik)* | **87,46%** | **58,05%** | 71,73% | **64,17%** |
| 6 | **SVM RBF + RandomUnderSampler** | 85,33% | 52,11% | 77,75% | 62,40% |

### Ringkasan Analisis:
1. **SVM RBF + SMOTENC** terpilih sebagai model terbaik untuk antarmuka pengguna karena memperoleh **Akurasi tertinggi (87,46%)**, **Presisi tertinggi (58,05%)**, dan **F1-Score tertinggi (64,17%)**, serta meminimalkan kesalahan False Positive menjadi hanya 198 kasus.
2. **Gaussian Naive Bayes** mencatat Recall tertinggi (>90%), tetapi mengorbankan presisi (21,92% - 29,17%) akibat asumsi *conditional independence* yang terlanggar pada fitur analytics yang saling berkorelasi tinggi.
3. **SMOTENC** secara konsisten menghasilkan Akurasi, Presisi, dan F1-Score yang lebih seimbang dibandingkan RandomUnderSampler.

---

## 6. Antarmuka Pengguna Redesigned: Purchase Intent Analytics

Aplikasi web didesain ulang dengan standar visual produk SaaS analitik modern:
- **📊 Overview & Dashboard**: Kartu metrik performa model aktif, visualisasi komparatif interaktif Altair bar chart, dan ringkasan dataset.
- **🎯 Prediction Workspace**: Formulir input 17 fitur yang dikelompokkan ke dalam 3 tab (Aktivitas Halaman, Metrik Sesi Google Analytics, dan Profil Pengunjung), dilengkapi preset cepat ("Niat Beli Tinggi" dan "Pengunjung Kasual"), serta panel hasil prediksi probabilistik.
- **📈 Evaluasi & Komparasi**: Tabel benchmark interaktif 6 model, Confusion Matrix SVM RBF + SMOTENC, dekomposisi TP/TN/FP/FN, dan analisis mendalam.
- **📖 Metodologi & Dataset**: Dokumentasi teknis alur preprocessing, isolasi resampling bebas kebocoran data, dan arsitektur model.

Tangkapan layar asli tersimpan di folder `outputs/screenshots/`:
- `outputs/screenshots/overview_dashboard.png`
- `outputs/screenshots/prediction_result_positive.png`
- `outputs/screenshots/prediction_result_negative.png`
- `outputs/screenshots/evaluasi_komparasi.png`
- `outputs/screenshots/metodologi_dataset.png`

---

## 7. Panduan Menjalankan Program

### Prasyarat Dependensi
Pastikan dependensi pada `requirements.txt` telah terpasang:
```bash
pip install -r requirements.txt
```

### A. Menjalankan Eksperimen Pelatihan & Evaluasi
Untuk melatih ulang seluruh model dan menghasilkan tabel serta grafik:
```bash
python src/main.py
```
Hasil evaluasi akan otomatis disimpan pada:
- `outputs/tables/evaluasi_model_komparasi.csv`
- `outputs/figures/` (grafik matriks konfusi dan komparasi metrik)
- `outputs/models/best_model_bundle.joblib` (bundel model terbaik)

### B. Menjalankan Aplikasi Antarmuka Streamlit
Untuk menjalankan aplikasi web interaktif:
```bash
streamlit run app.py
```
Aplikasi akan terbuka otomatis di peramban web pada alamat:
`http://localhost:8501`

### C. Menghasilkan Dokumen Laporan DOCX dan PDF
Untuk memperbarui atau membuat ulang file laporan lengkap:
```bash
python src/generate_report.py
```

### D. Menjalankan Unit Test Terotomasi
Untuk memverifikasi fungsi data service, model service, validasi input, dan inferensi:
```bash
python -m unittest discover tests
```

---

## 8. Keterbatasan Model & Catatan Praktis
1. **Kompleksitas Komputasi SVM**: Pelatihan SVM dengan kernel RBF memiliki kompleksitas kuadratik terhadap ukuran sampel resample. Pada dataset dengan jutaan baris, disarankan menggunakan linear SVM atau subsampling.
2. **Karakteristik Data Kunjungan**: Prediksi model didasarkan murni pada 17 fitur perilaku browsing pengguna. Faktor eksternal seperti harga promo diskon khusus, ketersediaan stok, atau kampanye pemasaran di luar sesi tidak terekam dalam dataset.