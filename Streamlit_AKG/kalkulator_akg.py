import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- CSS KUSTOM & TEMA (PERUBAHAN WARNA ULTRA BOLD/DARK) ---
st.markdown("""
<style>
    /* 1. Latar Belakang Utama Aplikasi (Gelap/Deep Blue untuk kesan tegas) */
    .stApp {
        background-color: #0B2447; /* Biru Tua Sangat Pekat (Deep Navy) */
        color: #F0F0F0; /* Warna teks utama terang */
        font-family: 'Georgia', serif; /* Font lebih variatif/serius */
    }

    /* 2. Latar Belakang Sidebar (Kontras Lebih Cerah) */
    .st-emotion-cache-1ldfqsx { 
        background-color: #19376D; /* Biru sedang pekat */
    }

    /* 3. Warna Teks di Sidebar */
    .st-emotion-cache-1ldfqsx label, .st-emotion-cache-1ldfqsx h2 {
        color: #F0F0F0 !important; /* Teks terang di sidebar */
    }

    /* 4. Judul Utama (Sangat Mencolok - Kuning Emas/Orange) */
    h1 {
        color: #FFB300; /* Kuning Emas/Amber Pekat */
        text-align: center;
        font-weight: 900;
        padding-bottom: 15px;
        border-bottom: 3px solid #FFB300;
    }
    
    /* 5. Subjudul & Header lainnya */
    h2, h3, h4 {
        color: #A5D7E8; /* Biru Muda Cerah/Kontras */
        font-weight: 700;
        border-left: 5px solid #A5D7E8;
        padding-left: 10px;
    }

    /* 6. Styling Kotak Output/Widget (Memberi bentuk) */
    .st-emotion-cache-h44nrf, .st-emotion-cache-12fm521 { 
        border-radius: 12px;
        box-shadow: 0px 8px 20px rgba(0, 0, 0, 0.5); /* Shadow sangat pekat */
        padding: 25px;
        background-color: #19376D; /* Background container lebih gelap dari main */
        color: #FFFFFF; /* Teks di container Putih */
        border: 1px solid #A5D7E8;
    }
    
    /* 7. Kotak Success (Hasil Estimasi) - Sangat Kontras */
    .st-emotion-cache-199v4c3 { /* Success Box */
        background-color: #40A2E3; /* Biru Terang Mencolok */
        border-left: 8px solid #000000; /* Garis Hitam Tegas */
        padding: 20px;
        border-radius: 10px;
        font-size: 20px;
        color: #000000; /* Teks Hitam di Success Box */
        font-weight: bold;
    }
    
    /* 8. Metric (Nilai Angka Sangat Menonjol) */
    .st-emotion-cache-14xtmhp {
        color: #FFD700; /* Warna Kuning Emas Murni */
        font-weight: 900; /* Extra Bold */
        font-size: 34px;
        text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.7);
    }
    
    /* 9. Tombol Hitung */
    .st-emotion-cache-1cpx6a9 {
        background-color: #40A2E3; /* Biru Cerah */
        color: #000000;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

st.title("🔥 GIZI ANTI RIBET: Kalkulator AKG Lagrange")
st.markdown("Aplikasi ini menggunakan **Interpolasi Polinomial Lagrange** untuk mengestimasi Angka Kecukupan Gizi (AKG) berdasarkan Berat Badan target (30 kg - 100 kg) dari data rujukan.")
st.markdown("---")

# ----------------------------------------------------------------------
# BAGIAN 1: FUNGSI UTAMA ESTIMASI LAGRANGE
# ----------------------------------------------------------------------
def Estimasi_AKG_Lagrange(X_Acuan, Y_Nilai_Gizi, BB_Target):
    """Melakukan estimasi Kebutuhan Gizi harian (Y) berdasarkan Berat Badan (X)
    menggunakan metode Interpolasi Polinomial Lagrange.
    """
    n = len(X_Acuan)
    hasil_estimasi = 0.0
    
    if len(np.unique(X_Acuan)) < n:
        st.error("Daftar Berat Badan Acuan (X) memiliki nilai ganda. Estimasi tidak dapat dilakukan.")
        return 0.0

    for i in range(n):
        Basis_Li = 1.0
        for j in range(n):
            if i != j:
                Basis_Li *= (BB_Target - X_Acuan[j]) / (X_Acuan[i] - X_Acuan[j])
        hasil_estimasi += Y_Nilai_Gizi[i] * Basis_Li
    return hasil_estimasi

# ----------------------------------------------------------------------
# BAGIAN 2: SUMBER DATA AKG RUJUKAN (BATASAN USIA DIPERBARUI)
# ----------------------------------------------------------------------
# Data Air dan Serat (Dipertahankan di sini untuk metrik terpisah, namun kami akan menghapusnya di tampilan hasil)
Tabel_Kebutuhan_Air_Serat = {
    'Laki-laki (Remaja 10-20 th)': {'Air': 2.2, 'Serat': 32, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Laki-laki (Dewasa 21-60 th)': {'Air': 2.5, 'Serat': 37, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Laki-laki (Lansia 61-80+ th)': {'Air': 2.5, 'Serat': 30, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Perempuan (Remaja 10-20 th)': {'Air': 2.2, 'Serat': 26, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Perempuan (Dewasa 21-60 th)': {'Air': 2.5, 'Serat': 32, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Perempuan (Lansia 61-80+ th)': {'Air': 2.5, 'Serat': 25, 'unit_air': 'liter', 'unit_serat': 'g'},
}

# Data AKG 
Tabel_Kebutuhan_Gizi_Rujukan = {
    # A. LAKI-LAKI
    'Laki-laki (Remaja 10-20 th)': {
        'Berat_Badan_Acuan_X': np.array([30.0, 36.0, 50.0, 75.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1750, 2000, 2400, 3000, 3600]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([45, 50, 70, 95, 120]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([55, 65, 80, 110, 140]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([270, 300, 350, 480, 600]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Kalsium (Ca)': {'data': np.array([1200, 1200, 1200, 1200, 1200]), 'unit': 'mg', 'desc': 'Kebutuhan Kalsium'},
            'Besi (Fe)': {'data': np.array([9, 10, 11, 11, 11]), 'unit': 'mg', 'desc': 'Kebutuhan Besi'},
            # Tambahkan Air dan Serat sebagai rujukan nilai tunggal agar bisa dipilih di dropdown
            'Air': {'data': np.array([2.2]), 'unit': 'liter', 'desc': 'Kebutuhan Air'}, 
            'Serat': {'data': np.array([32]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
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
            # Tambahkan Air dan Serat
            'Air': {'data': np.array([2.5]), 'unit': 'liter', 'desc': 'Kebutuhan Air'}, 
            'Serat': {'data': np.array([37]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
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
            # Tambahkan Air dan Serat
            'Air': {'data': np.array([2.5]), 'unit': 'liter', 'desc': 'Kebutuhan Air'}, 
            'Serat': {'data': np.array([30]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
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
            # Tambahkan Air dan Serat
            'Air': {'data': np.array([2.2]), 'unit': 'liter', 'desc': 'Kebutuhan Air'}, 
            'Serat': {'data': np.array([26]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
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
            # Tambahkan Air dan Serat
            'Air': {'data': np.array([2.5]), 'unit': 'liter', 'desc': 'Kebutuhan Air'}, 
            'Serat': {'data': np.array([32]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
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
            # Tambahkan Air dan Serat
            'Air': {'data': np.array([2.5]), 'unit': 'liter', 'desc': 'Kebutuhan Air'}, 
            'Serat': {'data': np.array([25]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
        }
    },
}
# ----------------------------------------------------------------------
# BAGIAN 3: FUNGSI SARAN MAKANAN
# ----------------------------------------------------------------------
def get_saran_makanan(Jenis_Gizi_Key, hasil_estimasi, Unit_Gizi):
    """Memberikan saran makanan/minuman berdasarkan jenis gizi yang diestimasi."""
    saran = []
    
    if Jenis_Gizi_Key == 'Energi':
        saran = [
            f"Untuk memenuhi **{hasil_estimasi:.0f} {Unit_Gizi}**, perbanyak asupan karbohidrat kompleks (nasi merah, ubi, gandum).",
            "Sertakan makanan sumber energi padat seperti kacang-kacangan atau alpukat dalam porsi yang seimbang. Energi adalah kunci performa harian."
        ]
    elif Jenis_Gizi_Key == 'Protein':
        saran = [
            f"Target **{hasil_estimasi:.0f} {Unit_Gizi}** protein bisa dipenuhi dengan konsumsi daging tanpa lemak, telur, ikan, atau produk kedelai (tahu/tempe).",
            "Protein sangat penting untuk pembentukan otot, perbaikan sel, dan kekebalan tubuh."
        ]
    elif Jenis_Gizi_Key == 'Lemak Total':
        saran = [
            f"Pastikan **{hasil_estimasi:.0f} {Unit_Gizi}** lemak Anda didominasi lemak sehat (tak jenuh) seperti minyak zaitun, ikan salmon, atau biji-bijian.",
            "Batasi lemak jenuh dari gorengan atau makanan olahan untuk menjaga kesehatan jantung."
        ]
    elif Jenis_Gizi_Key == 'Karbohidrat':
        saran = [
            f"Untuk **{hasil_estimasi:.0f} {Unit_Gizi}** karbohidrat, pilih sumber karbohidrat kompleks seperti nasi merah, oat, atau roti gandum utuh.",
            "Karbohidrat adalah sumber energi utama tubuh, pilih yang memiliki indeks glikemik rendah."
        ]
    elif Jenis_Gizi_Key == 'Kalsium (Ca)':
        saran = [
            f"Pastikan asupan kalsium mencapai **{hasil_estimasi:.0f} {Unit_Gizi}** dengan mengonsumsi susu, keju, yogurt, atau sayuran hijau gelap.",
            "Kalsium sangat penting untuk kesehatan tulang, gigi, dan fungsi saraf."
        ]
    elif Jenis_Gizi_Key == 'Besi (Fe)':
        saran = [
            f"Untuk mencapai **{hasil_estimasi:.0f} {Unit_Gizi}** zat besi, konsumsi daging merah, hati, bayam, atau kacang-kacangan.",
            "Penting untuk mencegah anemia dan meningkatkan transportasi oksigen dalam darah. Konsumsi Vitamin C untuk membantu penyerapan."
        ]
    elif Jenis_Gizi_Key == 'Air':
        saran = [
            f"Kebutuhan air harian adalah **{hasil_estimasi:.1f} {Unit_Gizi}**. Jangan tunggu haus, minumlah secara teratur sepanjang hari.",
            "Hidrasi yang cukup mendukung fungsi ginjal, metabolisme, dan menjaga elastisitas kulit."
        ]
    elif Jenis_Gizi_Key == 'Serat':
        saran = [
            f"Target serat harian Anda adalah **{hasil_estimasi:.0f} {Unit_Gizi}**. Penuhi dengan buah-buahan, sayuran, dan biji-bijian utuh.",
            "Serat membantu melancarkan pencernaan, menjaga kesehatan mikrobiota usus, dan mengontrol kadar gula darah."
        ]
    else:
        saran = ["Saran makanan umum: Konsumsi lima porsi buah dan sayur setiap hari, dan pertahankan pola makan seimbang."]

    return saran

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
        
        # 2. Jenis Gizi
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

            # Ambil Data Lagrange
            X_data_BB = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Berat_Badan_Acuan_X']
            Y_data_Gizi = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Kebutuhan_Gizi'][Jenis_Gizi_Key]['data']
            Unit_Gizi = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Kebutuhan_Gizi'][Jenis_Gizi_Key]['unit']
            Deskripsi_Gizi = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Kebutuhan_Gizi'][Jenis_Gizi_Key]['desc']
            
            # Estimasi Nilai Lagrange. Jika Air/Serat, np.array hanya berisi 1 nilai, hasilnya adalah nilai itu sendiri
            hasil_estimasi = Estimasi_AKG_Lagrange(X_data_BB, Y_data_Gizi, BB_Target_Val)
            
            # Hitung BMI
            TB_meter = TB_Val / 100
            BMI = BB_Target_Val / (TB_meter ** 2)

            st.header(f"Ringkasan Profil Gizi untuk {Kelompok_Populasi_Key}")

            # Tampilkan Hasil BMI (Metric) - Hanya 1 Metrik Utama
            st.metric(
                label="Indeks Massa Tubuh (BMI)",
                value=f"{BMI:.1f}",
                delta=f"BB: {BB_Target_Val} kg, TB: {TB_Val} cm",
                delta_color="off"
            )
            
            st.markdown("---")
            
            # Tampilkan Hasil Utama Gizi Lagrange
            st.subheader(f"✅ HASIL ESTIMASI: {Deskripsi_Gizi}")
            
            # Tampilkan hasil estimasi dalam kotak SUCCESS
            st.success(f"Perkiraan kebutuhan **{Deskripsi_Gizi}** harian Anda adalah **{hasil_estimasi:.2f} {Unit_Gizi}**.")

            # Saran Makanan
            st.subheader("💡 Saran Makanan Harian")
            saran_list = get_saran_makanan(Jenis_Gizi_Key, hasil_estimasi, Unit_Gizi)
            for saran in saran_list:
                st.markdown(f"**-** {saran}")
                
            st.markdown("---")

            # Analisis Data dan Visualisasi (Hanya tampilkan jika bukan Air/Serat)
            if Jenis_Gizi_Key not in ['Air', 'Serat']:
                st.header("📈 Analisis Data dan Kurva Lagrange")
                col_data, col_viz = st.columns([1, 1])
                
                with col_data:
                    st.subheader("1. Titik Data Rujukan AKG")
                    df_data = pd.DataFrame({
                        f'Berat Badan Acuan (kg, X)': X_data_BB,
                        f'{Deskripsi_Gizi} Rujukan ({Unit_Gizi}, Y)': Y_data_Gizi
                    })
                    st.dataframe(df_data, use_container_width=True)
                    
                    st.markdown("**Interpretasi Tabel:**")
                    st.write("Tabel ini menunjukkan pasangan data yang digunakan sebagai input untuk interpolasi Lagrange. Metode ini menjamin kurva estimasi melewati semua titik rujukan ini.")
                    
                with col_viz:
                    st.subheader("2. Kurva Estimasi Lagrange")
                    
                    # Visualisasi Plot Matplotlib
                    min_BB = X_data_BB.min()
                    max_BB = X_data_BB.max()
                    X_plot = np.linspace(min_BB, max_BB, 100)
                    Y_plot = [Estimasi_AKG_Lagrange(X_data_BB, Y_data_Gizi, x) for x in X_plot]
                    
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.scatter(X_data_BB, Y_data_Gizi, color='#FFB300', s=100, label='Titik Data AKG Rujukan', zorder=5) # Kuning Emas
                    ax.plot(X_plot, Y_plot, color='#A5D7E8', linestyle='-', label='Kurva Model Estimasi Lagrange') # Biru Muda Cerah
                    ax.scatter(BB_Target_Val, hasil_estimasi, color='#40A2E3', marker='X', s=250, label=f'Estimasi Target ({BB_Target_Val} kg)', zorder=6) # Biru Terang
                    
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
                    
                    # Interpretasi Grafik
                    st.markdown("**Interpretasi Grafik:**")
                    st.write("Garis (Kurva Polinomial Lagrange) mewakili estimasi kebutuhan gizi untuk rentang berat badan. Titik **X biru terang** adalah hasil estimasi spesifik Anda.")
            else:
                 st.info("Visualisasi kurva Lagrange tidak ditampilkan untuk Kebutuhan Air dan Serat karena nilainya adalah rujukan tetap berdasarkan kelompok usia, bukan hasil interpolasi berat badan.")

                
        except Exception as e:
            st.error(f"❌ ERROR KRITIS: Terjadi Kesalahan Dalam Perhitungan: {e}")
            st.session_state['hitung'] = False
    else:
        st.warning("Tekan tombol **'HITUNG ESTIMASI GIZI SEKARANG 🎯'** di tab **Input Parameter** untuk memulai analisis.")


# --- TAB 3: Tentang Metode ---
with tab_metode:
    st.header("🧠 Otak di Balik Akurasi: Metode Interpolasi Lagrange")
    st.info("Kalkulator ini menggunakan Interpolasi Lagrange, sebuah metode matematika canggih yang memungkinkan kita mengestimasi nilai Angka Kecukupan Gizi (AKG) yang sangat spesifik.")
    st.subheader("Konsep Matematis Polinomial Lagrange")
    st.latex(r"""
        P(x) = \sum_{j=0}^{n} y_j L_j(x)
    """)
    st.latex(r"""
        \text{dimana Basis Polinomial } L_j(x) = \prod_{i=0, i \neq j}^{n} \frac{x - x_i}{x_j - x_i}
    """)
