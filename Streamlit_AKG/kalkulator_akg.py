import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

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
# BAGIAN 2: SUMBER DATA AKG RUJUKAN (DATA AKG 2019 DENGAN RENTANG USIA BARU)
# ----------------------------------------------------------------------
# Dewasa: 19-60 th
# Lansia: 61+ th

Tabel_Kebutuhan_Gizi_Rujukan = {
    # A. LAKI-LAKI
    'Laki-laki (Remaja 10-18 th)': {
        # BB acuan: 36, 50, 60, 75, 100 kg
        'Berat_Badan_Acuan_X': np.array([36.0, 50.0, 60.0, 75.0, 100.0]),
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([2000, 2400, 2650, 2900, 3400]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'},
            'Protein': {'data': np.array([50, 70, 75, 85, 110]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([65, 80, 85, 95, 130]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([300, 350, 400, 470, 560]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Serat': {'data': np.array([28, 34, 37, 37, 42]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
            'Air': {'data': np.array([1850, 2100, 2300, 2500, 2600]), 'unit': 'l', 'desc': 'Kebutuhan Air'},
        }
    },
    'Laki-laki (Dewasa 19-60 th)': { # NAMA KELOMPOK DEWASA BARU
        # BB acuan: 60, 75, 90, 100 kg
        'Berat_Badan_Acuan_X': np.array([60.0, 75.0, 90.0, 100.0]),
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([2550, 2800, 3100, 3400]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([65, 80, 95, 110]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([70, 85, 105, 130]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([415, 450, 500, 560]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Serat': {'data': np.array([36, 40, 43, 45]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
            'Air': {'data': np.array([2500, 2700, 2900, 3100]), 'unit': 'l', 'desc': 'Kebutuhan Air'},
        }
    },
    'Laki-laki (Lansia 61+ th)': { # NAMA KELOMPOK LANSIA BARU
        # BB acuan: 58, 70, 80, 90, 100 kg (Lebih detail di rentang BB rendah)
        'Berat_Badan_Acuan_X': np.array([58.0, 70.0, 80.0, 90.0, 100.0]),
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1800, 2000, 2200, 2350, 2550]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([64, 70, 78, 88, 100]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([50, 60, 70, 80, 95]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([275, 300, 320, 360, 400]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Serat': {'data': np.array([25, 27, 28, 30, 32]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
            'Air': {'data': np.array([1800, 1950, 2100, 2200, 2400]), 'unit': 'l', 'desc': 'Kebutuhan Air'},
        }
    },
    
    # B. PEREMPUAN
    'Perempuan (Remaja 10-18 th)': {
        # BB acuan: 38, 48, 52, 75, 100 kg
        'Berat_Badan_Acuan_X': np.array([38.0, 48.0, 52.0, 75.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1900, 2050, 2100, 2400, 2800]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'},
            'Protein': {'data': np.array([55, 65, 65, 80, 100]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([65, 70, 70, 90, 110]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([280, 300, 300, 380, 470]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Serat': {'data': np.array([27, 29, 29, 33, 38]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
            'Air': {'data': np.array([1850, 2100, 2150, 2300, 2500]), 'unit': 'l', 'desc': 'Kebutuhan Air'},
        }
    },
    'Perempuan (Dewasa 19-60 th)': { # NAMA KELOMPOK DEWASA BARU
        # BB acuan: 55, 75, 90, 100 kg
        'Berat_Badan_Acuan_X': np.array([55.0, 75.0, 90.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([2250, 2500, 2750, 3000]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'},
            'Protein': {'data': np.array([60, 70, 85, 100]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([65, 80, 95, 115]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([360, 400, 440, 480]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Serat': {'data': np.array([32, 35, 38, 41]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
            'Air': {'data': np.array([2350, 2550, 2750, 2950]), 'unit': 'l', 'desc': 'Kebutuhan Air'},
        }
    },
    'Perempuan (Lansia 61+ th)': { # NAMA KELOMPOK LANSIA BARU
        # BB acuan: 53, 65, 75, 90, 100 kg (Lebih detail di rentang BB rendah)
        'Berat_Badan_Acuan_X': np.array([53.0, 65.0, 75.0, 90.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1550, 1650, 1750, 1950, 2150]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([58, 62, 68, 80, 95]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([45, 50, 60, 75, 90]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([230, 250, 260, 290, 320]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Serat': {'data': np.array([22, 24, 25, 27, 29]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
            'Air': {'data': np.array([1550, 1600, 1700, 1850, 2000]), 'unit': 'l', 'desc': 'Kebutuhan Air'},
        }
    },
}

# ----------------------------------------------------------------------
# BAGIAN 3: ANTARMUKA STREAMLIT
# ----------------------------------------------------------------------

# Konfigurasi Halaman dan Judul
st.set_page_config(
    page_title="Kalkulator AKG Lagrange",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("⚙️ Kalkulator Estimasi Kebutuhan Gizi Harian (Metode Lagrange)")
st.markdown("Aplikasi ini menggunakan **Interpolasi Polinomial Lagrange** untuk mengestimasi Angka Kecukupan Gizi (AKG) **berdasarkan Berat Badan target**.")
st.markdown("---")

# --- 1. Input Parameter (Side Bar) ---
with st.sidebar:
    st.header("Input Parameter Estimasi")
    Kelompok_options = list(Tabel_Kebutuhan_Gizi_Rujukan.keys())

    # Dropdown Kelompok Usia
    Kelompok_Populasi_Key = st.selectbox(
        '1. Pilih Kelompok Usia:',
        Kelompok_options,
        index=2, # Default ke Dewasa Laki-laki
    )

    # Dropdown Jenis Gizi
    Gizi_options = list(Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Kebutuhan_Gizi'].keys())
    Jenis_Gizi_Key = st.selectbox(
        '2. Pilih Jenis Kebutuhan Gizi:',
        Gizi_options,
        index=0,
    )

    # Input Berat Badan Target
    BB_Target_Val = st.number_input(
        '3. Berat Badan Target (kg):',
        min_value=30.0,
        max_value=100.0,
        value=60.0,
        step=0.1,
        format="%.1f",
        help="Masukkan BB antara 30.0 kg hingga 100.0 kg"
    )

    # Input Tinggi Badan
    TB_Val = st.number_input(
        '4. Tinggi Badan (cm):',
        min_value=100.0,
        max_value=220.0,
        value=165.0, # Nilai default TB rata-rata
        step=0.1,
        format="%.1f",
        help="Masukkan Tinggi Badan dalam satuan cm."
    )
    st.markdown("---")
    
    # Tombol Hitung
    if st.button('Hitung Estimasi 🚀', use_container_width=True, type="primary"):
        st.session_state['hitung'] = True

# Inisialisasi session state
if 'hitung' not in st.session_state:
    st.session_state['hitung'] = False

# --- 2. Logika Perhitungan & Output Utama ---
if st.session_state['hitung']:
    try:
        # Ambil Data
        X_data_BB = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Berat_Badan_Acuan_X']
        Y_data_Gizi = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Kebutuhan_Gizi'][Jenis_Gizi_Key]['data']
        Unit_Gizi = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Kebutuhan_Gizi'][Jenis_Gizi_Key]['unit']
        Deskripsi_Gizi = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Kebutuhan_Gizi'][Jenis_Gizi_Key]['desc']
        
        # Estimasi Nilai Lagrange
        hasil_estimasi = Estimasi_AKG_Lagrange(X_data_BB, Y_data_Gizi, BB_Target_Val)

        st.header(f"Hasil Estimasi untuk {Kelompok_Populasi_Key}")

        # Tampilkan Hasil Utama
        col_res, col_info = st.columns([1, 2])
        
        with col_res:
             st.subheader(f"🎯 Kebutuhan {Jenis_Gizi_Key}")
             st.metric(
                label=f"BB Target {BB_Target_Val} kg (TB {TB_Val} cm)", 
                value=f"{hasil_estimasi:.2f} {Unit_Gizi}",
                delta=f"Basis: {X_data_BB.min()} - {X_data_BB.max()} kg",
                delta_color="off"
            )

        with col_info:
            st.info(f"Perkiraan kebutuhan **{Deskripsi_Gizi}** harian adalah **{hasil_estimasi:.2f} {Unit_Gizi}**.")

        # Logika IMT (Koreksi Tambahan)
        TB_meter = TB_Val / 100
        IMT = BB_Target_Val / (TB_meter ** 2)
        
        st.subheader("Pengecekan Indeks Massa Tubuh (IMT)")
        st.metric(label="IMT Anda", value=f"{IMT:.2f}")

        if IMT < 18.5:
            st.warning("⚠️ Status IMT Anda: **Kekurangan Berat Badan**.\nPerkiraan gizi ini dihitung berdasarkan target BB Anda. Disarankan konsultasi dengan ahli gizi untuk rencana penambahan berat badan yang aman.")
        elif IMT >= 18.5 and IMT < 25.0:
            st.success("✅ Status IMT Anda: **Normal**.\nPerkiraan gizi ini sesuai untuk BB dan TB ideal.")
        elif IMT >= 25.0 and IMT < 30.0:
            st.warning("🔶 Status IMT Anda: **Kelebihan Berat Badan (Pre-obesitas)**.\nPerkiraan gizi ini dihitung berdasarkan target BB Anda. Disarankan konsultasi dengan ahli gizi untuk rencana penurunan berat badan.")
        else:
            st.error("🛑 Status IMT Anda: **Obesitas**.\nPerkiraan gizi ini dihitung berdasarkan target BB Anda. **Sangat disarankan** konsultasi dengan ahli gizi dan dokter.")
        
        st.markdown("---")
        
        # Tampilkan Data Acuan dan Visualisasi
        colA, colB = st.columns([1, 1])
        
        with colA:
            st.subheader("Titik Data Rujukan AKG")
            df_data = pd.DataFrame({
                f'Berat Badan Acuan (kg, X)': X_data_BB,
                f'{Deskripsi_Gizi} Rujukan ({Unit_Gizi}, Y)': Y_data_Gizi
            })
            st.dataframe(df_data, use_container_width=True)
            
        with colB:
            st.subheader("Kurva Estimasi Lagrange")
            
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
            
    except Exception as e:
        st.error(f"❌ ERROR DALAM PERHITUNGAN: Terjadi Kesalahan: {e}")

