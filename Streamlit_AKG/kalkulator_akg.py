import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- CSS KUSTOM & TEMA (REVISI V9 - Saran Makanan Dinamis BMI) ---
st.markdown("""
<style>
    /* 1. Latar Belakang Utama Aplikasi (Deep Navy) */
    .stApp {
        background-color: #0B2447; /* Biru Tua Sangat Pekat (Deep Navy) */
        color: #F0F0F0; /* Warna teks utama terang */
        font-family: 'Georgia', serif; 
    }

    /* 2. Latar Belakang Sidebar & Containers */
    .st-emotion-cache-1ldfqsx, .st-emotion-cache-h44nrf, .st-emotion-cache-12fm521 { 
        background-color: #19376D; /* Biru sedang pekat */
        border-radius: 12px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.5); 
        padding: 25px;
        color: #FFFFFF;
        border: 1px solid #A5D7E8; /* Garis tepi kontainer */
    }
    
    /* FIX: Teks di Sidebar */
    .st-emotion-cache-1ldfqsx label, .st-emotion-cache-1ldfqsx h2 {
        color: #F0F0F0 !important;
    }

    /* 3. Judul Utama */
    h1 {
        color: #FFB300; /* Kuning Emas/Amber Pekat */
        text-align: center;
        font-weight: 900;
        padding-bottom: 15px;
        border-bottom: 3px solid #FFB300;
    }
    
    /* 4. Subjudul & Header lainnya */
    h2, h3, h4 {
        color: #A5D7E8; /* Biru Muda Cerah/Kontras */
        font-weight: 700;
        border-left: 5px solid #A5D7E8;
        padding-left: 10px;
    }

    /* 🔥 FIX: KOTAK SUCCESS (st.success) -> PUTIH TEKS HITAM */
    .st-emotion-cache-199v4c3 { 
        background-color: #f7f3e8; /* Background Putih Pucat (Off-White) */
        border-left: 8px solid #FFB300; /* Garis samping Kuning Emas */
        font-weight: bold;
    }
    
    .st-emotion-cache-199v4c3 p {
        color: #000000 !important; /* Teks di st.success menjadi HITAM */
        font-weight: bold !important;
    }
    
    /* FIX: BACKGROUND KOTAK INPUT */
    [data-baseweb="select"] div:first-child,
    [data-baseweb="input"] input,
    .st-emotion-cache-1y4pm5r div, 
    .st-emotion-cache-15tx6ry div,
    .st-emotion-cache-1u48l0g { 
        background-color: #0B2447 !important; /* Background input field jadi Deep Navy */
        color: #F0F0F0 !important; /* Teks di dalam input field jadi terang */
    }
    
    /* FIX AGGRESSIVE: Teks label di atas input field */
    label { 
        color: #A5D7E8 !important; /* Warna label input field jadi Biru Muda Cerah */
    }
    
    /* PERBAIKAN FINAL: CONTAINER DI TAB INPUT */
    .stTabs > div:first-child + div > div:first-child {
        background-color: #19376D; /* Warna kotak container input */
        padding: 30px; 
        border-radius: 12px;
        margin-top: 10px; 
        border: 1px solid #A5D7E8;
    }

    /* 🔥 PERBAIKAN TAB KRUSIAL (Warna Oranye) */
    .stTabs [aria-selected="true"] {
        /* Warna teks tab aktif */
        color: #F0F0F0 !important; 
        /* Tambahkan garis batas tipis cerah */
        border: 1px solid #FFB300 !important; 
        border-radius: 6px;
    }
    
    .stTabs [aria-selected="true"]::after {
        /* Garis bawah tab aktif (Warna Oranye) */
        background: #FFB300 !important; 
    }
    
    .stTabs [data-baseweb="tab"] {
        /* Pastikan tab tidak aktif punya border */
        border: 1px solid transparent; 
        border-radius: 6px;
    }
    
    /* STYLE UNTUK METRIK CUSTOM (GANTI st.metric) */
    .custom-metric-container {
        background-color: #19376D; 
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #A5D7E8;
        height: 100%;
    }
    
    .custom-metric-label {
        color: #F0F0F0;
        font-weight: bold;
        font-size: 1rem;
        margin-bottom: 5px;
    }
    
    /* 🔥 WARNA NILAI UTAMA BIRU MUDA */
    .custom-metric-value {
        color: #A5D7E8; /* Warna Nilai Utama JADI BIRU MUDA */
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.1;
    }
    
    /* 🔥 WARNA SUBTEKS PUTIH */
    .custom-metric-subtext {
        color: #F0F0F0; /* Subteks (Rujukan Usia/Status Gizi) JADI PUTIH */
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
</style>
""", unsafe_allow_html=True)

