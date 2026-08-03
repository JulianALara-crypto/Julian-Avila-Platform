import requests
import pandas as pd
import streamlit as st

from config.config import URL_USUARIOS



# ==========================================
# CARGAR HISTORIAL DE MEDIDAS
# ==========================================

@st.cache_data(ttl=300)
def cargar_medidas():

    try:

        respuesta = requests.get(
            URL_USUARIOS
        )


        datos = respuesta.json()


        historial_raw = datos.get(
            "historial",
            []
        )


        if len(historial_raw) <= 1:

            return pd.DataFrame()



        columnas = [
            str(c).strip().lower()
            for c in historial_raw[0]
        ]


        df = pd.DataFrame(
            historial_raw[1:],
            columns=columnas
        )



        # Normalizar cédulas

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


        # Fechas formato plataforma

        if "fecha_evaluacion" in df.columns:

            df["fecha_evaluacion"] = (
                pd.to_datetime(
                    df["fecha_evaluacion"],
                    errors="coerce"
                )
                .dt.strftime(
                    "%d-%m-%Y"
                )
            )


        return df



    except Exception as e:


        st.error(
            f"Error cargando medidas: {e}"
        )


        return pd.DataFrame()



# ==========================================
# FILTRAR MEDIDAS DE CLIENTE
# ==========================================

def obtener_medidas_cliente(
    cedula
):


    df = cargar_medidas()


    if df.empty:

        return pd.DataFrame()



    return df[
        df["cedula"].astype(str)
        ==
        str(cedula)
    ]
