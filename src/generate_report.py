import os
from pathlib import Path
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

ROOT_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DOCX = ROOT_DIR / "Laporan_Praktikum_Pertemuan_8.docx"
OUTPUT_PDF = ROOT_DIR / "Laporan_Praktikum_Pertemuan_8.pdf"
FIGURES_DIR = ROOT_DIR / "outputs" / "figures"
SCREENSHOTS_DIR = ROOT_DIR / "outputs" / "screenshots"


def set_cell_shading(cell, color_hex):
    """Set background color of a table cell."""
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{color_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set inner padding of a table cell."""
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_table_borders(table, color="CCCCCC", sz="4", val="single"):
    """Apply clean light borders to a table."""
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>\n'
        f'  <w:insideV w:val="none"/>\n'
        f'  <w:left w:val="none"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def add_code_block(doc, code_text):
    """Add a neatly formatted code block inside a shaded box."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)

    cell = table.cell(0, 0)
    set_cell_shading(cell, "F8F9FA")
    set_cell_margins(cell, top=120, bottom=120, left=180, right=180)
    
    # Border for code block
    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="single" w:sz="6" w:space="0" w:color="007ACC"/>\n'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>\n'
        f'  <w:left w:val="single" w:sz="16" w:space="0" w:color="007ACC"/>\n'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="E0E0E0"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.15
    run = p.add_run(code_text.strip())
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(36, 41, 46)

    # Empty space after table
    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)


