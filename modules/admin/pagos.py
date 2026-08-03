import streamlit as st
from datetime import datetime

from database.gimnasio import (
    cargar_clientes_gym,
    enviar_accion_gym
)



def mostrar_pagos():


    st.header(
        "💳 Pagos y Contabilidad"
    )


    clientes = cargar_clientes_gym()



    if clientes.empty:

        st.info(
            "No existen clientes registrados."
        )

        return



    cliente_sel = st.selectbox(
        "Seleccionar Cliente:",
        clientes["cedula"].astype(str)
        +
        " - "
        +
        clientes["nombre_completo"]
    )



    cedula = (
        cliente_sel
        .split("-")[0]
        .strip()
    )


    cliente = clientes[
        clientes["cedula"].astype(str)
        ==
        cedula
    ].iloc[0]



    st.divider()



    st.subheader(
        f"👤 {cliente['nombre_completo']}"
    )



    with st.form(
        "nuevo_pago"
    ):


        valor = st.number_input(
            "Valor del pago:",
            min_value=0,
            step=1000
        )


        metodo = st.selectbox(
            "Método de pago:",
            [
                "Efectivo",
                "Transferencia",
                "Nequi",
                "DaviPlata",
                "Tarjeta",
                "Otro"
            ]
        )



        observacion = st.text_area(
            "Observación:"
        )



        guardar = st.form_submit_button(
            "Registrar Pago"
        )



        if guardar:


            fecha = datetime.today().strftime(
                "%d-%m-%Y"
            )


            id_pago = (
                f"{cedula}_"
                +
                datetime.today().strftime(
                    "%Y%m%d%H%M%S"
                )
            )



            fila = [

                id_pago,

                cedula,

                cliente["nombre_completo"],

                fecha,

                valor,

                metodo,

                observacion

            ]



            resultado = enviar_accion_gym(

                "registrar_pago",

                {
                    "row": fila
                }

            )



            if "error" not in resultado:


                st.success(
                    "✅ Pago registrado correctamente"
                )


                st.cache_data.clear()



            else:


                st.error(
                    resultado["error"]
                )
