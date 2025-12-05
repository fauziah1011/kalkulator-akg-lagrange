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
    
    # Cek duplikasi nilai X (Berat Badan Acuan)
    if len(np.unique(X_Acuan)) < n:
        raise ValueError("Daftar Berat Badan Acuan (X) memiliki nilai ganda. Estimasi tidak dapat dilakukan.")
        
    # Rumus Interpolasi Lagrange
    for i in range(n):
        Basis_Li = 1.0
        for j in range(n):
            if i != j:
                Basis_Li *= (BB_Target - X_Acuan[j]) / (X_Acuan[i] - X_Acuan[j])
        hasil_estimasi += Y_Nilai_Gizi[i] * Basis_Li
    return hasil_estimasi

# ----------------------------------------------------------------------
# BAGIAN 2: SUMBER DATA AKG RUJUKAN (HANYA MAKRONUTRIEN + AIR)
# ----------------------------------------------------------------------

Tabel_Kebutuhan_Gizi_Rujukan = {
    # A. LAKI-LAKI
    'Laki-laki (Remaja 10-18 th)': {
        'Berat_Badan_Acuan_X': np.array([36.0, 50.0, 60.0, 75.0, 100.0]),
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([2000, 2400, 2650, 2900, 3400]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'},
            'Protein': {'data': np.array([50, 70, 75, 85, 110]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([65, 80, 85, 95, 130]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([300, 350, 400, 470, 560]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Serat': {'data': np.array([28, 34, 37, 37, 42]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
            'Air': {'data': np.array([1.85, 2.10, 2.30, 2.50, 2.60]), 'unit': 'L', 'desc': 'Kebutuhan Air'}, 
        }
    },
    'Laki-laki (Dewasa 19-60 th)': {
        'Berat_Badan_Acuan_X': np.array([60.0, 75.0, 90.0, 100.0]),
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([2550, 2800, 3100, 3400]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([65, 80, 95, 110]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([70, 85, 105, 130]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([415, 450, 500, 560]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Serat': {'data': np.array([36, 40, 43, 45]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
            'Air': {'data': np.array([2.50, 2.70, 2.90, 3.10]), 'unit': 'L', 'desc': 'Kebutuhan Air'}, 
        }
    },
    'Laki-laki (Lansia 61+ th)': {
        'Berat_Badan_Acuan_X': np.array([58.0, 70.0, 80.0, 90.0, 100.0]),
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1800, 2000, 2200, 2350, 2550]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([64, 70, 78, 88, 100]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([50, 60, 70, 80, 95]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([275, 300, 320, 360, 400]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Serat': {'data': np.array([25, 27, 28, 30, 32]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
            'Air': {'data': np.array([1.80, 1.95, 2.10, 2.20, 2.40]), 'unit': 'L', 'desc': 'Kebutuhan Air'}, 
        }
    },
    
    # B. PEREMPUAN
    'Perempuan (Remaja 10-18 th)': {
        'Berat_Badan_Acuan_X': np.array([38.0, 48.0, 52.0, 75.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1900, 2050, 2100, 2400, 2800]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'},
            'Protein': {'data': np.array([55, 65, 65, 80, 100]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([65, 70, 70, 90, 110]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([280, 300, 300, 380, 470]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Serat': {'data': np.array([27, 29, 29, 33, 38]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
            'Air': {'data': np.array([1.85, 2.10, 2.15, 2.30, 2.50]), 'unit': 'L', 'desc': 'Kebutuhan Air'},
        }
    },
    'Perempuan (Dewasa 19-60 th)': {
        'Berat_Badan_Acuan_X': np.array([55.0, 75.0, 90.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([2250, 2500, 2750, 3000]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'},
            'Protein': {'data': np.array([60, 70, 85, 100]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([65, 80, 95, 115]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([360, 400, 440, 480]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Serat': {'data': np.array([32, 35, 38, 41]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
            'Air': {'data': np.array([2.35, 2.55, 2.75, 2.95]), 'unit': 'L', 'desc': 'Kebutuhan Air'}, 
        }
    },
    'Perempuan (Lansia 61+ th)': {
        'Berat_Badan_Acuan_X': np.array([53.0, 65.0, 75.0, 90.0, 100.0]), 
        'Kebutuhan_Gizi': {
            'Energi': {'data': np.array([1550, 1650, 1750, 1950, 2150]), 'unit': 'kkal', 'desc': 'Kebutuhan Energi'}, 
            'Protein': {'data': np.array([58, 62, 68, 80, 95]), 'unit': 'g', 'desc': 'Kebutuhan Protein'},
            'Lemak Total': {'data': np.array([45, 50, 60, 75, 90]), 'unit': 'g', 'desc': 'Kebutuhan Lemak Total'},
            'Karbohidrat': {'data': np.array([230, 250, 260, 290, 320]), 'unit': 'g', 'desc': 'Kebutuhan Karbohidrat'},
            'Serat': {'data': np.array([22, 24, 25, 27, 29]), 'unit': 'g', 'desc': 'Kebutuhan Serat'},
            'Air': {'data': np.array([1.55, 1.60, 1.70, 1.85, 2.00]), 'unit': 'L', 'desc': 'Kebutuhan Air'}, 
        }
    },
}

# ----------------------------------------------------------------------
# BAGIAN 3: FUNGSI SARAN KONSUMSI BARU
# ----------------------------------------------------------------------
def Saran_Konsumsi(Jenis_Gizi_Key):
    """Memberikan saran makanan/minuman berdasarkan jenis gizi yang dipilih."""
    
    if Jenis_Gizi_Key == 'Energi':
        return """
        * **Sumber Utama Karbohidrat Kompleks (Energi Tahan Lama):** Nasi merah, ubi jalar, oatmeal, roti gandum utuh.
        * **Tambahkan Lemak Sehat:** Alpukat, kacang-kacangan (almond, kenari), minyak zaitun untuk memasak.
        """
    elif Jenis_Gizi_Key == 'Protein':
        return """
        * **Protein Hewani:** Daging tanpa lemak (dada ayam, ikan salmon), telur, produk susu rendah lemak (yogurt, keju).
        * **Protein Nabati:** Tahu, tempe, kacang-kacangan (lentil, buncis), *chia seeds*.
        """
    elif Jenis_Gizi_Key == 'Lemak Total':
        return """
        * **Pilih Lemak Tak Jenuh (Sehat):** Ikan berlemak (makarel, sarden), alpukat, biji-bijian, minyak zaitun/canola.
        * **Hindari Lemak Trans:** Makanan cepat saji, gorengan yang dipanaskan ulang, kue kering kemasan.
        """
    elif Jenis_Gizi_Key == 'Karbohidrat':
        return """
        * **Karbohidrat Kompleks (Utama):** Nasi cokelat/merah, sereal gandum utuh, pasta gandum, kentang.
        * **Hindari Gula Berlebihan:** Minuman manis, permen, dan makanan olahan tinggi gula.
        """
    elif Jenis_Gizi_Key == 'Serat':
        return """
        * **Buah dan Sayuran:** Apel (dengan kulit), pir, brokoli, wortel, sayuran hijau gelap.
        * **Biji-bijian dan Polong-polongan:** Kacang merah, kacang hijau, biji-bijian utuh, *flaxseed*.
        """
    elif Jenis_Gizi_Key == 'Air':
        return """
        * **Air Putih adalah Kunci:** Minum secara teratur, jangan tunggu haus.
        * **Sumber Hidrasi Lain:** Teh herbal tanpa gula, air kelapa, buah-buahan tinggi air (semangka, melon).
        """
    else:
        return "Tidak ada saran spesifik tersedia untuk jenis gizi ini."

# ----------------------------------------------------------------------
# BAGIAN 4: ANTARMUKA STREAMLIT
# ----------------------------------------------------------------------

# Konfigurasi Halaman dan Judul
st.set_page_config(
    page_title="Kalkulator AKG Makro Individual (Lagrange)",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("NutriMatch: Kebutuhan Gizi yang Pas Buat Kamu")
# REVISI TEKS MARKDOWN UTAMA
st.markdown("""
Aplikasi ini pakai metode Interpolasi Lagrange buat ngebantu kamu ngitung satu *kebutuhan gizi* secara akurat, sesuai usia dan target berat badan idealmu.
Mulai cek kebutuhan nutrisimu lewat menu di sidebar ya!
""")
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
    
    # Dropdown Jenis Gizi Individual
    Gizi_options = list(Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Kebutuhan_Gizi'].keys())
    Jenis_Gizi_Key = st.selectbox(
        '2. Pilih Jenis Kebutuhan Gizi:',
        Gizi_options,
        index=0, # Default ke Energi
    )
    st.markdown("---")

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
    
    # Fungsi yang dipanggil saat tombol ditekan
    def run_calculation():
        st.session_state['run_calculation'] = True
        
    # Tombol Hitung
    st.button(f'Hitung Estimasi {Jenis_Gizi_Key} 🚀', 
              on_click=run_calculation,
              use_container_width=True, 
              type="primary")

# Inisialisasi session state
if 'run_calculation' not in st.session_state:
    st.session_state['run_calculation'] = False

# --- 2. Logika Perhitungan & Output Utama ---

# Cek apakah status 'run_calculation' True
if st.session_state.get('run_calculation', False):
    try:
        # Ambil Data
        X_data_BB = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Berat_Badan_Acuan_X']
        data_gizi = Tabel_Kebutuhan_Gizi_Rujukan[Kelompok_Populasi_Key]['Kebutuhan_Gizi'][Jenis_Gizi_Key]
        
        Y_data_Gizi = data_gizi['data']
        Unit_Gizi = data_gizi['unit']
        Deskripsi_Gizi = data_gizi['desc']
        
        # Estimasi Nilai Lagrange
        hasil_estimasi = Estimasi_AKG_Lagrange(X_data_BB, Y_data_Gizi, BB_Target_Val)

        st.header(f"Hasil Estimasi **{Jenis_Gizi_Key}** untuk {Kelompok_Populasi_Key}")

        # --- Tampilkan Hasil Utama (Metrik) ---
        col_res, col_info = st.columns([1, 2])
        
        with col_res:
             st.subheader(f"🎯 Kebutuhan **{Jenis_Gizi_Key}**")
             st.metric(
                label=f"BB Target {BB_Target_Val} kg (TB {TB_Val} cm)", 
                value=f"{hasil_estimasi:.2f} {Unit_Gizi}",
                delta=f"Basis Acuan: {X_data_BB.min()} - {X_data_BB.max()} kg",
                delta_color="off"
            )

        with col_info:
            # REVISI TEKS MARKDOWN HASIL
            st.success(f"🎉 **SELAMAT!** Perkiraan kebutuhan **{Deskripsi_Gizi}** harian Anda adalah **{hasil_estimasi:.2f} {Unit_Gizi}**.")
            st.markdown("Angka ini adalah panduan personal untuk mencapai target kesehatan Anda. Ganti pilihan Anda di *sidebar* untuk eksplorasi nutrisi lainnya!")

        st.markdown("---")
        
        # ----------------------------------------------------------------------
        ## 💡 Saran Konsumsi Harian
        # ----------------------------------------------------------------------
        st.subheader(f"Saran Makanan & Minuman untuk Mencapai Target **{Jenis_Gizi_Key}**")
        st.markdown(Saran_Konsumsi(Jenis_Gizi_Key))
        st.markdown("---")
        
        # --- Pengecekan IMT ---
        st.subheader("Pengecekan Indeks Massa Tubuh (IMT)")
        TB_meter = TB_Val / 100
        IMT = BB_Target_Val / (TB_meter ** 2)
        
        st.metric(label="IMT Anda", value=f"{IMT:.2f}")

        if IMT < 18.5:
            st.warning("⚠️ Status IMT Anda: **Kekurangan Berat Badan**.")
        elif IMT >= 18.5 and IMT < 25.0:
            st.success("✅ Status IMT Anda: **Normal**.")
        elif IMT >= 25.0 and IMT < 30.0:
            st.warning("🔶 Status IMT Anda: **Kelebihan Berat Badan (Pre-obesitas)**.")
        else:
            st.error("🛑 Status IMT Anda: **Obesitas**.")
        
        st.info("Catatan: Estimasi AKG ini disesuaikan dengan Berat Badan target Anda.")
        
        st.markdown("---")
        
        # --- Tampilkan Data Acuan dan Visualisasi ---
        
        colA, colB = st.columns([1, 1])
        
        with colA:
            st.subheader("Tabel Data Rujukan AKG")
            df_data = pd.DataFrame({
                f'Berat Badan Acuan (kg, X)': X_data_BB,
                f'{Deskripsi_Gizi} Rujukan ({Unit_Gizi}, Y)': Y_data_Gizi
            })
            st.dataframe(df_data, use_container_width=True)
            
        with colB:
            st.subheader(f"Kurva Estimasi Lagrange: {Jenis_Gizi_Key}")
            
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
        st.error(f"❌ ERROR DALAM PERHITUNGAN: Terjadi Kesalahan: {e}. Pastikan data rujukan valid.")
        
    # Nonaktifkan status hitung untuk iterasi berikutnya (Penting untuk menghindari loop)
    st.session_state['run_calculation'] = False