def add_callout_box(doc, text, title="Catatan Penting:", color_hex="0288D1", bg_hex="E1F5FE"):
    """Add an alert / callout box."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = Inches(6.5)

    cell = table.cell(0, 0)
    set_cell_shading(cell, bg_hex)
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)

    tblPr = table._tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>\n'
        f'  <w:top w:val="none"/>\n'
        f'  <w:bottom w:val="none"/>\n'
        f'  <w:left w:val="single" w:sz="24" w:space="0" w:color="{color_hex}"/>\n'
        f'  <w:right w:val="none"/>\n'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

    p = cell.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    run_t = p.add_run(f"{title} ")
    run_t.bold = True
    run_t.font.name = "Calibri"
    run_t.font.size = Pt(10)
    run_t.font.color.rgb = RGBColor(1, 87, 155)

    run_b = p.add_run(text)
    run_b.font.name = "Calibri"
    run_b.font.size = Pt(10)
    run_b.font.color.rgb = RGBColor(33, 33, 33)

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(4)


def add_image_safe(doc, img_path, caption="", width=Inches(5.5)):
    """Add an image with center alignment and caption."""
    if Path(img_path).exists():
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p.paragraph_format.space_before = Pt(6)
        p.paragraph_format.space_after = Pt(2)
        p.add_run().add_picture(str(img_path), width=width)

        if caption:
            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(8)
            run_cap = p_cap.add_run(caption)
            run_cap.font.name = "Calibri"
            run_cap.font.size = Pt(9)
            run_cap.font.italic = True
            run_cap.font.color.rgb = RGBColor(100, 100, 100)
    else:
        p = doc.add_paragraph(f"[Gambar tidak ditemukan: {Path(img_path).name}]")
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER


def add_two_images_row(doc, img_left, cap_left, img_right, cap_right, width=Inches(3.1)):
    """Add two images side by side in a row with individual captions."""
    table = doc.add_table(rows=2, cols=2)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    table.autofit = False
    table.columns[0].width = width
    table.columns[1].width = width

    # Row 0: Images
    cell_l, cell_r = table.cell(0, 0), table.cell(0, 1)
    if Path(img_left).exists():
        p_l = cell_l.paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_l.add_run().add_picture(str(img_left), width=width)
    if Path(img_right).exists():
        p_r = cell_r.paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_r.add_run().add_picture(str(img_right), width=width)

    # Row 1: Captions
    c_cap_l, c_cap_r = table.cell(1, 0), table.cell(1, 1)
    p_cl = c_cap_l.paragraphs[0]
    p_cl.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_cl = p_cl.add_run(cap_left)
    run_cl.font.name = "Calibri"
    run_cl.font.size = Pt(8.5)
    run_cl.font.italic = True
    run_cl.font.color.rgb = RGBColor(100, 100, 100)

    p_cr = c_cap_r.paragraphs[0]
    p_cr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_cr = p_cr.add_run(cap_right)
    run_cr.font.name = "Calibri"
    run_cr.font.size = Pt(8.5)
    run_cr.font.italic = True
    run_cr.font.color.rgb = RGBColor(100, 100, 100)

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(6)


def build_laporan_docx():
    print(f"Creating document: {OUTPUT_DOCX}")
    doc = Document()

    # Page Margins: 1 inch (2.54 cm)
    for section in doc.sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)

    # Set default font
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(11)
    font_normal.color.rgb = RGBColor(33, 33, 33)

    # ==================== JUDUL & IDENTITAS ====================
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(4)
    run_inst = p_title.add_run("UNIVERSITAS AIRLANGGA\nFAKULTAS VOKASI\nPROGRAM STUDI D4 TEKNIK INFORMATIKA\n")
    run_inst.bold = True
    run_inst.font.size = Pt(13)
    run_inst.font.color.rgb = RGBColor(0, 32, 96)

    run_title = p_title.add_run("LAPORAN PRAKTIKUM PEMBELAJARAN MESIN\nPERTEMUAN 8\n")
    run_title.bold = True
    run_title.font.size = Pt(14)
    run_title.font.color.rgb = RGBColor(0, 51, 102)

    run_subtitle = p_title.add_run(
        "Klasifikasi Naïve Bayes, Support Vector Machine (SVM), dan Decision Tree pada Dataset Online Shoppers Purchasing Intention Serta Implementasi Antarmuka Streamlit\n"
    )
    run_subtitle.bold = True
    run_subtitle.font.size = Pt(12)
    run_subtitle.font.color.rgb = RGBColor(80, 80, 80)

    # Horizontal divider line
    p_div = doc.add_paragraph()
    p_div.paragraph_format.space_before = Pt(2)
    p_div.paragraph_format.space_after = Pt(12)
    run_div = p_div.add_run("―" * 55)
    run_div.font.color.rgb = RGBColor(0, 102, 204)
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Identity Box
    id_table = doc.add_table(rows=5, cols=2)
    id_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    id_table.autofit = False
    id_table.columns[0].width = Inches(2.2)
    id_table.columns[1].width = Inches(4.3)
    set_table_borders(id_table, color="D0D7DE", sz="4")

    id_data = [
        ("Mata Kuliah / SKS", ": Praktikum Pembelajaran Mesin (1 SKS)"),
        ("Dosen Pengampu", ": Dr. Indah Werdiningsih, S.Si., M.Kom\n  Barry Nuqoba, S.Si., M.Kom., Ph.D\n  Purbandini, S.Si., M.Kom"),
        ("Nama Mahasiswa / Kelompok", ": [NAMA MAHASISWA / KELOMPOK - Silakan disesuaikan]"),
        ("NIM", ": [NIM MAHASISWA - Silakan disesuaikan]"),
        ("Semester / Tahun Akademik", ": Semester 5 (Ganjil) / 2026-2027"),
    ]

    for r_idx, (k, v) in enumerate(id_data):
        row = id_table.rows[r_idx]
        set_cell_shading(row.cells[0], "F8F9FA")
        set_cell_shading(row.cells[1], "FFFFFF")
        set_cell_margins(row.cells[0], top=80, bottom=80, left=100, right=100)
        set_cell_margins(row.cells[1], top=80, bottom=80, left=100, right=100)
        
        p0 = row.cells[0].paragraphs[0]
        run0 = p0.add_run(k)
        run0.bold = True
        run0.font.size = Pt(10)
        p0.paragraph_format.space_after = Pt(2)

        p1 = row.cells[1].paragraphs[0]
        run1 = p1.add_run(v)
        run1.font.size = Pt(10)
        p1.paragraph_format.space_after = Pt(2)

    doc.add_paragraph().paragraph_format.space_after = Pt(12)

    # ==================== 1. TUJUAN PRAKTIKUM ====================
    h1 = doc.add_heading("1. TUJUAN PRAKTIKUM", level=1)
    h1.paragraph_format.space_before = Pt(12)
    h1.paragraph_format.space_after = Pt(6)

    tujuan_items = [
        "Mampu memahami teori dan mengimplementasikan algoritma klasifikasi Naïve Bayes (GaussianNB) dan Support Vector Machine (SVM/SVC) menggunakan pustaka Scikit-Learn pada bahasa pemrograman Python.",
        "Mampu memproses dataset nyata (Online Shoppers Purchasing Intention) melalui tahapan preprocessing yang bersih, mencakup penanganan nilai kosong (missing values), penghapusan data duplikat, dan deteksi nilai pencilan (outliers).",
        "Mampu menangani ketidakseimbangan kelas target (imbalanced data) menggunakan metode SMOTENC (oversampling) dan RandomUnderSampler (undersampling) secara terisolasi pada data training tanpa menimbulkan kebocoran data (data leakage).",
        "Mampu membandingkan kinerja model Decision Tree (hasil baseline UTS), Gaussian Naïve Bayes, dan Support Vector Machine RBF berdasarkan Confusion Matrix serta metrik evaluasi Accuracy, Precision, Recall, dan F1-Score.",
        "Mampu menganalisis komparasi kinerja secara adil (apples-to-apples) dengan pembagian data uji yang identik (80% training dan 20% testing).",
        "Mampu mengintegrasikan model klasifikasi dengan performa terbaik ke dalam aplikasi antarmuka pengguna interaktif (UI/UX) berbasis Streamlit untuk memprediksi niat belanja pengunjung website secara langsung.",
    ]
    for it in tujuan_items:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_before = Pt(2)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(it)
        run.font.size = Pt(11)

    # ==================== 2. DESKRIPSI DATASET ====================
    h2 = doc.add_heading("2. DESKRIPSI DATASET ONLINE SHOPPERS PURCHASING INTENTION", level=1)
    h2.paragraph_format.space_before = Pt(14)
    h2.paragraph_format.space_after = Pt(6)

    p_ds = doc.add_paragraph()
    p_ds.paragraph_format.line_spacing = 1.15
    p_ds.paragraph_format.space_after = Pt(6)
    p_ds.add_run(
        "Dataset yang digunakan dalam praktikum ini adalah Online Shoppers Purchasing Intention (file: online_shoppers_intention.csv). "
        "Dataset ini merekam sesi kunjungan pengguna pada situs web e-commerce selama periode satu tahun untuk memprediksi apakah suatu sesi kunjungan "
        "akan berakhir dengan transaksi pembelian (Revenue = True) atau tidak menghasilkan pembelian (Revenue = False)."
    )

    p_ds2 = doc.add_paragraph()
    p_ds2.paragraph_format.line_spacing = 1.15
    p_ds2.paragraph_format.space_after = Pt(6)
    p_ds2.add_run(
        "Dataset terdiri dari 12.330 baris data dan 18 kolom (17 fitur prediktor dan 1 variabel target). "
        "Karakteristik target Revenue menunjukkan ketidakseimbangan kelas yang signifikan, dengan proporsi awal sebagai berikut:"
    )

    p_imb = doc.add_paragraph(style='List Bullet')
    p_imb.add_run("Kelas False (Tidak Beli) : 10.422 sampel (84,53%)\n")
    p_imb.add_run("Kelas True (Membeli) : 1.908 sampel (15,47%)\n")
    p_imb.add_run("Rasio Ketimpangan Kelas : ~ 5,46 : 1")

    # Feature descriptions table
    t_feat = doc.add_table(rows=1, cols=3)
    t_feat.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_feat.autofit = False
    t_feat.columns[0].width = Inches(2.0)
    t_feat.columns[1].width = Inches(1.5)
    t_feat.columns[2].width = Inches(3.0)
    set_table_borders(t_feat, color="D0D7DE")

    hdr_cells = t_feat.rows[0].cells
    hdr_titles = ["Nama Fitur", "Tipe Data", "Deskripsi & Rentang Nilai"]
    for i, title in enumerate(hdr_titles):
        set_cell_shading(hdr_cells[i], "003366")
        set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
        p = hdr_cells[i].paragraphs[0]
        run = p.add_run(title)
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.font.size = Pt(9.5)

    feat_list = [
        ("Administrative", "Numerik (int64)", "Jumlah halaman akun/administratif yang dibuka (0 - 27)"),
        ("Administrative_Duration", "Numerik (float64)", "Total waktu (detik) pada halaman administratif (0 - 3398.75)"),
        ("Informational", "Numerik (int64)", "Jumlah halaman informasi/kontak yang dikunjungi (0 - 24)"),
        ("Informational_Duration", "Numerik (float64)", "Total waktu (detik) pada halaman informasi (0 - 2549.38)"),
        ("ProductRelated", "Numerik (int64)", "Jumlah halaman katalog produk yang dikunjungi (0 - 705)"),
        ("ProductRelated_Duration", "Numerik (float64)", "Total waktu (detik) melihat katalog produk (0 - 63973.52)"),
        ("BounceRates", "Numerik (float64)", "Persentase sesi yang langsung keluar tanpa interaksi (0.0 - 0.2)"),
        ("ExitRates", "Numerik (float64)", "Persentase halaman yang menjadi akhir sesi pengunjung (0.0 - 0.2)"),
        ("PageValues", "Numerik (float64)", "Rata-rata kontribusi halaman terhadap transaksi e-commerce (0.0 - 361.76)"),
        ("SpecialDay", "Numerik (float64)", "Kedekatan tanggal kunjungan dengan hari perayaan khusus (0.0 - 1.0)"),
        ("OperatingSystems", "Numerik Kategori (int64)", "Kode sistem operasi perangkat pengguna (1 - 8)"),
        ("Browser", "Numerik Kategori (int64)", "Kode peramban web yang digunakan (1 - 13)"),
        ("Region", "Numerik Kategori (int64)", "Kode wilayah geografis pengunjung (1 - 9)"),
        ("TrafficType", "Numerik Kategori (int64)", "Kode sumber lalu lintas pengunjung (1 - 20)"),
        ("Month", "Kategorikal (object)", "Bulan kunjungan ('Feb', 'Mar', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')"),
        ("VisitorType", "Kategorikal (object)", "Tipe pengunjung ('Returning_Visitor', 'New_Visitor', 'Other')"),
        ("Weekend", "Kategorikal (bool)", "Indikator apakah sesi berlangsung di akhir pekan (False / True)"),
        ("Revenue (Target)", "Boolean (bool)", "Status transaksi pembelian akhir: True (Membeli), False (Tidak Beli)"),
    ]

    for f_name, f_type, f_desc in feat_list:
        row = t_feat.add_row()
        for idx, text in enumerate([f_name, f_type, f_desc]):
            c = row.cells[idx]
            set_cell_margins(c, top=60, bottom=60, left=100, right=100)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            run = p.add_run(text)
            run.font.size = Pt(8.5)
            if idx == 0:
                run.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ==================== 3. PREPROCESSING & TRANSFORMATION ====================
    h3 = doc.add_heading("3. TAHAPAN PREPROCESSING DAN TRANSFORMASI DATA", level=1)
    h3.paragraph_format.space_before = Pt(14)
    h3.paragraph_format.space_after = Pt(6)

    p_prep = doc.add_paragraph()
    p_prep.paragraph_format.line_spacing = 1.15
    p_prep.paragraph_format.space_after = Pt(6)
    p_prep.add_run(
        "Mengikuti tahapan baku pada praktikum dan evaluasi UTS, preprocessing dilakukan secara terstruktur untuk menjamin kebersihan data tanpa data leakage:"
    )

    steps_prep = [
        ("Pemeriksaan Missing Value", "Dataset diperiksa menggunakan df.isna().sum(). Hasilnya menunjukkan tidak ada nilai kosong (missing values = 0) pada seluruh 18 kolom."),
        ("Pemeriksaan dan Pembersihan Data Duplikat", "Ditemukan sebanyak 125 baris duplikat identik. Seluruh baris duplikat ini dihapus menggunakan df.drop_duplicates(), sehingga jumlah data bersih yang digunakan adalah 12.205 baris."),
        ("Deteksi Nilai Pencilan (Outliers)", "Deteksi outlier dilakukan pada kolom numerik menggunakan metode Interquartile Range (IQR = Q3 - Q1, batas bawah = Q1 - 1.5*IQR, batas atas = Q3 + 1.5*IQR). Hasil deteksi menemukan adanya outlier pada fitur durasi dan PageValues. Sesuai kesepakatan UTS, outlier dipertahankan (tidak dibuang) karena merepresentasikan perilaku belanja nyata pengunjung yang memiliki durasi browsing tinggi atau nilai transaksi besar."),
        ("Pemisahan Fitur dan Target", "Data bersih dipisahkan menjadi matriks fitur X (17 fitur) dan vektor label target y (Revenue)."),
        ("Pembagian Data Train-Test (80:20)", "Data dibagi menjadi 80% data training (9.764 baris) dan 20% data testing (2.441 baris) menggunakan train_test_split dengan random_state=42 dan parameter stratify=y untuk mempertahankan rasio kelas target yang seimbang antara train dan test."),
    ]
    for s_title, s_desc in steps_prep:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        run_t = p.add_run(f"{s_title}: ")
        run_t.bold = True
        run_d = p.add_run(s_desc)

    add_callout_box(
        doc,
        "Seluruh proses fitting transformer (StandardScaler dan OneHotEncoder) serta resampling HANYA dilakukan pada data training. "
        "Data testing (2.441 baris) disimpan dalam kondisi aslinya dan hanya ditransformasikan secara pasif menggunakan transformer yang telah di-fit pada data training. "
        "Hal ini menjamin 100% tidak terjadinya kebocoran informasi (data leakage) dari data uji ke model.",
        title="Prinsip Bebas Data Leakage:",
        color_hex="2E7D32",
        bg_hex="E8F5E9"
    )

    p_code_intro = doc.add_paragraph()
    p_code_intro.add_run("Potongan kode preprocessing (src/data_preprocessing.py):").italic = True
    add_code_block(doc, """def preprocess_data(df):
    # 1. Check and handle missing values
    missing = df.isna().sum().sum()
    if missing > 0:
        df = df.dropna().copy()

    # 2. Check and handle duplicates
    duplicates = df.duplicated().sum()
    if duplicates > 0:
        df = df.drop_duplicates().copy()

    # 3. Detect outliers with IQR (outliers retained)
    ...
    # 4. Separate features and target
    X = df.drop(columns=['Revenue'])
    y = df['Revenue']
    return X, y""")

    p_trans_intro = doc.add_paragraph()
    p_trans_intro.add_run("Potongan kode transformasi fitur (src/data_transformation.py):").italic = True
    add_code_block(doc, """def get_preprocessor(X):
    num_cols = X.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = X.select_dtypes(exclude=[np.number]).columns.tolist()

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_cols),
            ('cat', OneHotEncoder(handle_unknown='ignore', drop='first'), cat_cols)
        ]
    )
    return preprocessor, num_cols, cat_cols""")

    # ==================== 4. PENANGANAN IMBALANCED DATA ====================
    h4 = doc.add_heading("4. PENANGANAN KETIDAKSEIMBANGAN KELAS (RESAMPLING)", level=1)
    h4.paragraph_format.space_before = Pt(14)
    h4.paragraph_format.space_after = Pt(6)

    p_imb_desc = doc.add_paragraph()
    p_imb_desc.paragraph_format.line_spacing = 1.15
    p_imb_desc.paragraph_format.space_after = Pt(6)
    p_imb_desc.add_run(
        "Pada data training sebanyak 9.764 sampel, kelas mayoritas False berjumlah 8.238 baris (84,37%) dan kelas minoritas True hanya berjumlah 1.526 baris (15,63%). "
        "Jika model dilatih langsung pada data yang sangat tidak seimbang, model cenderung memprioritaskan akurasi pada kelas mayoritas dan mengabaikan kelas minoritas (pembeli). "
        "Oleh karena itu, diimplementasikan dua teknik resampling pada data training:"
    )

    p_smote = doc.add_paragraph(style='List Bullet')
    p_smote.paragraph_format.line_spacing = 1.15
    p_smote.add_run("1. SMOTENC (Synthetic Minority Over-sampling Technique for Nominal and Continuous):\n").bold = True
    p_smote.add_run(
        "Metode oversampling khusus untuk dataset dengan fitur campuran. SMOTENC menginterpolasi fitur numerik di antara tetangga terdekat (k-NN), "
        "sementara fitur kategorikal (Month, VisitorType, Weekend) ditentukan berdasarkan modus (kategori terbanyak) dari tetangga terdekatnya. "
        "Dengan menerapkan SMOTENC SEBELUM OneHotEncoder, data sintetis yang dihasilkan tetap mempertahankan nilai kategori valid dan tidak menghasilkan nilai dummy pecahan. "
        "Hasil SMOTENC menyeimbangkan kelas training menjadi 8.238 False dan 8.238 True (total 16.476 sampel)."
    )

    p_rus = doc.add_paragraph(style='List Bullet')
    p_rus.paragraph_format.line_spacing = 1.15
    p_rus.add_run("2. RandomUnderSampler (RUS):\n").bold = True
    p_rus.add_run(
        "Metode undersampling yang secara acak memangkas sampel dari kelas mayoritas False agar jumlahnya sama dengan kelas minoritas True. "
        "Hasil RandomUnderSampler menghasilkan data training seimbang dengan 1.526 False dan 1.526 True (total 3.052 sampel)."
    )

    # Images of class distributions
    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    add_image_safe(
        doc,
        FIGURES_DIR / "dist_before_resampling.png",
        caption="Gambar 1: Distribusi Kelas Data Training Sebelum Resampling (Ketidakseimbangan Rasio ~5.4 : 1)",
        width=Inches(4.5)
    )

    add_two_images_row(
        doc,
        FIGURES_DIR / "dist_after_smotenc.png",
        "Gambar 2a: Distribusi Training Setelah SMOTENC (16.476 sampel)",
        FIGURES_DIR / "dist_after_rus.png",
        "Gambar 2b: Distribusi Training Setelah RandomUnderSampler (3.052 sampel)",
        width=Inches(3.1)
    )

    # ==================== 5. METODE KLASIFIKASI ====================
    h5 = doc.add_heading("5. METODE KLASIFIKASI (DECISION TREE, NAÏVE BAYES, DAN SVM)", level=1)
    h5.paragraph_format.space_before = Pt(14)
    h5.paragraph_format.space_after = Pt(6)

    methods = [
        ("A. Decision Tree Classifier (Baseline UTS)",
         "Decision Tree membangun model klasifikasi berbentuk pohon keputusan dengan mempartisi ruang fitur berdasarkan aturan keputusan sederhana. "
         "Pada eksperimen ini, parameter yang digunakan sesuai UTS adalah max_depth=10 dan random_state=42. "
         "Pembatasan kedalaman pohon dilakukan untuk menghindari overfitting pada data training."),
        ("B. Gaussian Naïve Bayes (Pertemuan 8)",
         "Naïve Bayes didasarkan pada Teorema Bayes dengan asumsi 'naif' bahwa semua fitur bersifat saling bebas (conditional independence) jika diberikan label kelas. "
         "Karena fitur input telah distandardisasi menjadi distribusi kontinu, model mengasumsikan setiap fitur berdistribusi normal (Gaussian). "
         "Parameter var_smoothing=1e-9 digunakan untuk menambahkan porsi variansi terbesar agar estimasi probabilitas numerik tetap stabil."),
        ("C. Support Vector Machine / SVM RBF (Pertemuan 8)",
         "SVM mencari bidang pemisah (hyperplane) optimal yang memaksimalkan jarak margin antara dua kelas data. "
         "Karena hubungan antar fitur pengunjung e-commerce bersifat non-linear dan kompleks, digunakan kernel Radial Basis Function (RBF). "
         "SVM sangat diuntungkan oleh tahapan StandardScaler karena algoritma margin sensitif terhadap skala fitur. "
         "Parameter yang digunakan adalah C=1.0, random_state=42, dan probability=True untuk mengaktifkan estimasi probabilitas Platt Scaling."),
    ]
    for m_title, m_desc in methods:
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(4)
        run_t = p.add_run(f"{m_title}\n")
        run_t.bold = True
        run_d = p.add_run(m_desc)

    # ==================== 6. HASIL EVALUASI & KOMPARASI ====================
    h6 = doc.add_heading("6. HASIL EVALUASI AKTUAL DAN ANALISIS KOMPARASI", level=1)
    h6.paragraph_format.space_before = Pt(14)
    h6.paragraph_format.space_after = Pt(6)

    p_eval_intro = doc.add_paragraph()
    p_eval_intro.paragraph_format.line_spacing = 1.15
    p_eval_intro.paragraph_format.space_after = Pt(6)
    p_eval_intro.add_run(
        "Seluruh eksperimen dievaluasi pada data testing yang persis sama sebanyak 2.441 sampel (2.059 False dan 382 True). "
        "Metrik dihitung dengan menetapkan kelas Revenue = True (pembeli) sebagai target positif (pos_label=True). "
        "Tabel berikut menyajikan hasil evaluasi aktual dari eksekusi program terpadu:"
    )

    # Evaluation Table
    t_res = doc.add_table(rows=1, cols=5)
    t_res.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_res.autofit = False
    t_res.columns[0].width = Inches(2.5)
    t_res.columns[1].width = Inches(1.0)
    t_res.columns[2].width = Inches(1.0)
    t_res.columns[3].width = Inches(1.0)
    t_res.columns[4].width = Inches(1.0)
    set_table_borders(t_res, color="D0D7DE")

    hdr_res = t_res.rows[0].cells
    hdr_res_titles = ["Model & Resampling", "Accuracy", "Precision", "Recall", "F1-Score"]
    for i, title in enumerate(hdr_res_titles):
        set_cell_shading(hdr_res[i], "003366")
        set_cell_margins(hdr_res[i], top=100, bottom=100, left=80, right=80)
        p = hdr_res[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.font.size = Pt(9.5)

    eval_rows = [
        ("Decision Tree + SMOTENC", "86,89%", "56,20%", "73,56%", "63,72%"),
        ("Decision Tree + RandomUnderSampler", "83,61%", "48,59%", "81,41%", "60,86%"),
        ("Gaussian Naive Bayes + SMOTENC", "48,26%", "21,92%", "90,05%", "35,26%"),
        ("Gaussian Naive Bayes + RandomUnderSampler", "63,87%", "29,17%", "91,62%", "44,25%"),
        ("SVM RBF + SMOTENC (Terpilih ⭐)", "87,46%", "58,05%", "71,73%", "64,17%"),
        ("SVM RBF + RandomUnderSampler", "85,33%", "52,11%", "77,75%", "62,40%"),
    ]

    for m_name, acc, prec, rec, f1 in eval_rows:
        row = t_res.add_row()
        is_best = "⭐" in m_name
        for idx, text in enumerate([m_name, acc, prec, rec, f1]):
            c = row.cells[idx]
            if is_best:
                set_cell_shading(c, "E8F5E9")
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            if idx > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(text)
            run.font.size = Pt(9)
            if is_best:
                run.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Metrics comparison figure
    add_image_safe(
        doc,
        FIGURES_DIR / "perbandingan_metrik.png",
        caption="Gambar 3: Grafik Batang Perbandingan Metrik Evaluasi 6 Kombinasi Model",
        width=Inches(6.0)
    )

    # ==================== 7. ANALISIS CONFUSION MATRIX ====================
    h7 = doc.add_heading("7. ANALISIS CONFUSION MATRIX DAN PEMBAHASAN TP, TN, FP, FN", level=1)
    h7.paragraph_format.space_before = Pt(14)
    h7.paragraph_format.space_after = Pt(6)

    p_cm_intro = doc.add_paragraph()
    p_cm_intro.paragraph_format.line_spacing = 1.15
    p_cm_intro.paragraph_format.space_after = Pt(6)
    p_cm_intro.add_run(
        "Confusion Matrix memetakan prediksi model terhadap kondisi aktual pada data testing (2.059 kelas False dan 382 kelas True). "
        "Struktur matriks konfusi menggunakan urutan baris [Aktual False, Aktual True] dan kolom [Prediksi False, Prediksi True]:"
    )

    cm_expl = [
        ("True Positive (TP)", "Pengunjung yang diprediksi membeli (True) dan secara aktual memang membeli."),
        ("True Negative (TN)", "Pengunjung yang diprediksi tidak membeli (False) dan secara aktual memang tidak membeli."),
        ("False Positive (FP)", "Pengunjung yang diprediksi membeli (True) padahal sebenarnya tidak membeli (False Alarm). Kesalahan ini berpotensi membuang biaya pemasaran atau penawaran diskon yang sia-sia."),
        ("False Negative (FN)", "Pengunjung yang diprediksi tidak membeli (False) padahal sebenarnya membeli (Missed Opportunity). Kesalahan ini menyebabkan e-commerce kehilangan kesempatan mendorong transaksi."),
    ]
    for c_title, c_desc in cm_expl:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.line_spacing = 1.15
        run_t = p.add_run(f"{c_title}: ")
        run_t.bold = True
        p.add_run(c_desc)

    p_cm_t = doc.add_paragraph()
    p_cm_t.paragraph_format.space_before = Pt(6)
    p_cm_t.add_run("Tabel Rincian Elemen Confusion Matrix Aktual 6 Model:").bold = True

    t_cm = doc.add_table(rows=1, cols=5)
    t_cm.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_cm.autofit = False
    t_cm.columns[0].width = Inches(2.5)
    t_cm.columns[1].width = Inches(1.0)
    t_cm.columns[2].width = Inches(1.0)
    t_cm.columns[3].width = Inches(1.0)
    t_cm.columns[4].width = Inches(1.0)
    set_table_borders(t_cm, color="D0D7DE")

    hdr_cm = t_cm.rows[0].cells
    hdr_cm_titles = ["Model & Resampling", "TN", "FP", "FN", "TP"]
    for i, title in enumerate(hdr_cm_titles):
        set_cell_shading(hdr_cm[i], "003366")
        set_cell_margins(hdr_cm[i], top=80, bottom=80, left=80, right=80)
        p = hdr_cm[i].paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(title)
        run.bold = True
        run.font.color.rgb = RGBColor(255, 255, 255)
        run.font.size = Pt(9.5)

    cm_data = [
        ("Decision Tree + SMOTENC", "1.840", "219", "101", "281"),
        ("Decision Tree + RandomUnderSampler", "1.730", "329", "71", "311"),
        ("Gaussian Naive Bayes + SMOTENC", "834", "1.225", "38", "344"),
        ("Gaussian Naive Bayes + RandomUnderSampler", "1.209", "850", "32", "350"),
        ("SVM RBF + SMOTENC (Terpilih ⭐)", "1.861", "198", "108", "274"),
        ("SVM RBF + RandomUnderSampler", "1.786", "273", "85", "297"),
    ]

    for m_name, tn, fp, fn, tp in cm_data:
        row = t_cm.add_row()
        is_best = "⭐" in m_name
        for idx, text in enumerate([m_name, tn, fp, fn, tp]):
            c = row.cells[idx]
            if is_best:
                set_cell_shading(c, "E8F5E9")
            set_cell_margins(c, top=60, bottom=60, left=80, right=80)
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            if idx > 0:
                p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            run = p.add_run(text)
            run.font.size = Pt(9)
            if is_best:
                run.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # Confusion matrix visual side by side
    add_two_images_row(
        doc,
        FIGURES_DIR / "cm_dt_smotenc.png",
        "Gambar 4a: Confusion Matrix Decision Tree + SMOTENC",
        FIGURES_DIR / "cm_dt_rus.png",
        "Gambar 4b: Confusion Matrix Decision Tree + RUS",
        width=Inches(3.1)
    )
    add_two_images_row(
        doc,
        FIGURES_DIR / "cm_nb_smotenc.png",
        "Gambar 4c: Confusion Matrix Naïve Bayes + SMOTENC",
        FIGURES_DIR / "cm_nb_rus.png",
        "Gambar 4d: Confusion Matrix Naïve Bayes + RUS",
        width=Inches(3.1)
    )
    add_two_images_row(
        doc,
        FIGURES_DIR / "cm_svm_smotenc.png",
        "Gambar 4e: Confusion Matrix SVM RBF + SMOTENC",
        FIGURES_DIR / "cm_svm_rus.png",
        "Gambar 4f: Confusion Matrix SVM RBF + RUS",
        width=Inches(3.1)
    )

    # Detailed discussion of metrics
    h7_2 = doc.add_heading("Pembahasan Perbandingan Metrik & Karakteristik Algoritma", level=2)
    h7_2.paragraph_format.space_before = Pt(10)
    h7_2.paragraph_format.space_after = Pt(4)

    p_disc = doc.add_paragraph()
    p_disc.paragraph_format.line_spacing = 1.15
    p_disc.paragraph_format.space_after = Pt(6)
    p_disc.add_run(
        "1. Mengapa Akurasi Tinggi Saja Tidak Cukup?\n"
        "Pada dataset imbalanced dengan proporsi mayoritas 84,53% (False), sebuah model 'dummy' yang selalu menebak False akan dengan mudah meraih akurasi 84,53%. "
        "Namun, model tersebut tidak memiliki kemampuan sama sekali untuk mendeteksi pembeli (Recall = 0% dan F1-Score = 0%). "
        "Oleh karena itu, metrik Precision, Recall, dan F1-Score pada kelas True adalah tolok ukur esensial dalam mengevaluasi efektivitas model klasifikasi ini.\n\n"
        "2. Anomali Kinerja Gaussian Naïve Bayes:\n"
        "Meskipun Naïve Bayes mencatat Recall yang sangat tinggi (>90%), akurasi dan presisinya anjlok drastis (akurasi hanya 48,26% pada SMOTENC dan 63,87% pada RUS). "
        "Hal ini disebabkan oleh pelanggaran asumsi independensi fitur (conditional independence). Fitur-fitur web analytics seperti BounceRates dan ExitRates, "
        "atau ProductRelated dan ProductRelated_Duration, memiliki korelasi linear yang sangat kuat (r > 0.85). Akibatnya, bukti probabilitas dihitung berulang kali "
        "secara berlebihan, mendistorsi probabilitas posterior ke arah kelas minoritas sehingga menghasilkan jumlah False Positive yang masif (1.225 FP pada SMOTENC).\n\n"
        "3. Efek Resampling SMOTENC vs RandomUnderSampler:\n"
        "Pada seluruh model, RandomUnderSampler menghasilkan Recall yang lebih tinggi dibandingkan SMOTENC karena pemangkasan agresif kelas mayoritas memaksa model lebih berani menebak True. "
        "Namun, hal tersebut dibayar dengan penurunan Presisi dan Akurasi. Sebaliknya, SMOTENC memberikan generalisasi yang jauh lebih solid, menghasilkan F1-Score dan Akurasi tertinggi.\n\n"
        "4. Keunggulan SVM RBF + SMOTENC:\n"
        "SVM dengan kernel RBF berhasil memetakan pola interaksi non-linear dengan sangat baik berkat bantuan StandardScaler. "
        "Model ini menekan kesalahan False Positive hingga ke angka terendah (198 kasus), sehingga memperoleh Presisi tertinggi (58,05%), Akurasi tertinggi (87,46%), "
        "dan F1-Score tertinggi (64,17%) dengan tetap menjaga Recall di atas 71,73%."
    )

    # ==================== 8. IMPLEMENTASI UI STREAMLIT ====================
    h8 = doc.add_heading("8. IMPLEMENTASI DAN PENGUJIAN APLIKASI UI/UX STREAMLIT", level=1)
    h8.paragraph_format.space_before = Pt(14)
    h8.paragraph_format.space_after = Pt(6)

    p_ui_intro = doc.add_paragraph()
    p_ui_intro.paragraph_format.line_spacing = 1.15
    p_ui_intro.paragraph_format.space_after = Pt(6)
    p_ui_intro.add_run(
        "Sesuai ketentuan tugas nomor 6, dibangun aplikasi antarmuka pengguna interaktif (UI/UX) berbasis Streamlit (file: app.py) "
        "menggunakan model terbaik terpilih, yaitu SVM RBF + SMOTENC."
    )

    ui_features = [
        ("Arsitektur Tanpa Pelatihan Ulang (Zero-Retraining)", "Model SVM dan ColumnTransformer terlatih disimpan ke dalam satu file bundel (best_model_bundle.joblib). Aplikasi memuat artefak ini menggunakan dekorator @st.cache_resource, sehingga model langsung siap melayani prediksi secara instan tanpa membebani server dengan proses pelatihan ulang."),
        ("Pengelompokan Formulir 17 Fitur", "Input 17 fitur dikelompokkan secara ergonomis ke dalam 3 tab (Aktivitas Halaman & Durasi, Metrik Sesi Analytics, dan Profil Pengunjung & Waktu) dengan validasi tipe data (int64, float64, string, bool) dan urutan fitur yang identik dengan dataset asli."),
        ("Fitur Preset Pengujian Cepat", "Disediakan tombol cepat di sidebar untuk mengisi nilai formulir secara otomatis: 'Niat Beli Tinggi' (sampel pembeli nyata) dan 'Bouncing / Kasual' (sampel pengunjung yang langsung keluar)."),
        ("Visualisasi Keyakinan Probabilitas", "Hasil prediksi dilengkapi dengan badge status klasifikasi berbahasa Indonesia dan progress bar visual probabilitas kelas (P(False) dan P(True)) yang dihasilkan dari metode model.predict_proba()."),
    ]
    for u_title, u_desc in ui_features:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.add_run(f"{u_title}: ").bold = True
        p.add_run(u_desc)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)
    add_image_safe(
        doc,
        SCREENSHOTS_DIR / "overview_dashboard.png",
        caption="Gambar 5: Tampilan Antarmuka AI Analytics Dashboard 'Purchase Intent Analytics' (Streamlit)",
        width=Inches(6.0)
    )

    h8_2 = doc.add_heading("Hasil Pengujian Dua Skenario Input Pengunjung", level=2)
    h8_2.paragraph_format.space_before = Pt(10)
    h8_2.paragraph_format.space_after = Pt(4)

    p_scen = doc.add_paragraph()
    p_scen.paragraph_format.line_spacing = 1.15
    p_scen.paragraph_format.space_after = Pt(6)
    p_scen.add_run(
        "Aplikasi telah diuji menggunakan dua skenario karakteristik pengunjung yang berbeda:\n"
        "• Skenario 1 (Pengunjung Berniat Beli Tinggi): Administrative=3, ProductRelated=27, Duration=798s, PageValues=22.92, BounceRates=0.0. "
        "Hasil prediksi menghasilkan status 'Berpotensi Menghasilkan Pembelian (Revenue = True)' dengan probabilitas niat beli mencapai 86,23% (P(True) = 0.862).\n"
        "• Skenario 2 (Pengunjung Kasual / Langsung Keluar): Administrative=0, ProductRelated=1, Duration=0s, PageValues=0.0, BounceRates=0.20, ExitRates=0.20. "
        "Hasil prediksi menghasilkan status 'Tidak Terindikasi Menghasilkan Pembelian (Revenue = False)' dengan probabilitas tidak beli mencapai 94,47% (P(False) = 0.945)."
    )

    add_two_images_row(
        doc,
        SCREENSHOTS_DIR / "prediction_result_positive.png",
        "Gambar 6a: Hasil Prediksi Skenario 1 (Niat Beli Tinggi - True: 86.23%)",
        SCREENSHOTS_DIR / "prediction_result_negative.png",
        "Gambar 6b: Hasil Prediksi Skenario 2 (Kasual / Bouncing - False: 94.47%)",
        width=Inches(3.1)
    )


    # ==================== 9. KESIMPULAN & KETERBATASAN ====================
    h9 = doc.add_heading("9. KESIMPULAN DAN KETERBATASAN", level=1)
    h9.paragraph_format.space_before = Pt(14)
    h9.paragraph_format.space_after = Pt(6)

    p_kesimpulan = doc.add_paragraph()
    p_kesimpulan.paragraph_format.line_spacing = 1.15
    p_kesimpulan.paragraph_format.space_after = Pt(6)
    p_kesimpulan.add_run("Berdasarkan seluruh rangkaian eksperimen dan evaluasi praktikum pertemuan 8, dapat ditarik beberapa kesimpulan pokok:\n").bold = True

    kesimpulan_pts = [
        "SVM RBF + SMOTENC merupakan model terbaik secara komprehensif pada dataset Online Shoppers Purchasing Intention, dengan meraih Akurasi tertinggi (87,46%), Presisi tertinggi (58,05%), F1-Score tertinggi (64,17%), dan menekan False Positive ke angka terendah (198).",
        "Decision Tree + SMOTENC menempati posisi kedua yang kompetitif dengan Akurasi 86,89% dan F1-Score 63,72%, serta memiliki keunggulan waktu inferensi yang sangat cepat dan pohon keputusan yang mudah diinterpretasikan.",
        "Gaussian Naïve Bayes tidak cocok digunakan pada dataset web analytics ini karena asumsi independensi fitur terlanggar berat oleh adanya multikolinearitas antar fitur, menyebabkan lonjakan False Positive yang masif dan menjatuhkan Akurasi ke rentang 48% - 63%.",
        "SMOTENC terbukti jauh lebih unggul dan seimbang dibandingkan RandomUnderSampler karena mempertahankan seluruh informasi mayoritas asli dan hanya mensintesis sampel minoritas baru.",
        "Aplikasi web Streamlit berhasil mengimplementasikan inferensi model terlatih tanpa pelatihan ulang, menyediakan antarmuka 17 fitur yang terstruktur, dan memberikan prediksi probabilistik yang akurat.",
    ]
    for kp in kesimpulan_pts:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.add_run(kp)

    p_limit = doc.add_paragraph()
    p_limit.paragraph_format.space_before = Pt(8)
    p_limit.paragraph_format.line_spacing = 1.15
    p_limit.paragraph_format.space_after = Pt(6)
    p_limit.add_run("Keterbatasan Eksperimen:\n").bold = True
    limit_pts = [
        "Kompleksitas Komputasi SVM: Waktu pelatihan SVM RBF bertambah secara kuadratik terhadap jumlah data resample (16.476 baris), sehingga untuk dataset skala jutaan baris diperlukan metode aproksimasi linear atau subsampling.",
        "Representasi Kategorikal Numerik: Fitur OperatingSystems, Browser, Region, dan TrafficType pada baseline UTS diproses sebagai numerik. Pada pengembangan lebih lanjut, penerapan embedding atau grouping kategori berfrekuensi rendah dapat diuji untuk mengeksplorasi potensi peningkatan akurasi.",
    ]
    for lp in limit_pts:
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        p.add_run(lp)

    # ==================== 10. PETUNJUK MENJALANKAN & STRUKTUR FILE ====================
    h10 = doc.add_heading("10. PETUNJUK MENJALANKAN PROGRAM DAN STRUKTUR FILE", level=1)
    h10.paragraph_format.space_before = Pt(14)
    h10.paragraph_format.space_after = Pt(6)

    p_run = doc.add_paragraph()
    p_run.paragraph_format.line_spacing = 1.15
    p_run.paragraph_format.space_after = Pt(4)
    p_run.add_run("A. Instalasi Dependensi:\nPastikan modul Python yang dibutuhkan telah terpasang dengan perintah:")
    add_code_block(doc, "pip install -r requirements.txt")

    p_run_exp = doc.add_paragraph()
    p_run_exp.paragraph_format.line_spacing = 1.15
    p_run_exp.paragraph_format.space_after = Pt(4)
    p_run_exp.add_run("B. Menjalankan Eksperimen Pelatihan & Komparasi:\nUntuk mengeksekusi pipeline 6 eksperimen dan menghasilkan tabel serta grafik:")
    add_code_block(doc, "python src/main.py")

    p_run_app = doc.add_paragraph()
    p_run_app.paragraph_format.line_spacing = 1.15
    p_run_app.paragraph_format.space_after = Pt(4)
    p_run_app.add_run("C. Menjalankan Aplikasi Antarmuka Streamlit:\nUntuk membuka aplikasi web pada browser lokal di http://localhost:8501:")
    add_code_block(doc, "streamlit run app.py")

    p_tree = doc.add_paragraph()
    p_tree.paragraph_format.line_spacing = 1.15
    p_tree.paragraph_format.space_after = Pt(4)
    p_tree.add_run("D. Struktur Berkas yang Dikumpulkan:")
    add_code_block(doc, """praktikum_ml_tm8/
