import streamlit as st
import pandas as pd
import numpy as np
import time
import plotly.graph_objects as go
from datetime import datetime

# Sayfa Yapılandırması
st.set_page_config(page_title="NursTwin-Home Digital Twin", layout="wide")

# --- 1. VERİ TOPLAMA VE ÖN İŞLEME (Simülasyon) ---
def get_sensor_data():
    """IoT ve Giyilebilir Sensörlerden veri akışını simüle eder."""
    return {
        "timestamp": datetime.now().strftime("%H:%M:%S"),
        "nabiz": np.random.randint(60, 110),
        "spo2": np.random.randint(94, 100),
        "hareket": np.random.choice(["Hareketsiz", "Yatakta Dönme", "Ayağa Kalkma"]),
        "sicaklik": round(np.random.uniform(22.0, 26.0), 1),
        "nem": np.random.randint(40, 60)
    }

# --- 2. DİJİTAL İKİZ MOTORU (Veri Füzyonu & Karar Destek) ---
def analyze_data(data):
    """Hemşirelik Karar Destek Çıktıları ve NIC Önerileri."""
    status = "Normal"
    nic_suggestion = "Rutin izleme devam ediyor."
    alert_level = "success"

    if data["nabiz"] > 100 or data["spo2"] < 95:
        status = "Kritik: Fizyolojik Risk"
        nic_suggestion = "NIC: Vital Bulguların İzlenmesi & Oksijen Terapi Hazırlığı"
        alert_level = "danger"
    elif data["hareket"] == "Ayağa Kalkma":
        status = "Uyarı: Düşme Riski"
        nic_suggestion = "NIC: Düşme Önleme Protokolü Aktivasyonu"
        alert_level = "warning"
        
    return status, nic_suggestion, alert_level

# --- 3. HEMŞİRE ARAYÜZÜ (Streamlit UI) ---
st.title("🏥 NursTwin-Home: Hemşirelik Dijital İkiz Paneli")
st.markdown(f"**Hasta & Ev Ortamı Takibi** | Son Güncelleme: {datetime.now().strftime('%Y-%m-%d')}")

# Kenar Çubuğu - Cihaz Durumu
st.sidebar.header("İletişim Katmanı")
st.sidebar.success("MQTT: Bağlı")
st.sidebar.success("Wi-Fi / BLE: Aktif")

# Dashboard Alanı
col1, col2, col3 = st.columns(3)
placeholder = st.empty()

# Veri Geçmişi için DataFrame
if 'history' not in st.session_state:
    st.session_state.history = pd.DataFrame(columns=["Zaman", "Nabız", "SpO2", "Durum"])

# --- GERİBİLDİRİM DÖNGÜSÜ (Canlı Döngü) ---
while True:
    current_data = get_sensor_data()
    status, nic, alert_type = analyze_data(current_data)
    
    # Geçmişe ekle
    new_row = {"Zaman": current_data["timestamp"], "Nabız": current_data["nabiz"], 
               "SpO2": current_data["spo2"], "Durum": status}
    st.session_state.history = pd.concat([pd.DataFrame([new_row]), st.session_state.history]).head(10)

    with placeholder.container():
        # Metrik Kartları
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("Nabız (BPM)", current_data["nabiz"])
        m2.metric("SpO2 (%)", current_data["spo2"])
        m3.metric("Ortam Isısı", f"{current_data['sicaklik']}°C")
        m4.metric("Hareket", current_data["hareket"])

        st.divider()

        # Grafik ve Karar Destek
        left_col, right_col = st.columns([2, 1])

        with left_col:
            st.subheader("Fizyolojik Veri Trendi")
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=st.session_state.history["Zaman"], y=st.session_state.history["Nabız"], name="Nabız"))
            fig.update_layout(height=300, margin=dict(l=0, r=0, t=0, b=0))
            st.plotly_chart(fig, use_container_width=True)

        with right_col:
            st.subheader("Hemşirelik Karar Destek")
            if alert_type == "danger":
                st.error(f"**DURUM:** {status}")
            elif alert_type == "warning":
                st.warning(f"**DURUM:** {status}")
            else:
                st.info(f"**DURUM:** {status}")
            
            st.info(f"💡 **Öneri:** {nic}")
            
            if st.button("Hemşire Müdahalesini Onayla"):
                st.success("Müdahale kaydedildi, Dijital İkiz güncellendi.")

        st.subheader("Son Veri Kayıtları")
        st.table(st.session_state.history)

    time.sleep(3) # 3 saniyede bir güncelle (Gerçek zamanlı simülasyon)