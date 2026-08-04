import streamlit as st
import pandas as pd
import urllib.parse

from datetime import datetime, timedelta

from database.gimnasio import cargar_clientes_gym
from database.planes import cargar_planes
from database.medidas import cargar_medidas



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

        clientes = clientes.copy()

        clientes["fecha_dt"] = pd.to_datetime(

            clientes["fecha_vencimiento"],

            dayfirst=True,

            errors="coerce"

        ).dt.date

        alertas_clientes = clientes[
            clientes["fecha_dt"] <= limite
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

                        f"te recordamos que tu membresía "

                        f"vence el {fila['fecha_vencimiento']}. "

                        f"Si deseas renovarla puedes comunicarte con nosotros."

                    )

                    url = (

                        "https://wa.me/"

                        + telefono

                        + "?text="

                        + urllib.parse.quote(
                            mensaje
                        )

                    )

                    st.link_button(
                        "📲 Enviar WhatsApp",
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

    else:

        planes = planes.copy()

        planes["fecha_dt"] = pd.to_datetime(

            planes["fecha_fin"],

            dayfirst=True,

            errors="coerce"

        ).dt.date

        alertas_planes = planes[
            planes["fecha_dt"] <= limite
        ]

        if alertas_planes.empty:

            st.success(
                "No hay planes próximos a vencer."
            )

        else:

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



    # ======================================
    # CLIENTES SIN EVALUACIÓN FÍSICA
    # ======================================

    st.subheader(
        "📈 Clientes sin evaluación física"
    )

    medidas = cargar_medidas()

    if clientes.empty:

        st.info(
            "No existen clientes registrados."
        )

    else:

        if medidas.empty:

            sin_medidas = clientes.copy()

        else:

            cedulas_medidas = (
                medidas["cedula"]
                .astype(str)
                .unique()
            )

            sin_medidas = clientes[
                ~clientes["cedula"]
                .astype(str)
                .isin(cedulas_medidas)
            ]

        if sin_medidas.empty:

            st.success(
                "Todos los clientes tienen al menos una evaluación física."
            )

        else:

            st.warning(
                f"{len(sin_medidas)} clientes aún no tienen evaluación."
            )

            st.dataframe(

                sin_medidas[
                    [
                        "cedula",
                        "nombre_completo",
                        "whatsapp",
                        "fecha_ingreso"
                    ]
                ],

                hide_index=True,

                use_container_width=True

            )



    st.divider()



    # ======================================
    # CLIENTES SIN PERSONAL TRAINING
    # ======================================

    st.subheader(
        "💪 Clientes sin Personal Training"
    )

    if clientes.empty:

        st.info(
            "No existen clientes registrados."
        )

    else:

        if planes.empty:

            sin_plan = clientes.copy()

        else:

            cedulas_plan = (
                planes["cedula"]
                .astype(str)
                .unique()
            )

            sin_plan = clientes[
                ~clientes["cedula"]
                .astype(str)
                .isin(cedulas_plan)
            ]

        if sin_plan.empty:

            st.success(
                "Todos los clientes tienen un plan personalizado."
            )

        else:

            st.info(
                f"{len(sin_plan)} clientes son candidatos para Personal Training."
            )

            st.dataframe(

                sin_plan[
                    [
                        "cedula",
                        "nombre_completo",
                        "whatsapp",
                        "fecha_ingreso"
                    ]
                ],

                hide_index=True,

                use_container_width=True

            )
