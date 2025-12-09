import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- CSS KUSTOM & TEMA (PERUBAHAN WARNA PEKAT) ---
st.markdown("""
<style>
    /* 1. Latar Belakang Utama Aplikasi (Tidak Putih Monoton) */
    .stApp {
        background-color: #F8F8F8; /* Abu-abu muda/krem lembut */
        color: #333333; /* Warna teks utama lebih pekat */
        font-family: 'Arial', sans-serif;
    }

    /* 2. Latar Belakang Sidebar (Kontras) */
    .st-emotion-cache-1ldfqsx { 
        background-color: #333333; /* Abu-abu gelap untuk sidebar */
    }

    /* 3. Warna Teks di Sidebar (Agar terbaca) */
    .st-emotion-cache-1ldfqsx label, .st-emotion-cache-1ldfqsx h2 {
        color: #FFFFFF !important; /* Teks putih di sidebar */
    }

    /* 4. Judul Utama (Lebih mencolok) */
    h1 {
        color: #1E8449; /* Hijau tua yang pekat */
        text-align: center;
        padding-bottom: 10px;
    }

    /* 5. Styling Kotak Output/Widget (Memberi bentuk) */
    .st-emotion-cache-h44nrf, .st-emotion-cache-12fm521 { 
        border-radius: 10px;
        box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2); /* Shadow lebih pekat */
        padding: 15px;
        background-color: #FFFFFF; /* Kontainer tetap putih agar mudah dibaca */
    }
    
    /* 6. Kotak Info & Success (Aksen Warna) */
    .st-emotion-cache-1mmpn3a, .st-emotion-cache-199v4c3 { /* Info/Success Box */
        background-color: #EBF5FB; /* Biru muda */
        border-left: 5px solid #3498DB; /* Garis biru pekat */
        padding: 10px;
        border-radius: 5px;
    }
    
    /* 7. Metric (Aksen Cepat) */
    .st-emotion-cache-14xtmhp {
        color: #D35400; /* Warna oranye untuk nilai metric */
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
# Data Air dan Serat
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
# BAGIAN 3: FUNGSI SARAN MAKANAN
# ----------------------------------------------------------------------
def get_saran_makanan(Jenis_Gizi_Key, hasil_estimasi):
    """Memberikan saran makanan/minuman berdasarkan jenis gizi yang diestimasi."""
    saran = []
    
    if Jenis_Gizi_Key == 'Energi':
        saran = [
            f"Untuk memenuhi {hasil_estimasi:.0f} kkal, perbanyak asupan karbohidrat kompleks (nasi, ubi, gandum).",
            "Sertakan makanan sumber energi padat seperti kacang-kacangan atau alpukat dalam porsi yang seimbang."
        ]
    elif Jenis_Gizi_Key == 'Protein':
        saran = [
            f"Target {hasil_estimasi:.0f} gram protein bisa dipenuhi dengan konsumsi daging tanpa lemak, telur, ikan, atau produk kedelai (tahu/tempe).",
            "Protein juga penting untuk pembentukan otot dan perbaikan sel."
        ]
    elif Jenis_Gizi_Key == 'Lemak Total':
        saran = [
            f"Pastikan {hasil_estimasi:.0f} gram lemak Anda didominasi lemak sehat (tak jenuh) seperti minyak zaitun, ikan salmon, atau biji-bijian.",
            "Batasi lemak jenuh dari gorengan atau makanan olahan."
        ]
    elif Jenis_Gizi_Key == 'Karbohidrat':
        saran = [
            f"Untuk {hasil_estimasi:.0f} gram karbohidrat, pilih sumber karbohidrat kompleks seperti nasi merah, oat, atau roti gandum utuh.",
            "Karbohidrat adalah sumber energi utama tubuh."
        ]
    elif Jenis_Gizi_Key == 'Kalsium (Ca)':
        saran = [
            f"Pastikan asupan kalsium mencapai {hasil_estimasi:.0f} mg dengan mengonsumsi susu, keju, yogurt, atau sayuran hijau gelap.",
            "Kalsium sangat penting untuk kesehatan tulang dan gigi."
        ]
    elif Jenis_Gizi_Key == 'Besi (Fe)':
        saran = [
            f"Untuk mencapai {hasil_estimasi:.0f} mg zat besi, konsumsi daging merah, hati, bayam, atau kacang-kacangan.",
            "Vitamin C membantu penyerapan zat besi!"
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
    if st.button('Hitung Estimasi Sekarang 🚀', use_container_width=True, type="primary"):
        st.session_state['hitung'] = True
        st.success("Perhitungan AKG Selesai! Silakan cek Tab 'Hasil Estimasi & Visualisasi'.")
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
            
            # Data Air dan Serat
            Air_Rujukan = Tabel_Kebutuhan_Air_Serat[Kelompok_Populasi_Key]['Air']
            Serat_Rujukan = Tabel_Kebutuhan_Air_Serat[Kelompok_Populasi_Key]['Serat']
            Unit_Air = Tabel_Kebutuhan_Air_Serat[Kelompok_Populasi_Key]['unit_air']
            Unit_Serat = Tabel_Kebutuhan_Air_Serat[Kelompok_Populasi_Key]['unit_serat']

            # Estimasi Nilai Lagrange
            hasil_estimasi = Estimasi_AKG_Lagrange(X_data_BB, Y_data_Gizi, BB_Target_Val)
            
            # Hitung BMI
            TB_meter = TB_Val / 100
            BMI = BB_Target_Val / (TB_meter ** 2)

            st.header(f"Ringkasan Hasil Estimasi AKG untuk {Kelompok_Populasi_Key}")

            # Tampilkan Hasil Utama (Metric)
            col_bmi, col_air, col_serat = st.columns(3)
            
            with col_bmi:
                st.metric(
                    label="Indeks Massa Tubuh (BMI)",
                    value=f"{BMI:.1f}",
                    delta=f"BB: {BB_Target_Val} kg, TB: {TB_Val} cm",
                    delta_color="off"
                )
                
            with col_air:
                st.metric(
                    label="Kebutuhan Air Harian",
                    value=f"{Air_Rujukan} {Unit_Air}",
                    delta="Berdasarkan Kelompok Usia",
                    delta_color="off"
                )
                
            with col_serat:
                st.metric(
                    label="Kebutuhan Serat Harian",
                    value=f"{Serat_Rujukan} {Unit_Serat}",
                    delta="Berdasarkan Kelompok Usia",
                    delta_color="off"
                )
                
            st.markdown("---")
            
            # Tampilkan Hasil Utama Gizi Lagrange
            st.subheader(f"🎯 Estimasi {Deskripsi_Gizi}")
            st.success(f"Perkiraan kebutuhan **{Deskripsi_Gizi}** harian Anda pada Berat Badan **{BB_Target_Val:.1f} kg** adalah **{hasil_estimasi:.2f} {Unit_Gizi}**.")

            # Saran Makanan
            st.subheader("💡 Saran Makanan dan Minuman")
            saran_list = get_saran_makanan(Jenis_Gizi_Key, hasil_estimasi)
            for saran in saran_list:
                st.markdown(f"* {saran}")
                
            st.markdown("---")

            # Analisis Data dan Visualisasi
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
                ax.scatter(X_data_BB, Y_data_Gizi, color='red', s=100, label='Titik Data AKG Rujukan', zorder=5)
                ax.plot(X_plot, Y_plot, color='blue', linestyle='-', label='Kurva Model Estimasi Lagrange')
                ax.scatter(BB_Target_Val, hasil_estimasi, color='green', marker='X', s=250, label=f'Estimasi Target ({BB_Target_Val} kg)', zorder=6)
                
                ax.set_title(f"Estimasi {Deskripsi_Gizi} vs Berat Badan")
                ax.set_xlabel("Berat Badan (kg)")
                ax.set_ylabel(f"Kebutuhan Harian ({Unit_Gizi})")
                ax.grid(True, linestyle='--', alpha=0.6)
                ax.legend()
                
                st.pyplot(fig)
                
                # Interpretasi Grafik
                st.markdown("**Interpretasi Grafik:**")
                st.write("Garis biru menunjukkan **Kurva Polinomial Lagrange** yang mulus. Kurva ini melewati semua Titik Data Rujukan (lingkaran merah) yang Anda masukkan.")
                st.write(f"Tanda **X hijau** menunjukkan hasil estimasi Anda: pada Berat Badan **{BB_Target_Val:.1f} kg**, kebutuhan Anda diproyeksikan berada tepat di atas kurva pada nilai **{hasil_estimasi:.2f} {Unit_Gizi}**.")

                
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
