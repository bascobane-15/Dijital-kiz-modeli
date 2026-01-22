import streamlit as st
import pandas as pd

st.set_page_config(page_title="NursTwin-Home", layout="wide")
st.title("🏠 NursTwin-Home")
st.subheader("Evde Bakım Hastası için Dijital İkiz Karar Destek Paneli")

# -------------------
# SOL PANEL – GİRDİLER
# -------------------
st.sidebar.header("📥 Hasta Parametreleri")

nabiz = st.sidebar.slider("Nabız (bpm)", 40, 140, 80)
spo2 = st.sidebar.slider("SpO₂ (%)", 80, 100, 96)
hrv = st.sidebar.slider("HRV (ms)", 10, 120, 60)
stres = st.sidebar.selectbox("Psikolojik Stres", ["Düşük", "Orta", "Yüksek"])

# -------------------
# RİSK HESAPLAMA
# -------------------
risk = 0

if nabiz < 50 or nabiz > 110:
    risk += 25

if spo2 < 92:
    risk += 30

if hrv < 40:
    risk += 25

if stres == "Orta":
    risk += 10
elif stres == "Yüksek":
    risk += 20

# -------------------
# SAĞ PANEL – ÇIKTILAR
# -------------------
col1, col2 = st.columns(2)

with col1:
    st.header("🔢 Genel Risk Skoru")
    st.metric(label="Risk Skoru", value=f"%{risk}")

if risk <= 40:
    st.success("🟢 Stabil – Rutin izlem yeterli")

    st.markdown("### 🩺 NANDA Hemşirelik Tanısı")
    st.info("Sağlığı Geliştirmeye Hazır Olma")

    st.markdown("### 📩 Hemşire Bilgilendirme Mesajı")
    st.write(
        "Hasta fizyolojik ve psikososyal açıdan stabil görünmektedir. "
        "Rutin izlem ve mevcut bakım planının sürdürülmesi önerilir."
    )

elif risk <= 70:
    st.warning("🟡 Riskli – Yakın izlem önerilir")

    st.markdown("### 🩺 NANDA Hemşirelik Tanısı")
    st.info("Deri Bütünlüğünde Bozulma Riski")

    st.markdown("### 📩 Hemşire Bilgilendirme Mesajı")
    st.write(
        "Hastada hareketlilik azalması ve fizyolojik değişiklikler gözlenmektedir. "
        "Pozisyon değişim aralıklarının kısaltılması ve cilt bütünlüğünün yakından izlenmesi önerilir."
    )

else:
    st.error("🔴 Yüksek Risk – Müdahale gerekli")

    st.markdown("### 🩺 NANDA Hemşirelik Tanısı")
    st.info("Gaz Değişiminde Bozulma / Aktivite İntoleransı")

    st.markdown("### 📩 Hemşire Acil Uyarı Mesajı")
    st.write(
        "Hastada ciddi fizyolojik riskler tespit edilmiştir. "
        "Derhal hemşirelik müdahalesi uygulanmalı, gerekirse hekim bilgilendirilmelidir."
    )


with col2:
    st.header("📊 Risk Bileşenleri")

    data = {
        "Parametre": ["Nabız", "SpO₂", "HRV", "Stres"],
        "Risk Katkısı": [
            25 if (nabiz < 50 or nabiz > 110) else 0,
            30 if spo2 < 92 else 0,
            25 if hrv < 40 else 0,
            20 if stres == "Yüksek" else 10 if stres == "Orta" else 0
        ]
    }

    df = pd.DataFrame(data)
    st.bar_chart(df.set_index("Parametre"))


