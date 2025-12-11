import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- CSS KUSTOM & TEMA (TETAP SAMA) ---
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
    
    /* Teks di Sidebar */
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
    
    /* KOTAK SUCCESS (st.success) -> PUTIH TEKS HITAM */
    .st-emotion-cache-199v4c3 { 
        background-color: #f7f3e8; /* Background Putih Pucat (Off-White) */
        border-left: 8px solid #FFB300; /* Garis samping Kuning Emas */
        font-weight: bold;
    }
    
    .st-emotion-cache-199v4c3 p {
        color: #000000 !important; /* Teks di st.success menjadi HITAM */
        font-weight: bold !important;
    }
    
    /* BACKGROUND KOTAK INPUT */
    [data-baseweb="select"] div:first-child,
    [data-baseweb="input"] input,
    .st-emotion-cache-1y4pm5r div, 
    .st-emotion-cache-15tx6ry div,
    .st.emotion-cache-1u48l0g { 
        background-color: #0B2447 !important; /* Background input field jadi Deep Navy */
        color: #F0F0F0 !important; /* Teks di dalam input field jadi terang */
    }
    
    /* Teks label di atas input field */
    label { 
        color: #A5D7E8 !important; /* Warna label input field jadi Biru Muda Cerah */
    }
    
    /* CONTAINER DI TAB INPUT */
    .stTabs > div:first-child + div > div:first-child {
        background-color: #19376D; /* Warna kotak container input */
        padding: 30px; 
        border-radius: 12px;
        margin-top: 10px; 
        border: 1px solid #A5D7E8;
    }

    /* TAB KRUSIAL (Warna Oranye) */
    .stTabs [aria-selected="true"] {
        /* Warna teks tab aktif */
        color: #FFB300 !important; /* <--- Warna teks saat aktif */
        /* Tambahkan garis batas tipis cerah */
        border: 1px solid #FFB300 !important; 
        border-radius: 6px;
    }
    
    .stTabs [aria-selected="true"]::after {
        /* Garis bawah tab aktif (Warna Oranye) */
        background: #FFB300 !important; 
    }
    
    .stTabs [data-baseweb="tab"] {
        /* Warna teks tab tidak aktif */
        color: #FFFFFF !important; /* <--- Warna teks saat tidak aktif */
        /* Pastikan tab tidak aktif punya border */
        border: 1px solid transparent; 
        border-radius: 6px;
    }
    
    /* STYLE UNTUK METRIK CUSTOM */
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
    
    /* WARNA NILAI UTAMA BIRU MUDA */
    .custom-metric-value {
        color: #A5D7E8; /* Warna Nilai Utama JADI BIRU MUDA */
        font-size: 2.2rem;
        font-weight: 700;
        line-height: 1.1;
    }
    
    /* WARNA SUBTEKS PUTIH */
    .custom-metric-subtext {
        color: #F0F0F0; /* Subteks (Rujukan Usia/Status Gizi) JADI PUTIH */
        font-size: 0.9rem;
        margin-top: 5px;
    }
    
    /* WARNA TOMBOL PRIMARY JADI HIJAU (UNTUK TOMBOL HITUNG) */
    .stButton > button {
        background-color: #00BFA6; 
        color: #000000; /* Teks Hitam */
        border: 2px solid #00BFA6;
    }
    
