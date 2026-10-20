from pathlib import Path
import streamlit as st

from services.data_service import get_confusion_matrix_path
from ui.components import render_badge


def render_evaluation_page(bundle, eval_df):
    """Merender halaman Evaluasi Komparatif & Diagnostik Model yang ramah, edukatif, dan adaptif tema."""
    
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                <span class="kira-badge kira-badge-violet" style="margin: 0;">📊 Benchmark Komparatif</span>
                <span class="kira-badge kira-badge-emerald" style="margin: 0;">Fokus Kelas Positif: Revenue = True</span>
            </div>
            <h1 style="font-size: 2.2rem; font-weight: 800; color: var(--text-main); margin: 0.5rem 0 0.35rem 0; line-height: 1.2;">
                Evaluasi Kinerja 6 Eksperimen Model
            </h1>
            <p style="font-size: 1.02rem; color: var(--text-muted); margin: 0; line-height: 1.5;">
                Perbandingan komparasi empiris antara Decision Tree (UTS), Gaussian Naïve Bayes, dan Support Vector Machine (SVM) pada 2.441 data testing yang identik.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Callout Penting: Revenue = True sebagai Kelas Positif
    st.markdown(
        """
        <div style="background: var(--badge-indigo-bg); border: 1px solid var(--badge-indigo-border); border-radius: 14px; padding: 1rem 1.25rem; margin-bottom: 1.5rem; display: flex; align-items: flex-start; gap: 12px;">
            <span style="font-size: 1.5rem; line-height: 1;">💡</span>
            <div style="font-size: 0.88rem; color: var(--badge-indigo-text); line-height: 1.5;">
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
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 8px;">
                    <h4 style="font-size: 1.05rem; font-weight: 700; color: var(--text-main); margin: 0;">
                        Confusion Matrix Model Aktif
                    </h4>
                    <span class="kira-badge kira-badge-indigo" style="margin: 0;">{bundle['model_name']}</span>
                </div>
            """,
            unsafe_allow_html=True,
        )

        tab_matrix_adaptive, tab_matrix_plot = st.tabs(["🎨 Matriks Adaptif Tema", "🖼️ Plot Matriks Asli"])

        with tab_matrix_adaptive:
            st.markdown(
                """
                <div style="margin: 0.5rem 0; overflow-x: auto;">
                    <table style="width: 100%; border-collapse: separate; border-spacing: 6px; font-size: 0.86rem; text-align: center;">
                        <thead>
                            <tr>
                                <th style="background: transparent; border: none;"></th>
                                <th style="background: var(--card-bg-hover); color: var(--text-main); padding: 8px; border-radius: 8px; border: 1px solid var(--card-border);" colspan="2">Prediksi Model</th>
                            </tr>
                            <tr>
                                <th style="background: transparent; border: none; font-size: 0.8rem; color: var(--text-muted);">Aktual</th>
                                <th style="background: var(--card-bg-hover); color: var(--text-sub); padding: 6px; border-radius: 6px;">False (Kasual)</th>
                                <th style="background: var(--card-bg-hover); color: var(--text-sub); padding: 6px; border-radius: 6px;">True (Beli)</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <th style="background: var(--card-bg-hover); color: var(--text-sub); padding: 8px; border-radius: 6px; font-weight: 600;">False</th>
                                <td style="background: rgba(79, 70, 229, 0.15); border: 1px solid rgba(79, 70, 229, 0.3); border-radius: 10px; padding: 12px;">
                                    <div style="font-size: 1.25rem; font-weight: 800; color: var(--text-main);">1.861</div>
                                    <div style="font-size: 0.72rem; color: var(--accent-indigo); font-weight: 700;">TN (76.24%)</div>
                                </td>
                                <td style="background: rgba(245, 158, 11, 0.12); border: 1px solid rgba(245, 158, 11, 0.25); border-radius: 10px; padding: 12px;">
                                    <div style="font-size: 1.25rem; font-weight: 800; color: var(--text-main);">198</div>
                                    <div style="font-size: 0.72rem; color: #D97706; font-weight: 700;">FP (8.11%)</div>
                                </td>
                            </tr>
                            <tr>
                                <th style="background: var(--card-bg-hover); color: var(--text-sub); padding: 8px; border-radius: 6px; font-weight: 600;">True</th>
                                <td style="background: rgba(239, 68, 68, 0.12); border: 1px solid rgba(239, 68, 68, 0.25); border-radius: 10px; padding: 12px;">
                                    <div style="font-size: 1.25rem; font-weight: 800; color: var(--text-main);">108</div>
                                    <div style="font-size: 0.72rem; color: #DC2626; font-weight: 700;">FN (4.42%)</div>
                                </td>
                                <td style="background: rgba(16, 185, 129, 0.15); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 12px;">
                                    <div style="font-size: 1.25rem; font-weight: 800; color: var(--text-main);">274</div>
                                    <div style="font-size: 0.72rem; color: #059669; font-weight: 700;">TP (11.23%)</div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div style="font-size: 0.76rem; color: var(--text-muted); text-align: center; margin-top: 4px;">
                    Matriks adaptif tema dengan kontras tinggi untuk light & dark mode.
                </div>
                """,
                unsafe_allow_html=True,
            )

        with tab_matrix_plot:
            if cm_path.exists():
                st.image(str(cm_path), caption="Plot Matriks Konfusi Asli (2.441 Sampel Uji)", use_container_width=True)

        st.markdown("</div>", unsafe_allow_html=True)

    with col_cm_desc:
        st.markdown(
            """
            <div class="kira-card">
                <h4 style="font-size: 1.05rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.75rem;">
                    🔍 Dekomposisi 4 Kuadran Matriks Konfusi
                </h4>
                <div style="display: flex; flex-direction: column; gap: 0.65rem; font-size: 0.88rem; line-height: 1.55;">
                    <div style="background: var(--badge-emerald-bg); border-left: 4px solid #10B981; padding: 0.65rem 0.85rem; border-radius: 8px;">
                        <strong style="color: var(--badge-emerald-text);">True Positive (TP = 274):</strong><br>
                        <span style="color: var(--text-sub);">Pengunjung riil pembeli yang berhasil diprediksi tepat sebagai pembeli. Menghasilkan konversi transaksi nyata.</span>
                    </div>
                    <div style="background: var(--card-bg-hover); border-left: 4px solid var(--text-muted); border: 1px solid var(--card-border); border-left-width: 4px; padding: 0.65rem 0.85rem; border-radius: 8px;">
                        <strong style="color: var(--text-main);">True Negative (TN = 1.861):</strong><br>
                        <span style="color: var(--text-sub);">Pengunjung kasual yang diprediksi tepat tidak berbelanja. Menghindarkan promosi diskon yang sia-sia.</span>
                    </div>
                    <div style="background: var(--badge-amber-bg); border-left: 4px solid #F59E0B; padding: 0.65rem 0.85rem; border-radius: 8px;">
                        <strong style="color: var(--badge-amber-text);">False Positive (FP = 198) — False Alarm:</strong><br>
                        <span style="color: var(--text-sub);">Pengunjung tidak membeli namun diprediksi membeli. Model SVM RBF berhasil menekan kesalahan ini ke level terendah dibanding Naïve Bayes (1.225) dan Decision Tree (236).</span>
                    </div>
                    <div style="background: rgba(239, 68, 68, 0.12); border-left: 4px solid #EF4444; border: 1px solid rgba(239, 68, 68, 0.25); border-left-width: 4px; padding: 0.65rem 0.85rem; border-radius: 8px;">
                        <strong style="color: #EF4444;">False Negative (FN = 108) — Missed Opportunity:</strong><br>
                        <span style="color: var(--text-sub);">Pengunjung pembeli riil yang terlewat dan diprediksi tidak membeli.</span>
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
            <h3 style="font-size: 1.15rem; font-weight: 700; color: var(--text-main); margin-bottom: 0.75rem;">
                🧠 Pemahaman Edukatif: Mengapa Akurasi Menyesatkan pada Data Tidak Seimbang?
            </h3>
            <p style="font-size: 0.9rem; color: var(--text-sub); line-height: 1.6; margin-bottom: 0.75rem;">
                Dalam e-commerce, 84,53% pengunjung tidak pernah berbelanja. Jika sebuah sistem selalu menebak <em>"Tidak Beli"</em> untuk semua orang, sistem tersebut secara otomatis memperoleh <strong>Akurasi 84,53%</strong>. Namun sistem tersebut bernilai nol secara bisnis karena sama sekali gagal mendeteksi pembeli (Recall = 0%).
            </p>
            <p style="font-size: 0.9rem; color: var(--text-sub); line-height: 1.6; margin-bottom: 0.75rem;">
                <strong>Fenomena Gaussian Naïve Bayes:</strong> Model Naïve Bayes meraih Recall sangat tinggi (>90%), namun Presisinya jatuh drastis ke 21,92% dengan 1.225 False Alarm. Ini terjadi karena asumsi independensi bersyarat dilanggar oleh fitur web analytics yang saling berhubungan erat (misal <code>BounceRates</code> dan <code>ExitRates</code>).
            </p>
            <p style="font-size: 0.9rem; color: var(--text-sub); line-height: 1.6; margin: 0;">
                <strong>Keunggulan SVM RBF + SMOTENC:</strong> SVM dengan fungsi kernel Radial Basis Function (RBF) memetakan interaksi non-linear antartur dengan sangat seimbang. Model ini mencapai kompromi terbaik dengan <strong>Akurasi tertinggi (87,46%)</strong>, <strong>Presisi tertinggi (58,05%)</strong>, dan <strong>F1-Score tertinggi (64,17%)</strong>.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