├── dataset/
│   └── online_shoppers_intention.csv
├── outputs/
│   ├── figures/ (cm_*.png, dist_*.png, perbandingan_metrik.png)
│   ├── models/ (best_model_bundle.joblib)
│   ├── screenshots/ (ui_halaman_utama.png, ui_prediksi_*.png)
│   └── tables/ (evaluasi_model_komparasi.csv)
├── src/
│   ├── data_preprocessing.py
│   ├── data_transformation.py
│   ├── imbalanced_data.py
│   ├── decision_tree.py
│   ├── naive_bayes.py
│   ├── svm.py
│   ├── evaluation.py
│   └── main.py
├── app.py
├── requirements.txt
├── README.md
├── Laporan_Praktikum_Pertemuan_8.docx
└── Laporan_Praktikum_Pertemuan_8.pdf""")

    # Save document
    doc.save(str(OUTPUT_DOCX))
    print(f"Document successfully created and saved at: {OUTPUT_DOCX}")


def convert_docx_to_pdf():
    """Convert generated DOCX to PDF using Word COM."""
    print(f"Converting DOCX to PDF using Microsoft Word COM...")
    import comtypes.client
    import time

    word = None
    try:
        word = comtypes.client.CreateObject('Word.Application')
        word.Visible = False
        doc = word.Documents.Open(str(OUTPUT_DOCX.resolve()))
        # 17 is the wdFormatPDF constant in Microsoft Word
        doc.SaveAs(str(OUTPUT_PDF.resolve()), FileFormat=17)
        doc.Close()
        word.Quit()
        word = None
        print(f"PDF successfully exported at: {OUTPUT_PDF}")
    except Exception as e:
        print(f"Error during PDF conversion via Word COM: {e}")
        if word:
            try:
                word.Quit()
            except:
                pass


if __name__ == "__main__":
    build_laporan_docx()
    convert_docx_to_pdf()
