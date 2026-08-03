import requests
import pandas as pd
import streamlit as st
from datetime import datetime

from config.config import URL_GYM



# ==========================================
# CARGAR HISTORIAL DE PAGOS
# ==========================================

@st.cache_data(ttl=300)
def cargar_pagos():

    try:

        url = URL_GYM + "?action=pagos"


        respuesta = requests.get(
            url
        )


        datos = respuesta.json()



        if len(datos) <= 1:

            return pd.DataFrame(
                columns=[
                    "cedula",
                    "nombre_completo",
                    "fecha_pago",
                    "valor",
                    "concepto"
                ]
            )



        columnas = [
            "cedula",
            "nombre_completo",
            "fecha_pago",
            "valor",
            "concepto"
        ]



        df = pd.DataFrame(
            datos[1:],
            columns=columnas
        )



        if "valor" in df.columns:

            df["valor"] = pd.to_numeric(
                df["valor"],
                errors="coerce"
            ).fillna(0)



        if "fecha_pago" in df.columns:

            fechas = pd.to_datetime(
                df["fecha_pago"],
                errors="coerce",
                dayfirst=True
            )


            df["fecha_pago"] = fechas.dt.strftime(
                "%d-%m-%Y"
            )



        return df



    except Exception as e:


        st.error(
            f"Error cargando pagos: {e}"
        )


        return pd.DataFrame()



# ==========================================
# REGISTRAR PAGO
# ==========================================

def registrar_pago(
    cedula,
    nombre,
    valor,
    concepto
):

    try:

        fecha_pago = datetime.today().strftime(
            "%d-%m-%Y"
        )


        respuesta = requests.post(

            URL_GYM,

            json={

                "action":"registrar_pago",

                "cedula":str(cedula),

                "nombre_completo":nombre,

                "fecha_pago":fecha_pago,

                "valor":int(valor),

                "concepto":concepto

            }

        )


        return respuesta.json()



    except Exception as e:


        return {

            "status":"error",

            "mensaje":str(e)

        }
