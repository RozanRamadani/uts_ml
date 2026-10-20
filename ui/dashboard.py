import altair as alt
import streamlit as st

from services.data_service import get_dataset_summary
from ui.components import render_badge, render_metric_tile


def render_dashboard(bundle, eval_df):
    """Merender halaman Dashboard dengan gaya ramah, modern, dan informatif ala Kira Learning."""
    
    # Kira Hero Section
    actual_metrics = bundle["metrics"]
    dataset_info = get_dataset_summary()

    st.markdown(
        """
        <div class="kira-hero">
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                <span class="kira-badge kira-badge-violet" style="margin: 0;">✨ AI Visitor Intelligence</span>
                <span class="kira-badge kira-badge-indigo" style="margin: 0;">Versi 2.0 (Kira Edition)</span>
            </div>
            <h1 style="font-size: 2.25rem; font-weight: 800; color: var(--text-main); margin: 0.75rem 0 0.5rem 0; line-height: 1.2;">
                Selamat Datang di Purchase Intent Analytics
            </h1>
            <p style="font-size: 1.05rem; color: var(--text-sub); margin: 0 0 1.25rem 0; line-height: 1.6; max-width: 820px;">
                Aplikasi kecerdasan buatan untuk mengidentifikasi potensi niat belanja pengunjung website secara probabilistik. 
                Dirancang ramah, intuitif, dan mudah dipahami untuk membantu pengambilan keputusan bisnis e-commerce.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Action CTA Banner / Trigger Prediksi
    c_cta1, c_cta2 = st.columns([3, 1])
    with c_cta1:
        st.markdown(
            f"""
            <div style="display: flex; align-items: center; gap: 12px; background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 14px; padding: 0.85rem 1.25rem; margin-bottom: 1.25rem;">
                <span style="font-size: 1.4rem;">🎯</span>
                <div style="font-size: 0.92rem; color: var(--text-main);">
                    Model aktif <strong>{bundle['model_name']}</strong> siap melakukan estimasi probabilitas belanja untuk sesi pengunjung Anda.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with c_cta2:
        if st.button("🚀 Buka Prediction Workspace", use_container_width=True, type="primary", key="dash_btn_goto_pred"):
            st.session_state.nav_radio = "🎯 Prediction Workspace"
            st.rerun()

    # 4 Key Metric Cards
    st.markdown("### 📊 Performa Model Terpilih (Data Uji Riil)")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_tile(
            "Akurasi Model",
            f"{actual_metrics['Accuracy']*100:.2f}%",
            "🏆 Tertinggi dari 6 Eksperimen",
            is_positive=True,
            icon="🎯",
        )
    with c2:
        render_metric_tile(
            "Presisi (Revenue=True)",
            f"{actual_metrics['Precision']*100:.2f}%",
            "✨ Minim False Alarm (198)",
            is_positive=True,
            icon="💎",
        )
    with c3:
        render_metric_tile(
            "Recall (Sensitivitas)",
            f"{actual_metrics['Recall']*100:.2f}%",
            "🛍️ 274 Pembeli Terdeteksi",
            is_positive=True,
            icon="🔍",
        )
    with c4:
        render_metric_tile(
            "F1-Score Harmonik",
            f"{actual_metrics['F1-Score']*100:.2f}%",
            "⚖️ Keseimbangan Terbaik",
            is_positive=True,
            icon="🌟",
        )

    st.markdown("<div style='margin-top: 1.75rem;'></div>", unsafe_allow_html=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        st.markdown(
            """
            <div class="kira-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 8px;">
                    <h3 style="font-size: 1.15rem; font-weight: 700; color: var(--text-main); margin: 0;">
                        📈 Benchmark Komparasi 6 Model
                    </h3>
                    <span class="kira-badge kira-badge-indigo" style="margin: 0;">2.441 Data Uji</span>
                </div>
                <p style="font-size: 0.88rem; color: var(--text-muted); margin-bottom: 1rem; line-height: 1.5;">
                    Perbandingan metrik evaluasi pada data testing suci yang tidak pernah di-resampling (zero data leakage).
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        if eval_df is not None:
            df_melt = eval_df.melt(id_vars="Model", var_name="Metric", value_name="Score")

            # Altair Chart dengan Palette Kira dan label netral
            chart = (
                alt.Chart(df_melt)
                .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
                .encode(
                    x=alt.X("Metric:N", title=None, axis=alt.Axis(labelAngle=0, labelFontSize=12, labelFontWeight="bold", labelColor="#94A3B8")),
                    y=alt.Y("Score:Q", title="Skor Metrik (0 - 1.0)", scale=alt.Scale(domain=[0, 1.05]), axis=alt.Axis(labelColor="#94A3B8", titleColor="#94A3B8")),
                    color=alt.Color(
                        "Model:N",
                        scale=alt.Scale(
                            domain=[
                                "Decision Tree + SMOTENC",
                                "Decision Tree + RandomUnderSampler",
                                "Gaussian Naive Bayes + SMOTENC",
                                "Gaussian Naive Bayes + RandomUnderSampler",
                                "SVM RBF + SMOTENC",
                                "SVM RBF + RandomUnderSampler",
                            ],
                            range=["#94A3B8", "#64748B", "#F59E0B", "#D97706", "#4F46E5", "#06B6D4"],
                        ),
                        legend=alt.Legend(title="Kombinasi Algoritma & Resampling", orient="bottom", columns=2, labelColor="#94A3B8", titleColor="#94A3B8"),
                    ),
                    tooltip=[
                        alt.Tooltip("Model:N", title="Model"),
                        alt.Tooltip("Metric:N", title="Metrik"),
                        alt.Tooltip("Score:Q", title="Skor", format=".2%"),
                    ],
                )
                .properties(height=340)
                .configure_view(strokeOpacity=0)
            )
            st.altair_chart(chart, use_container_width=True)

    with col_right:
        st.markdown(
            f"""
            <div class="kira-card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem; flex-wrap: wrap; gap: 8px;">
                    <h3 style="font-size: 1.15rem; font-weight: 700; color: var(--text-main); margin: 0;">
                        📚 Profil & Ringkasan Dataset
                    </h3>
                    <span class="kira-badge kira-badge-slate" style="margin: 0;">Dataset Riil</span>
                </div>
                <div style="display: flex; flex-direction: column; gap: 0.75rem;">
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--card-border); padding-bottom: 0.5rem; flex-wrap: wrap; gap: 4px;">
                        <span style="font-size: 0.88rem; color: var(--text-muted);">Nama Dataset</span>
                        <span style="font-size: 0.88rem; font-weight: 700; color: var(--text-main);">{dataset_info['dataset_name']}</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--card-border); padding-bottom: 0.5rem; flex-wrap: wrap; gap: 4px;">
                        <span style="font-size: 0.88rem; color: var(--text-muted);">Total Baris Bersih</span>
                        <span style="font-size: 0.88rem; font-weight: 700; color: var(--text-main);">{dataset_info['clean_rows']} baris <span style="font-size: 0.78rem; font-weight: normal; color: var(--text-muted);">({dataset_info['duplicates_removed']} duplikat dibersihkan)</span></span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--card-border); padding-bottom: 0.5rem; flex-wrap: wrap; gap: 4px;">
                        <span style="font-size: 0.88rem; color: var(--text-muted);">Jumlah Fitur Input</span>
                        <span style="font-size: 0.88rem; font-weight: 700; color: var(--text-main);">{dataset_info['feature_count']} Fitur (10 Numerik + 7 Kategori/Diskrit)</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--card-border); padding-bottom: 0.5rem; flex-wrap: wrap; gap: 4px;">
                        <span style="font-size: 0.88rem; color: var(--text-muted);">Pembagian Data Uji</span>
                        <span style="font-size: 0.88rem; font-weight: 700; color: var(--text-main);">{dataset_info['train_ratio']} Latih &bull; {dataset_info['test_ratio']} Uji ({dataset_info['test_rows']} baris)</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; border-bottom: 1px solid var(--card-border); padding-bottom: 0.5rem; flex-wrap: wrap; gap: 4px;">
                        <span style="font-size: 0.88rem; color: var(--text-muted);">Distribusi Kelas Target</span>
                        <span style="font-size: 0.88rem; font-weight: 700; color: var(--text-main);">{dataset_info['class_true_pct']:.2f}% True : {dataset_info['class_false_pct']:.2f}% False</span>
                    </div>
                    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 4px;">
                        <span style="font-size: 0.88rem; color: var(--text-muted);">Model Produksi Terpilih</span>
                        <span style="font-size: 0.88rem; font-weight: 800; color: var(--accent-indigo);">{bundle['model_name']}</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.info(
            "💡 **Prinsip Validitas Ilmiah**: Seluruh metrik evaluasi dihitung secara independen dari 2.441 sampel data testing asli "
            "tanpa kebocoran data. Model memprediksi secara probabilistik berdasarkan pola browsing pengunjung."
        )


