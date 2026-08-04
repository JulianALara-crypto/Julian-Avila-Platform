import pandas as pd

from database.medidas import obtener_medidas_cliente
from database.gimnasio import buscar_cliente_gym
from database.planes import buscar_plan_cliente
from database.pagos import cargar_pagos




# ==========================================
# RESUMEN COMPLETO CLIENTE
# ==========================================

def resumen_cliente(cedula):


    datos = {}



    cedula = str(
        cedula
    )



    # ======================================
    # CLIENTE
    # ======================================


    cliente = buscar_cliente_gym(
        cedula
    )


    if not cliente.empty:


        datos["cliente"] = cliente.iloc[0]





    # ======================================
    # PLAN PERSONALIZADO
    # ======================================


    plan = buscar_plan_cliente(
        cedula
    )


    if not plan.empty:


        plan = plan.sort_values(
            "fecha_inicio"
        )


        datos["plan"] = plan.iloc[-1]





    # ======================================
    # MEDIDAS FÍSICAS
    # ======================================


    medidas = obtener_medidas_cliente(
        cedula
    )



    if not medidas.empty:


        if "fecha_evaluacion" in medidas.columns:


            medidas["_fecha"] = pd.to_datetime(

                medidas["fecha_evaluacion"],

                dayfirst=True,

                errors="coerce"

            )


            medidas = (

                medidas

                .sort_values("_fecha")

                .drop(columns="_fecha")

            )


        else:


            medidas = medidas.sort_index()



        datos["inicial"] = medidas.iloc[0]


        datos["actual"] = medidas.iloc[-1]


        datos["historial"] = medidas





    # ======================================
    # PAGOS
    # ======================================


    pagos = cargar_pagos()



    if not pagos.empty and "cedula" in pagos.columns:


        pagos_cliente = pagos[

            pagos["cedula"].astype(str)

            ==

            cedula

        ]


        if not pagos_cliente.empty:


            datos["pagos"] = pagos_cliente





    return datos
