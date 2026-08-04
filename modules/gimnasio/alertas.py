import streamlit as st
import pandas as pd

from datetime import datetime, timedelta

from database.gimnasio import cargar_clientes_gym
from database.planes import cargar_planes
from database.pagos import cargar_pagos
from database.medidas import cargar_medidas




# ==========================================
# ALERTAS GIMNASIO
# ==========================================

def mostrar_alertas():


    st.header(
        "🚨 Alertas del Gimnasio"
    )



    hoy = datetime.today()



    clientes = cargar_clientes_gym()

    planes = cargar_planes()

    pagos = cargar_pagos()

    medidas = cargar_medidas()



    alertas_planes = []

    alertas_medidas = []

    alertas_pagos = []



    # ======================================
    # ALERTAS PLANES
    # ======================================


    if not planes.empty:


        for _, fila in planes.iterrows():


            try:


                fecha_fin = pd.to_datetime(

                    fila["fecha_fin"],

                    dayfirst=True

                )


                dias = (

                    fecha_fin - hoy

                ).days



                if dias < 0:


                    alertas_planes.append({

                        "Cliente":

                            fila["nombre_completo"],

                        "Alerta":

                            "Plan vencido",

                        "Días":

                            dias

                    })



                elif dias <= 7:


                    alertas_planes.append({

                        "Cliente":

                            fila["nombre_completo"],

                        "Alerta":

                            "Vence pronto",

                        "Días":

                            dias

                    })



            except:

                pass





    # ======================================
    # ALERTAS EVALUACIONES
    # ======================================


    clientes_con_medidas = set()



    if not medidas.empty and "cedula" in medidas.columns:


        clientes_con_medidas = set(

            medidas["cedula"]

            .astype(str)

            .tolist()

        )



    for _, cliente in clientes.iterrows():


        cedula = str(

            cliente["cedula"]

        )



        if cedula not in clientes_con_medidas:


            alertas_medidas.append({

                "Cliente":

                    cliente["nombre_completo"],

                "Alerta":

                    "Sin evaluación física"

            })





    # ======================================
    # ALERTAS PAGOS
    # ======================================


    clientes_con_pago = set()



    if not pagos.empty and "cedula" in pagos.columns:


        clientes_con_pago = set(

            pagos["cedula"]

            .astype(str)

            .tolist()

        )



    for _, cliente in clientes.iterrows():


        cedula = str(

            cliente["cedula"]

        )



        if cedula not in clientes_con_pago:


            alertas_pagos.append({

                "Cliente":

                    cliente["nombre_completo"],

                "Alerta":

                    "Sin pagos registrados"

            })





    # ======================================
    # MOSTRAR RESULTADOS
    # ======================================


    st.subheader(
        "🏋️ Planes"
    )


    if alertas_planes:


        st.dataframe(

            pd.DataFrame(alertas_planes),

            use_container_width=True,

            hide_index=True

        )


    else:


        st.success(
            "No hay alertas de planes."
        )



    st.divider()



    st.subheader(
        "📈 Evaluaciones físicas"
    )


    if alertas_medidas:


        st.dataframe(

            pd.DataFrame(alertas_medidas),

            use_container_width=True,

            hide_index=True

        )


    else:


        st.success(

            "Todos los clientes tienen evaluaciones."

        )



    st.divider()



    st.subheader(
        "💰 Pagos"
    )


    if alertas_pagos:


        st.dataframe(

            pd.DataFrame(alertas_pagos),

            use_container_width=True,

            hide_index=True

        )


    else:


        st.success(

            "Todos los clientes tienen pagos."

        )
