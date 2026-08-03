import requests
import pandas as pd
import streamlit as st

from config.config import URL_GYM



# ==========================================
# CARGAR CLIENTES GIMNASIO
# ==========================================

@st.cache_data(ttl=300)
def cargar_clientes_gym():

    try:

        respuesta = requests.get(
            URL_GYM
        )


        datos = respuesta.json()



        # En el Script 2 viene directamente
        # la tabla de clientes

        if len(datos) <= 1:

            return pd.DataFrame()



        columnas = [
            "cedula",
            "nombre_completo",
            "eps",
            "whatsapp",
            "metodo_pago",
            "fecha_ingreso",
            "valor_pagado",
            "fecha_vencimiento"
        ]


        df = pd.DataFrame(
            datos[1:],
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



        # Formato fechas plataforma

        for columna in [
            "fecha_ingreso",
            "fecha_vencimiento"
        ]:


            if columna in df.columns:


                fechas = pd.to_datetime(
                    df[columna],
                    errors="coerce"
                )


                df[columna] = (
                    fechas.dt.strftime(
                        "%d-%m-%Y"
                    )
                )



        return df



    except Exception as e:


        st.error(
            f"Error cargando clientes gimnasio: {e}"
        )


        return pd.DataFrame()



# ==========================================
# BUSCAR CLIENTE GYM
# ==========================================

def buscar_cliente_gym(
    cedula
):

    df = cargar_clientes_gym()


    if df.empty:

        return pd.DataFrame()



    return df[
        df["cedula"].astype(str)
        ==
        str(cedula)
    ]



# ==========================================
# ENVIAR ACCIONES GOOGLE APPS SCRIPT
# ==========================================

def enviar_accion_gym(
    accion,
    datos
):

    try:

        respuesta = requests.post(
            URL_GYM,
            json={
                "action": accion,
                **datos
            }
        )


        return respuesta.json()


    except Exception as e:


        return {
            "error": str(e)
        }
