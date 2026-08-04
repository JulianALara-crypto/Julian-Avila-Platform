import pandas as pd

from database.pagos import cargar_pagos
from database.planes import buscar_plan_cliente
from database.medidas import obtener_medidas_cliente



# ==========================================
# HISTORIAL COMPLETO CLIENTE
# ==========================================

def construir_historial_cliente(
    cedula
):


    historial = []



    cedula = str(cedula)



    # ======================================
    # PAGOS
    # ======================================

    pagos = cargar_pagos()


    if not pagos.empty:


        pagos_cliente = pagos[

            pagos["cedula"].astype(str)
            ==
            cedula

        ]


        for _, fila in pagos_cliente.iterrows():

            historial.append({

                "fecha": fila.get(
                    "fecha_pago"
                ),

                "tipo": "Pago",

                "descripcion": fila.get(
                    "concepto",
                    ""
                ),

                "valor": fila.get(
                    "valor",
                    0
                )

            })



    # ======================================
    # PLAN ACTUAL
    # ======================================

    plan = buscar_plan_cliente(
        cedula
    )


    if not plan.empty:


        fila = plan.iloc[0]


        historial.append({

            "fecha": fila.get(
                "fecha_inicio"
            ),

            "tipo": "Plan",

            "descripcion": fila.get(
                "tipo_plan",
                ""
            ),

            "valor": None

        })



    # ======================================
    # MEDIDAS
    # ======================================

    medidas = obtener_medidas_cliente(
        cedula
    )


    if not medidas.empty:


        for _, fila in medidas.iterrows():


            historial.append({

                "fecha": fila.get(
                    "fecha_evaluacion"
                ),

                "tipo": "Evaluación",

                "descripcion":
                    "Evaluación física",

                "valor": None

            })



    # ======================================
    # DATAFRAME FINAL
    # ======================================

    if not historial:

        return pd.DataFrame()



    df = pd.DataFrame(
        historial
    )



    if "fecha" in df.columns:


        df["fecha"] = pd.to_datetime(

            df["fecha"],

            errors="coerce"

        )


        df = df.sort_values(
            "fecha"
        )



    return df.reset_index(
        drop=True
    )
