import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --- CSS KUSTOM & TEMA ---
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
    
    # 1. Status BMI
    saran.append(f"**Status Gizi (BMI):** {BMI_Saran_Subtext}")
    saran.append("---")
    
    # 2. Saran Utama Gizi (dengan format TINGKATKAN/KURANGI)
    saran_data = Tabel_Saran_Makro_Mikro.get(Jenis_Gizi_Key, {})
    
    saran.append(f"### Target Utama: {hasil_estimasi:.0f} {Unit_Gizi} ({Jenis_Gizi_Key})")
    
    # TINGKATKAN/JAGA
    tingkatkan_jaga = saran_data.get(BMI_Key, {}).get('Tingkatkan/Jaga', "Informasi saran belum tersedia.")
    saran.append(f"**⬆️ FOKUS TINGKATKAN/JAGA:** {tingkatkan_jaga}")
    
    # KURANGI/BATASI
    kurangi_batasi = saran_data.get(BMI_Key, {}).get('Kurangi/Batasi', "Informasi saran belum tersedia.")
    saran.append(f"**⬇️ FOKUS KURANGI/BATASI:** {kurangi_batasi}")
    
    saran.append("---")
    
    # 3. Saran Air dan Serat (Rujukan Tetap)
    saran.append(f"### Kebutuhan Pelengkap Harian")
    saran.append(f"**💧 Air:** Target **{Air_Rujukan} liter/hari**. Pastikan minum air putih secara teratur, hindari minuman manis berlebihan.")
    saran.append(f"**🥦 Serat:** Target **{Serat_Rujukan} g/hari**. Konsumsi sayur dan buah minimal 5 porsi/hari dan pilih biji-bijian utuh (whole grain).")
    
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

