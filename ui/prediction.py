import pandas as pd
import streamlit as st

from services.model_service import get_preset_data, predict_sample
from ui.components import render_badge, render_prediction_banner


def render_prediction_workspace(bundle):
    """Merender antarmuka Prediction Workspace yang ramah, intuitif, dan responsif."""
    
    if "form_version" not in st.session_state:
        st.session_state.form_version = 0

    # Header Workspace
    st.markdown(
        """
        <div style="margin-bottom: 1.5rem;">
            <div style="display: flex; align-items: center; gap: 8px; flex-wrap: wrap;">
                <span class="kira-badge kira-badge-indigo" style="margin: 0;">🎯 Workspace Interaktif</span>
                <span class="kira-badge kira-badge-violet" style="margin: 0;">17 Parameter Sesi</span>
            </div>
            <h1 style="font-size: 2.2rem; font-weight: 800; color: var(--text-main); margin: 0.5rem 0 0.35rem 0; line-height: 1.2;">
                Prediksi Niat Pembelian Sesi Pengunjung
            </h1>
            <p style="font-size: 1.02rem; color: var(--text-muted); margin: 0; line-height: 1.5;">
                Konfigurasikan parameter aktivitas browsing pengunjung untuk memperkirakan probabilitas terjadinya transaksi (Revenue).
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Quick Preset Chips right at the top
    st.markdown(
        """
        <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.5rem; flex-wrap: wrap; gap: 4px;">
            <span style="font-size: 0.82rem; font-weight: 700; color: var(--text-sub); text-transform: uppercase; letter-spacing: 0.04em;">
                ⚡ Muat Contoh Skenario Cepat (Presets)
            </span>
            <span style="font-size: 0.78rem; color: var(--text-muted);">Klik untuk mengisi nilai otomatis</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cp1, cp2, cp3 = st.columns(3)
    with cp1:
        if st.button("🛍️ Contoh: Niat Beli Tinggi", use_container_width=True, key="pred_chip_buyer", help="Sesi aktif dengan PageValues tinggi & durasi belanja panjang"):
            st.session_state.form_data = get_preset_data("buyer")
            st.session_state.prediction_result = None
            st.session_state.form_version += 1
            st.toast("✅ Preset Niat Beli Tinggi berhasil dimuat!", icon="🛍️")
            st.rerun()
    with cp2:
        if st.button("👀 Contoh: Pengunjung Kasual", use_container_width=True, key="pred_chip_casual", help="Sesi keluar cepat (bouncing) tanpa ketertarikan produk"):
            st.session_state.form_data = get_preset_data("casual")
            st.session_state.prediction_result = None
            st.session_state.form_version += 1
            st.toast("ℹ️ Preset Pengunjung Kasual berhasil dimuat!", icon="👀")
            st.rerun()
    with cp3:
        if st.button("🔄 Reset ke Nilai Rata-rata", use_container_width=True, key="pred_chip_reset", help="Kembalikan semua formulir ke baseline standar"):
            st.session_state.form_data = get_preset_data("reset")
            st.session_state.prediction_result = None
            st.session_state.form_version += 1
            st.toast("🔄 Formulir dikembalikan ke nilai standar.", icon="🔄")
            st.rerun()

    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    fd = st.session_state.form_data

    # Form input 17 fitur terstruktur dengan key dinamis agar preset langsung ter-update 1-klik
    current_fver = st.session_state.form_version
    with st.form(f"inference_form_{current_fver}", clear_on_submit=False):
        tab_act, tab_analytics, tab_visitor = st.tabs([
            "📄 1. Aktivitas Halaman & Durasi",
            "📊 2. Metrik Kualitas Sesi (Analytics)",
            "👤 3. Profil Pengunjung & Waktu",
        ])

        with tab_act:
            st.markdown(
                "<p style='font-size: 0.88rem; color: var(--text-muted); margin-bottom: 1.25rem;'>Atur frekuensi kunjungan halaman dan total durasi waktu yang dihabiskan pada sesi browsing:</p>",
                unsafe_allow_html=True,
            )
            col_a1, col_a2 = st.columns(2)
            with col_a1:
                administrative = st.number_input(
                    "Administrative (Halaman Akun / Keranjang)",
                    min_value=0,
                    max_value=30,
                    value=int(fd["Administrative"]),
                    key=f"inp_admin_{current_fver}",
                    help="Jumlah halaman akun, pengaturan checkout, atau administratif yang dibuka pengguna.",
                )
                informational = st.number_input(
                    "Informational (Halaman Informasi / Blog / Bantuan)",
                    min_value=0,
                    max_value=30,
                    value=int(fd["Informational"]),
                    key=f"inp_info_{current_fver}",
                    help="Jumlah halaman artikel, FAQ situs, atau kontak layanan yang dikunjungi.",
                )
                product_related = st.number_input(
                    "ProductRelated (Halaman Katalog & Detail Produk)",
                    min_value=0,
                    max_value=800,
                    value=int(fd["ProductRelated"]),
                    key=f"inp_prod_{current_fver}",
                    help="Jumlah halaman katalog produk atau detail barang belanjaan yang dibuka.",
                )
            with col_a2:
                administrative_duration = st.number_input(
                    "Administrative Duration (total detik)",
                    min_value=0.0,
                    max_value=5000.0,
                    value=float(fd["Administrative_Duration"]),
                    step=1.0,
                    key=f"inp_admin_dur_{current_fver}",
                    help="Total waktu yang dihabiskan pengunjung pada halaman administratif (detik).",
                )
                informational_duration = st.number_input(
                    "Informational Duration (total detik)",
                    min_value=0.0,
                    max_value=5000.0,
                    value=float(fd["Informational_Duration"]),
                    step=1.0,
                    key=f"inp_info_dur_{current_fver}",
                    help="Total waktu yang dihabiskan pengunjung pada halaman informasi (detik).",
                )
                product_related_duration = st.number_input(
                    "ProductRelated Duration (total detik)",
                    min_value=0.0,
                    max_value=70000.0,
                    value=float(fd["ProductRelated_Duration"]),
                    step=10.0,
                    key=f"inp_prod_dur_{current_fver}",
                    help="Total waktu browsing pada halaman katalog produk (detik).",
                )

        with tab_analytics:
            st.markdown(
                "<p style='font-size: 0.88rem; color: var(--text-muted); margin-bottom: 1.25rem;'>Metrik interaksi pengunjung yang terekam oleh pelacak analitik web (Google Analytics):</p>",
                unsafe_allow_html=True,
            )
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                bounce_rates = st.number_input(
                    "Bounce Rates (Tingkat Pentalan)",
                    min_value=0.0,
                    max_value=0.20,
                    value=float(fd["BounceRates"]),
                    step=0.005,
                    format="%.4f",
                    key=f"inp_bounce_{current_fver}",
                    help="Persentase pengunjung yang membuka satu halaman lalu langsung meninggalkan situs (0.00 s/d 0.20).",
                )
                exit_rates = st.number_input(
                    "Exit Rates (Tingkat Keluar)",
                    min_value=0.0,
                    max_value=0.20,
                    value=float(fd["ExitRates"]),
                    step=0.005,
                    format="%.4f",
                    key=f"inp_exit_{current_fver}",
                    help="Rasio tampilan halaman yang menjadi akhir dari sesi pengunjung (0.00 s/d 0.20).",
                )
            with col_b2:
                page_values = st.number_input(
                    "Page Values (Nilai Kontribusi Transaksi Halaman)",
                    min_value=0.0,
                    max_value=400.0,
                    value=float(fd["PageValues"]),
                    step=1.0,
                    format="%.2f",
                    key=f"inp_pv_{current_fver}",
                    help="Estimasi nilai rata-rata kontribusi halaman terhadap transaksi e-commerce (fitur paling berpengaruh).",
                )
                sd_opts = [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]
                cur_sd = float(fd["SpecialDay"])
                sd_index = sd_opts.index(cur_sd) if cur_sd in sd_opts else 0
                special_day = st.selectbox(
                    "Special Day (Kedekatan Hari Perayaan / Promo Diskon)",
                    options=sd_opts,
                    index=sd_index,
                    key=f"inp_sd_{current_fver}",
                    help="Kedekatan waktu kunjungan dengan hari belanja nasional atau hari libur (0.0 = jauh, 1.0 = tepat hari H).",
                )

        with tab_visitor:
            st.markdown(
                "<p style='font-size: 0.88rem; color: var(--text-muted); margin-bottom: 1.25rem;'>Data teknis peramban, saluran rujukan, demografi wilayah, dan waktu sesi:</p>",
                unsafe_allow_html=True,
            )
            col_c1, col_c2, col_c3 = st.columns(3)
            with col_c1:
                month_opts = ["Feb", "Mar", "May", "June", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
                m_val = fd["Month"]
                m_idx = month_opts.index(m_val) if m_val in month_opts else 0
                month = st.selectbox("Bulan Sesi (Month)", options=month_opts, index=m_idx, key=f"inp_month_{current_fver}")

                vt_opts = ["Returning_Visitor", "New_Visitor", "Other"]
                vt_val = fd["VisitorType"]
                vt_idx = vt_opts.index(vt_val) if vt_val in vt_opts else 0
                visitor_type = st.selectbox(
                    "Tipe Pengunjung (VisitorType)", 
                    options=vt_opts, 
                    index=vt_idx,
                    key=f"inp_vt_{current_fver}",
                    format_func=lambda x: "Pengunjung Lama (Returning)" if x == "Returning_Visitor" else ("Pengunjung Baru (New)" if x == "New_Visitor" else "Lainnya (Other)"),
                )

                wk_opts = [False, True]
                wk_val = bool(fd["Weekend"])
                weekend = st.selectbox(
                    "Waktu Kunjungan (Weekend)",
                    options=wk_opts,
                    index=wk_opts.index(wk_val),
                    key=f"inp_wk_{current_fver}",
                    format_func=lambda x: "Akhir Pekan (Sabtu / Minggu)" if x else "Hari Kerja (Senin - Jumat)",
                )

            with col_c2:
                operating_systems = st.selectbox(
                    "Sistem Operasi (OS)",
                    options=list(range(1, 9)),
                    index=list(range(1, 9)).index(int(fd["OperatingSystems"])) if int(fd["OperatingSystems"]) in range(1, 9) else 1,
                    key=f"inp_os_{current_fver}",
                    help="Kode integer kategori sistem operasi yang digunakan pengunjung (1 - 8).",
                )
                browser = st.selectbox(
                    "Peramban Web (Browser)",
                    options=list(range(1, 14)),
                    index=list(range(1, 14)).index(int(fd["Browser"])) if int(fd["Browser"]) in range(1, 14) else 1,
                    key=f"inp_browser_{current_fver}",
                    help="Kode integer kategori peramban web pengunjung (1 - 13).",
                )

            with col_c3:
                region = st.selectbox(
                    "Wilayah Geografis (Region)",
                    options=list(range(1, 10)),
                    index=list(range(1, 10)).index(int(fd["Region"])) if int(fd["Region"]) in range(1, 10) else 0,
                    key=f"inp_region_{current_fver}",
                    help="Kode integer wilayah geografis pengunjung (1 - 9).",
                )
                traffic_type = st.selectbox(
                    "Sumber Lalu Lintas (TrafficType)",
                    options=list(range(1, 21)),
                    index=list(range(1, 21)).index(int(fd["TrafficType"])) if int(fd["TrafficType"]) in range(1, 21) else 0,
                    key=f"inp_traffic_{current_fver}",
                    help="Saluran pemasaran rujukan sesi seperti direct, organic search, atau ads (1 - 20).",
                )

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("⚡ Analisis & Prediksi Niat Pembelian", use_container_width=True, type="primary")

    # Eksekusi prediksi saat tombol ditekan
    if submit_btn:
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

        # Simpan state form terkini
        st.session_state.form_data = input_dict

        try:
            with st.spinner("Mengevaluasi parameter melalui pipeline model SVM RBF + SMOTENC..."):
                result = predict_sample(bundle, input_dict)
                st.session_state.prediction_result = result
        except Exception as e:
            st.error(f"Gagal melakukan inferensi data input: {e}")

    # Tampilkan hasil prediksi
    if st.session_state.prediction_result is not None:
        res = st.session_state.prediction_result
        is_buyer = res["prediction"]
        p_true = res["prob_true"]
        p_false = res["prob_false"]

        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        st.markdown("### 📋 Hasil Estimasi Model Pembelajaran Mesin")

        col_res_main, col_res_bar = st.columns([3, 2])

        with col_res_main:
            render_prediction_banner(is_buyer, prob_true=p_true)

        with col_res_bar:
            st.markdown(
                """
                <div class="kira-card" style="padding: 1.35rem;">
                    <div style="font-size: 0.8rem; font-weight: 700; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.75rem; display: flex; align-items: center; gap: 6px;">
                        <span>📊</span> Keyakinan Probabilitas Model
                    </div>
                """,
                unsafe_allow_html=True,
            )
            st.write(f"**Niat Beli (Revenue = True):** `{p_true * 100:.2f}%`")
            st.progress(p_true)
            st.write(f"**Tidak Beli (Revenue = False):** `{p_false * 100:.2f}%`")
            st.progress(p_false)
            
            # Accessible interpretation adaptif dark mode
            if is_buyer:
                st.markdown(
                    f"""
                    <div style="font-size: 0.84rem; color: var(--res-pos-text); background: var(--badge-emerald-bg); border: 1px solid var(--badge-emerald-border); border-radius: 10px; padding: 0.75rem 0.9rem; margin-top: 0.75rem; line-height: 1.5;">
                        💡 <strong>Rekomendasi Bisnis:</strong> Peluang transaksi tinggi ({p_true*100:.2f}%). Sangat disarankan menampilkan insentif checkout instan (misal voucher gratis ongkir terbatas) untuk memfinalisasi transaksi.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f"""
                    <div style="font-size: 0.84rem; color: var(--text-sub); background: var(--badge-slate-bg); border: 1px solid var(--badge-slate-border); border-radius: 10px; padding: 0.75rem 0.9rem; margin-top: 0.75rem; line-height: 1.5;">
                        💡 <strong>Rekomendasi Bisnis:</strong> Peluang transaksi rendah ({p_true*100:.2f}%). Alihkan fokus pada pemberian rekomendasi konten populer, retensi newsletter, atau peningkatan daya tarik halaman katalog.
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            st.markdown("</div>", unsafe_allow_html=True)

        with st.expander("🔍 Inspeksi Matriks Data Input Sesi Pengunjung", expanded=False):
            st.dataframe(res["input_df"], use_container_width=True)

        st.caption(
            "📌 **Disklamer Model**: Hasil ini merupakan estimasi probabilistik berbasis model klasifikasi terstandarisasi "
            f"({bundle['model_name']}) pada data historis, bukan jaminan mutlak tindakan pengguna di masa depan."
        )


