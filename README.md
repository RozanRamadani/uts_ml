# UTS Praktikum Pembelajaran Mesin - Soal C

Repository ini berisi implementasi Decision Tree pada dataset Online Shoppers Purchasing Intention dengan penanganan imbalanced data menggunakan metode SMOTENC dan RandomUnderSampler.

## 1. Dataset
Dataset yang digunakan adalah `online_shoppers_intention.csv` dengan target klasifikasi **Revenue**.

- **Jumlah data awal**: 12.330 baris
- **Jumlah kolom**: 18
- **Missing value**: 0
- **Duplikat**: 125 baris
- **Data setelah penghapusan duplikat**: 12.205 baris
- **Kelas target**:
  - `False` : 10.422 data (84,53%)
  - `True` : 1.908 data (15,47%)

Distribusi tersebut menunjukkan adanya ketidakseimbangan kelas sehingga digunakan metode resampling pada data training.

## 2. Struktur Repository
```text
uts_ml/
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
│   │   ├── dist_after_rus.png
│   │   ├── dist_after_smotenc.png
│   │   ├── dist_before_resampling.png
│   │   └── perbandingan_metrik.png
│   │
│   └── tables/
│       └── evaluasi_model.csv
│
├── src/
│   ├── main.py
│   ├── data_preprocessing.py
│   ├── data_transformation.py
│   ├── imbalanced_data.py
│   ├── decision_tree.py
│   └── evaluation.py
│
├── requirements.txt
└── README.md
```

## 3. Pembagian Modul Program

| File | Fungsi |
| --- | --- |
| `data_preprocessing.py` | Load data, pemeriksaan missing value, duplikat, deteksi outlier, serta pemisahan fitur dan target |
| `data_transformation.py` | Transformasi fitur numerik menggunakan StandardScaler dan fitur kategorikal menggunakan OneHotEncoder |
| `imbalanced_data.py` | Menangani ketidakseimbangan kelas menggunakan SMOTENC dan RandomUnderSampler |
| `decision_tree.py` | Membuat model DecisionTreeClassifier |
| `evaluation.py` | Menghitung metrik evaluasi dan membuat grafik |
| `main.py` | Mengatur dan menjalankan seluruh alur program |

## 4. Alur Program
Program mengikuti alur pada soal UTS:

```text
Input Data
    ↓
Preprocessing
    ↓
Split Data 80:20
    ↓
 ┌───────────────┐
 │               │
Training       Testing
 │               │
Resampling    Transformation
 │               │
Transformation   │
 │               │
Decision Tree    │
 │               │
Testing ←────────┘
    ↓
Evaluasi
```
Resampling hanya dilakukan pada data training, sedangkan data testing tetap digunakan dalam kondisi aslinya untuk evaluasi.

**Tahapan Detail:**
1. **Input**: Membaca dataset `online_shoppers_intention.csv`.
2. **Preprocessing**:
   - Memeriksa missing value.
   - Menghapus data duplikat.
   - Mendeteksi outlier menggunakan metode IQR.
   - Outlier tidak dihapus karena Decision Tree relatif tidak sensitif terhadap nilai ekstrem.
3. **Split Data**: Data dibagi menjadi 80% training (9.764 data) dan 20% testing (2.441 data) dengan stratifikasi berdasarkan target Revenue.
4. **Resampling**: Dua metode dibandingkan pada data training: SMOTENC dan RandomUnderSampler.
5. **Transformation**: Numerik dengan StandardScaler dan Kategorikal dengan OneHotEncoder. Transformer di-fit menggunakan data training.
6. **Training**: Data hasil resampling dan transformasi digunakan untuk melatih Decision Tree.
7. **Testing**: Model memprediksi `X_test` yang asli.
8. **Evaluasi**: Performa dievaluasi menggunakan Confusion Matrix, Accuracy, Precision, Recall, dan F1-Score.

## 5. Hasil Eksperimen

### Decision Tree + SMOTENC
- **Distribusi training setelah SMOTENC**:
  - `False` : 8238
  - `True`  : 8238

| Metrik | Nilai |
| --- | --- |
| Accuracy | 86,89% |
| Precision | 56,20% |
| Recall | 73,56% |
| F1-Score | 63,72% |

**Confusion Matrix**:
```text
[[1840  219]
 [ 101  281]]
```

### Decision Tree + RandomUnderSampler
- **Distribusi training setelah RandomUnderSampler**:
  - `False` : 1526
  - `True`  : 1526

| Metrik | Nilai |
| --- | --- |
| Accuracy | 83,61% |
| Precision | 48,59% |
| Recall | 81,41% |
| F1-Score | 60,86% |

**Confusion Matrix**:
```text
[[1730  329]
 [  71  311]]
```

### Perbandingan
SMOTENC menghasilkan Accuracy, Precision, dan F1-Score yang lebih tinggi, sedangkan RandomUnderSampler menghasilkan Recall yang lebih tinggi. Dengan demikian, pada eksperimen ini SMOTENC memberikan performa yang lebih seimbang berdasarkan F1-Score dan Accuracy. Sementara itu, RandomUnderSampler lebih baik jika prioritas utama adalah menangkap sebanyak mungkin data dari kelas True atau pembeli.

## 6. Cara Menjalankan
Pastikan dependency pada `requirements.txt` telah terpasang, kemudian dari root repository jalankan:

```bash
python src/main.py
```

Hasil evaluasi akan disimpan pada `outputs/tables/evaluasi_model.csv`, sedangkan grafik disimpan pada folder `outputs/figures/`.