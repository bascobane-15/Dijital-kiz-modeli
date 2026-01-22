import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(page_title="NursTwin-Home Digital Twin", layout="wide")

# --- VERİ TOPLAMA SİMÜLASYONU ---
def get_sensor_data():
    return {
        "Zaman": datetime.now().strftime("%H:%M:%S"),
        "Nabız (BPM)": np.random.randint(65, 105),
        "SpO2 (%)": np.random.randint(93, 100),
        "Vücut Isısı (°C)": round(np.random.uniform(36.2, 37.8), 1),
        "Hareket Durumu": np.random.choice(["Stabil", "Hareketli", "Yatakta Dönme"]),
        "Oda Nemi (%)": np.random.randint(40, 55)
    }

# --- KARAR DESTEK MOTORU ---
def analyze_patient(data):
    if data["Nabız (BPM)"] > 100 or data["SpO2 (%)"] < 94:
        return "⚠️ KRİTİK", "NIC: Vital Bulguların Sık Takibi & Oksijen Desteği", "red"
    elif data["Vücut Isısı (°C)"] > 37.5:
        return "🟡 UYARI", "NIC: Ateş Yönetimi & Sıvı Takibi", "orange"
    return "✅ NORMAL", "Rutin İzlem: Veri akışı stabil.", "green"

# --- ARAYÜZ ---
st.title("🏥 NursTwin-Home: Gelişmiş Dijital İkiz Paneli")

# Sidebar: Veri Yönetimi
st.sidebar.header("📊 Veri Kayıt Yönetimi")
if 'db' not in st.session_state:
    st.session_state.db = pd.DataFrame()

# Dosyayı İndirme Butonu
if not st.session_state.db.empty:
    csv = st.session_state.db.to_csv(index=False).encode('utf-8-sig')
    st.sidebar.download_button(
        label="📥 Verileri Excel Olarak İndir",
        data=csv,
        file_name=f"NursTwin_Kayit_{datetime.now().strftime('%d_%m_%Y')}.csv",
        mime='text/csv',
    )
    if st.sidebar.button("🗑️ Kayıtları Temizle"):
        st.session_state.db = pd.DataFrame()
        st.rerun()

# Ana Panel Alanı
placeholder = st.empty()

while True:
    current = get_sensor_data()
    status, nic_advice, color = analyze_patient(current)
    
    # Veriyi hafızaya ekle
    temp_df = pd.DataFrame([current])
    temp_df['Durum'] = status
    st.session_state.db = pd.concat([temp_df, st.session_state.db]).head(100)

    with placeholder.container():
        # Metrik Kartları
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Nabız", f"{current['Nabız (BPM)']} bpm")
        c2.metric("SpO2", f"%{current['SpO2 (%)']}")
        c3.metric("Ateş", f"{current['Vücut Isısı (°C)']}°C")
        c4.metric("Hareket", current['Hareket Durumu'])

        st.divider()
        col_left, col_right = st.columns([2, 1])

        with col_left:
            st.subheader("📈 Anlık Fizyolojik Grafik")
            fig = go.Figure()
            fig.add_trace(go.Scatter(y=st.session_state.db["Nabız (BPM)"].iloc[::-1], name="Nabız", line=dict(color='red')))
            fig.add_trace(go.Scatter(y=st.session_state.db["SpO2 (%)"].iloc[::-1], name="SpO2", line=dict(color='blue')))
            fig.update_layout(height=350, margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)

        with col_right:
            st.subheader("📋 Hemşire Karar Destek")
            st.markdown(f"### <span style='color:{color}'>{status}</span>", unsafe_allow_html=True)
            st.info(f"**Önerilen Müdahale:**\n\n{nic_advice}")
            
        st.subheader("📄 Son Veri Kayıtları")
        st.table(st.session_state.db.head(5))

    time.sleep(3)
