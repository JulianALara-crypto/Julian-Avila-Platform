import streamlit as st
import pandas as pd

from database.medidas import obtener_medidas_cliente



# ==========================================
# EVOLUCIÓN FÍSICA ADMIN
# ==========================================

def mostrar_evolucion_admin():

    st.header(
        "📈 Evolución Física Clientes"
    )


    cedula = st.text_input(
        "Buscar cliente por cédula"
    )



    if not cedula:

        st.info(
            "Ingrese una cédula para consultar evolución."
        )

        return



    registros = obtener_medidas_cliente(
        cedula
    )



    if registros.empty:

        st.warning(
            "No existen evaluaciones para este cliente."
        )

        return



    # ======================================
    # LIMPIEZA DE DATOS
    # ======================================

    # Limpia espacios en nombres de columnas

    registros.columns = (
        registros.columns
        .astype(str)
        .str.strip()
    )


    # Elimina columnas duplicadas

    registros = registros.loc[
        :,
        ~registros.columns.duplicated()
    ]



    st.subheader(
        "📋 Historial de evaluaciones"
    )



    st.dataframe(
        registros.astype(str),
        use_container_width=True
    )



    st.divider()



    # ===============================
    # GRÁFICAS
    # ===============================


    st.subheader(
        "📊 Progreso del cliente"
    )



    columnas = [

        "peso_kg",

        "porcentaje_grasa",

        "cintura_cm",

        "pecho_cm",

        "cadera_cm"

    ]



    disponibles = [

        c for c in columnas

        if c in registros.columns

    ]



    if disponibles:


        grafica = registros[

            disponibles

        ].apply(

            pd.to_numeric,

            errors="coerce"

        )


        st.line_chart(
            grafica
        )


    else:

        st.info(
            "No hay datos suficientes para generar gráfica."
        )
