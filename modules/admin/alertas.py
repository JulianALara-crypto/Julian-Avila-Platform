import streamlit as st
import pandas as pd
import urllib.parse

from datetime import datetime, timedelta

from database.gimnasio import cargar_clientes_gym
from database.planes import cargar_planes



# ==========================================
# ALERTAS DE VENCIMIENTO
# ==========================================

def mostrar_alertas():


    st.header(
        "🚨 Alertas de vencimiento"
    )


    hoy = datetime.today().date()



    dias_alerta = st.number_input(

        "Mostrar vencimientos dentro de los próximos días",

        min_value=1,

        value=3

    )



    limite = hoy + timedelta(
        days=dias_alerta
    )



    # ======================================
    # MEMBRESÍAS GIMNASIO
    # ======================================

    st.subheader(
        "🏋️ Membresías gimnasio"
    )



    clientes = cargar_clientes_gym()



    if not clientes.empty:


        clientes["fecha_dt"] = pd.to_datetime(

            clientes["fecha_vencimiento"],

            dayfirst=True,

            errors="coerce"

        ).dt.date



        alertas_clientes = clientes[

            clientes["fecha_dt"]

            <=

            limite

        ]



        if alertas_clientes.empty:


            st.success(
                "No hay membresías próximas a vencer."
            )


        else:


            st.warning(

                f"{len(alertas_clientes)} membresías requieren atención."

            )



            for _, fila in alertas_clientes.iterrows():


                fecha = fila["fecha_dt"]



                estado = (

                    "🔴 VENCIDO"

                    if fecha < hoy

                    else

                    "🟡 POR VENCER"

                )



                st.write(

                    f"👤 {fila['nombre_completo']}"

                )


                st.write(

                    f"📅 Vence: {fila['fecha_vencimiento']}"

                )


                st.write(
                    estado
                )



                telefono = str(
                    fila.get(
                        "whatsapp",
                        ""
                    )
                ).replace(
                    ".0",
                    ""
                )



                if telefono:


                    if not telefono.startswith("57"):

                        telefono = "57" + telefono



                    mensaje = (

                        f"Hola {fila['nombre_completo']}, "

                        f"te informamos que tu membresía "

                        f"vence el {fila['fecha_vencimiento']}."

                    )



                    url = (

                        "https://wa.me/"

                        +

                        telefono

                        +

                        "?text="

                        +

                        urllib.parse.quote(
                            mensaje
                        )

                    )



                    st.link_button(

                        "📲 WhatsApp",

                        url

                    )



                st.divider()



    else:


        st.info(
            "No hay clientes registrados."
        )





    # ======================================
    # PLANES PERSONAL TRAINING
    # ======================================


    st.subheader(
        "🏋️‍♂️ Planes Personal Training"
    )



    planes = cargar_planes()



    if planes.empty:


        st.info(
            "No existen planes registrados."
        )

        return



    planes["fecha_dt"] = pd.to_datetime(

        planes["fecha_fin"],

        dayfirst=True,

        errors="coerce"

    ).dt.date



    alertas_planes = planes[

        planes["fecha_dt"]

        <=

        limite

    ]



    if alertas_planes.empty:


        st.success(
            "No hay planes próximos a vencer."
        )

        return



    st.warning(

        f"{len(alertas_planes)} planes requieren atención."

    )



    for _, fila in alertas_planes.iterrows():


        fecha = fila["fecha_dt"]



        estado = (

            "🔴 VENCIDO"

            if fecha < hoy

            else

            "🟡 POR VENCER"

        )



        st.write(

            f"👤 {fila['nombre_completo']}"

        )


        st.write(

            f"🏋️ Plan: {fila['tipo_plan']}"

        )


        st.write(

            f"📅 Finaliza: {fila['fecha_fin']}"

        )


        st.write(
            estado
        )


        st.divider()
