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
            url,
            timeout=10
        )


        respuesta.raise_for_status()


        datos = respuesta.json()



        columnas = [

            "cedula",

            "nombre_completo",

            "fecha_pago",

            "valor",

            "concepto"

        ]



        if (
            not datos
            or len(datos) <= 1
        ):

            return pd.DataFrame(
                columns=columnas
            )



        filas = []


        for fila in datos[1:]:


            if len(fila) >= 5:

                filas.append(
                    fila[:5]
                )



        df = pd.DataFrame(

            filas,

            columns=columnas

        )



        # ==================================
        # LIMPIAR FILAS VACÍAS
        # ==================================

        df = df.dropna(
            how="all"
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



        # ==================================
        # LIMPIAR VALOR DEL PAGO
        # ==================================

        if "valor" in df.columns:


            df["valor"] = (

                df["valor"]

                .astype(str)

                .str.replace(
                    "$",
                    "",
                    regex=False
                )

                .str.replace(
                    " ",
                    "",
                    regex=False
                )

                .str.replace(
                    ".",
                    "",
                    regex=False
                )

                .str.replace(
                    ",",
                    "",
                    regex=False
                )

            )


            df["valor"] = pd.to_numeric(

                df["valor"],

                errors="coerce"

            ).fillna(0)



        # ==================================
        # LIMPIAR FECHAS
        # ==================================

        if "fecha_pago" in df.columns:


            fechas = pd.to_datetime(

                df["fecha_pago"],

                errors="coerce",

                dayfirst=True

            )


            df["fecha_pago"] = (

                fechas

                .dt.strftime(
                    "%d-%m-%Y"
                )

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

                "action":

                    "registrar_pago",


                "cedula":

                    str(cedula),


                "nombre_completo":

                    nombre,


                "fecha_pago":

                    fecha_pago,


                "valor":

                    int(valor),


                "concepto":

                    concepto

            },

            timeout=10

        )


        return respuesta.json()



    except Exception as e:


        return {

            "status":

                "error",


            "mensaje":

                str(e)

        }
