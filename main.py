import streamlit as st
import pandas as pd
from agents.agent_workflow import run_workflow
from utils.generate_pdf import generate_stride_pdf
from utils.save_temp_file import save_uploaded_file

st.set_page_config(page_title="Análise STRIDE", layout="wide")

if "running" not in st.session_state:
    st.session_state.running = False

st.title(" 🛡️ Modelagem de Ameaças STRIDE com IA")
st.markdown("Faça o upload do seu diagrama de arquitetura para identificar vulnerabilidades e mitigações.")

with st.sidebar:
    st.header("Sobre o Projeto")
    st.info(
        "Esta ferramenta utiliza Visão Computacional e LLMs para mapear componentes de infraestrutura e aplicar a metodologia STRIDE.")

uploaded_file = st.file_uploader(
    "Faça upload do diagrama de arquitetura",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file:
    col1, col2 = st.columns([1, 1])

    with col1:
        st.image(uploaded_file, caption="Diagrama Original", use_container_width=True)

    if st.button(
            "Analisando..." if st.session_state.running else "🚀 Analisar Arquitetura",
            disabled=st.session_state.running,
            type="primary"
    ):
        st.session_state.running = True
        st.rerun()

    if st.session_state.running:
        try:
            with st.spinner("IA processando componentes e fluxos..."):
                image_path = save_uploaded_file(uploaded_file)
                result = run_workflow(image_path)
                st.session_state.analysis_done = True

            st.success("Análise concluída!")
            tab_report, tab_components, tab_flow, tab_raw = st.tabs([
                "📋 Relatório de Ameaças",
                "🏗️ Componentes Detectados",
                "🔄 Fluxos de Dados",
                "📄 JSON Bruto"
            ])

            with tab_report:
                col_txt, col_btn = st.columns([0.8, 0.2])
                with col_btn:
                    pdf_bytes = generate_stride_pdf(image_path, result.get("stride_output", ""))
                    st.download_button(
                        label="📥 Baixar PDF",
                        data=pdf_bytes,
                        file_name="analise_stride.pdf",
                        mime="application/pdf"
                    )
                st.markdown(result.get("stride_output", "Nenhum relatório gerado."))

            with tab_components:
                st.subheader("Inventário de Infraestrutura")
                components = result.get("vision_output", {}).get("components", [])
                if components:
                    df_comp = pd.DataFrame(components)
                    cols = ['name', 'type', 'trust_zone', 'internet_exposed', 'is_managed_service', 'notes']
                    st.dataframe(df_comp[cols], use_container_width=True)
                else:
                    st.warning("Nenhum componente identificado.")

            with tab_flow:
                st.subheader("Matriz de Comunicação")
                flows = result.get("vision_output", {}).get("flows", [])
                if flows:
                    df_flows = pd.DataFrame(flows)
                    st.table(df_flows[['source_id', 'target_id', 'interaction_type', 'direction']])
                else:
                    st.info("Nenhum fluxo de dados mapeado.")

            with tab_raw:
                st.json(result)

        except Exception as e:
            st.error(f"Erro durante a análise: {e}")
        finally:
            st.session_state.running = False