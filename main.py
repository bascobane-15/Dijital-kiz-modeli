import streamlit as st

st.set_page_config(page_title="BioTwin-Systems", layout="centered")

st.title("🧠 BioTwin-Systems")
st.subheader("Sinir ve Endokrin Sistem Dijital İkizi")
st.markdown("Her hormon için ayrı senaryo üzerinden **neden–sonuç ilişkileri** gözlemlenir.")

st.divider()

# SEKME YAPISI
tabs = st.tabs(["🟠 Kortizol", "🔵 İnsülin", "🟣 Tiroksin"])

# ------------------------------------------------
# KORTİZOL SEKME
# ------------------------------------------------
with tabs[0]:
    st.header("Kortizol Hormonu (Stres Hormonu)")

    stress = st.slider("Stres Düzeyi", 0, 100, 50)
    kortizol = stress  # basit ilişki

    st.metric("Kortizol Düzeyi", kortizol)

    if kortizol > 70:
        st.error("⚠️ Kortizol Fazlalığı")
        st.markdown("""
        **Olası Sonuçlar:**
        - Bağışıklık sisteminin baskılanması  
        - Kan şekerinde artış  
        - Uyku bozuklukları  

        **İlişkili Hastalıklar:**
        - Cushing Sendromu  
        - Kronik stres kaynaklı bağışıklık zayıflığı
        """)
    elif kortizol < 3
