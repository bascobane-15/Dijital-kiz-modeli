import pandas as pd
import streamlit as st

st.subheader("İnsülin – Glukagon Antagonizması (Kan Şekeri Dengesi)")

glucose = st.slider("Kan Glikoz Alımı", 0, 100, 60)

insulin = max(0, glucose - 30)
glucagon = max(0, 70 - glucose)

df = pd.DataFrame({
    "Hormon": ["İnsülin", "Glukagon"],
    "Düzey": [insulin, glucagon]
})

st.bar_chart(df.set_index("Hormon"))

# Biyolojik yorum
if insulin > glucagon:
    st.success("✅ İnsülin baskın → Kan şekeri düşürülüyor")
elif glucagon > insulin:
    st.warning("⚠️ Glukagon baskın → Kan şekeri yükseltiliyor")
else:
    st.info("ℹ️ Hormonlar dengede → Homeostaz sağlanıyor")


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
    elif kortizol < 30:
        st.warning("⚠️ Kortizol Eksikliği")
        st.markdown("""
        **Olası Sonuçlar:**
        - Düşük stres toleransı  
        - Halsizlik  
        - Düşük tansiyon  

        **İlişkili Hastalık:**
        - Addison Hastalığı
        """)
    else:
        st.success("✅ Kortizol dengede. Homeostaz korunuyor.")

# ------------------------------------------------
# İNSÜLİN SEKME
# ------------------------------------------------
with tabs[1]:
    st.header("İnsülin – Glukagon Dengesi (Antagonist Hormonlar)")

    glucose = st.slider("Kan Glikoz Alımı", 0, 100, 60)

    insulin = max(0, glucose - 30)
    glucagon = max(0, 70 - glucose)

    st.metric("İnsülin Düzeyi", insulin)
    st.metric("Glukagon Düzeyi", glucagon)

    if insulin > glucagon:
        st.success("✅ İnsülin baskın → Kan şekeri düşürülüyor")
    elif glucagon > insulin:
        st.warning("⚠️ Glukagon baskın → Kan şekeri yükseltiliyor")
    else:
        st.info("ℹ️ Denge durumu")

    if insulin < 20:
        st.error("""
        ❗ **İnsülin Eksikliği**
        - Kan şekeri yükselir  
        - Hücreler glikozu kullanamaz  

        **İlişkili Hastalık:**  
        - Diyabet
        """)

    if glucagon > 70:
        st.warning("""
        ⚠️ **Glukagon Fazlalığı**
        - Sürekli kan şekeri yükselmesi  

        **İlişkili Durum:**  
        - Hiperglisemi
        """)


# ------------------------------------------------
# TİROKSİN SEKME
# ------------------------------------------------
with tabs[2]:
    st.header("Tiroksin (T4) Hormonu – Metabolizma Düzenleyici")

    tiroksin = st.slider("Tiroksin (T4) Düzeyi", 0, 100, 50)
    st.metric("Tiroksin Düzeyi", tiroksin)

    if tiroksin < 30:
        st.warning("⚠️ Tiroksin Eksikliği")
        st.markdown("""
        **Olası Sonuçlar:**
        - Metabolizma hızının yavaşlaması  
        - Kilo artışı  
        - Yorgunluk, soğuğa hassasiyet  

        **İlişkili Hastalık:**
        - Hipotiroidi
        """)
    elif tiroksin > 70:
        st.error("⚠️ Tiroksin Fazlalığı")
        st.markdown("""
        **Olası Sonuçlar:**
        - Metabolizma hızının artması  
        - Kilo kaybı  
        - Çarpıntı, sinirlilik  

        **İlişkili Hastalık:**
        - Hipertiroidi
        """)
    else:
        st.success("✅ Tiroksin dengede. Metabolik denge sağlanıyor.")

st.divider()
st.caption("BioTwin-Systems | Eğitim Amaçlı Dijital İkiz Modeli")


