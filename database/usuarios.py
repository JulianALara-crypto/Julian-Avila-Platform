import requests
import pandas as pd
import streamlit as st

from config.config import URL_USUARIOS



@st.cache_data(ttl=300)
def cargar_usuarios():

    try:

        respuesta = requests.get(
            URL_USUARIOS
        )


        datos = respuesta.json()


        usuarios_raw = datos.get(
            "usuarios",
            []
        )


        if len(usuarios_raw) <= 1:

            return pd.DataFrame()



        columnas = [
            str(c).strip().lower()
            for c in usuarios_raw[0]
        ]


        df = pd.DataFrame(
            usuarios_raw[1:],
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



    except Exception as e:

        st.error(
            f"Error cargando usuarios: {e}"
        )

        return pd.DataFrame()
