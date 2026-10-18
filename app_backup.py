from pathlib import Path
import joblib
import numpy as np
import pandas as pd
import streamlit as st

# Konfigurasi halaman Streamlit
st.set_page_config(
    page_title="Prediksi Niat Pembelian Pengunjung Website",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Jalur direktori dan artefak
ROOT_DIR = Path(__file__).resolve().parent
BUNDLE_PATH = ROOT_DIR / "outputs" / "models" / "best_model_bundle.joblib"
CM_IMAGE_PATH = ROOT_DIR / "outputs" / "figures" / "cm_svm_smotenc.png"


@st.cache_resource(show_spinner="Memuat model klasifikasi...")
def load_bundle(path):
    """Memuat bundel model dan transformer tanpa melatih ulang."""
    if not path.exists():
        raise FileNotFoundError(
            f"File bundel model tidak ditemukan di: {path}. "
            "Pastikan telah menjalankan 'python src/main.py' terlebih dahulu."
        )
    return joblib.load(path)


def main():
    # Inisialisasi state untuk nilai default formulir
    if "form_data" not in st.session_state:
        st.session_state.form_data = {
            "Administrative": 1,
            "Administrative_Duration": 10.0,
            "Informational": 0,
            "Informational_Duration": 0.0,
            "ProductRelated": 15,
            "ProductRelated_Duration": 500.0,
            "BounceRates": 0.01,
            "ExitRates": 0.03,
            "PageValues": 15.0,
            "SpecialDay": 0.0,
            "Month": "Nov",
            "OperatingSystems": 2,
            "Browser": 2,
            "Region": 1,
            "TrafficType": 2,
            "VisitorType": "Returning_Visitor",
            "Weekend": False,
        }

    # Muat bundel model
    try:
        bundle = load_bundle(BUNDLE_PATH)
        model = bundle["model"]
        transformer = bundle["transformer"]
        feature_names = bundle["feature_names"]
        metrics = bundle["metrics"]
        model_name = bundle["model_name"]
    except Exception as e:
        st.error(f"⚠️ Terjadi kesalahan saat memuat model: {e}")
        st.stop()

    # --- SIDEBAR: INFORMASI MODEL & PRESET ---
    with st.sidebar:
        st.header("⚙️ Informasi Model")
        st.info(
            f"**Model Aktif**: `{model_name}`\n\n"
            "Model ini dipilih berdasarkan hasil komparasi 6 eksperimen, "
            "karena memperoleh Akurasi, Presisi, dan F1-Score tertinggi."
        )

        st.subheader("📊 Metrik Performa (Data Uji)")
        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Accuracy", f"{metrics['Accuracy'] * 100:.2f}%")
            st.metric("Precision", f"{metrics['Precision'] * 100:.2f}%")
        with col_m2:
            st.metric("Recall", f"{metrics['Recall'] * 100:.2f}%")
            st.metric("F1-Score", f"{metrics['F1-Score'] * 100:.2f}%")

        if CM_IMAGE_PATH.exists():
            st.subheader("📈 Confusion Matrix")
            st.image(str(CM_IMAGE_PATH), caption=f"Confusion Matrix: {model_name}")

        st.markdown("---")
        st.subheader("⚡ Muat Contoh Pengujian")
        st.caption("Klik tombol di bawah untuk mengisi form secara otomatis:")

        col_btn1, col_btn2 = st.columns(2)
        with col_btn1:
            if st.button("🛍️ Niat Beli Tinggi", use_container_width=True):
                set_preset("buyer")
                st.rerun()
        with col_btn2:
            if st.button("👀 Bouncing / Kasual", use_container_width=True):
                set_preset("casual")
                st.rerun()

        if st.button("🔄 Reset Nilai Standar", use_container_width=True):
            set_preset("reset")
            st.rerun()

    # --- HALAMAN UTAMA ---
    st.title("🛒 Prediksi Niat Pembelian Pengunjung Website")
    st.markdown(
        "Aplikasi demonstrasi klasifikasi untuk memperkirakan apakah sesi kunjungan website menghasilkan "
        "**Revenue** berdasarkan karakteristik sesi pengunjung. Masukkan parameter kunjungan di bawah ini, "
        "kemudian tekan tombol **Prediksi Revenue**."
    )
    st.markdown("---")

    # Mengambil nilai state formulir saat ini
    fd = st.session_state.form_data

    # Form input 17 fitur dikelompokkan ke dalam 3 kolom expander / container
    with st.form("prediction_form"):
        tab1, tab2, tab3 = st.tabs([
            "📄 1. Aktivitas Halaman & Durasi",
            "📊 2. Metrik Sesi (Analytics)",
            "👤 3. Profil Pengunjung & Waktu",
        ])

        with tab1:
            st.markdown("##### Jumlah halaman yang dikunjungi dan durasi yang dihabiskan (detik):")
            c1, c2 = st.columns(2)
            with c1:
                administrative = st.number_input(
                    "Administrative (Halaman Akun / Admin)",
                    min_value=0,
                    max_value=50,
                    value=int(fd["Administrative"]),
                    help="Jumlah halaman administratif yang dikunjungi.",
                )
                informational = st.number_input(
                    "Informational (Halaman Informasi / Blog / Kontak)",
                    min_value=0,
                    max_value=50,
                    value=int(fd["Informational"]),
                    help="Jumlah halaman informasi yang dikunjungi.",
                )
                product_related = st.number_input(
                    "ProductRelated (Halaman Katalog Produk)",
                    min_value=0,
                    max_value=1000,
                    value=int(fd["ProductRelated"]),
                    help="Jumlah halaman katalog produk yang dikunjungi.",
                )
            with c2:
                administrative_duration = st.number_input(
                    "Administrative Duration (detik)",
                    min_value=0.0,
                    max_value=10000.0,
                    value=float(fd["Administrative_Duration"]),
                    step=1.0,
                    help="Total waktu yang dihabiskan pada halaman administratif.",
                )
                informational_duration = st.number_input(
                    "Informational Duration (detik)",
                    min_value=0.0,
                    max_value=10000.0,
                    value=float(fd["Informational_Duration"]),
                    step=1.0,
                    help="Total waktu yang dihabiskan pada halaman informasi.",
                )
                product_related_duration = st.number_input(
                    "ProductRelated Duration (detik)",
                    min_value=0.0,
                    max_value=100000.0,
                    value=float(fd["ProductRelated_Duration"]),
                    step=10.0,
                    help="Total waktu yang dihabiskan pada halaman produk.",
                )

        with tab2:
            st.markdown("##### Metrik Google Analytics untuk kualitas kunjungan:")
            c3, c4 = st.columns(2)
            with c3:
                bounce_rates = st.number_input(
                    "Bounce Rates",
                    min_value=0.0,
                    max_value=0.20,
                    value=float(fd["BounceRates"]),
                    step=0.005,
                    format="%.4f",
                    help="Persentase pengunjung yang masuk dan langsung keluar tanpa melihat halaman lain.",
                )
                exit_rates = st.number_input(
                    "Exit Rates",
                    min_value=0.0,
                    max_value=0.20,
                    value=float(fd["ExitRates"]),
                    step=0.005,
                    format="%.4f",
                    help="Persentase tampilan halaman yang merupakan akhir dari sesi pengunjung.",
                )
            with c4:
                page_values = st.number_input(
                    "Page Values",
                    min_value=0.0,
                    max_value=500.0,
                    value=float(fd["PageValues"]),
                    step=1.0,
                    format="%.2f",
                    help="Rata-rata nilai halaman yang berkontribusi terhadap transaksi atau tujuan situs.",
                )
                special_day_options = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
                curr_sd = float(fd["SpecialDay"])
                sd_idx = special_day_options.index(curr_sd) if curr_sd in special_day_options else 0
                special_day = st.selectbox(
                    "Special Day (Kedekatan Hari Khusus / Libur)",
                    options=special_day_options,
                    index=sd_idx,
                    help="Kedekatan waktu kunjungan dengan hari khusus (seperti Hari Ibu, Valentine) dengan skala 0 hingga 1.",
                )

        with tab3:
            st.markdown("##### Karakteristik teknis, tipe pengunjung, dan kalender kunjungan:")
            c5, c6, c7 = st.columns(3)
            with c5:
                month_options = ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                curr_m = fd["Month"]
                m_idx = month_options.index(curr_m) if curr_m in month_options else 0
                month = st.selectbox("Bulan (Month)", options=month_options, index=m_idx)

                visitor_options = ["Returning_Visitor", "New_Visitor", "Other"]
                curr_vt = fd["VisitorType"]
                vt_idx = visitor_options.index(curr_vt) if curr_vt in visitor_options else 0
                visitor_type = st.selectbox("Tipe Pengunjung (VisitorType)", options=visitor_options, index=vt_idx)

                weekend_options = [False, True]
                curr_wk = bool(fd["Weekend"])
                wk_idx = weekend_options.index(curr_wk)
                weekend = st.selectbox(
                    "Akhir Pekan (Weekend)",
                    options=weekend_options,
                    index=wk_idx,
                    format_func=lambda x: "Ya (Akhir Pekan)" if x else "Tidak (Hari Kerja)",
                )

            with c6:
                os_options = list(range(1, 9))
                curr_os = int(fd["OperatingSystems"])
                os_idx = os_options.index(curr_os) if curr_os in os_options else 1
                operating_systems = st.selectbox("Operating Systems (OS)", options=os_options, index=os_idx)

                browser_options = list(range(1, 14))
                curr_br = int(fd["Browser"])
                br_idx = browser_options.index(curr_br) if curr_br in browser_options else 1
                browser = st.selectbox("Browser", options=browser_options, index=br_idx)

            with c7:
                region_options = list(range(1, 10))
                curr_rg = int(fd["Region"])
                rg_idx = region_options.index(curr_rg) if curr_rg in region_options else 0
                region = st.selectbox("Wilayah (Region)", options=region_options, index=rg_idx)

                traffic_options = list(range(1, 21))
                curr_tf = int(fd["TrafficType"])
                tf_idx = traffic_options.index(curr_tf) if curr_tf in traffic_options else 0
                traffic_type = st.selectbox("Traffic Type (Sumber Lalu Lintas)", options=traffic_options, index=tf_idx)

        st.markdown("")
        submit_button = st.form_submit_button("🚀 Prediksi Revenue", use_container_width=True)

    # --- PROSES DAN TAMPILAN PREDIKSI ---
    if submit_button:
        # 1. Susun DataFrame input 1 baris sesuai urutan 17 fitur
        input_dict = {
            "Administrative": int(administrative),
            "Administrative_Duration": float(administrative_duration),
            "Informational": int(informational),
            "Informational_Duration": float(informational_duration),
            "ProductRelated": int(product_related),
            "ProductRelated_Duration": float(product_related_duration),
            "BounceRates": float(bounce_rates),
            "ExitRates": float(exit_rates),
            "PageValues": float(page_values),
            "SpecialDay": float(special_day),
            "Month": str(month),
            "OperatingSystems": int(operating_systems),
            "Browser": int(browser),
            "Region": int(region),
            "TrafficType": int(traffic_type),
            "VisitorType": str(visitor_type),
            "Weekend": bool(weekend),
        }

        input_df = pd.DataFrame([input_dict], columns=feature_names)

        # 2. Transformasi dan Prediksi
        try:
            input_transformed = transformer.transform(input_df)
            prediction = model.predict(input_transformed)[0]
            probabilities = model.predict_proba(input_transformed)[0]
            prob_false = float(probabilities[0])
            prob_true = float(probabilities[1])

            st.markdown("### 📋 Hasil Prediksi")

            res_col1, res_col2 = st.columns([3, 2])
            with res_col1:
                if prediction == True:
                    st.success(
                        "### ✅ Berpotensi Menghasilkan Pembelian\n\n"
                        "Karakteristik sesi pengunjung mengindikasikan adanya niat transaksi (*Revenue = True*)."
                    )
                else:
                    st.warning(
                        "### ℹ️ Tidak Terindikasi Menghasilkan Pembelian\n\n"
                        "Karakteristik sesi pengunjung cenderung hanya melihat-lihat (*Revenue = False*)."
                    )

            with res_col2:
                st.markdown("##### Probabilitas Keyakinan Model:")
                st.write(f"**Niat Beli (Revenue = True):** `{prob_true * 100:.2f}%`")
                st.progress(prob_true)
                st.write(f"**Tidak Beli (Revenue = False):** `{prob_false * 100:.2f}%`")
                st.progress(prob_false)

            # Ringkasan data input yang diproses
            with st.expander("🔍 Lihat Detail Data Input Sesi Pengunjung", expanded=False):
                st.dataframe(input_df, use_container_width=True)

            st.caption(
                "📌 **Catatan**: Hasil di atas merupakan estimasi model probabilitas statistik berbasis machine learning "
                f"({model_name}), bukan merupakan jaminan mutlak perilaku pembelian aktual pengunjung."
            )

        except Exception as err:
            st.error(f"Terjadi kesalahan saat memproses data input: {err}")


if __name__ == "__main__":
    main()

