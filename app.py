import streamlit as st

from config.config import APP_NAME
from auth.login import mostrar_login


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


    p,label,.stMarkdown {
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
# INICIALIZAR SESIÓN
# ==========================================

if "autenticado" not in st.session_state:

    st.session_state["autenticado"] = False



# ==========================================
# PANEL PRINCIPAL
# ==========================================

def panel_principal():

    usuario = st.session_state["usuario"]


    st.sidebar.title(
        "Julian Avila Platform"
    )


    st.sidebar.write(
        f"👤 {usuario['nombre']}"
    )


    st.sidebar.write(
        f"Rol: {usuario['rol']}"
    )


    if st.sidebar.button(
        "Cerrar Sesión"
    ):

        st.session_state.clear()

        st.rerun()



    st.title(
        "JULIAN AVILA PLATFORM"
    )


    if usuario["rol"] == "Admin":

        st.success(
            "Panel Administrador"
        )

        st.write(
            "Aquí estará el control total del sistema."
        )


    else:

        st.success(
            "Perfil Cliente"
        )

        st.write(
            "Aquí aparecerá tu evolución, medidas y planes."
        )



# ==========================================
# EJECUCIÓN
# ==========================================

if not st.session_state["autenticado"]:

    mostrar_login()


else:

    panel_principal()
if __name__ == "__main__":
    main()
