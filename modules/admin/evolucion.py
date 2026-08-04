import streamlit as st
import pandas as pd

from database.medidas import obtener_medidas_cliente
from database.gimnasio import cargar_clientes_gym



# ==========================================
# EVOLUCIÓN FÍSICA ADMIN
# ==========================================

def mostrar_evolucion_admin():


    st.header(
        "📈 Evolución Física Clientes"
    )



    # ======================================
    # SELECCIÓN CLIENTE
    # ======================================


    clientes = cargar_clientes_gym()



    if clientes.empty:


        st.warning(
            "No existen clientes registrados."
        )

        return



    opciones = (

        clientes["nombre_completo"]

        .astype(str)

        .tolist()

    )



    seleccionado = st.selectbox(

        "Seleccionar cliente",

        opciones

    )



    cliente = clientes[

        clientes["nombre_completo"]

        ==

        seleccionado

    ].iloc[0]



    cedula = str(

        cliente["cedula"]

    )



    st.write(

        f"🪪 Cédula: {cedula}"

    )



    st.divider()



    registros = obtener_medidas_cliente(

        cedula

    )



    if registros.empty:


        st.warning(

            "No existen evaluaciones para este cliente."

        )

        return





    # ======================================
    # LIMPIEZA
    # ======================================


    registros.columns = (

        registros.columns

        .astype(str)

        .str.strip()

        .str.lower()

    )



    registros = registros.loc[

        :,

        ~registros.columns.duplicated()

    ]





    st.subheader(

        f"👤 {cliente['nombre_completo']}"

    )





    # ======================================
    # ORDENAR EVALUACIONES
    # ======================================


    if "fecha_evaluacion" in registros.columns:


        registros["_fecha"] = pd.to_datetime(

            registros["fecha_evaluacion"],

            dayfirst=True,

            errors="coerce"

        )


        registros = (

            registros

            .sort_values(

                "_fecha"

            )

            .drop(

                columns="_fecha"

            )

        )





    inicial = registros.iloc[0]

    actual = registros.iloc[-1]





    # ======================================
    # FUNCIÓN NUMÉRICA
    # ======================================


    def valor(

        fila,

        columna

    ):


        try:


            return float(

                fila[columna]

            )


        except:


            return 0





    peso_i = valor(

        inicial,

        "peso_kg"

    )


    peso_a = valor(

        actual,

        "peso_kg"

    )



    grasa_i = valor(

        inicial,

        "porcentaje_grasa"

    )


    grasa_a = valor(

        actual,

        "porcentaje_grasa"

    )



    cintura_i = valor(

        inicial,

        "cintura_cm"

    )


    cintura_a = valor(

        actual,

        "cintura_cm"

    )



    pecho_i = valor(

        inicial,

        "pecho_cm"

    )


    pecho_a = valor(

        actual,

        "pecho_cm"

    )





    # ======================================
    # PROGRESO
    # ======================================


    st.subheader(

        "📊 Progreso"

    )



    c1,c2,c3,c4 = st.columns(4)



    c1.metric(

        "⚖️ Peso",

        f"{peso_a} kg",

        f"{peso_a-peso_i:.1f}"

    )



    c2.metric(

        "🔥 % Grasa",

        f"{grasa_a}%",

        f"{grasa_a-grasa_i:.1f}"

    )



    c3.metric(

        "📏 Cintura",

        f"{cintura_a} cm",

        f"{cintura_a-cintura_i:.1f}"

    )



    c4.metric(

        "💪 Pecho",

        f"{pecho_a} cm",

        f"{pecho_a-pecho_i:.1f}"

    )





    st.divider()





    # ======================================
    # GRÁFICA
    # ======================================


    st.subheader(

        "📈 Tendencia"

    )



    columnas = [

        "peso_kg",

        "porcentaje_grasa",

        "cintura_cm",

        "pecho_cm"

    ]



    disponibles = [

        c

        for c in columnas

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





    st.divider()





    # ======================================
    # HISTORIAL
    # ======================================


    st.subheader(

        "📋 Historial completo"

    )



    st.dataframe(

        registros.astype(str),

        use_container_width=True

    )