</style>
""", unsafe_allow_html=True)

st.title("🧮NutriMatch : Kebutuhan Gizi yang Pas Buat Kamu🍳")
st.markdown("💡Aplikasi ini menggunakan **Interpolasi Polinomial Lagrange** untuk mengestimasi Angka Kecukupan Gizi (AKG) berdasarkan **Berat Badan Target** dari data rujukan.")
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
# FUNGSI KLASIFIKASI BMI
# ----------------------------------------------------------------------
def Klasifikasi_BMI_HTML(BMI, BB, TB):
    
    if BMI < 18.5:
        status = "⚠️ Kurang (Underweight)"
        saran = f"BB Awal {BB:.1f} kg, TB {TB:.1f} cm. **Waspada!** Status Gizi Kurang."
        color_code = "#FF4B4B" # Merah
        bmi_key = 'Saran_Kurus'
    elif 18.5 <= BMI < 23.0:
        status = "✅ Normal"
        saran = f"BB Awal {BB:.1f} kg, TB {TB:.1f} cm. **Pertahankan!** Status Gizi Normal."
        color_code = "#00BFA6" # Hijau
        bmi_key = 'Saran_Normal'
    else:
        if BMI < 25.0:
            status = "🟡 Gemuk (Overweight)"
            color_code = "#FFC82C" # Kuning
        else:
            status = "🚨 Obesitas"
            color_code = "#FF4B4B" # Merah
        
        saran = f"BB Awal {BB:.1f} kg, TB {TB:.1f} cm. **Perhatian!** Status Gizi Berlebih."
        bmi_key = 'Saran_Gemuk_Obesitas'
        
    return status, saran, color_code, bmi_key
    
# ----------------------------------------------------------------------
# FUNGSI CUSTOM METRIC
# ----------------------------------------------------------------------
def custom_metric(label, value, subtext):
    html_code = f"""
    <div class="custom-metric-container">
        <div class="custom-metric-label">{label}</div>
        <div class="custom-metric-value">{value}</div>
        <div class="custom-metric-subtext">{subtext}</div>
    </div>
    """
    st.markdown(html_code, unsafe_allow_html=True)

# ----------------------------------------------------------------------
# FUNGSI SARAN MAKANAN DINAMIS (MEMASUKKAN TUJUAN BB - BAHASA SANTAI)
# ----------------------------------------------------------------------
def get_saran_makanan(Jenis_Gizi_Key, hasil_estimasi, Unit_Gizi, BB_Awal, BB_Target):
    saran = []
    saran_data = Tabel_Saran_Makro_Mikro.get(Jenis_Gizi_Key, {})
    
    # Menentukan Tujuan Berat Badan (Menggunakan Bahasa Santai)
    if BB_Target > BB_Awal + 0.5:
        Tujuan_Key = 'Saran_Naik'
        Tujuan_Goal = "Makan Lebih Banyak Kalori (Surplus) dari Kebutuhan Energi Harian."
        Tujuan_Text = f"Anda bertujuan **MENAIKKAN** BB dari {BB_Awal:.1f} kg menjadi {BB_Target:.1f} kg."
    elif BB_Target < BB_Awal - 0.5:
        Tujuan_Key = 'Saran_Turun'
        Tujuan_Goal = "Makan Lebih Hemat Kalori (Defisit) dari Kebutuhan Energi Harian."
        Tujuan_Text = f"Anda bertujuan **MENURUNKAN** BB dari {BB_Awal:.1f} kg menjadi {BB_Target:.1f} kg."
    else:
        Tujuan_Key = 'Saran_Jaga'
        Tujuan_Goal = "Jaga Kalori Tetap Stabil sesuai Kebutuhan Energi Harian."
        Tujuan_Text = f"Anda bertujuan **MEMPERTAHANKAN** BB di sekitar {BB_Target:.1f} kg."
        
    # --- BAGIAN 1: TARGET GIZI UTAMA & TUJUAN BB ---
    saran.append(f"### 🎯 Kebutuhan Harian **{Jenis_Gizi_Key}** (untuk BB Target {BB_Target:.1f} kg): {hasil_estimasi:.0f} {Unit_Gizi}")
    saran.append(f"**Tujuan Besar Anda:** {Tujuan_Text}")
    saran.append(f"**Strategi Utama Energi:** {Tujuan_Goal}")
    saran.append("---")
    
    # --- BAGIAN 2: STRATEGI UTAMA BERDASARKAN TUJUAN BB ---
    saran.append(f"### Strategi Gizi Khusus ({Jenis_Gizi_Key})")
    
    # TINGKATKAN/JAGA
    tingkatkan_jaga = saran_data.get(Tujuan_Key, {}).get('Tingkatkan/Jaga', "Informasi strategi peningkatan belum tersedia.")
    saran.append(f"**⬆️ FOKUS TINGKATKAN / JAGA:**")
    # Tampilkan sebagai list yang mudah dibaca
    for item in tingkatkan_jaga.split(';'):
        saran.append(f"* {item.strip()}")
    
    # KURANGI/BATASI
    kurangi_batasi = saran_data.get(Tujuan_Key, {}).get('Kurangi/Batasi', "Informasi strategi pembatasan belum tersedia.")
    saran.append(f"**⬇️ FOKUS KURANGI / BATASI:**")
    for item in kurangi_batasi.split(';'):
        saran.append(f"* {item.strip()}")
    
    saran.append("---")
    
    # --- BAGIAN 3: CONTOH PRAKTIS & PELENGKAP ---
    saran.append(f"### Contoh Praktis & Pelengkap Harian")
    
    # CONTOH PRAKTIS SPESIFIK
    contoh_praktis = saran_data.get(Tujuan_Key, {}).get('Contoh Praktis', "Contoh makanan spesifik belum tersedia.")
    saran.append(f"**🍽️ SUBSTITUSI / OPSI MENU YANG GAMPANG DICOBA:**")
    for item in contoh_praktis.split(';'):
        saran.append(f"* {item.strip()}")
    saran.append("") # Baris kosong

    # Saran Air dan Serat (Rujukan Tetap)
    Air_Rujukan = Tabel_Kebutuhan_Air_Serat[st.session_state['kelompok']]['Air']
    Serat_Rujukan = Tabel_Kebutuhan_Air_Serat[st.session_state['kelompok']]['Serat']
    saran.append(f"**💧 Air:** Target **{Air_Rujukan} liter/hari**. Jangan tunggu haus untuk minum!")
    saran.append(f"**🥦 Serat:** Target **{Serat_Rujukan} g/hari**. Pastikan ada sayur dan buah di setiap piring Anda.")
    
    return saran

# ----------------------------------------------------------------------
# BAGIAN 3: SUMBER DATA AKG RUJUKAN📊 & SARAN VARIATIF (BAHASA SANTAI)
# ----------------------------------------------------------------------
Tabel_Kebutuhan_Air_Serat = {
    'Laki-laki (Remaja 10-20 th)': {'Air': 2.2, 'Serat': 32, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Laki-laki (Dewasa 21-60 th)': {'Air': 2.5, 'Serat': 37, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Laki-laki (Lansia 61-80+ th)': {'Air': 2.5, 'Serat': 30, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Perempuan (Remaja 10-20 th)': {'Air': 2.2, 'Serat': 26, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Perempuan (Dewasa 21-60 th)': {'Air': 2.5, 'Serat': 32, 'unit_air': 'liter', 'unit_serat': 'g'},
    'Perempuan (Lansia 61-80+ th)': {'Air': 2.5, 'Serat': 25, 'unit_air': 'liter', 'unit_serat': 'g'},
}

# STRUKTUR SARAN MAKANAN BERDASARKAN TUJUAN BB (Naik, Turun, Jaga)
Tabel_Saran_Makro_Mikro = {
    'Energi': {
        'Saran_Naik': {
            'Tingkatkan/Jaga': "Asupan kalori total (makan lebih banyak); Fokus pada makanan padat gizi tinggi kalori seperti alpukat, kacang-kacangan; Makan porsi lebih sering atau lebih besar; Tambahkan sumber lemak sehat seperti 1 sendok makan minyak zaitun di makanan.",
            'Kurangi/Batasi': "Minuman rendah kalori atau diet; Porsi sayuran yang terlalu besar (karena cepat membuat kenyang) sebelum makan utama.",
            'Contoh Praktis': "Tambahkan *topping* keju, alpukat, atau *nut butter* pada roti/bubur; Minum susu *full cream* atau *smoothie* buah + kacang di sela waktu makan; Jangan lewatkan waktu makan utama."
        }, 
        'Saran_Turun': {
            'Tingkatkan/Jaga': "Makan lebih sedikit kalori (Makan Lebih Hemat Kalori); Fokus pada makanan yang tinggi serat dan banyak air (seperti 1 mangkuk sayur dan 1 buah apel); Minum air putih yang cukup (sekitar 2.5 liter).",
            'Kurangi/Batasi': "Gula tambahan (permen, minuman kemasan manis); Makanan yang diolah dengan cara digoreng (*deep fried*); Porsi Karbohidrat sederhana seperti nasi putih/mie instan (batasi jadi 1 porsi kecil).",
            'Contoh Praktis': "Pilih *snack* protein rendah lemak (1 butir telur rebus, *yogurt plain*); Ganti nasi biasa dengan nasi merah/shirataki/sayuran rebus; Olah makanan dengan metode rebus/kukus/panggang."
        }
    }, 
    'Protein': {
        'Saran_Naik': {
            'Tingkatkan/Jaga': "Protein berkualitas tinggi di setiap sesi makan untuk membantu membangun massa otot (jika diiringi latihan beban); Konsumsi protein dari berbagai sumber (misalnya, 100g dada ayam dan 1 potong tempe per hari).",
            'Kurangi/Batasi': "Protein yang digoreng atau diolah dengan krim/santan yang tinggi kalori; Sumber protein yang terlalu tinggi serat dan membuat cepat kenyang (seperti kacang-kacangan besar).",
            'Contoh Praktis': "Makan 100g dada ayam/ikan atau 2 butir telur per porsi makan; Minum protein shake (whey/kedelai) sebagai camilan; Tambahkan kacang-kacangan seperti almond/mete dalam bubur/sereal."
        },
        'Saran_Turun': {
            'Tingkatkan/Jaga': "Protein tinggi dan rendah lemak; Ini sangat penting untuk menjaga massa otot saat kalori sedang dibatasi; Pilih metode masak yang tidak menggunakan minyak banyak (misal, 1 potong ikan bakar).",
            'Kurangi/Batasi': "Potongan daging berlemak tinggi (sapi berlemak/kulit ayam); Produk olahan seperti sosis, *bacon*, atau *nugget* yang digoreng (maksimal 1 potong kecil per hari).",
            'Contoh Praktis': "Pilih ikan (tuna/bandeng), tahu/tempe, atau ayam tanpa kulit; Pilih *low fat yogurt* atau susu *skim*; Masak dengan cara dipanggang, direbus, atau dikukus."
        },
        'Saran_Jaga': {
            'Tingkatkan/Jaga': "Sumber protein yang beragam (daging, telur, ikan, tahu/tempe); Perhatikan porsi agar sesuai target AKG harian (misalnya, 1 porsi lauk setara telapak tangan).",
            'Kurangi/Batasi': "Protein yang datang bersamaan dengan lemak jenuh berlebih (misalnya: jeroan); Hindari protein yang diolah dengan cara digoreng atau menggunakan minyak berlebihan.",
            'Contoh Praktis': "Variasikan sumber protein (ayam, ikan, telur, tempe); Coba olahan ikan/ayam dengan bumbu pepes atau tumis dengan sedikit minyak; Pastikan porsi protein cukup besar di piring Anda."
        }
    },
    'Lemak Total': {
        'Saran_Naik': {
            'Tingkatkan/Jaga': "Lemak sehat (tak jenuh) yang padat kalori untuk mencapai target kenaikan energi; Contoh: 1/4 buah alpukat, 1 genggam kacang-kacangan, minyak zaitun.",
            'Kurangi/Batasi': "Lemak trans buatan (pada makanan kemasan yang digoreng ulang); Batasi makanan yang tinggi gula/karbohidrat sederhana saja (harus diimbangi lemak/protein).",
            'Contoh Praktis': "Tambahkan 1 sdm minyak zaitun ke salad atau sup; Makan kacang mede, almond, atau biji-bijian (labu) sebagai *snack* harian; Gunakan minyak kelapa/mentega dalam jumlah wajar untuk memasak."
        },
        'Saran_Turun': {
            'Tingkatkan/Jaga': "Batasi asupan lemak total serendah mungkin; Jika harus makan lemak, pilih Lemak tak jenuh esensial (omega-3) yang baik untuk jantung (misal, 1 potong ikan salmon).",
            'Kurangi/Batasi': "Semua sumber lemak jenuh tinggi (mentega, santan kental, krim kental) dan minyak yang digunakan untuk menggoreng; Hindari *dressing* salad yang berbasis krim/mayones.",
            'Contoh Praktis': "Pilih alpukat (dalam batas porsi kecil); Gunakan minyak kanola atau minyak biji bunga matahari untuk menumis; Ganti santan dengan susu rendah lemak atau krimer nabati non-santan."
        },
        'Saran_Jaga': {
            'Tingkatkan/Jaga': "Proporsi Lemak Sehat (omega-3 dan tak jenuh) sesuai anjuran AKG; Konsumsi ikan berlemak untuk asupan omega-3 (sekitar 1-2 kali seminggu).",
            'Kurangi/Batasi': "Batasi *deep fried* food (gorengan); Kontrol porsi kacang-kacangan dan biji-bijian agar tidak berlebihan (maksimal 1 genggam kecil per hari).",
            'Contoh Praktis': "Masak dengan porsi minyak terukur (1-2 sdm per hari); Konsumsi ikan berlemak (salmon, sarden) 1-2 kali seminggu; Pilih *dressing* salad berbasis cuka atau lemon."
        }
    },
    'Karbohidrat': {
        'Saran_Naik': {
            'Tingkatkan/Jaga': "Karbohidrat kompleks dalam porsi yang lebih besar sebagai sumber energi utama untuk mencapai target kalori (misal, 1.5 porsi nasi per makan); Konsumsi Karbohidrat di sela waktu makan.",
            'Kurangi/Batasi': "Mengganti nasi/roti dengan hanya sayuran yang berserat tinggi (ini akan membuat Anda cepat kenyang dan sulit menambah kalori); Jangan tinggalkan Karbohidrat saat makan utama.",
            'Contoh Praktis': "Makan kentang, ubi, atau pasta sebagai sumber Karbohidrat selain nasi; Tambahkan 1 porsi roti di sarapan/camilan; Jangan mengurangi porsi nasi saat makan siang."
        },
        'Saran_Turun': {
            'Tingkatkan/Jaga': "Pilih Karbohidrat kompleks yang tinggi serat dan memiliki indeks glikemik rendah (misal, 1 porsi nasi merah); Prioritaskan serat untuk rasa kenyang yang lebih lama.",
            'Kurangi/Batasi': "Porsi nasi putih, mie, atau roti putih (Karbohidrat sederhana) (batasi porsi menjadi 1 porsi sedang); Gula tambahan dan minuman manis yang tinggi Karbohidrat dan kalori.",
            'Contoh Praktis': "Ganti 1/2 porsi nasi putih dengan nasi merah, beras shirataki, atau sayuran rebus; Prioritaskan sayur/buah di awal makan; Sarapan dengan *oatmeal* tanpa gula tambahan."
        },
        'Saran_Jaga': {
            'Tingkatkan/Jaga': "Variasikan sumber Karbohidrat kompleks (nasi merah, oat, roti gandum utuh); Pastikan asupan Karbohidrat stabil dan tidak berlebihan (misal, 1 porsi nasi per makan).",
            'Kurangi/Batasi': "Karbohidrat olahan dan gula tambahan; Batasi Karbohidrat dalam jumlah besar di malam hari (jika Anda tidak aktif setelah itu).",
            'Contoh Praktis': "Pilih roti gandum utuh 100%; Selalu konsumsi serat (sayur/buah) bersamaan dengan Karbohidrat utama; Batasi *dessert* manis maksimal 1-2 kali seminggu."
        }
    },
    'Kalsium (Ca)': {
        'Saran_Naik': {
            'Tingkatkan/Jaga': "Produk susu *full cream* (2 gelas per hari) atau *whole milk* untuk bonus kalori dan kalsium; Konsumsi sayuran hijau gelap.",
            'Kurangi/Batasi': "Minuman bersoda atau berkafein berlebih yang dapat mengganggu penyerapan kalsium.",
            'Contoh Praktis': "Minum 2 gelas susu *full cream* per hari; Tambahkan keju parut ke dalam omelet/masakan Anda; Coba *yogurt* dengan madu dan buah."
        },
        'Saran_Turun': {
            'Tingkatkan/Jaga': "Susu atau produk olahan rendah lemak/non-fat (1 gelas per hari) (tanpa gula); Sumber nabati Kalsium (tahu/tempe, brokoli).",
            'Kurangi/Batasi': "Susu tinggi lemak atau produk *dessert* yang tinggi gula dan kalsium.",
            'Contoh Praktis': "Pilih *yogurt plain* rendah lemak; Pilih susu nabati yang sudah difortifikasi Kalsium; Makan tempe atau tahu 1-2 porsi sehari."
        },
        'Saran_Jaga': {
            'Tingkatkan/Jaga': "Produk susu (rendah/sedang lemak) (1-2 gelas per hari), tahu/tempe, dan sayuran hijau gelap secara teratur.",
            'Kurangi/Batasi': "Mengonsumsi suplemen kalsium bersamaan dengan makanan kaya zat besi (harus diberi jeda waktu).",
            'Contoh Praktis': "Jadikan *yogurt* atau kefir sebagai camilan sore; Variasikan sayuran hijau (bayam, kale); Minum susu rendah lemak setiap pagi."
        }
    },
    'Besi (Fe)': {
        'Saran_Naik': {
            'Tingkatkan/Jaga': "Sumber Besi Heme (daging merah, hati) (1 potong per hari) dikombinasikan dengan Vitamin C untuk penyerapan terbaik.",
            'Kurangi/Batasi': "Mengonsumsi teh/kopi segera setelah makan karena kandungan tanin dapat menghambat penyerapan Besi.",
            'Contoh Praktis': "Konsumsi hati ayam/sapi 1 porsi seminggu; Minum jus jeruk/jambu saat makan daging; Pilih daging tanpa lemak untuk menghindari lemak jenuh berlebih."
        },
        'Saran_Turun': {
            'Tingkatkan/Jaga': "Sumber Besi hewani rendah lemak (ikan/daging tanpa lemak) dan sumber nabati (kacang-kacangan) (3-4 kali seminggu).",
            'Kurangi/Batasi': "Daging merah yang sangat berlemak tinggi.",
            'Contoh Praktis': "Pilih ikan tuna, salmon, atau daging ayam; Makan kacang-kacangan (lentil, buncis) sebagai lauk 3 kali seminggu; Masak menggunakan panci besi cor."
        },
        'Saran_Jaga': {
            'Tingkatkan/Jaga': "Sumber Besi beragam (hewani dan nabati); Pastikan asupan Vitamin C cukup untuk membantu penyerapan (misal, 1 porsi buah per hari).",
            'Kurangi/Batasi': "Menghindari antasida atau suplemen Kalsium dalam waktu yang sama dengan makanan kaya Besi.",
            'Contoh Praktis': "Jaga konsumsi Vitamin C dari buah-buahan; Masak dengan panci besi cor untuk meningkatkan kandungan Besi pada makanan; Konsumsi daging 3-4 kali seminggu."
        }
    },
}

# ----------------------------------------------------------------------
# BAGIAN 4: DATA AKG RUJUKAN (TETAP SAMA, DITAMPILKAN LAGI UNTUK KELENGKAPAN)
# ----------------------------------------------------------------------
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
            'Kalsium (Ca)': {'data': np.array([1200, 1200, 1200, 1200]), 'unit': 'mg', 'desc': 'Kebutuhan Kalsium'},
            'Besi (Fe)': {'data': np.array([8, 8, 8, 8]), 'unit': 'mg', 'desc': 'Kebutuhan Besi'},
        }
    },
}
# ----------------------------------------------------------------------
# BAGIAN 5: ANTARMUKA STREAMLIT
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
if 'bb_awal' not in st.session_state: 
    st.session_state['bb_awal'] = 60.0
if 'bb_target' not in st.session_state:
    st.session_state['bb_target'] = 60.0
if 'tb_val' not in st.session_state:
    st.session_state['tb_val'] = 160.0


# --- Buat Tab Interaktif ---
tab_input, tab_hasil, tab_metode = st.tabs(["1️⃣ Input Parameter", "2️⃣ Hasil Estimasi & Visualisasi", "3️⃣ Tentang Metode"])

# --- TAB 1: Input Parameter ---
with tab_input:
    st.header("Masukkan Profil dan Kebutuhan")
    
    col_gizi, col_bb_awal, col_tb = st.columns(3)
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

    st.markdown("---")
    
    col_bb_awal, col_bb_target, col_tb = st.columns(3)

    with col_bb_awal:
        # 3. Berat Badan Awal (Untuk hitung BMI)
        BB_Awal_Val = st.number_input(
            '3. Berat Badan Awal Saat Ini (kg):',
            min_value=30.0,
            max_value=120.0,
            value=st.session_state['bb_awal'],
            step=0.1,
            format="%.1f",
            help="BB Anda saat ini, digunakan untuk menghitung BMI.",
            key='bb_awal'
        )
        
    with col_bb_target:
        # 4. Berat Badan Target (Untuk hitung AKG)
        BB_Target_Val = st.number_input(
            '4. Berat Badan Target Ideal (kg):',
            min_value=30.0,
            max_value=120.0,
            value=st.session_state['bb_target'],
            step=0.1,
            format="%.1f",
            help="BB yang Anda targetkan. Estimasi AKG didasarkan pada BB ini.",
            key='bb_target'
        )

    with col_tb:
        # 5. Tinggi Badan
        TB_Val = st.number_input(
            '5. Tinggi Badan (cm):',
            min_value=100.0,
            max_value=220.0,
            value=st.session_state['tb_val'],
            step=1.0,
            format="%.1f",
            help="Tinggi Badan untuk perhitungan BMI",
            key='tb_val'
        )
    
    st.markdown("---")
    
    if st.button('HITUNG ESTIMASI GIZI SEKARANG 🎯', use_container_width=True, type="primary"):
        if BB_Awal_Val <= 0 or TB_Val <= 0 or BB_Target_Val <= 0:
            st.error("Semua nilai Berat Badan dan Tinggi Badan harus lebih besar dari nol.")
        else:
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
            BB_Awal_Val = st.session_state['bb_awal'] 
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
            
            # Estimasi Nilai Lagrange (Menggunakan BB TARGET)
            hasil_estimasi = Estimasi_AKG_Lagrange(X_data_BB, Y_data_Gizi, BB_Target_Val)
            
            # Hitung BMI (Menggunakan BB AWAL)
            TB_meter = TB_Val / 100
            BMI_Awal = BB_Awal_Val / (TB_meter ** 2)
            
            # Klasifikasi BMI Kustom
            BMI_Status, BMI_Saran_Subtext, BMI_Color_Code, BMI_Key = Klasifikasi_BMI_HTML(BMI_Awal, BB_Awal_Val, TB_Val)

            st.header(f"Ringkasan Profil Gizi untuk {Kelompok_Populasi_Key}")

            # CUSTOM METRIC
            col_bmi, col_bb_target, col_bb_diff = st.columns(3)
            
            with col_bmi:
                custom_metric(
                    label="Indeks Massa Tubuh (BMI) Awal",
                    value=f"{BMI_Awal:.1f}",
                    subtext=f'<span style="color:{BMI_Color_Code}; font-weight:bold;">{BMI_Status}</span>'
                )
                
            with col_bb_target:
                diff = BB_Target_Val - BB_Awal_Val
                if diff > 0.5:
                    label_diff = "Tujuan: Naik BB"
                    val_diff = f"+{diff:.1f} kg"
                    color_diff = "#FFB300"
                elif diff < -0.5:
                    label_diff = "Tujuan: Turun BB"
                    val_diff = f"{diff:.1f} kg"
                    color_diff = "#FF4B4B"
                else:
                    label_diff = "Tujuan: Jaga BB"
                    val_diff = f"{diff:.1f} kg"
                    color_diff = "#00BFA6"
                    
                custom_metric(
                    label="Berat Badan Target",
                    value=f"{BB_Target_Val:.1f} kg",
                    subtext=f'Perubahan: <span style="color:{color_diff}; font-weight:bold;">{val_diff}</span>'
                )
                
            with col_bb_diff:
                 custom_metric(
                    label="Kebutuhan Air & Serat",
                    value=f"{Air_Rujukan} {Unit_Air}",
                    subtext=f"Serat: {Serat_Rujukan} {Unit_Serat}/hari"
                )
            
            st.markdown("---")
            
            # Tampilkan Hasil Utama Gizi Lagrange
            st.subheader(f"✅ HASIL ESTIMASI AKG: {Deskripsi_Gizi} ")
            
            # Tampilkan hasil estimasi dalam kotak SUCCESS 
            st.success(f"Perkiraan kebutuhan **{Deskripsi_Gizi}** harian Anda untuk mencapai BB Target **{BB_Target_Val:.1f} kg** adalah **{hasil_estimasi:.2f} {Unit_Gizi}**.")

            # Saran Makanan 
            st.subheader("💡 Saran Gizi, Makanan & Minuman Harian Dinamis")
            
            # Tentukan saran berdasarkan BB Awal dan BB Target (FUNGSI BARU BAHASA SANTAI)
            saran_list = get_saran_makanan(
                Jenis_Gizi_Key, 
                hasil_estimasi, 
                Unit_Gizi, 
                BB_Awal_Val, 
                BB_Target_Val, 
            )
            
            for saran in saran_list:
                st.markdown(saran)
                
            st.markdown("---")

            # Analisis Data dan Visualisasi (Plot menggunakan BB TARGET)
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
                * Estimasi Lagrange menggunakan data ini untuk memprediksi kebutuhan gizi pada BB Target Anda ({BB_Target_Val:.1f} kg).
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
                
                # Tampilkan BB Awal dan BB Target pada plot
                ax.scatter(BB_Awal_Val, Estimasi_AKG_Lagrange(X_data_BB, Y_data_Gizi, BB_Awal_Val), color='#FF4B4B', marker='o', s=150, alpha=0.7, label=f'BB Awal ({BB_Awal_Val} kg)', zorder=6) 
                ax.scatter(BB_Target_Val, hasil_estimasi, color='#40A2E3', marker='X', s=250, label=f'BB Target ({BB_Target_Val} kg)', zorder=7) 

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
                1.  **Titik Merah (o)**: Kebutuhan gizi yang diekspektasikan pada **BB Awal** Anda ({BB_Awal_Val:.1f} kg).
                2.  **Tanda X Biru Cerah (X)**: Kebutuhan gizi yang diperlukan pada **BB Target** Anda ({BB_Target_Val:.1f} kg).
                3.  **Jarak antara kedua titik** menunjukkan perubahan nutrisi yang perlu Anda lakukan untuk mencapai BB Target.
                """)
                # --- AKHIR PENJELASAN GRAFIK ---

                
        except Exception as e:
            st.error(f"❌ ERROR KRITIS: Terjadi Kesalahan Dalam Perhitungan. Pastikan semua input sudah valid. Detail Error: {e}")
            st.session_state['hitung'] = False
    else:
        st.warning("Tekan tombol **'HITUNG ESTIMASI GIZI SEKARANG 🎯'** di tab **Input Parameter** untuk memulai analisis.")

