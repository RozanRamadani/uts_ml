import streamlit as st


def render_badge(text, variant="indigo"):
    """Merender badge pill Kira-inspired yang ramah dan modern.
    
    Pilihan varian: 'indigo', 'violet', 'emerald', 'amber', 'slate'.
    """
    cls = f"kira-badge kira-badge-{variant}"
    st.markdown(f'<div class="{cls}">{text}</div>', unsafe_allow_html=True)


def render_metric_tile(title, value, subtitle="", is_positive=True, icon="⚡"):
    """Merender kartu metrik modern dengan aksen gradien halus."""
    sub_color = "#059669" if is_positive else "var(--accent-indigo)"
    sub_html = f'<div class="kira-metric-sub" style="color: {sub_color};">{subtitle}</div>' if subtitle else ""
    st.markdown(
        f"""
        <div class="kira-metric-tile">
            <div class="kira-metric-title">
                <span>{icon}</span>
                <span>{title}</span>
            </div>
            <div class="kira-metric-value">{value}</div>
            {sub_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sidebar_branding():
    """Merender header produk dan identitas pada sidebar yang bersih dan ramah tema."""
    st.markdown(
        """
        <div style="padding: 0.5rem 0 1.25rem 0;">
            <div class="kira-badge kira-badge-violet">
                <span>✨</span> AI Analytics Suite
            </div>
            <h2 style="font-size: 1.35rem; font-weight: 800; color: var(--text-main); margin: 0; line-height: 1.2;">
                Purchase Intent
            </h2>
            <p style="font-size: 0.82rem; color: var(--text-muted); margin-top: 5px; line-height: 1.4;">
                Platform Prediksi Niat Belanja & Analitik Perilaku Pengunjung
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_active_model_badge(model_name, accuracy, f1_score):
    """Merender kartu informasi model aktif pada sidebar yang adaptif light/dark mode."""
    st.markdown(
        f"""
        <div style="background: var(--card-bg); border: 1px solid var(--card-border); border-radius: 14px; padding: 1rem; margin-bottom: 0.5rem;">
            <div style="font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--accent-indigo); font-weight: 700; display: flex; align-items: center; gap: 5px;">
                <span>🟢</span> Model Aktif Terbaik
            </div>
            <div style="font-size: 0.96rem; font-weight: 800; color: var(--text-main); margin-top: 4px;">
                {model_name}
            </div>
            <div style="font-size: 0.8rem; color: var(--text-sub); margin-top: 5px; line-height: 1.4;">
                F1-Score: <strong style="color: var(--accent-indigo);">{f1_score*100:.2f}%</strong> &bull; Akurasi: <strong style="color: var(--text-main);">{accuracy*100:.2f}%</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_prediction_banner(is_buyer, prob_true=None):
    """Merender banner status hasil prediksi yang ramah, jelas, dan adaptif tema."""
    if is_buyer:
        prob_str = f" ({prob_true*100:.2f}% keyakinan)" if prob_true is not None else ""
        st.markdown(
            f"""
            <div class="kira-result-card-positive">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.35rem; flex-wrap: wrap;">
                    <span class="kira-badge kira-badge-emerald" style="margin: 0;">PREDIKSI POSITIF</span>
                    <span style="font-size: 0.82rem; font-weight: 700;">Revenue = True{prob_str}</span>
                </div>
                <h2 style="font-size: 1.55rem; font-weight: 800; margin: 0.35rem 0 0.5rem 0; line-height: 1.25;">
                    🎉 Kemungkinan Membeli Tinggi
                </h2>
                <p style="font-size: 0.92rem; line-height: 1.55; margin: 0; opacity: 0.95;">
                    Sesi browsing pengunjung menunjukkan minat transaksional yang kuat (aktivitas melihat produk intensif dan kontribusi nilai halaman tinggi). Pengunjung berada pada fase siap belanja.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        prob_str = f" ({(1.0 - prob_true)*100:.2f}% keyakinan kasual)" if prob_true is not None else ""
        st.markdown(
            f"""
            <div class="kira-result-card-negative">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 0.35rem; flex-wrap: wrap;">
                    <span class="kira-badge kira-badge-slate" style="margin: 0;">PREDIKSI NON-PEMBELI</span>
                    <span style="font-size: 0.82rem; font-weight: 700;">Revenue = False{prob_str}</span>
                </div>
                <h2 style="font-size: 1.55rem; font-weight: 800; margin: 0.35rem 0 0.5rem 0; line-height: 1.25;">
                    👀 Kemungkinan Membeli Rendah
                </h2>
                <p style="font-size: 0.92rem; line-height: 1.55; margin: 0; opacity: 0.95;">
                    Sesi browsing pengunjung tergolong eksplorasi kasual atau mencari informasi umum tanpa intensi checkout (tingkat keluar cepat atau nilai halaman rendah).
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )


