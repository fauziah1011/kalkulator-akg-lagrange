import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- CSS KUSTOM & TEMA (PERUBAHAN WARNA PEKAT/BOLD) ---
st.markdown("""
<style>
    /* 1. Latar Belakang Utama Aplikasi (Kembali Putih agar Aksen Menjadi Bold) */
    .stApp {
        background-color: #FFFFFF; 
        color: #1A1A1A; /* Warna teks utama sangat pekat */
        font-family: 'Arial', sans-serif;
    }

    /* 2. Latar Belakang Sidebar (Kontras Gelap) */
    .st-emotion-cache-1ldfqsx { 
        background-color: #2C3E50; /* Biru Tua/Navy yang sangat pekat */
    }

    /* 3. Warna Teks di Sidebar (Agar terbaca) */
    .st-emotion-cache-1ldfqsx label, .st-emotion-cache-1ldfqsx h2 {
        color: #F8F8F8 !important; /* Teks putih di sidebar */
    }

    /* 4. Judul Utama (Sangat Mencolok) */
    h1 {
        color: #C0392B; /* Merah Marun/Bata yang pekat */
        text-align: center;
        padding-bottom: 10px;
    }
    
    /* 5. Subjudul & Header lainnya */
    h2, h3, h4 {
        color: #2980B9; /* Biru cerah yang pekat */
    }

    /* 6. Styling Kotak Output/Widget */
    .st-emotion-cache-h44nrf, .st-emotion-cache-12fm521 { 
        border-radius: 12px;
        box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.3); /* Shadow super pekat */
        padding: 20px;
        background-color: #FDFEFE; 
        border: 1px solid #BDC3C7;
    }
    
    /* 7. Kotak Success (Hasil Estimasi) */
    .st-emotion-cache-199v4c3 { /* Success Box */
        background-color: #F9EBEA; /* Latar Merah Muda Soft */
        border-left: 6px solid #E74C3C; /* Garis Merah Menyala */
        padding: 15px;
        border-radius: 8px;
        font-size: 18px;
    }
    
    /* 8. Metric (Nilai Angka Sangat Menonjol) */
    .st-emotion-cache-14xtmhp {
        color: #E67E22; /* Warna Oranye Terang untuk nilai metric */
        font-weight: 900; /* Extra Bold */
        font-size: 32px;
    }
    
    /* 9. Tombol Hitung */
    .st-emotion-cache-1cpx6a9 {
        background-color: #1ABC9C; /* Hijau Mint yang cerah */
        color: white;
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
    # Jika data rujukan hanya punya 1 nilai (seperti Air dan Serat), langsung kembalikan nilai itu.
    if len(Y_Nilai_Gizi) == 1:
        return Y_Nilai_Gizi[0]
        
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
# BAGIAN 2: SUMBER DATA AKG RUJUKAN (AIR DAN SERAT DIINTEGRASIKAN)
# ----------------------------------------------------------------------
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
            'Air': {'data': np.array([2.2]), 'unit': 'liter', 'desc': 'Kebutuhan Air'}, # Nilai tunggal
            'Serat': {'data': np.array([32]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},   # Nilai tunggal
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
            'Air': {'data': np.array([2.5]), 'unit': 'liter', 'desc': 'Kebutuhan Air'},   # Nilai tunggal
            'Serat': {'data': np.array([37]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},   # Nilai tunggal
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
            'Air': {'data': np.array([2.5]), 'unit': 'liter', 'desc': 'Kebutuhan Air'},   # Nilai tunggal
            'Serat': {'data': np.array([30]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},   # Nilai tunggal
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
            'Air': {'data': np.array([2.2]), 'unit': 'liter', 'desc': 'Kebutuhan Air'},   # Nilai tunggal
            'Serat': {'data': np.array([26]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},   # Nilai tunggal
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
            'Air': {'data': np.array([2.5]), 'unit': 'liter', 'desc': 'Kebutuhan Air'},   # Nilai tunggal
            'Serat': {'data': np.array([32]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},   # Nilai tunggal
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
            'Air': {'data': np.array([2.5]), 'unit': 'liter', 'desc': 'Kebutuhan Air'},   # Nilai tunggal
            'Serat': {'data': np.array([25]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},   # Nilai tunggal
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
            f"Untuk memenuhi {hasil_estimasi:.0f} {Unit_Gizi}, perbanyak asupan karbohidrat kompleks (nasi, ubi, gandum).",
            "Sertakan makanan sumber energi padat seperti kacang-kacangan atau alpukat dalam porsi yang seimbang."
        ]
    elif Jenis_Gizi_Key == 'Protein':
        saran = [
            f"Target {hasil_estimasi:.0f} {Unit_Gizi} protein bisa dipenuhi dengan konsumsi daging tanpa lemak, telur, ikan, atau produk kedelai (tahu/tempe).",
            "Protein juga penting untuk pembentukan otot dan perbaikan sel."
        ]
    elif Jenis_Gizi_Key == 'Lemak Total':
        saran = [
            f"Pastikan {hasil_estimasi:.0f} {Unit_Gizi} lemak Anda didominasi lemak sehat (tak jenuh) seperti minyak zaitun, ikan salmon, atau biji-bijian.",
            "Batasi lemak jenuh dari gorengan atau makanan olahan."
        ]
    elif Jenis_Gizi_Key == 'Karbohidrat':
        saran = [
            f"Untuk {hasil_estimasi:.0f} {Unit_Gizi} karbohidrat, pilih sumber karbohidrat kompleks seperti nasi merah, oat, atau roti gandum utuh.",
            "Karbohidrat adalah sumber energi utama tubuh."
        ]
    elif Jenis_Gizi_Key == 'Kalsium (Ca)':
        saran = [
            f"Pastikan asupan kalsium mencapai {hasil_estimasi:.0f} {Unit_Gizi} dengan mengonsumsi susu, keju, yogurt, atau sayuran hijau gelap.",
            "Kalsium sangat penting untuk kesehatan tulang dan gigi."
        ]
    elif Jenis_Gizi_Key == 'Besi (Fe)':
        saran = [
            f"Untuk mencapai {hasil_estimasi:.0f} {Unit_Gizi} zat besi, konsumsi daging merah, hati, bayam, atau kacang-kacangan.",
            "Vitamin C membantu penyerapan zat besi!"
        ]
    elif Jenis_Gizi_Key == 'Air':
        saran = [
            f"Kebutuhan air harian adalah {hasil_estimasi:.1f} {Unit_Gizi}. Pastikan Anda minum secara teratur sepanjang hari, tidak hanya saat haus.",
            "Air penting untuk semua fungsi tubuh, termasuk metabolisme dan regulasi suhu."
        ]
    elif Jenis_Gizi_Key == 'Serat':
        saran = [
            f"Target serat harian Anda adalah {hasil_estimasi:.0f} {Unit_Gizi}. Penuhi dengan buah-buahan, sayuran, dan biji-bijian utuh.",
            "Serat membantu melancarkan pencernaan dan mengontrol kadar gula darah."
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
        
        # 2. Jenis Gizi (Air & Serat termasuk di sini)
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
    if st.button('Hitung Estimasi Sekarang 🚀', use_container_width=True, type="primary"):
        st.session_state['hitung'] = True
        st.success(f"Perhitungan {Jenis_Gizi_Key} Selesai! Silakan cek Tab 'Hasil Estimasi & Visualisasi'.")
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
            
            # Estimasi Nilai Lagrange
            hasil_estimasi = Estimasi_AKG_Lagrange(X_data_BB, Y_data_Gizi, BB_Target_Val)
            
            # Hitung BMI
            TB_meter = TB_Val / 100
            BMI = BB_Target_Val / (TB_meter ** 2)

            st.header(f"Ringkasan Profil untuk {Kelompok_Populasi_Key}")

            # Tampilkan Hasil BMI (Metric)
            st.metric(
                label="Indeks Massa Tubuh (BMI)",
                value=f"{BMI:.1f}",
                delta=f"BB: {BB_Target_Val} kg, TB: {TB_Val} cm",
                delta_color="off"
            )
            
            st.markdown("---")
            
            # Tampilkan Hasil Utama Gizi Lagrange
            st.subheader(f"🎯 Estimasi {Deskripsi_Gizi}")
            
            if Jenis_Gizi_Key in ['Air', 'Serat']:
                 st.info(f"Kebutuhan **{Deskripsi_Gizi}** harian Anda (berdasarkan kelompok usia) adalah **{hasil_estimasi:.2f} {Unit_Gizi}**.")
            else:
                 st.success(f"Perkiraan kebutuhan **{Deskripsi_Gizi}** harian Anda pada Berat Badan **{BB_Target_Val:.1f} kg** adalah **{hasil_estimasi:.2f} {Unit_Gizi}**.")

            # Saran Makanan
            st.subheader("💡 Saran Makanan dan Minuman")
            saran_list = get_saran_makanan(Jenis_Gizi_Key, hasil_estimasi, Unit_Gizi)
            for saran in saran_list:
                st.markdown(f"* {saran}")
                
            st.markdown("---")

            # Analisis Data dan Visualisasi (Hanya tampilkan jika bukan Air/Serat)
            if Jenis_Gizi_Key not in ['Air', 'Serat']:
                st.header("📊 Analisis Data dan Kurva")
                col_data, col_viz = st.columns([1, 1])
                
                with col_data:
                    st.subheader("1. Titik Data Rujukan AKG")
                    df_data = pd.DataFrame({
                        f'Berat Badan Acuan (kg, X)': X_data_BB,
                        f'{Deskripsi_Gizi} Rujukan ({Unit_Gizi}, Y)': Y_data_Gizi
                    })
                    st.dataframe(df_data, use_container_width=True)
                    
                    # Interpretasi Tabel
                    st.markdown("**Interpretasi Tabel:**")
                    st.write(f"Tabel ini menunjukkan pasangan data yang digunakan sebagai input untuk interpolasi. Kolom X adalah Berat Badan acuan, dan Kolom Y adalah {Deskripsi_Gizi} yang diatur oleh pedoman AKG untuk {Kelompok_Populasi_Key}.")
                    st.write(f"Metode Lagrange menggunakan semua titik data ini untuk membuat kurva estimasi.")
                    
                with col_viz:
                    st.subheader("2. Kurva Estimasi Lagrange")
                    
                    # Visualisasi Plot Matplotlib
                    min_BB = X_data_BB.min()
                    max_BB = X_data_BB.max()
                    X_plot = np.linspace(min_BB, max_BB, 100)
                    Y_plot = [Estimasi_AKG_Lagrange(X_data_BB, Y_data_Gizi, x) for x in X_plot]
                    
                    fig, ax = plt.subplots(figsize=(8, 5))
                    ax.scatter(X_data_BB, Y_data_Gizi, color='#C0392B', s=100, label='Titik Data AKG Rujukan', zorder=5) # Merah Marun
                    ax.plot(X_plot, Y_plot, color='#2980B9', linestyle='-', label='Kurva Model Estimasi Lagrange') # Biru Pekat
                    ax.scatter(BB_Target_Val, hasil_estimasi, color='#1ABC9C', marker='X', s=250, label=f'Estimasi Target ({BB_Target_Val} kg)', zorder=6) # Hijau Mint
                    
                    ax.set_title(f"Estimasi {Deskripsi_Gizi} vs Berat Badan")
                    ax.set_xlabel("Berat Badan (kg)")
                    ax.set_ylabel(f"Kebutuhan Harian ({Unit_Gizi})")
                    ax.grid(True, linestyle='--', alpha=0.6)
                    ax.legend()
                    
                    st.pyplot(fig)
                    
                    # Interpretasi Grafik
                    st.markdown("**Interpretasi Grafik:**")
                    st.write("Garis biru menunjukkan **Kurva Polinomial Lagrange** yang mulus. Kurva ini melewati semua Titik Data Rujukan (lingkaran merah marun) yang Anda masukkan.")
                    st.write(f"Tanda **X hijau** menunjukkan hasil estimasi Anda: pada Berat Badan **{BB_Target_Val:.1f} kg**, kebutuhan Anda diproyeksikan berada tepat di atas kurva pada nilai **{hasil_estimasi:.2f} {Unit_Gizi}**.")
            else:
                 st.warning("Visualisasi kurva Lagrange tidak ditampilkan untuk Kebutuhan Air dan Serat karena nilainya adalah rujukan tetap berdasarkan kelompok usia, bukan hasil interpolasi berat badan.")

                
        except Exception as e:
            st.error(f"❌ ERROR DALAM PERHITUNGAN: Terjadi Kesalahan: {e}")
            st.session_state['hitung'] = False
    else:
        st.warning("Tekan tombol **'Hitung Estimasi Sekarang 🚀'** di tab **Input Parameter** untuk melihat hasil.")


# --- TAB 3: Tentang Metode ---
with tab_metode:
    st.header("🧠 Otak di Balik Akurasi: Metode Interpolasi Lagrange")
    st.info("Kalkulator ini menggunakan Interpolasi Lagrange, sebuah metode matematika canggih yang memungkinkan kita mengestimasi nilai Angka Kecukupan Gizi (AKG) yang sangat spesifik, bahkan untuk Berat Badan yang tidak tercantum langsung dalam tabel rujukan Kemenkes/WHO.")
    st.subheader("Konsep Matematis Polinomial Lagrange")
    st.latex(r"""
        P(x) = \sum_{j=0}^{n} y_j L_j(x)
    """)
    st.latex(r"""
        \text{dimana Basis Polinomial } L_j(x) = \prod_{i=0, i \neq j}^{n} \frac{x - x_i}{x_j - x_i}
    """)
