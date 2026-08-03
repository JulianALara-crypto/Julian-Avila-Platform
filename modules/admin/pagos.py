import streamlit as st
import pandas as pd


from database.gimnasio import cargar_clientes_gym
from database.pagos import (
    cargar_pagos,
    registrar_pago
)



# ==========================================
# PAGOS Y CONTABILIDAD
# ==========================================

def mostrar_pagos():


    st.header(
        "💳 Pagos y Contabilidad"
    )


    clientes = cargar_clientes_gym()

    pagos = cargar_pagos()



    # ======================================
    # MÉTRICAS
    # ======================================

    col1,col2,col3 = st.columns(3)



    if not pagos.empty:


        total_pagado = pagos["valor"].sum()


    else:

        total_pagado = 0



    col1.metric(
        "💰 Total recaudado",
        f"${int(total_pagado):,}"
    )


    col2.metric(
        "👥 Clientes",
        len(clientes)
    )


    col3.metric(
        "🧾 Pagos registrados",
        len(pagos)
    )



    st.divider()



    # ======================================
    # REGISTRAR NUEVO PAGO
    # ======================================

    st.subheader(
        "➕ Registrar nuevo pago"
    )


    if clientes.empty:

        st.warning(
            "No existen clientes registrados."
        )

        return



    cliente_nombre = st.selectbox(

        "Seleccionar cliente",

        clientes["nombre_completo"].tolist()

    )



    cliente = clientes[
        clientes["nombre_completo"]
        ==
        cliente_nombre
    ].iloc[0]



    valor = st.number_input(

        "Valor del pago",

        min_value=0,

        step=1000

    )



    concepto = st.selectbox(

        "Concepto",

        [

            "Mensualidad",

            "Abono personalizado",

            "Pago parcial",

            "Otro"

        ]

    )



    if st.button(
        "💾 Guardar pago"
    ):



        resultado = registrar_pago(

            cliente["cedula"],

            cliente["nombre_completo"],

            valor,

            concepto

        )



        if resultado.get("status") == "success":


            st.success(
                "Pago registrado correctamente."
            )


            st.cache_data.clear()

            st.rerun()



        else:

            st.error(
                resultado
            )



    st.divider()



    # ======================================
    # HISTORIAL PAGOS
    # ======================================


    st.subheader(
        "📋 Historial de pagos"
    )



    if pagos.empty:


        st.info(
            "Aún no existen pagos registrados."
        )


    else:


        filtro = st.selectbox(

            "Filtrar cliente",

            [

                "Todos"

            ]
            +
            pagos["nombre_completo"]
            .unique()
            .tolist()

        )



        tabla = pagos.copy()



        if filtro != "Todos":

            tabla = tabla[
                tabla["nombre_completo"]
                ==
                filtro
            ]



        st.dataframe(

            tabla,

            use_container_width=True

        )



        st.divider()



        st.subheader(
            "📈 Ingresos"
        )



        grafica = (
            pagos
            .groupby(
                "fecha_pago"
            )["valor"]
            .sum()
        )


        st.line_chart(
            grafica
        )
