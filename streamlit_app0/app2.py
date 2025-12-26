import streamlit as st

st.title("Basit Streamlit Uygulaması")

st.write("Merhaba! Bu benim ilk Streamlit uygulamam.")

isim = st.text_input("Adınızı girin:")

if st.button("Selamla"):
    if isim:
        st.success(f"Merhaba {isim} 👋")
    else:
        st.warning("Lütfen adınızı girin.")
