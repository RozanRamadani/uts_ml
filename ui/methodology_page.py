import streamlit as st

from ui.components import render_badge


def render_methodology_page():
    """Merender halaman Tentang Model & Metodologi dengan gaya ramah dan edukatif."""
    
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="kira-badge kira-badge-violet" style="margin: 0;">📖 Dokumentasi Ilmiah</span>
                <span class="kira-badge kira-badge-indigo" style="margin: 0;">Metodologi Bebas Data Leakage</span>
            </div>
            <h1 style="font-size: 2.2rem; font-weight: 800; color: #0F172A; margin: 0.5rem 0 0.35rem 0; line-height: 1.2;">
                Tentang Model & Arsitektur Pipeline
            </h1>
            <p style="font-size: 1.02rem; color: #64748B; margin: 0; line-height: 1.5;">
                Panduan komprehensif mengenai dataset, rekayasa fitur, isolasi resampling data latih, dan pemilihan model terbaik.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_m1, c_m2 = st.columns(2)

    with c_m1:
        st.markdown(
            """
            <div class="kira-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.75rem;">
                    <span style="font-size: 1.25rem;">🧹</span>
                    <h3 style="font-size: 1.1rem; font-weight: 700; color: #0F172A; margin: 0;">
                        1. Pembersihan Data (Preprocessing)
                    </h3>
                </div>
                <ul style="font-size: 0.88rem; color: #475569; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
                    <li><strong>Kelengkapan Data:</strong> Tidak ditemukan nilai kosong (0 <em>missing values</em>) pada seluruh 17 kolom.</li>
                    <li><strong>Deduplikasi:</strong> Sebanyak 125 baris duplikat identik dihapus menggunakan <code>drop_duplicates()</code>, menyisakan 12.205 sampel bersih.</li>
                    <li><strong>Pencilan (Outliers):</strong> Nilai ekstrem pada durasi dan nilai halaman dipertahankan karena mencerminkan perilaku belanja dunia nyata.</li>
                    <li><strong>Pemisahan Data:</strong> 80% data latih (9.764) dan 20% data uji (2.441) dengan stratifikasi target (<code>stratify=y</code>, <code>random_state=42</code>).</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="kira-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.75rem;">
                    <span style="font-size: 1.25rem;">⚖️</span>
                    <h3 style="font-size: 1.1rem; font-weight: 700; color: #0F172A; margin: 0;">
                        2. Penanganan Imbalance (Zero Leakage)
                    </h3>
                </div>
                <ul style="font-size: 0.88rem; color: #475569; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
                    <li><strong>Isolasi Resampling:</strong> Resampling <em>hanya</em> diterapkan pada data training, tidak pernah menyentuh data testing.</li>
                    <li><strong>SMOTENC (Oversampling):</strong> Dilakukan sebelum OneHotEncoder untuk mereplikasi data sintetis fitur kategori secara valid (16.476 sampel seimbang).</li>
                    <li><strong>RandomUnderSampler (Undersampling):</strong> Memangkas acak kelas mayoritas training (3.052 sampel seimbang).</li>
                    <li><strong>Integritas Evaluasi:</strong> Data uji (2.441 baris) tetap mempertahankan distribusi asli untuk menguji generalisasi model yang sebenarnya.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with c_m2:
        st.markdown(
            """
            <div class="kira-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.75rem;">
                    <span style="font-size: 1.25rem;">⚙️</span>
                    <h3 style="font-size: 1.1rem; font-weight: 700; color: #0F172A; margin: 0;">
                        3. Rekayasa Transformasi (ColumnTransformer)
                    </h3>
                </div>
                <ul style="font-size: 0.88rem; color: #475569; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
                    <li><strong>StandardScaler:</strong> Menstandarisasi 14 fitur numerik (mean=0, std=1) agar fitur berjangkauan besar (seperti durasi) tidak mendominasi perhitungan jarak.</li>
                    <li><strong>OneHotEncoder:</strong> Mengonversi fitur teks/boolean (<code>Month</code>, <code>VisitorType</code>, <code>Weekend</code>) dengan <code>drop='first'</code> untuk mencegah multikolinearitas.</li>
                    <li><strong>Fit Isolation:</strong> Transformer di-<em>fit</em> khusus pada data latih hasil resample, kemudian melakukan transformasi pasif pada data uji.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown(
            """
            <div class="kira-card">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.75rem;">
                    <span style="font-size: 1.25rem;">🤖</span>
                    <h3 style="font-size: 1.1rem; font-weight: 700; color: #0F172A; margin: 0;">
                        4. Tiga Algoritma Pembelajaran Mesin
                    </h3>
                </div>
                <ul style="font-size: 0.88rem; color: #475569; line-height: 1.6; padding-left: 1.2rem; margin: 0;">
                    <li><strong>Decision Tree:</strong> Model pohon keputusan berbasis aturan (<code>max_depth=10, random_state=42</code>) sebagai baseline UTS.</li>
                    <li><strong>Gaussian Naïve Bayes:</strong> Model probabilistik berbasis Teorema Bayes dengan asumsi distribusi Gaussian (<code>var_smoothing=1e-9</code>).</li>
                    <li><strong>SVM RBF (Model Terbaik):</strong> Pemetaan ruang dimensi tinggi menggunakan kernel Radial Basis Function (RBF) yang efektif menangkap batas keputusan non-linear.</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="kira-card" style="margin-top: 0.5rem; background: #FFFBEB; border: 1px solid #FDE68A;">
            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.5rem;">
                <span style="font-size: 1.2rem;">⚠️</span>
                <h4 style="font-size: 1.02rem; font-weight: 700; color: #92400E; margin: 0;">
                    Batasan Praktis & Asumsi Model
                </h4>
            </div>
            <p style="font-size: 0.88rem; color: #78350F; line-height: 1.6; margin: 0;">
                1. <strong>Faktor Eksternal Di Luar Sesi:</strong> Prediksi model murni mengacu pada 17 fitur perilaku interaksi browsing. Faktor offline seperti diskon toko fisik pesaing, keterbatasan saldo rekening pengguna, atau gangguan jaringan tidak terekam dalam dataset.<br>
                2. <strong>Kompleksitas Komputasi SVM:</strong> Algoritma SVM dengan kernel RBF memerlukan memori dan waktu komputasi kuadratik terhadap jumlah sampel latih. Untuk skala data jutaan baris di lingkungan produksi massal, diperlukan teknik aproksimasi kernel linear atau *mini-batch sampling*.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

