import streamlit as st
import pandas as pd

from database.resumen_cliente import resumen_cliente



def mostrar_evolucion():


    st.header(
        "📈 Mi Evolución Física"
    )


    usuario = st.session_state["usuario"]


    cedula = str(
        usuario["cedula"]
    )



    resumen = resumen_cliente(
        cedula
    )



    if "historial" not in resumen:


        st.info(
            "Todavía no tienes evaluaciones registradas."
        )

        return



    registros = resumen["historial"].copy()



    if registros.empty:


        st.info(
            "Todavía no tienes evaluaciones registradas."
        )

        return



    # =====================================
    # ORDEN CRONOLÓGICO
    # =====================================


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



    inicial = resumen.get(
        "inicial"
    )


    actual = resumen.get(
        "actual"
    )



    # =====================================
    # RESUMEN DE PROGRESO
    # =====================================


    st.subheader(
        "📊 Resumen de progreso"
    )



    if inicial is not None and actual is not None:



        def numero(
            fila,
            columna
        ):


            try:

                return float(
                    fila.get(
                        columna,
                        0
                    )
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



        col1, col2, col3 = st.columns(3)



        col1.metric(

            "⚖️ Peso",

            f"{peso_a:.1f} kg",

            f"{peso_a - peso_i:.1f} kg"

        )



        col2.metric(

            "🔥 Grasa corporal",

            f"{grasa_a:.1f} %",

            f"{grasa_a - grasa_i:.1f} %"

        )



        col3.metric(

            "📏 Cintura",

            f"{cintura_a:.1f} cm",

            f"{cintura_a - cintura_i:.1f} cm"

        )



        st.write("")



        resumen_tabla = pd.DataFrame({

            "Medida": [

                "Peso",

                "Grasa corporal",

                "Cintura"

            ],

            "Inicial": [

                f"{peso_i:.1f}",

                f"{grasa_i:.1f}",

                f"{cintura_i:.1f}"

            ],

            "Actual": [

                f"{peso_a:.1f}",

                f"{grasa_a:.1f}",

                f"{cintura_a:.1f}"

            ]

        })



        st.dataframe(

            resumen_tabla,

            hide_index=True,

            use_container_width=True

        )



    st.divider()



    # =====================================
    # GRÁFICAS
    # =====================================


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

        columna

        for columna in columnas

        if columna in datos.columns

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



    else:


        st.info(
            "No hay datos suficientes para generar gráficos."
        )



    st.divider()



    # =====================================
    # HISTORIAL COMPLETO
    # =====================================


    st.subheader(
        "📋 Historial completo"
    )



    st.dataframe(

        registros.astype(str),

        use_container_width=True,

        hide_index=True

    )
