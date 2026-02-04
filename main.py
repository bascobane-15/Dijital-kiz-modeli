import streamlit as st
import pandas as pd

st.set_page_config(page_title="BioTwin-Systems", layout="centered")

st.title("🧠🧪 BioTwin-Systems")
st.subheader("Sinir ve Endokrin Sistem Dijital İkizi")

st.markdown(
"""
Bu dijital ikiz, **hormon düzeyleri ile fizyolojik sonuçlar arasındaki ilişkileri**
etkileşimli olarak gözlemlemek amacıyla geliştirilmiştir.
"""
)

st.divider()

# -----------------------------
# ÇEVRESEL DEĞİŞKENLER
# -----------------------------
st.header("🌍 Çevresel ve Fizyolojik Değişkenler")

stress = st.slider("Stres Düzeyi", 0, 100, 50)
sleep = st.slider("Uyku Süresi (saat/gün)", 0, 10, 7)
nutrition = st.slider("Beslenme Düzeyi", 0, 100, 60)

st.divider()

# -----------------------------
# HORMON DÜZEYLERİ
# -----------------------------
st.header("🧬 Hormon Düzeyleri")

kortizol = st.slider("Kortizol", 0, 100, stress)
insulin = st.slider("İnsülin", 0, 100, nutrition)
tiroksin = st.slider("Tiroksin (T4)", 0, 100, 50)

st.divider()

# -----------------------------
# FİZYOLOJİK ETKİLER
# -----------------------------
st.header("📊 Fizyolojik Tepkiler")

# Basitleştirilmiş model ilişkileri
kan_sekeri = 100 + (kortizol * 0.5) - (insulin * 0.7)
metabolizma = tiroksin * 1.2
bagisiklik = max(0, 100 - kortizol * 0.6)
enerji = max(0, (sleep * 10) + insulin - kortizol * 0.5)

df = pd.DataFrame({
    "Parametre": ["Kan Şekeri", "Metabolizma Hızı", "Bağışıklık", "Enerji Düzeyi"],
    "Değer": [kan_sekeri, metabolizma, bagisiklik, enerji]
})

st.bar_chart(df.set_index("Parametre"))

st.divider()

# -----------------------------
# KLİNİK YORUM
# -----------------------------
st.header("🩺 Dijital İkiz Klinik Yorum")

if kortizol > 70:
    st.warning("⚠️ Yüksek kortizol: Kronik stres, bağışıklık baskılanması ve uyku bozukluğu riski.")
elif kortizol < 30:
    st.info("ℹ️ Düşük kortizol: Stres yanıtı zayıf.")

if insulin < 30:
    st.error("❗ İnsülin eksikliği: Hiperglisemi ve diyabet riski.")
elif insulin > 70:
    st.warning("⚠️ İnsülin fazlalığı: Hipoglisemi riski.")

if tiroksin < 30:
    st.warning("⚠️ Tiroksin düşük: Hipotiroidi – yavaş metabolizma.")
elif tiroksin > 70:
    st.warning("⚠️ Tiroksin yüksek: Hipertiroidi – hızlı metabolizma.")

st.success("✅ Sistemler arası etkileşim başarıyla gözlemleniyor.")

st.caption("BioTwin-Systems | Eğitim Amaçlı Dijital İkiz Modeli")
