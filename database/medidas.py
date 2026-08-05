import requests
import pandas as pd
import streamlit as st

from config.config import URL_USUARIOS



@st.cache_data(ttl=300)
def cargar_medidas():

    try:

        respuesta = requests.get(
            URL_USUARIOS,
            timeout=10
        )

        respuesta.raise_for_status()

        datos = respuesta.json()


        historial_raw = datos.get(
            "historial",
            []
        )


        if (
            not historial_raw
            or len(historial_raw) <= 1
        ):
            return pd.DataFrame()



        if not isinstance(historial_raw[0], list):
            return pd.DataFrame()



        columnas = [
            str(c).strip().lower()
            for c in historial_raw[0]
        ]


        df = pd.DataFrame(
            historial_raw[1:],
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



def obtener_medidas_cliente(
    cedula
):

    df = cargar_medidas()


    if df.empty:
        return pd.DataFrame()


    if "cedula" not in df.columns:
        return pd.DataFrame()


    return df[
        df["cedula"].astype(str)
        ==
        str(cedula)
    ]
