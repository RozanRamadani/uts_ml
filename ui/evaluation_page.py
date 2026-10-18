from pathlib import Path
import streamlit as st

from services.data_service import get_confusion_matrix_path
from ui.components import render_badge


def render_evaluation_page(bundle, eval_df):
    """Merender halaman Evaluasi Komparatif & Diagnostik Model yang ramah dan edukatif."""
    
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="kira-badge kira-badge-violet" style="margin: 0;">📊 Benchmark Komparatif</span>
                <span class="kira-badge kira-badge-emerald" style="margin: 0;">Fokus Kelas Positif: Revenue = True</span>
            </div>
            <h1 style="font-size: 2.2rem; font-weight: 800; color: #0F172A; margin: 0.5rem 0 0.35rem 0; line-height: 1.2;">
                Evaluasi Kinerja 6 Eksperimen Model
            </h1>
            <p style="font-size: 1.02rem; color: #64748B; margin: 0; line-height: 1.5;">
                Perbandingan komparasi empiris antara Decision Tree (UTS), Gaussian Naïve Bayes, dan Support Vector Machine (SVM) pada 2.441 data testing yang identik.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Callout Penting: Revenue = True sebagai Kelas Positif
    st.markdown(
        """
        <div style="background: #EEF2FF; border: 1px solid #C7D2FE; border-radius: 14px; padding: 1rem 1.25rem; margin-bottom: 1.5rem; display: flex; align-items: flex-start; gap: 12px;">
            <span style="font-size: 1.5rem; line-height: 1;">💡</span>
            <div style="font-size: 0.88rem; color: #3730A3; line-height: 1.5;">
                <strong>Penetapan Kelas Target Positif:</strong> Dalam klasifikasi niat beli e-commerce ini, kelas positif didefinisikan secara tegas sebagai 
                <strong><code>Revenue = True</code> (Pengunjung yang melakukan pembelian)</strong>. Seluruh metrik Presisi, Recall, dan F1-Score dihitung untuk mengukur kemampuan model mendeteksi kelas pembeli minoritas (15,5% dari total data).
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if eval_df is not None:
        display_df = eval_df.copy()
        for col in ["Accuracy", "Precision", "Recall", "F1-Score"]:
            display_df[col] = display_df[col].apply(lambda x: f"{x * 100:.2f}%")

        st.markdown("### 📋 Tabel Hasil Evaluasi Data Testing Riil (2.441 Sampel)")
        st.dataframe(
            display_df,
            use_container_width=True,
            column_config={
                "Model": st.column_config.TextColumn("Kombinasi Algoritma & Resampling", width="large"),
                "Accuracy": st.column_config.TextColumn("Akurasi Global", width="small"),
                "Precision": st.column_config.TextColumn("Presisi (True)", width="small"),
                "Recall": st.column_config.TextColumn("Recall (True)", width="small"),
                "F1-Score": st.column_config.TextColumn("F1-Score", width="small"),
            },
            hide_index=True,
        )

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)

    col_cm_img, col_cm_desc = st.columns([1, 1])
    cm_path = get_confusion_matrix_path()

    with col_cm_img:
        st.markdown(
            f"""
            <div class="kira-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
                    <h4 style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin: 0;">
                        Confusion Matrix Model Aktif
                    </h4>
                    <span class="kira-badge kira-badge-indigo" style="margin: 0;">{bundle['model_name']}</span>
                </div>
            """,
            unsafe_allow_html=True,
        )
        if cm_path.exists():
            st.image(str(cm_path), caption="Matriks Konfusi Aktual Data Testing (2.441 Sampel: 2.059 False, 382 True)")
        st.markdown("</div>", unsafe_allow_html=True)

    with col_cm_desc:
        st.markdown(
            """
            <div class="kira-card">
                <h4 style="font-size: 1.05rem; font-weight: 700; color: #0F172A; margin-bottom: 0.75rem;">
                    🔍 Dekomposisi 4 Kuadran Matriks Konfusi
                </h4>
                <div style="display: flex; flex-direction: column; gap: 0.65rem; font-size: 0.88rem; line-height: 1.55;">
                    <div style="background: #F0FDF4; border-left: 4px solid #22C55E; padding: 0.65rem 0.85rem; border-radius: 8px;">
                        <strong style="color: #14532D;">True Positive (TP = 274):</strong><br>
                        Pengunjung riil pembeli yang berhasil diprediksi tepat sebagai pembeli. Menghasilkan konversi transaksi nyata.
                    </div>
                    <div style="background: #F8FAFC; border-left: 4px solid #64748B; padding: 0.65rem 0.85rem; border-radius: 8px;">
                        <strong style="color: #0F172A;">True Negative (TN = 1.861):</strong><br>
                        Pengunjung kasual yang diprediksi tepat tidak berbelanja. Menghindarkan promosi diskon yang sia-sia.
                    </div>
                    <div style="background: #FEF3C7; border-left: 4px solid #F59E0B; padding: 0.65rem 0.85rem; border-radius: 8px;">
                        <strong style="color: #92400E;">False Positive (FP = 198) — False Alarm:</strong><br>
                        Pengunjung tidak membeli namun diprediksi membeli. Model SVM RBF berhasil menekan kesalahan ini ke level terendah dibanding Naïve Bayes (1.225) dan Decision Tree (236).
                    </div>
                    <div style="background: #FEE2E2; border-left: 4px solid #EF4444; padding: 0.65rem 0.85rem; border-radius: 8px;">
                        <strong style="color: #991B1B;">False Negative (FN = 108) — Missed Opportunity:</strong><br>
                        Pengunjung pembeli riil yang terlewat dan diprediksi tidak membeli.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # Narrative explanation in accessible Indonesian
    st.markdown(
        """
        <div class="kira-card" style="margin-top: 1rem;">
            <h3 style="font-size: 1.15rem; font-weight: 700; color: #0F172A; margin-bottom: 0.75rem;">
                🧠 Pemahaman Edukatif: Mengapa Akurasi Menyesatkan pada Data Tidak Seimbang?
            </h3>
            <p style="font-size: 0.9rem; color: #475569; line-height: 1.6; margin-bottom: 0.75rem;">
                Dalam e-commerce, 84,53% pengunjung tidak pernah berbelanja. Jika sebuah sistem selalu menebak <em>"Tidak Beli"</em> untuk semua orang, sistem tersebut secara otomatis memperoleh <strong>Akurasi 84,53%</strong>. Namun sistem tersebut bernilai nol secara bisnis karena sama sekali gagal mendeteksi pembeli (Recall = 0%).
            </p>
            <p style="font-size: 0.9rem; color: #475569; line-height: 1.6; margin-bottom: 0.75rem;">
                <strong>Fenomena Gaussian Naïve Bayes:</strong> Model Naïve Bayes meraih Recall sangat tinggi (>90%), namun Presisinya jatuh drastis ke 21,92% dengan 1.225 False Alarm. Ini terjadi karena asumsi independensi bersyarat dilanggar oleh fitur web analytics yang saling berhubungan erat (misal <code>BounceRates</code> dan <code>ExitRates</code>).
            </p>
            <p style="font-size: 0.9rem; color: #475569; line-height: 1.6; margin: 0;">
                <strong>Keunggulan SVM RBF + SMOTENC:</strong> SVM dengan fungsi kernel Radial Basis Function (RBF) memetakan interaksi non-linear antartur dengan sangat seimbang. Model ini mencapai kompromi terbaik dengan <strong>Akurasi tertinggi (87,46%)</strong>, <strong>Presisi tertinggi (58,05%)</strong>, dan <strong>F1-Score tertinggi (64,17%)</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

