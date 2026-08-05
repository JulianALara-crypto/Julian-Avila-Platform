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



        # ==================================
        # SIN DATOS
        # ==================================

        if not datos:

            return pd.DataFrame(
                columns=columnas
            )



        # ==================================
        # CONVERTIR JSON A DATAFRAME
        # ==================================

        df = pd.DataFrame(datos)



        # Crear columnas faltantes

        for columna in columnas:

            if columna not in df.columns:

                df[columna] = ""



        # Orden correcto

        df = df[columnas]




        # ==================================
        # LIMPIAR FILAS VACÍAS
        # ==================================

        df = df.dropna(
            how="all"
        )



        # ==================================
        # LIMPIAR CÉDULA
        # ==================================

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
        # LIMPIAR VALOR
        # ==================================

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

        df["fecha_pago"] = pd.to_datetime(

            df["fecha_pago"],

            errors="coerce",

            dayfirst=True

        ).dt.strftime(

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



        fila = [

            str(cedula),

            nombre,

            fecha_pago,

            int(valor),

            concepto

        ]




        respuesta = requests.post(

            URL_GYM,

            json={

                "action":

                    "registrar_pago",


                "row":

                    fila

            },

            timeout=10

        )



        return respuesta.json()




    except Exception as e:


        return {

            "status":

                "error",


            "message":

                str(e)

        }
