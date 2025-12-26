import streamlit as st
import math

st.set_page_config(page_title="Devir-İlerleme Hesaplama", layout="centered")

st.title("🛠️ Torna ve Freze Devir – İlerleme Hesaplama")
st.write("Formüllü – Yerine Koymalı – Sonuçlu Hesaplama")

# ------------------------------------------------
# KESME HIZLARI (m/dak)
# ------------------------------------------------
kesme_hizlari = {
    "Makine çeliği": 30,
    "Takım çeliği": 18,
    "Paslanmaz çelik": 20,
    "Dökme demir": 34,
    "Bronz ve pirinç": 35,
    "Alüminyum": 60
}

# ------------------------------------------------
# FREZE DİŞ BAŞINA İLERLEME TABLOSU (mm/diş)
# ------------------------------------------------
fz_tablosu = {
    "Makine çeliği": {
        "Alın freze": 0.30,
        "Helis freze": 0.33,
        "Kanal freze": 0.25,
        "Parmak freze": 0.20,
        "Form freze": 0.12
    },
    "Takım çeliği": {
        "Alın freze": 0.40,
        "Helis freze": 0.34,
        "Kanal freze": 0.22,
        "Parmak freze": 0.16,
        "Form freze": 0.19
    },
    "Paslanmaz çelik": {
        "Alın freze": 0.25,
        "Helis freze": 0.22,
        "Kanal freze": 0.13,
        "Parmak freze": 0.10,
        "Form freze": 0.065
    },
    "Dökme demir": {
        "Alın freze": 0.36,
        "Helis freze": 0.34,
        "Kanal freze": 0.26,
        "Parmak freze": 0.24,
        "Form freze": 0.12
    },
    "Bronz ve pirinç": {
        "Alın freze": 0.33,
        "Helis freze": 0.36,
        "Kanal freze": 0.24,
        "Parmak freze": 0.17,
        "Form freze": 0.14
    },
    "Alüminyum": {
        "Alın freze": 0.53,
        "Helis freze": 0.43,
        "Kanal freze": 0.315,
        "Parmak freze": 0.365,
        "Form freze": 0.165
    }
}

# ------------------------------------------------
# SEÇİMLER
# ------------------------------------------------
islem = st.selectbox("İşlem Türü", ["Torna / Matkap", "Freze"])
malzeme = st.selectbox("Malzeme Cinsi", kesme_hizlari.keys())
V = kesme_hizlari[malzeme]

D = st.number_input("Çap (mm)", min_value=1.0, value=20.0)

# ------------------------------------------------
# DEVİR HESABI
# ------------------------------------------------
N = (V * 1000) / (math.pi * D)

st.subheader("🔄 Devir Sayısı Hesabı")

st.code(f"""
N = (V × 1000) / (π × D)
N = ({V} × 1000) / (3.14 × {D})
N = {N:.0f} dev/dak
""")

# ------------------------------------------------
# FREZE İLERLEME
# ------------------------------------------------
if islem == "Freze":
    st.subheader("➡️ Freze İlerleme Hesabı")

    freze_tipi = st.selectbox("Freze Tipi", fz_tablosu[malzeme].keys())
    z = st.number_input("Freze Diş Sayısı (z)", min_value=1, value=4)

    fz = fz_tablosu[malzeme][freze_tipi]

    F = fz * z * N

    st.code(f"""
F = fz × z × N
F = {fz} × {z} × {N:.0f}
F = {F:.1f} mm/dak
""")


# ------------------------------------------------
# ÖĞRENCİYE MANTIKSAL AÇIKLAMA
# ------------------------------------------------
st.subheader("🧠 Hesaplama Mantığı (Kısa Açıklama)")

if islem == "Torna / Matkap":
    st.write(f"""
Bu işlemde **kesme hızı (V)** sabit alınmıştır.  
Parça çapı **{D} mm** olduğu için devir sayısı buna göre hesaplanır.  

➡️ Sonuç olarak parça, **{N:.0f} dev/dak** hızla dönmelidir.  
Çap büyürse devir azalır, çap küçülürse devir artar.
""")

if islem == "Freze":
    st.write(f"""
Önce kesme hızı ve freze çapı kullanılarak **devir sayısı** hesaplanmıştır.  
Seçilen frezede her diş, bir turda **{fz} mm** ilerler.  

Freze **{z} dişli** olduğu için toplam ilerleme artar.  
➡️ Bu nedenle tabla ilerlemesi **{F:.1f} mm/dak** olarak bulunmuştur.
""")
