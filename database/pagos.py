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

        # Enviamos petición especial al Apps Script
        respuesta = requests.get(
            URL_GYM
        )


        datos = respuesta.json()


        # Si no hay datos
        if not datos:

            return pd.DataFrame()



        # La hoja Pagos todavía no se lee
        # desde doGet, lo agregaremos después


        return pd.DataFrame()



    except Exception as e:


        st.error(
            f"Error cargando pagos: {e}"
        )


        return pd.DataFrame()



# ==========================================
# REGISTRAR NUEVO PAGO
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
