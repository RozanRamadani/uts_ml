import streamlit as st

from services.data_service import load_evaluation_metrics
from services.model_service import (
    get_default_form_data,
    get_preset_data,
    load_model_bundle,
)
from ui.components import (
    render_active_model_badge,
    render_sidebar_branding,
)
from ui.dashboard import render_dashboard
from ui.evaluation_page import render_evaluation_page
from ui.methodology_page import render_methodology_page
from ui.prediction import render_prediction_workspace
from ui.styles import get_custom_css


# --- KONFIGURASI HALAMAN STREAMLIT ---
st.set_page_config(
    page_title="Purchase Intent Analytics — AI Visitor Intelligence",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Injeksi CSS Kustom Desain Sistem Kira
st.markdown(get_custom_css(), unsafe_allow_html=True)

NAV_OPTIONS = [
    "📊 Dashboard",
    "🎯 Prediction Workspace",
    "📈 Evaluasi Model",
    "📖 Tentang Model",
]


def main():
    # Inisialisasi state sesi
    if "nav_radio" not in st.session_state or st.session_state.nav_radio not in NAV_OPTIONS:
        st.session_state.nav_radio = NAV_OPTIONS[0]

    if "form_data" not in st.session_state:
        st.session_state.form_data = get_default_form_data()

    if "form_version" not in st.session_state:
        st.session_state.form_version = 0

    if "prediction_result" not in st.session_state:
        st.session_state.prediction_result = None

    # Muat bundel model & data evaluasi
    try:
        bundle = load_model_bundle()
    except Exception as err:
        st.error(f"⚠️ Terjadi kendala saat memuat bundel model: {err}")
        st.stop()

    eval_df = load_evaluation_metrics()

    # --- SIDEBAR: NAVIGASI & BRANDING KIRA ---
    with st.sidebar:
        render_sidebar_branding()

        # Navigasi Aplikasi dengan direct key binding untuk keandalan 1-klik
        selected_nav = st.radio(
            "Navigasi Aplikasi",
            options=NAV_OPTIONS,
            key="nav_radio",
            label_visibility="collapsed",
        )

        st.markdown(
            "<hr style='border: 0; border-top: 1px solid var(--sidebar-border); margin: 1.25rem 0;'>",
            unsafe_allow_html=True,
        )

        # Kartu status model aktif
        metrics = bundle["metrics"]
        render_active_model_badge(
            model_name=bundle["model_name"],
            accuracy=metrics["Accuracy"],
            f1_score=metrics["F1-Score"],
        )

        # Tombol preset cepat khusus pada halaman Prediction Workspace
        if selected_nav == "🎯 Prediction Workspace":
            st.markdown("<div style='margin-top: 1.25rem;'>", unsafe_allow_html=True)
            st.caption("⚡ PRESET PENGUJIAN SIDEBAR")
            if st.button("🛍️ Niat Beli Tinggi", use_container_width=True, key="sb_btn_buyer"):
                st.session_state.form_data = get_preset_data("buyer")
                st.session_state.prediction_result = None
                st.session_state.form_version = st.session_state.get("form_version", 0) + 1
                st.toast("Preset Niat Beli Tinggi dimuat!", icon="🛍️")
                st.rerun()
            if st.button("👀 Pengunjung Kasual", use_container_width=True, key="sb_btn_casual"):
                st.session_state.form_data = get_preset_data("casual")
                st.session_state.prediction_result = None
                st.session_state.form_version = st.session_state.get("form_version", 0) + 1
                st.toast("Preset Pengunjung Kasual dimuat!", icon="👀")
                st.rerun()
            if st.button("🔄 Reset ke Standar", use_container_width=True, key="sb_btn_reset"):
                st.session_state.form_data = get_preset_data("reset")
                st.session_state.prediction_result = None
                st.session_state.form_version = st.session_state.get("form_version", 0) + 1
                st.toast("Formulir di-reset ke standar.", icon="🔄")
                st.rerun()
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown(
            """
            <div style="margin-top: 2.5rem; padding-top: 1rem; border-top: 1px solid var(--sidebar-border); font-size: 0.75rem; color: var(--text-muted); line-height: 1.5;">
                <strong style="color: var(--text-sub);">Praktikum ML TM8</strong><br>
                Engine: Scikit-Learn 1.6+<br>
                Design: Kira-Inspired Edition
            </div>
            """,
            unsafe_allow_html=True,
        )

    # --- ROUTING NAVIGASI UTAMA ---
    if selected_nav == "📊 Dashboard":
        render_dashboard(bundle, eval_df)
    elif selected_nav == "🎯 Prediction Workspace":
        render_prediction_workspace(bundle)
    elif selected_nav == "📈 Evaluasi Model":
        render_evaluation_page(bundle, eval_df)
    elif selected_nav == "📖 Tentang Model":
        render_methodology_page()


if __name__ == "__main__":
    main()