st.title("🧮NutriMatch : Kebutuhan Gizi yang Pas Buat Kamu🍳")
st.markdown("💡Aplikasi ini menggunakan **Interpolasi Polinomial Lagrange** untuk mengestimasi Angka Kecukupan Gizi (AKG) berdasarkan Berat Badan target (30 kg - 100 kg) dari data rujukan.")
st.markdown("---")

# ----------------------------------------------------------------------
# BAGIAN 1: FUNGSI UTAMA ESTIMASI LAGRANGE📈
# ----------------------------------------------------------------------
def Estimasi_AKG_Lagrange(X_Acuan, Y_Nilai_Gizi, BB_Target):
    n = len(X_Acuan)
    hasil_estimasi = 0.0
    
    if len(np.unique(X_Acuan)) < n:
        return 0.0

    for i in range(n):
        Basis_Li = 1.0
        for j in range(n):
            if i != j:
                Basis_Li *= (BB_Target - X_Acuan[j]) / (X_Acuan[i] - X_Acuan[j])
        hasil_estimasi += Y_Nilai_Gizi[i] * Basis_Li
    return hasil_estimasi

# ----------------------------------------------------------------------
# FUNGSI KLASIFIKASI BMI PALING INFORMATIF (MERAH, KUNING, HIJAU)
# ----------------------------------------------------------------------
def Klasifikasi_BMI_HTML(BMI, BB, TB):
    
    if BMI < 18.5:
        # Kurus: Merah
        status = "⚠️ Kurang (Underweight)"
        saran = f"BB {BB:.1f} kg, TB {TB:.1f} cm. **Waspada!** Status Gizi Kurang. Perlu peningkatan asupan energi dan protein."
        color_code = "#FF4B4B" # Merah
        bmi_key = 'Saran_Kurus'
    elif 18.5 <= BMI < 23.0:
        # Normal: Hijau
        status = "✅ Normal"
        saran = f"BB {BB:.1f} kg, TB {TB:.1f} cm. **Pertahankan!** Status Gizi Normal. Pola makan seimbang."
        color_code = "#00BFA6" # Hijau
        bmi_key = 'Saran_Normal'
    else: # BMI >= 23.0 (Gemuk/Obesitas)
        # Gemuk/Obesitas: Kuning/Merah
        if BMI < 25.0:
            status = "🟡 Gemuk (Overweight)"
            color_code = "#FFC82C" # Kuning
        else:
            status = "🚨 Obesitas"
            color_code = "#FF4B4B" # Merah
        
        saran = f"BB {BB:.1f} kg, TB {TB:.1f} cm. **Perhatian!** Status Gizi Berlebih. Perlu kontrol porsi dan batasi lemak/gula."
        bmi_key = 'Saran_Gemuk_Obesitas'
        
    return status, saran, color_code, bmi_key
    
