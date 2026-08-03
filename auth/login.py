import streamlit as st
import requests
import pandas as pd

from config.config import (
    URL_USUARIOS,
    ADMIN_USER,
    ADMIN_PASSWORD
)


# ==========================================
# CONSULTAR USUARIOS GOOGLE SHEETS
# ==========================================

@st.cache_data(ttl=300)
def obtener_usuarios():

    try:

        respuesta = requests.get(URL_USUARIOS)

        datos = respuesta.json()

        usuarios = datos.get(
            "usuarios",
            []
        )

        if len(usuarios) <= 1:
            return pd.DataFrame()


        columnas = [
            str(c).strip().lower()
            for c in usuarios[0]
        ]


        df = pd.DataFrame(
            usuarios[1:],
            columns=columnas
        )


        if "cedula" in df.columns:

            df["cedula"] = (
                df["cedula"]
                .astype(str)
                .str.replace(
                    ".0",
                    "",
                    regex=False
                )
                .str.strip()
            )


        return df


    except Exception as error:

        st.error(
            f"Error cargando usuarios: {error}"
        )

        return pd.DataFrame()



# ==========================================
# GUARDAR SESIÓN
# ==========================================

def crear_sesion(usuario):

    st.session_state["autenticado"] = True

    st.session_state["usuario"] = usuario



# ==========================================
# MOSTRAR LOGIN
# ==========================================

def mostrar_login():


    st.title(
        "🔐 Inicio de Sesión"
    )


    col1, col2 = st.columns(2)



    # ======================================
    # LOGIN
    # ======================================

    with col1:


        st.subheader(
            "Ingresar"
        )


        cedula = st.text_input(
            "Cédula / ID"
        )


        password = st.text_input(
            "Contraseña",
            type="password"
        )


        if st.button(
            "Ingresar",
            use_container_width=True
        ):


            # --------------------------
            # ADMIN
            # --------------------------

            if (
                cedula == ADMIN_USER
                and
                password == ADMIN_PASSWORD
            ):


                crear_sesion(
                    {
                        "cedula": "ADMIN",
                        "nombre": "JULIAN AVILA",
                        "rol": "Admin"
                    }
                )

                st.rerun()



            # --------------------------
            # CLIENTE
            # --------------------------

            else:


                df = obtener_usuarios()


                if df.empty:

                    st.error(
                        "No hay usuarios disponibles"
                    )


                else:


                    usuario = df[
                        df["cedula"] == cedula
                    ]


                    if usuario.empty:

                        st.error(
                            "Usuario no encontrado"
                        )


                    else:

                        datos = usuario.iloc[0]


                        if (
                            str(datos["password"]).strip()
                            ==
                            password
                        ):


                            crear_sesion(
                                {
                                    "cedula": str(datos["cedula"]),
                                    "nombre": datos["nombre_completo"],
                                    "rol": datos.get(
                                        "rol",
                                        "Cliente"
                                    )
                                }
                            )


                            st.rerun()


                        else:

                            st.error(
                                "Contraseña incorrecta"
                            )



    # ======================================
    # REGISTRO
    # ======================================

    with col2:


        st.subheader(
            "Crear cuenta nueva"
        )


        st.info(
            """
            El registro de clientes
            será conectado en la siguiente fase.
            """
        )
