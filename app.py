import streamlit as st

from config.config import APP_NAME


# ==========================================
# CONFIGURACIÓN DE PÁGINA
# ==========================================

st.set_page_config(
    page_title=APP_NAME,
    layout="wide",
    initial_sidebar_state="expanded"
)


# ==========================================
# ESTILO GLOBAL
# ==========================================

st.markdown(
    """
    <style>

    .stApp {
        background-color:#000000;
    }


    h1,h2,h3,h4 {
        color:white !important;
        text-align:center;
    }


    p,label {
        color:#dddddd !important;
    }


    div[data-testid="stDecoration"] {
        display:none;
    }


    </style>

    """,
    unsafe_allow_html=True
)


# ==========================================
# INICIO
# ==========================================

def main():

    st.title(
        "JULIAN AVILA PLATFORM"
    )


    st.markdown(
        """
        ### Plataforma integral

        Personal Training

        Evolution Tracker

        Gestión Gimnasio

        """
    )


    st.info(
        "Sistema en construcción - Fase inicial"
    )



if __name__ == "__main__":
    main()
