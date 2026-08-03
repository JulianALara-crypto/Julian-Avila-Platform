import streamlit as st

from config.config import APP_NAME
from auth.login import mostrar_login


# ==========================================
# MÓDULOS ADMIN
# ==========================================

from modules.admin.dashboard import mostrar_dashboard
from modules.admin.clientes import mostrar_clientes
from modules.admin.pagos import mostrar_pagos
from modules.admin.alertas import mostrar_alertas
from modules.admin.personal_training import mostrar_personal_training


# ==========================================
# MÓDULOS CLIENTE
# ==========================================

from modules.cliente.perfil import mostrar_perfil
from modules.cliente.evolucion import mostrar_evolucion
from modules.cliente.personalizado import mostrar_personalizado



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

    .stApp{
        background-color:#000000;
    }


    h1,h2,h3,h4{
        color:white !important;
        text-align:center;
    }


    p,label,.stMarkdown{
        color:#dddddd !important;
    }


    div[data-testid="stDecoration"]{
        display:none;
    }


    </style>
    """,
    unsafe_allow_html=True
)



# ==========================================
# SESIÓN
# ==========================================

if "autenticado" not in st.session_state:

    st.session_state["autenticado"] = False




# ==========================================
# PANEL PRINCIPAL
# ==========================================

def panel_principal():

    from auth.permissions import obtener_menu


    usuario = st.session_state.get(
        "usuario"
    )



    if usuario is None:


        st.error(
            "No existe una sesión válida."
        )


        st.session_state.clear()

        st.rerun()



    # ======================================
    # SIDEBAR
    # ======================================

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



    opciones = list(
        dict.fromkeys(
            obtener_menu(
                usuario["rol"]
            )
        )
    )



    if not opciones:

        st.error(
            "No hay módulos disponibles para este usuario."
        )

        return



    seleccion = st.sidebar.radio(

        "MENÚ",

        opciones,

        key=f"menu_{usuario['rol']}"

    )



    st.sidebar.divider()



    # ======================================
    # CERRAR SESIÓN
    # ======================================

    if st.sidebar.button(

        "Cerrar Sesión",

        use_container_width=True

    ):


        st.session_state.clear()

        st.rerun()




    # ======================================
    # TÍTULO
    # ======================================

    st.title(
        "JULIAN AVILA PLATFORM"
    )


    st.subheader(
        seleccion
    )





    # ======================================
    # ADMINISTRADOR
    # ======================================

    if usuario["rol"] == "Admin":



        if seleccion == "📊 Dashboard":


            mostrar_dashboard()



        elif seleccion == "👥 Clientes":


            mostrar_clientes()



        elif seleccion == "💳 Pagos y Contabilidad":


            mostrar_pagos()



        elif seleccion == "🚨 Alertas de Vencimiento":


            mostrar_alertas()



        elif seleccion == "🏋️ Personal Training":


            mostrar_personal_training()



        elif seleccion == "📈 Evolución Física":


            st.info(
                "Módulo en construcción."
            )



        elif seleccion == "📄 Documentos":


            st.info(
                "Módulo en construcción."
            )



        elif seleccion == "⚙️ Configuración":


            st.info(
                "Módulo en construcción."
            )



        else:


            st.warning(
                "Opción no disponible."
            )





    # ======================================
    # CLIENTE
    # ======================================

    else:



        if seleccion == "👤 Mi Perfil":


            mostrar_perfil()



        elif seleccion == "📏 Mis Medidas":


            mostrar_evolucion()



        elif seleccion == "📈 Mi Evolución":


            mostrar_evolucion()



        elif seleccion == "🏋️ Mi Plan Personalizado":


            mostrar_personalizado()



        elif seleccion == "📄 Documentos":


            st.info(
                "Próximamente podrás consultar aquí tus documentos."
            )



        else:


            st.warning(
                "Opción no disponible."
            )




# ==========================================
# EJECUCIÓN PRINCIPAL
# ==========================================

if not st.session_state["autenticado"]:


    mostrar_login()



else:


    panel_principal()
