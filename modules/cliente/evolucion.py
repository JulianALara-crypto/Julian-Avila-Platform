import streamlit as st
import pandas as pd

from database.medidas import obtener_medidas_cliente



def mostrar_evolucion():


    st.header(
        "📈 Mi Evolución Física"
    )


    usuario = st.session_state["usuario"]


    cedula = str(
        usuario["cedula"]
    )


    registros = obtener_medidas_cliente(
        cedula
    )



    if registros.empty:

        st.info(
            "Todavía no tienes evaluaciones registradas."
        )

        return



    # ==============================
    # ORDEN CRONOLÓGICO
    # ==============================


    if "fecha_evaluacion" in registros.columns:


        registros["_fecha"] = pd.to_datetime(
            registros["fecha_evaluacion"],
            errors="coerce",
            dayfirst=True
        )


        registros = (
            registros
            .sort_values(
                "_fecha"
            )
            .drop(
                columns=["_fecha"]
            )
        )



    st.subheader(
        "📊 Resumen de progreso"
    )



    if len(registros) >= 2:


        inicial = registros.iloc[0]

        actual = registros.iloc[-1]



        def numero(
            fila,
            columna
        ):

            try:

                return float(
                    fila[columna]
                )

            except:

                return 0



        peso_i = numero(
            inicial,
            "peso_kg"
        )

        peso_a = numero(
            actual,
            "peso_kg"
        )



        grasa_i = numero(
            inicial,
            "porcentaje_grasa"
        )

        grasa_a = numero(
            actual,
            "porcentaje_grasa"
        )



        cintura_i = numero(
            inicial,
            "cintura_cm"
        )

        cintura_a = numero(
            actual,
            "cintura_cm"
        )



        c1,c2,c3 = st.columns(3)



        c1.metric(
            "Peso actual",
            f"{peso_a} kg",
            f"{peso_a-peso_i:.1f}"
        )


        c2.metric(
            "% Grasa",
            f"{grasa_a} %",
            f"{grasa_a-grasa_i:.1f}"
        )


        c3.metric(
            Cintura",
            f"{cintura_a} cm",
            f"{cintura_a-cintura_i:.1f}"
        )



    st.divider()



    # ==============================
    # GRÁFICAS
    # ==============================


    st.subheader(
        "📈 Tendencia"
    )


    datos = registros.copy()



    if "fecha_evaluacion" in datos.columns:


        datos = datos.set_index(
            "fecha_evaluacion"
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
        if c in datos.columns

    ]



    if disponibles:


        datos_grafica = datos[
            disponibles
        ].apply(
            pd.to_numeric,
            errors="coerce"
        )


        st.line_chart(
            datos_grafica
        )



    st.divider()



    st.subheader(
        "📋 Historial completo"
    )


    st.dataframe(
        registros.astype(str),
        use_container_width=True
    )
