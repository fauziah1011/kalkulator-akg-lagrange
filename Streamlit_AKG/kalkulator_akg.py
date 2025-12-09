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
# BAGIAN 2: SUMBER DATA AKG RUJUKAN
# ----------------------------------------------------------------------
Tabel_Kebutuhan_Gizi_Rujukan = {
    # A. LAKI-LAKI
    'Laki-laki (Remaja 10-18 th)': {
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
    'Laki-laki (Dewasa 19-64 th)': {
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
    'Laki-laki (Lansia 65-80+ th)': {
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
    'Perempuan (Remaja 10-18 th)': {
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
    'Perempuan (Dewasa 19-64 th)': {
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
    'Perempuan (Lansia 65-80+ th)': {
        'Berat_Badan_Acuan_X': np.array([30.0, 50.0, 75.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1300, 1600, 2000, 2400]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([45, 58, 70, 85]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([35, 45, 65, 85]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([200, 230, 300, 370]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Kalsium (Ca)': {'data': np.array([1200, 1200, 1200, 1200]), 'unit': 'mg', 'desc': 'Kebutuhan Kalsium'},
            'Besi (Fe)': {'data': np.array([8, 8, 8, 8]), 'unit': 'mg', 'desc': 'Kebutuhan Besi'},
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
st.markdown("Aplikasi ini menggunakan **Interpolasi Polinomial Lagrange** untuk mengestimasi Angka Kecukupan Gizi (AKG) berdasarkan Berat Badan target (30 kg - 100 kg) dari data rujukan.")
st.markdown("---")

# --- 1. Input Parameter (Side Bar) ---
with st.sidebar:
    st.header("Input Parameter Estimasi")
    Kelompok_options = list(Tabel_Kebutuhan_Gizi_Rujukan.keys())

    # Dropdown Kelompok Usia
    Kelompok_Populasi_Key = st.selectbox(
        '1. Pilih Kelompok Usia:',
        Kelompok_options,
        index=1,
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
    st.markdown("---")
    
    # Tombol Hitung
    if st.button('Hitung Estimasi 🚀', use_container_width=True, type="primary"):
        # Menyimpan status hitung ke session state
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
        
        # Estimasi Nilai
        hasil_estimasi = Estimasi_AKG_Lagrange(X_data_BB, Y_data_Gizi, BB_Target_Val)

        st.header(f"Hasil Estimasi untuk {Kelompok_Populasi_Key}")

        # Tampilkan Hasil Utama
        col_res, col_info = st.columns([1, 2])
        
        with col_res:
             st.subheader(f"🎯 Kebutuhan {Jenis_Gizi_Key}")
             st.metric(
                label=f"BB Target {BB_Target_Val} kg", 
                value=f"{hasil_estimasi:.2f} {Unit_Gizi}",
                delta=f"Basis: {X_data_BB.min()} - {X_data_BB.max()} kg",
                delta_color="off"
            )

        with col_info:
            st.info(f"Perkiraan kebutuhan **{Deskripsi_Gizi}** harian adalah **{hasil_estimasi:.2f} {Unit_Gizi}**.")

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