# STRUKTUR SARAN MAKANAN BERDASARKAN BMI
Tabel_Saran_Makro_Mikro = {
    'Energi': {
        'Saran_Kurus': {
            'Tingkatkan/Jaga': "Asupan karbohidrat kompleks (nasi, roti, ubi) dan protein. Pilih makanan padat kalori (alpukat, kacang-kacangan) dan makan porsi lebih sering/besar.",
            'Kurangi/Batasi': "Minuman dan makanan yang terlalu banyak serat di awal makan (untuk memaksimalkan penyerapan kalori), makanan rendah kalori."
        }, 
        'Saran_Normal': {
            'Tingkatkan/Jaga': "Keseimbangan sumber energi (Karbohidrat, Protein, Lemak) sesuai target AKG. Fokus pada sumber energi yang bersih (whole foods).",
            'Kurangi/Batasi': "Kalori kosong seperti *snack* tinggi gula, minuman manis, dan *fast food* berlebihan."
        },
        'Saran_Gemuk_Obesitas': {
            'Tingkatkan/Jaga': "Sayuran non-pati dan serat (untuk kenyang tanpa kalori berlebih). Jaga asupan protein untuk massa otot.",
            'Kurangi/Batasi': "Porsi keseluruhan makanan (defisit kalori), gula tambahan, minuman manis, makanan yang digoreng, dan sumber karbohidrat sederhana."
        }
    }, 
    'Protein': {
        'Saran_Kurus': {
            'Tingkatkan/Jaga': "Asupan protein berkualitas tinggi (daging tanpa lemak, telur, ikan, whey) pada setiap kali makan untuk membangun massa otot.",
            'Kurangi/Batasi': "Hanya makan sayuran sebagai sumber protein utama; perlu kombinasi dengan protein hewani."
        },
        'Saran_Normal': {
            'Tingkatkan/Jaga': "Sumber protein beragam (daging, telur, ikan, tahu/tempe) untuk menjaga dan memperbaiki sel tubuh.",
            'Kurangi/Batasi': "Protein yang datang bersamaan dengan lemak jenuh berlebih (misalnya: kulit ayam, sosis, *bacon*)."
        },
        'Saran_Gemuk_Obesitas': {
            'Tingkatkan/Jaga': "Protein tinggi serat dan rendah lemak (dada ayam tanpa kulit, ikan, produk kedelai) untuk meningkatkan rasa kenyang.",
            'Kurangi/Batasi': "Potongan daging berlemak tinggi; hindari pengolahan protein dengan cara digoreng (pilih panggang/rebus)."
        }
    },
    'Lemak Total': {
        'Saran_Kurus': {
            'Tingkatkan/Jaga': "Lemak tak jenuh tunggal dan ganda (alpukat, kacang, minyak zaitun, ikan berlemak) untuk tambahan kalori bersih.",
            'Kurangi/Batasi': "Lemak trans buatan (roti-roti kemasan, makanan instan) dan lemak jenuh yang sangat tinggi."
        },
        'Saran_Normal': {
            'Tingkatkan/Jaga': "Proporsi Lemak Sehat (omega-3 dan tak jenuh) untuk kesehatan otak dan jantung.",
            'Kurangi/Batasi': "Lemak jenuh dari *junk food* dan lemak trans. Pertahankan jumlah lemak sesuai target AKG."
        },
        'Saran_Gemuk_Obesitas': {
            'Tingkatkan/Jaga': "Batasi lemak hingga batas minimum yang direkomendasikan AKG. Jika mengonsumsi lemak, pilih lemak tak jenuh.",
            'Kurangi/Batasi': "Semua sumber lemak jenuh (mentega, minyak kelapa sawit, *deep fried* food), serta semua makanan/minuman yang mengandung krim atau santan kental."
        }
    },
    'Karbohidrat': {
        'Saran_Kurus': {
            'Tingkatkan/Jaga': "Karbohidrat kompleks (nasi, pasta, roti gandum utuh) dalam porsi besar sebagai sumber energi utama.",
            'Kurangi/Batasi': "Diet rendah karbohidrat yang tidak perlu; hindari melewatkan jam makan utama berkarbohidrat."
        },
        'Saran_Normal': {
            'Tingkatkan/Jaga': "Pilih sumber Karbohidrat kompleks (oat, nasi merah, roti gandum) dan serat yang cukup.",
            'Kurangi/Batasi': "Gula sederhana (permen, *soft drink*, kue-kue) dan karbohidrat olahan."
        },
        'Saran_Gemuk_Obesitas': {
            'Tingkatkan/Jaga': "Karbohidrat yang datang bersamaan dengan serat tinggi (sayuran, kacang-kacangan, biji-bijian utuh) untuk rasa kenyang.",
            'Kurangi/Batasi': "Porsi nasi, mie, atau roti putih (Karbohidrat sederhana). Hindari minuman manis berkalori tinggi."
        }
    },
    'Kalsium (Ca)': {
        'Saran_Kurus': {
            'Tingkatkan/Jaga': "Susu *full cream* atau produk olahannya (keju/yogurt), bayam, dan brokoli.",
            'Kurangi/Batasi': "Minuman bersoda atau berkafein berlebih yang dapat mengganggu penyerapan Kalsium."
        },
        'Saran_Normal': {
            'Tingkatkan/Jaga': "Produk susu (rendah/sedang lemak), tahu/tempe, dan sayuran hijau gelap.",
            'Kurangi/Batasi': "Konsumsi fosfor berlebihan (misalnya dari minuman ringan) yang dapat mengganggu keseimbangan Ca."
        },
        'Saran_Gemuk_Obesitas': {
            'Tingkatkan/Jaga': "Susu atau produk olahan rendah lemak/non-fat, serta sumber nabati Kalsium (untuk membatasi kalori).",
            'Kurangi/Batasi': "Susu tinggi lemak atau produk *dessert* tinggi gula yang mengandung Kalsium."
        }
    },
    'Besi (Fe)': {
        'Saran_Kurus': {
            'Tingkatkan/Jaga': "Sumber Besi Heme (daging merah, hati) dikombinasikan dengan sumber Vitamin C (jeruk, jambu).",
            'Kurangi/Batasi': "Minum teh/kopi segera setelah makan karena kandungan tanin dapat menghambat penyerapan Besi."
        },
        'Saran_Normal': {
            'Tingkatkan/Jaga': "Sumber Besi beragam (hewani dan nabati) dan Vitamin C untuk penyerapan optimal.",
            'Kurangi/Batasi': "Antasida atau suplemen Kalsium dalam waktu yang sama dengan makanan kaya Besi."
        },
        'Saran_Gemuk_Obesitas': {
            'Tingkatkan/Jaga': "Sumber Besi hewani rendah lemak (misalnya ikan) atau sumber nabati (kacang-kacangan).",
            'Kurangi/Batasi': "Daging merah berlemak tinggi sebagai satu-satunya sumber Besi."
        }
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
            'Kalsium (Ca)': {'data': np.array([1200, 1200, 1200, 1200]), 'unit': 'mg', 'desc': 'Kebutuhan Kalsium'},
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
        st.snow()


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

            # IMPLEMENTASI CUSTOM METRIC (WARNA BIRU MUDA & PUTIH CERAH)
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
            # AKHIR IMPLEMENTASI CUSTOM METRIC
            
            st.markdown("---")
            
            # Tampilkan Hasil Utama Gizi Lagrange
            st.subheader(f"✅ HASIL ESTIMASI LAGRANGE: {Deskripsi_Gizi}")
            
            # Tampilkan hasil estimasi dalam kotak SUCCESS (PUTIH Pucat, Teks Hitam)
            st.success(f"Perkiraan kebutuhan **{Deskripsi_Gizi}** harian Anda pada Berat Badan **{BB_Target_Val:.1f} kg** adalah **{hasil_estimasi:.2f} {Unit_Gizi}**.")

            # Saran Makanan (Dinamis BMI - V10)
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

# --- TAB 3: Tentang Metode ---
with tab_metode:
    # PERBAIKAN: Menghilangkan spasi non-standar (U+00A0) di Baris ini.
    st.header("Metode Numerik: Interpolasi Polinomial Lagrange")
    st.markdown("Aplikasi ini menggunakan metode **Interpolasi Polinomial Lagrange** untuk mengestimasi nilai Angka Kecukupan Gizi (AKG) pada Berat Badan (BB) yang tidak tercantum langsung dalam tabel rujukan AKG resmi.")

    st.subheader("Konsep Dasar")
    st.markdown("""
    * **Interpolasi** adalah metode untuk membangun fungsi baru dari sekumpulan titik data yang diskrit. Dalam kasus ini, kita membuat fungsi yang menghubungkan kebutuhan gizi (Y) dengan Berat Badan (X).
    * **Polinomial Lagrange** adalah salah satu metode interpolasi yang menghasilkan polinomial unik berderajat $n-1$ yang melewati semua $n$ titik data yang diberikan.
    """)
    

    st.subheader("Rumus Polinomial Lagrange")
    st.markdown("Untuk $n$ titik data $(x_0, y_0), (x_1, y_1), \dots, (x_{n-1}, y_{n-1})$, Polinomial Lagrange $P(x)$ didefinisikan sebagai:")
    
    # PERBAIKAN: Menggunakan st.latex() dan Raw String (r"...")
    st.latex(r"P(x) = \sum_{i=0}^{n-1} y_i L_i(x)")
    
    st.markdown("Di mana $L_i(x)$ adalah **Basis Polinomial Lagrange** yang didefinisikan sebagai:")
    
    # PERBAIKAN: Menggunakan st.latex() dan Raw String (r"...")
    st.latex(r"L_i(x) = \prod_{j=0, j \neq i}^{n-1} \frac{x - x_j}{x_i - x_j}")
    
    st.markdown("""
    Dalam konteks aplikasi ini:
    * $x$ adalah **Berat Badan Target** (`BB_Target_Val`).
    * $x_i$ adalah **Berat Badan Acuan** dalam tabel (`X_data_BB`).
    * $y_i$ adalah **Kebutuhan Gizi Rujukan** dalam tabel (`Y_data_Gizi`).
    """)

    st.subheader("Mengapa menggunakan Lagrange?")
    st.markdown("""
    1.  **Akurasi Titik Rujukan:** Polinomial Lagrange menjamin akurasi penuh pada titik-titik data rujukan (kurva pasti melewati titik-titik tersebut).
    2.  **Solusi Unik:** Untuk set data yang diberikan, Polinomial Lagrange memberikan solusi polinomial unik.
    3.  **Kesinambungan Data Gizi:** Karena kebutuhan gizi sering kali berhubungan secara non-linear dengan berat badan, interpolasi polinomial memberikan estimasi yang lebih halus dan logis dibandingkan interpolasi linier.
    """) 
    
    st.markdown("---")
    st.markdown("""
    **Penting:** Meskipun metode ini sangat akurat di antara titik-titik data (interpolasi), metode ini mungkin kurang akurat jika digunakan untuk memprediksi di luar rentang data acuan (ekstrapolasi, misalnya BB < 30 kg atau BB > 100 kg).
    """)