# --- TAB 3: Tentang Metode (Tidak Berubah) ---
with tab_metode:
    st.header("Metode Numerik: Interpolasi Polinomial Lagrange")
    st.markdown("Aplikasi ini menggunakan metode **Interpolasi Polinomial Lagrange** untuk mengestimasi nilai Angka Kecukupan Gizi (AKG) pada Berat Badan (BB) yang tidak tercantum langsung dalam tabel rujukan AKG resmi.")

    st.subheader("Konsep Dasar")
    st.markdown("""
    * **Interpolasi** adalah metode untuk membangun fungsi baru dari sekumpulan titik data yang diskrit. Dalam kasus ini, kita membuat fungsi yang menghubungkan kebutuhan gizi (Y) dengan Berat Badan (X).
    * **Polinomial Lagrange** adalah salah satu metode interpolasi yang menghasilkan polinomial unik berderajat $n-1$ yang melewati semua $n$ titik data yang diberikan.
    """)
    
    st.subheader("Rumus Polinomial Lagrange")
    st.markdown("Untuk $n$ titik data $(x_0, y_0), (x_1, y_1), \dots, (x_{n-1}, y_{n-1})$, Polinomial Lagrange $P(x)$ didefinisikan sebagai:")
    
    st.latex(r"P(x) = \sum_{j=0}^{n-1} y_j L_j(x)")
    
    st.markdown("Di mana $L_j(x)$ adalah **Basis Polinomial Lagrange**:")
    
    st.latex(r"L_j(x) = \prod_{i=0, i \neq j}^{n-1} \frac{x - x_i}{x_j - x_i}")
    
    st.markdown("""
    Dalam konteks aplikasi ini:
    * $x$ adalah **Berat Badan Target** (`BB_Target_Val`).
    * $x_i$ adalah **Berat Badan Acuan** dalam tabel (`X_data_BB`).
    * $y_i$ adalah **Kebutuhan Gizi Rujukan** dalam tabel (`Y_data_Gizi`).
    """)

    st.subheader("Mengapa menggunakan Lagrange?")
    st.markdown("""
    1. **Akurasi Titik Rujukan:** Polinomial Lagrange menjamin akurasi penuh pada titik-titik data rujukan (kurva pasti melewati titik-titik tersebut).
    2. **Solusi Unik:** Untuk set data yang diberikan, Polinomial Lagrange memberikan solusi polinomial unik.
    3. **Kesinambungan Data Gizi:** Karena kebutuhan gizi sering kali berhubungan secara non-linear dengan berat badan, interpolasi polinomial memberikan estimasi yang lebih halus dan logis dibandingkan interpolasi linier.
    """) 
    
    st.markdown("---")
    st.markdown("""
    **Penting:** Meskipun metode ini sangat akurat di antara titik-titik data (interpolasi), metode ini mungkin kurang akurat jika digunakan untuk memprediksi di luar rentang data acuan (ekstrapolasi).
    """)

