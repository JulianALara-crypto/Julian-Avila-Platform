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

    from auth.permissions import obtener_menu


    usuario = st.session_state["usuario"]


    # ==================================
    # SIDEBAR USUARIO
    # ==================================

    st.sidebar.title(
        "Julian Avila Platform"
    )


    st.sidebar.write(
        f"👤 {usuario['nombre']}"
    )


    st.sidebar.write(
        f"Rol: {usuario['rol']}"
    )


    st.sidebar.divider()



    # ==================================
    # MENÚ SEGÚN ROL
    # ==================================

    opciones = obtener_menu(
        usuario["rol"]
    )


    seleccion = st.sidebar.radio(
        "MENÚ",
        opciones
    )


    st.sidebar.divider()


    if st.sidebar.button(
        "Cerrar Sesión"
    ):

        st.session_state.clear()

        st.rerun()



    # ==================================
    # CONTENIDO TEMPORAL
    # ==================================

    st.title(
        "JULIAN AVILA PLATFORM"
    )


    st.subheader(
        seleccion
    )


    if usuario["rol"] == "Admin":


        if seleccion == "📊 Dashboard":

            st.info(
                "Aquí estará el resumen financiero y estadísticas."
            )


        elif seleccion == "👥 Clientes":

            st.info(
                "Aquí estará la gestión completa de clientes."
            )


        elif seleccion == "💳 Pagos y Contabilidad":

            st.info(
                "Aquí estarán pagos parciales, ingresos y contabilidad."
            )


        else:

            st.info(
                f"Módulo administrador: {seleccion}"
            )



    else:


        if seleccion == "👤 Mi Perfil":

            st.info(
                "Aquí estará la información personal del cliente."
            )


        elif seleccion == "📏 Mis Medidas":

            st.info(
                "Aquí estarán las evaluaciones antropométricas."
            )


        elif seleccion == "📈 Mi Evolución":

            st.info(
                "Aquí estarán las gráficas de progreso."
            )


        else:

            st.info(
                f"Módulo cliente: {seleccion}"
            )
