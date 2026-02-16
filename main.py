import streamlit as st

from agents.agent_workflow import run_workflow
from utils.save_temp_file import save_uploaded_file

st.title("Threat Modeling com IA")

uploaded_file = st.file_uploader(
    "Faça upload do diagrama de arquitetura",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    st.image(uploaded_file, caption="Diagrama enviado")
    if st.button("Analisar diagrama"):
        with st.spinner("Analisando arquitetura..."):
            image_path = save_uploaded_file(uploaded_file)
            result = run_workflow(image_path)
            st.subheader("Resultado: ")
            st.json(result)
