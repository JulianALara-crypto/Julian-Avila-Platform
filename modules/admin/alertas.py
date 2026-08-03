import streamlit as st
import pandas as pd
import urllib.parse

from datetime import datetime, timedelta

from database.gimnasio import cargar_clientes_gym


def mostrar_alertas():

    st.header("🚨 Alertas de vencimiento")


    clientes = cargar_clientes_gym()


    if clientes.empty:

        st.info("No existen clientes registrados.")

        return


    hoy = datetime.today().date()


    clientes["fecha_dt"] = pd.to_datetime(

        clientes["fecha_vencimiento"],

        dayfirst=True,

        errors="coerce"

    ).dt.date


    alerta = clientes[

        clientes["fecha_dt"]

        <=

        hoy + timedelta(days=3)

    ]


    if alerta.empty:

        st.success("No existen clientes próximos a vencer.")

        return


    st.warning(

        f"Se encontraron {len(alerta)} clientes."

    )


    for _, fila in alerta.iterrows():

        estado = (

            "🔴 VENCIDO"

            if fila["fecha_dt"] < hoy

            else

            "🟡 POR VENCER"

        )


        telefono = str(

            fila["whatsapp"]

        ).replace(".0","")


        if not telefono.startswith("57"):

            telefono = "57"+telefono


        mensaje = (

            f"Hola {fila['nombre_completo']}, "

            f"tu plan vence el "

            f"{fila['fecha_vencimiento']}. "

            f"Te esperamos para renovarlo."

        )


        url = (

            "https://wa.me/"

            + telefono

            + "?text="

            + urllib.parse.quote(mensaje)

        )


        col1,col2 = st.columns([4,1])


        with col1:

            st.write(

                fila["nombre_completo"]

            )

            st.write(

                fila["fecha_vencimiento"]

            )

            st.write(

                estado

            )


        with col2:

            st.link_button(

                "WhatsApp",

                url,

                use_container_width=True

            )


        st.divider()
