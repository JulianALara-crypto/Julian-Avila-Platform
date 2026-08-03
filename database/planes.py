import requests
import pandas as pd
import streamlit as st

from config.config import URL_GYM



# ==========================================
# CARGAR PLANES
# ==========================================

@st.cache_data(ttl=300)
def cargar_planes():

    try:

        respuesta = requests.get(
            URL_GYM,
            params={
                "action":"planes"
            }
        )


        datos = respuesta.json()


        if len(datos) <= 1:

            return pd.DataFrame()



        columnas = [

            "cedula",
            "nombre_completo",
            "tipo_plan",
            "fecha_inicio",
            "fecha_fin",
            "estado",
            "observaciones"

        ]



        df = pd.DataFrame(
            datos[1:],
            columns=columnas
        )



        df["cedula"] = (

            df["cedula"]
            .astype(str)
            .str.strip()

        )



        return df



    except Exception as e:


        st.error(
            f"Error cargando planes: {e}"
        )


        return pd.DataFrame()




# ==========================================
# BUSCAR PLAN CLIENTE
# ==========================================

def buscar_plan_cliente(
    cedula
):


    df = cargar_planes()



    if df.empty:

        return pd.DataFrame()



    return df[

        df["cedula"]
        ==
        str(cedula)

    ]




# ==========================================
# CREAR PLAN
# ==========================================

def crear_plan(
    datos
):


    try:


        respuesta = requests.post(

            URL_GYM,

            json={

                "action":"crear_plan",

                **datos

            }

        )



        return respuesta.json()



    except Exception as e:


        return {

            "error":str(e)

        }
