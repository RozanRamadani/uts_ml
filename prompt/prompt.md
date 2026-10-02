Saya sedang mengerjakan UTS Praktikum Pembelajaran Mesin, Soal C, menggunakan Python di Visual Studio Code pada Windows.

Bertindaklah sebagai Machine Learning Engineer yang membantu saya mempersiapkan proyek ini secara bertahap. Untuk tahap sekarang, fokus hanya pada pemeriksaan workspace, dataset, dan perencanaan metodologi. Jangan membuat seluruh program atau laporan terlebih dahulu.

## 1. Ketentuan UTS

Soal C memiliki ketentuan:
- Dataset harus berupa klasifikasi dengan distribusi kelas imbalanced.
- Preprocessing: deteksi missing value, duplicate data, dan outlier.
- Transformation: bebas.
- Data splitting: 80% training dan 20% testing.
- Resampling: wajib menggunakan oversampling dan undersampling, hanya pada data training.
- Classification: Decision Tree.
- Evaluation: Confusion Matrix, Accuracy, Precision, Recall, dan F1-score.
- Output akhir berupa program Python dan laporan dengan screenshot hasil serta penjelasan.

## 2. Dataset yang direncanakan

Gunakan Online Shoppers Purchasing Intention Dataset dari Kaggle:

https://www.kaggle.com/datasets/imakash3011/online-shoppers-purchasing-intention-dataset

Target klasifikasi: Revenue.

Jika file dataset belum ada di workspace:
- Jangan membuat dataset palsu.
- Berikan instruksi mengunduh dataset dan meletakkannya di folder `dataset/`.
- Tunggu sampai dataset tersedia sebelum melakukan analisis aktual.

## 3. Pemeriksaan workspace

Periksa file yang tersedia di workspace, termasuk:
- Dokumen soal UTS.
- SPS atau daftar dataset dan metode yang digunakan kelompok lain.
- Dataset yang telah diunduh.

Jangan menghapus atau menimpa file yang sudah ada.

Periksa apakah Online Shoppers Purchasing Intention sudah digunakan oleh kelompok lain. Jika SPS tidak tersedia atau informasinya tidak lengkap, sampaikan bahwa keunikan dataset belum dapat dipastikan.

## 4. Analisis dataset

Jika dataset tersedia, gunakan Pandas untuk:
- Membaca dataset.
- Menampilkan 5 baris pertama.
- Menampilkan jumlah baris dan kolom.
- Menampilkan nama kolom dan tipe data.
- Mengidentifikasi kolom kategorikal dan numerik.
- Memeriksa missing value.
- Memeriksa jumlah baris duplikat.
- Menghitung distribusi kelas target Revenue.
- Menghitung persentase dan imbalance ratio.
- Memeriksa potensi outlier pada fitur numerik.

Jangan melakukan perubahan data permanen pada tahap ini.

## 5. Rencana metode

Evaluasi kelayakan metode berikut untuk dataset ini:
- Transformation: StandardScaler.
- Oversampling: SMOTE.
- Undersampling: RandomUnderSampler.
- Classification: Decision Tree.
- Evaluation: Confusion Matrix, Accuracy, Precision, Recall, dan F1-score.

Perhatikan bahwa dataset memiliki fitur kategorikal dan numerik. Pastikan strategi encoding dan resampling yang dipilih kompatibel dengan struktur data. Jika SMOTE biasa tidak sesuai, jelaskan alternatif yang secara teknis benar, misalnya SMOTENC, beserta alasannya.

Pastikan tidak terjadi data leakage. Transformation harus di-fit hanya pada data training, dan resampling tidak boleh diterapkan pada data testing.

## 6. Output tahap ini

Buat ringkasan analisis yang berisi:
1. Status ketersediaan dataset.
2. Struktur dan karakteristik dataset.
3. Distribusi kelas dan tingkat imbalance.
4. Hasil pemeriksaan missing value, duplicate, dan outlier.
5. Status keunikan dataset berdasarkan SPS.
6. Kelayakan dataset untuk Soal C.
7. Rekomendasi metode transformation dan resampling.
8. Rancangan alur pengerjaan tahap berikutnya.

Jika dataset tersedia, simpan ringkasan analisis ke `outputs/tables/analisis_dataset.csv` jika sesuai, dan buat ringkasan teks dalam `README.md` tanpa menghapus isi penting yang sudah ada.

Jangan membuat hasil yang tidak berasal dari pemeriksaan aktual. Jangan lanjut ke tahap pembuatan seluruh program sebelum saya meninjau hasil analisis ini.

Setelah selesai, tampilkan ringkasan hasil, file yang dibuat, kendala yang ditemukan, serta rekomendasi untuk melanjutkan ke Tahap 2.