# ----------------------------------------------------------------------
# FUNGSI CUSTOM METRIC (Pengganti st.metric)
# ----------------------------------------------------------------------
def custom_metric(label, value, subtext):
    # Menggunakan HTML/Markdown untuk kontrol warna total
    html_code = f"""
    <div class="custom-metric-container">
        <div class="custom-metric-label">{label}</div>
        <div class="custom-metric-value">{value}</div>
        <div class="custom-metric-subtext">{subtext}</div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# FUNGSI SARAN MAKANAN DINAMIS BARU (MEMASUKKAN LOGIKA BMI)
# ----------------------------------------------------------------------
def get_saran_makanan(Jenis_Gizi_Key, hasil_estimasi, Unit_Gizi, BMI_Saran_Subtext, Air_Rujukan, Serat_Rujukan, BMI_Key):
    saran = []
    
    saran.append(f"**Status Gizi (BMI):** {BMI_Saran_Subtext}")
    
    saran.append("---")
    
    # Ambil saran makro/mikro berdasarkan Jenis Gizi dan Status BMI
    saran_gizi_spesifik = Tabel_Saran_Makro_Mikro.get(Jenis_Gizi_Key, {}).get(BMI_Key, [f"Saran umum untuk {Jenis_Gizi_Key}."])[0]
    
    # 2. Saran Makro & Mikro Spesifik
    saran.append(f"**Target Utama Anda ({Jenis_Gizi_Key}):** {hasil_estimasi:.0f} {Unit_Gizi}. {saran_gizi_spesifik}")
    saran.append(f"**Target Air:** {Air_Rujukan} liter/hari. Pastikan minum air putih secara teratur, hindari minuman manis berlebihan.")
    saran.append(f"**Target Serat:** {Serat_Rujukan} g/hari. Konsumsi sayur dan buah minimal 5 porsi/hari dan pilih biji-bijian utuh (whole grain).")
    
    return saran

# ----------------------------------------------------------------------
# BAGIAN 2: SUMBER DATA AKG RUJUKAN📊
# ----------------------------------------------------------------------
Tabel_Kebutuhan_Air_Serat = {
    'Laki-laki (Remaja 10-20 th)': {'Air': 2.2, 'Serat': 32, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Laki-laki (Dewasa 21-60 th)': {'Air': 2.5, 'Serat': 37, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Laki-laki (Lansia 61-80+ th)': {'Air': 2.5, 'Serat': 30, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Perempuan (Remaja 10-20 th)': {'Air': 2.2, 'Serat': 26, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Perempuan (Dewasa 21-60 th)': {'Air': 2.5, 'Serat': 32, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Perempuan (Lansia 61-80+ th)': {'Air': 2.5, 'Serat': 25, 'unit_air': 'liter', 'unit_serat': 'g'},
}

# REVISI STRUKTUR SARAN MAKANAN BERDASARKAN BMI
Tabel_Saran_Makro_Mikro = {
    'Energi': {
        'Saran_Kurus': "Fokus pada makanan padat kalori tapi bernutrisi (avokad, kacang-kacangan, susu *full cream*). Konsumsi porsi lebih besar.",
        'Saran_Normal': "Jaga keseimbangan asupan kalori. Pilih karbohidrat kompleks (nasi merah, ubi) untuk energi stabil.",
        'Saran_Gemuk_Obesitas': "Kurangi makanan tinggi kalori, terutama yang mengandung gula dan lemak jenuh. Pilih porsi kecil dan makanan rendah GI."
    }, 
    'Protein': {
        'Saran_Kurus': "Tingkatkan konsumsi protein (daging, telur, ikan) untuk membantu pembentukan massa otot. Prioritaskan protein berkualitas tinggi.",
        'Saran_Normal': "Cukupi dengan daging tanpa lemak, telur, ikan, atau produk kedelai. Protein penting untuk perbaikan sel.",
        'Saran_Gemuk_Obesitas': "Pilih sumber protein rendah lemak (ikan, dada ayam tanpa kulit, tahu/tempe) untuk meningkatkan rasa kenyang dan menjaga massa otot selama defisit kalori."
    },
    'Lemak Total': {
        'Saran_Kurus': "Masukkan lemak sehat (alpukat, minyak zaitun, kacang-kacangan) untuk menambah kalori tanpa volume berlebihan.",
        'Saran_Normal': "Pilih lemak sehat tak jenuh (minyak zaitun, ikan salmon, biji-bijian). Batasi lemak jenuh dari gorengan.",
        'Saran_Gemuk_Obesitas': "Batasi asupan lemak total, terutama lemak jenuh dan trans (gorengan, makanan cepat saji). Utamakan lemak tak jenuh dalam jumlah minimal."
    },
    'Karbohidrat': {
        'Saran_Kurus': "Pilih karbohidrat kompleks dalam porsi besar. Sertakan buah-buahan dan sayuran bertepung.",
        'Saran_Normal': "Pilih sumber karbohidrat kompleks seperti nasi merah, oat, atau roti gandum utuh untuk energi berkelanjutan.",
        'Saran_Gemuk_Obesitas': "Pilih karbohidrat dengan indeks glikemik rendah dan tinggi serat (sayuran, kacang-kacangan). Kontrol porsi karbohidrat."
    },
    'Kalsium (Ca)': {
        'Saran_Kurus': "Konsumsi produk susu dan sayuran hijau. Kalsium penting, terutama jika asupan energi ditingkatkan.",
        'Saran_Normal': "Konsumsi susu, keju, yogurt, atau sayuran hijau gelap. Kalsium penting untuk kesehatan tulang dan gigi.",
        'Saran_Gemuk_Obesitas': "Pilih produk susu rendah lemak atau non-fat untuk memenuhi kebutuhan Kalsium tanpa menambah kalori berlebih."
    },
    'Besi (Fe)': {
        'Saran_Kurus': "Prioritaskan sumber zat Besi hewani (daging merah, hati) dan konsumsi dengan Vitamin C untuk penyerapan optimal.",
        'Saran_Normal': "Konsumsi daging merah, hati, bayam, atau kacang-kacangan. Konsumsi Vitamin C untuk membantu penyerapan Besi.",
        'Saran_Gemuk_Obesitas': "Pilih sumber Besi nabati atau hewani rendah lemak. Besi penting untuk transportasi oksigen."
    },
}

Tabel_Kebutuhan_Gizi_Rujukan = {
    'Laki-laki (Remaja 10-20 th)': {
        'Berat_Badan_Acuan_X': np.array([30.0, 36.0, 50.0, 75.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1750, 2000, 2400, 3000, 3600]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([45, 50, 70, 95, 120]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([55, 65, 80, 110, 140]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([270, 300, 350, 480, 600]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Kalsium (Ca)': {'data': np.array([1200, 1200, 1200, 1200, 1200]), 'unit': 'mg', 'desc': 'Kebutuhan Kalsium'},
            'Besi (Fe)': {'data': np.array([9, 10, 11, 11, 11]), 'unit': 'mg', 'desc': 'Kebutuhan Besi'},
        }
    },
    'Laki-laki (Dewasa 21-60 th)': {
        'Berat_Badan_Acuan_X': np.array([30.0, 60.0, 75.0, 90.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1900, 2477.5, 2900, 3200, 3400]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([50, 65, 85, 100, 110]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([60, 70, 95, 115, 130]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([280, 395, 470, 520, 560]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Kalsium (Ca)': {'data': np.array([1000, 1000, 1000, 1000, 1000]), 'unit': 'mg', 'desc': 'Kebutuhan Kalsium'},
            'Besi (Fe)': {'data': np.array([9, 9, 9, 9, 9]), 'unit': 'mg', 'desc': 'Kebutuhan Besi'},
        }
    },
    'Laki-laki (Lansia 61-80+ th)': {
        'Berat_Badan_Acuan_X': np.array([30.0, 55.0, 70.0, 85.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1500, 1900, 2200, 2500, 2800]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([50, 64, 75, 90, 105]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([40, 50, 70, 90, 110]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([220, 285, 330, 380, 430]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Kalsium (Ca)': {'data': np.array([1200, 1200, 1200, 1200, 1200]), 'unit': 'mg', 'desc': 'Kebutuhan Kalsium'},
            'Besi (Fe)': {'data': np.array([8, 9, 9, 9, 9]), 'unit': 'mg', 'desc': 'Kebutuhan Besi'},
        }
    },
    
    # B. PEREMPUAN
    'Perempuan (Remaja 10-20 th)': {
        'Berat_Badan_Acuan_X': np.array([30.0, 38.0, 52.0, 75.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1600, 1900, 2100, 2700, 3300]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([50, 55, 65, 90, 115]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([50, 65, 70, 100, 130]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([240, 280, 300, 420, 550]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Kalsium (Ca)': {'data': np.array([1200, 1200, 1200, 1200, 1200]), 'unit': 'mg', 'desc': 'Kebutuhan Kalsium'},
            'Besi (Fe)': {'data': np.array([13, 15, 15, 15, 15]), 'unit': 'mg', 'desc': 'Kebutuhan Besi'},
        }
    },
    'Perempuan (Dewasa 21-60 th)': {
        'Berat_Badan_Acuan_X': np.array([30.0, 55.0, 70.0, 85.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1700, 2250, 2500, 2800, 3100]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([50, 60, 75, 90, 105]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([50, 65, 80, 100, 120]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([260, 360, 410, 460, 510]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Kalsium (Ca)': {'data': np.array([1000, 1000, 1000, 1000, 1000]), 'unit': 'mg', 'desc': 'Kebutuhan Kalsium'},
            'Besi (Fe)': {'data': np.array([15, 18, 15, 15, 15]), 'unit': 'mg', 'desc': 'Kebutuhan Besi'},
        }
    },
    'Perempuan (Lansia 61-80+ th)': {
        'Berat_Badan_Acuan_X': np.array([30.0, 50.0, 75.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1300, 1600, 2000, 2400]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([45, 58, 70, 85]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([35, 45, 65, 85]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([200, 230, 300, 370]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Kalsium (Ca)': {'data': np.array([1200, 1200, 1200, 1200, 1200]), 'unit': 'mg', 'desc': 'Kebutuhan Kalsium'},
            'Besi (Fe)': {'data': np.array([8, 8, 8, 8]), 'unit': 'mg', 'desc': 'Kebutuhan Besi'},
        }
    },
}
# ----------------------------------------------------------------------
# BAGIAN 4: ANTARMUKA STREAMLIT
# ----------------------------------------------------------------------

# Konfigurasi Halaman 
st.set_page_config(
    page_title="Kalkulator AKG Lagrange",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inisialisasi session state
if 'hitung' not in st.session_state:
    st.session_state['hitung'] = False
if 'bb_target' not in st.session_state:
    st.session_state['bb_target'] = 60.0
if 'tb_val' not in st.session_state:
    st.session_state['tb_val'] = 160.0


# --- Buat Tab Interaktif ---
tab_input, tab_hasil, tab_metode = st.tabs(["1️⃣ Input Parameter", "2️⃣ Hasil Estimasi & Visualisasi", "3️⃣ Tentang Metode"])

# --- TAB 1: Input Parameter ---
with tab_input:
    st.header("Masukkan Profil dan Kebutuhan")
    
    col_gizi, col_bb, col_tb = st.columns(3)
    Kelompok_options = list(Tabel_Kebutuhan_Gizi_Rujukan.keys())

    with col_gizi:
        # 1. Kelompok Usia
        Kelompok_Populasi_Key = st.selectbox(
            '1. Kelompok Usia:',
            Kelompok_options,
            index=1,
            key='kelompok'
        )
        
        # 2. Jenis Gizi (Hanya gizi yang diinterpolasi)
        Gizi_options = list(Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Kebutuhan_Gizi'].keys())
        Jenis_Gizi_Key = st.selectbox(
            '2. Jenis Kebutuhan Gizi:',
            Gizi_options,
            index=0,
            key='gizi'
        )

    with col_bb:
        # 3. Berat Badan Target
        BB_Target_Val = st.number_input(
            '3. Berat Badan Target (kg):',
            min_value=30.0,
            max_value=100.0,
            value=st.session_state['bb_target'],
            step=0.1,
            format="%.1f",
            help="BB target antara 30.0 kg hingga 100.0 kg",
            key='bb_target'
        )
        
    with col_tb:
        # 4. Tinggi Badan
        TB_Val = st.number_input(
            '4. Tinggi Badan (cm):',
            min_value=100.0,
            max_value=220.0,
            value=st.session_state['tb_val'],
            step=1.0,
            format="%.1f",
            help="Masukkan Tinggi Badan untuk perhitungan BMI",
            key='tb_val'
        )
    
    st.markdown("---")
    
    # Tombol Hitung
    if st.button('HITUNG ESTIMASI GIZI SEKARANG 🎯', use_container_width=True, type="primary"):
        st.session_state['hitung'] = True
        st.info(f"Perhitungan {Jenis_Gizi_Key} Selesai! Silakan cek Tab 'Hasil Estimasi & Visualisasi'.")
        st.balloons()


# --- TAB 2: Logika Perhitungan & Output Utama ---
with tab_hasil:
    if st.session_state['hitung']:
        try:
            # Ambil nilai dari session state
            Kelompok_Populasi_Key = st.session_state['kelompok']
            Jenis_Gizi_Key = st.session_state['gizi']
            BB_Target_Val = st.session_state['bb_target']
            TB_Val = st.session_state['tb_val']

            # Ambil Data Lagrange Gizi yang Dipilih
            X_data_BB = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Berat_Badan_Acuan_X']
            Y_data_Gizi = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Kebutuhan_Gizi'][Jenis_Gizi_Key]['data']
            Unit_Gizi = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Kebutuhan_Gizi'][Jenis_Gizi_Key]['unit']
            Deskripsi_Gizi = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Kebutuhan_Gizi'][Jenis_Gizi_Key]['desc']
            
            # Ambil Data Air dan Serat
            Air_Rujukan = Tabel_Kebutuhan_Air_Serat[Kelompok_Populasi_Key]['Air']
            Serat_Rujukan = Tabel_Kebutuhan_Air_Serat[Kelompok_Populasi_Key]['Serat']
            Unit_Air = Tabel_Kebutuhan_Air_Serat[Kelompok_Populasi_Key]['unit_air']
            Unit_Serat = Tabel_Kebutuhan_Air_Serat[Kelompok_Populasi_Key]['unit_serat']
            
            # Estimasi Nilai Lagrange
            hasil_estimasi = Estimasi_AKG_Lagrange(X_data_BB, Y_data_Gizi, BB_Target_Val)
            
            # Hitung BMI
            TB_meter = TB_Val / 100
            BMI = BB_Target_Val / (TB_meter ** 2)
            
            # Klasifikasi BMI Kustom (MENDAPATKAN BMI_Key)
            BMI_Status, BMI_Saran_Subtext, BMI_Color_Code, BMI_Key = Klasifikasi_BMI_HTML(BMI, BB_Target_Val, TB_Val)

            st.header(f"Ringkasan Profil Gizi untuk {Kelompok_Populasi_Key}")

            # 🚨 IMPLEMENTASI CUSTOM METRIC (WARNA BIRU MUDA & PUTIH CERAH)
            col_bmi, col_air, col_serat = st.columns(3)
            
            with col_bmi:
                custom_metric(
                    label="Indeks Massa Tubuh (BMI)",
                    value=f"{BMI:.1f}",
                    subtext=f'<span style="color:{BMI_Color_Code}; font-weight:bold;">{BMI_Status}</span><br>{BMI_Saran_Subtext}'
                )
                
            with col_air:
                custom_metric(
                    label="Kebutuhan Air Harian",
                    value=f"{Air_Rujukan} {Unit_Air}",
                    subtext="💧 Rujukan Kelompok Usia"
                )
                
            with col_serat:
                custom_metric(
                    label="Kebutuhan Serat Harian",
                    value=f"{Serat_Rujukan} {Unit_Serat}",
                    subtext="🥦 Rujukan Kelompok Usia"
                )
            # 🚨 AKHIR IMPLEMENTASI CUSTOM METRIC
            
            st.markdown("---")
            
            # Tampilkan Hasil Utama Gizi Lagrange
            st.subheader(f"✅ HASIL ESTIMASI LAGRANGE: {Deskripsi_Gizi}")
            
            # Tampilkan hasil estimasi dalam kotak SUCCESS (PUTIH Pucat, Teks Hitam)
            st.success(f"Perkiraan kebutuhan **{Deskripsi_Gizi}** harian Anda pada Berat Badan **{BB_Target_Val:.1f} kg** adalah **{hasil_estimasi:.2f} {Unit_Gizi}**.")

            # Saran Makanan (Dinamis BMI)
            st.subheader("💡 Saran Gizi, Makanan & Minuman Harian Dinamis")
            saran_list = get_saran_makanan(Jenis_Gizi_Key, hasil_estimasi, Unit_Gizi, BMI_Saran_Subtext, Air_Rujukan, Serat_Rujukan, BMI_Key)
            
            for saran in saran_list:
                st.markdown(saran)
                
            st.markdown("---")

            # Analisis Data dan Visualisasi
            st.header("📈 Analisis Data dan Kurva Lagrange")
            col_data, col_viz = st.columns([1, 1])
            
            with col_data:
                st.subheader("1. Titik Data Rujukan AKG")
                df_data = pd.DataFrame({
                    f'Berat Badan Acuan (kg, X)': X_data_BB,
                    f'{Deskripsi_Gizi} Rujukan ({Unit_Gizi}, Y)': Y_data_Gizi
                })
                st.dataframe(df_data, use_container_width=True)
                
                # --- PENJELASAN TABEL LEBIH SPESIFIK ---
                st.markdown("**Interpretasi Tabel Rujukan:**")
                st.write(f"""
                Tabel ini menunjukkan **pasangan data rujukan resmi AKG** (Angka Kecukupan Gizi) untuk kelompok usia **{Kelompok_Populasi_Key}**. 
                * Kolom **X (Berat Badan Acuan)**: Merupakan titik-titik Berat Badan yang sudah ditetapkan dalam data AKG.
                * Kolom **Y ({Deskripsi_Gizi} Rujukan)**: Adalah kebutuhan gizi yang sesuai dengan masing-masing Berat Badan di kolom X.
                * Metode Interpolasi Lagrange menjamin **kurva estimasi akan melewati semua titik data** yang ada di tabel ini untuk memastikan akurasi model.
                """)
                # --- AKHIR PENJELASAN TABEL ---
                
            with col_viz:
                st.subheader("2. Kurva Estimasi Lagrange")
                
                # Visualisasi Plot Matplotlib
                min_BB = X_data_BB.min()
                max_BB = X_data_BB.max()
                X_plot = np.linspace(min_BB, max_BB, 100)
                Y_plot = [Estimasi_AKG_Lagrange(X_data_BB, Y_data_Gizi, x) for x in X_plot]
                
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.scatter(X_data_BB, Y_data_Gizi, color='#FFB300', s=100, label='Titik Data AKG Rujukan', zorder=5) 
                ax.plot(X_plot, Y_plot, color='#A5D7E8', linestyle='-', label='Kurva Model Estimasi Lagrange') 
                ax.scatter(BB_Target_Val, hasil_estimasi, color='#40A2E3', marker='X', s=250, label=f'Estimasi Target ({BB_Target_Val} kg)', zorder=6) 
                
                # Ubah warna background plot agar sesuai tema gelap
                ax.set_facecolor('#19376D') 
                fig.patch.set_facecolor('#19376D')
                ax.tick_params(colors='#F0F0F0')
                ax.xaxis.label.set_color('#F0F0F0')
                ax.yaxis.label.set_color('#F0F0F0')
                ax.title.set_color('#F0F0F0')
                
                ax.set_title(f"Estimasi {Deskripsi_Gizi} vs Berat Badan")
                ax.set_xlabel("Berat Badan (kg)")
                ax.set_ylabel(f"Kebutuhan Harian ({Unit_Gizi})")
                ax.grid(True, linestyle='--', alpha=0.3)
                ax.legend(facecolor='#19376D', labelcolor='#F0F0F0')
                
                st.pyplot(fig)
                
                # --- PENJELASAN GRAFIK LEBIH SPESIFIK ---
                st.markdown("**Interpretasi Kurva Lagrange:**")
                st.write(f"""
                1.  **Kurva Biru Muda (—)**: Ini adalah Kurva Polinomial Lagrange yang dibuat berdasarkan semua titik data di tabel. Kurva ini **menginterpolasi** (mengisi celah) antara titik-titik rujukan.
                2.  **Titik Kuning (•)**: Ini adalah Titik-Titik Data Rujukan AKG asli dari tabel. Perhatikan bahwa Kurva Lagrange **pasti melewati** titik-titik ini.
                3.  **Tanda X Biru Cerah (X)**: Ini adalah **Hasil Estimasi Anda** ({hasil_estimasi:.2f} {Unit_Gizi}) yang diprediksi oleh kurva Lagrange berdasarkan Berat Badan Target Anda ({BB_Target_Val:.1f} kg).
                """)
                # --- AKHIR PENJELASAN GRAFIK ---

                
        except Exception as e:
            st.error(f"❌ ERROR KRITIS: Terjadi Kesalahan Dalam Perhitungan. Pastikan semua input sudah valid. Detail Error: {e}")
            st.session_state['hitung'] = False
    else:
        st.warning("Tekan tombol **'HITUNG ESTIMASI GIZI SEKARANG 🎯'** di tab **Input Parameter** untuk memulai analisis.")
