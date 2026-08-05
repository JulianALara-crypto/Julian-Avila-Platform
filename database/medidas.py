import requests
import pandas as pd
import streamlit as st

from config.config import URL_USUARIOS



# ==========================================
# CARGAR HISTORIAL DE MEDIDAS
# ==========================================

@st.cache_data(ttl=1)
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



        encabezados = historial_raw[0]


        if not isinstance(
            encabezados,
            list
        ):

            return pd.DataFrame()



        # ==================================
        # NORMALIZAR NOMBRES DE COLUMNAS
        # ==================================

        columnas = []


        for columna in encabezados:


            nombre = (

                str(columna)

                .strip()

                .lower()

                .replace(
                    " ",
                    "_"
                )

            )


            # Evitar columnas duplicadas

            if nombre in columnas:

                contador = 2

                nuevo_nombre = f"{nombre}_{contador}"


                while nuevo_nombre in columnas:

                    contador += 1

                    nuevo_nombre = (
                        f"{nombre}_{contador}"
                    )


                nombre = nuevo_nombre



            columnas.append(nombre)



        df = pd.DataFrame(

            historial_raw[1:],

            columns=columnas

        )



        # ==================================
        # ELIMINAR COLUMNAS COMPLETAMENTE
        # DUPLICADAS
        # ==================================

        df = df.loc[
            :,
            ~df.columns.duplicated()
        ]



        # ==================================
        # NORMALIZAR CÉDULAS
        # ==================================

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
        # NORMALIZAR FECHAS
        # ==================================

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
# OBTENER MEDIDAS DE UN CLIENTE
# ==========================================

def obtener_medidas_cliente(
    cedula
):


    df = cargar_medidas()



    if df.empty:

        return pd.DataFrame()



    if "cedula" not in df.columns:

        return pd.DataFrame()



    return df[

        df["cedula"]

        .astype(str)

        ==

        str(cedula)

    ]
