import streamlit as st
import pandas as pd
from datetime import datetime

from database.gimnasio import cargar_clientes_gym
from database.pagos import registrar_pago



# ==========================================
# PAGOS Y CONTABILIDAD ADMIN
# ==========================================

def mostrar_pagos():


    st.header(
        "💳 Pagos y Contabilidad"
    )


    clientes = cargar_clientes_gym()



    if clientes.empty:

        st.warning(
            "No existen clientes registrados."
        )

        return



    # ======================================
    # NORMALIZAR DATOS
    # ======================================

    clientes["valor_pagado"] = pd.to_numeric(
        clientes["valor_pagado"],
        errors="coerce"
    ).fillna(0)



    total_clientes = len(clientes)


    ingresos = clientes["valor_pagado"].sum()



    activos = 0


    hoy = datetime.today().date()



    for fecha in clientes["fecha_vencimiento"]:

        try:

            vencimiento = datetime.strptime(
                fecha,
                "%d-%m-%Y"
            ).date()


            if vencimiento >= hoy:

                activos += 1


        except:

            pass



    # ======================================
    # MÉTRICAS
    # ======================================

    col1, col2, col3 = st.columns(3)


    col1.metric(
        "👥 Clientes",
        total_clientes
    )


    col2.metric(
        "🟢 Activos",
        activos
    )


    col3.metric(
        "💰 Ingresos registrados",
        f"${int(ingresos):,}"
    )



    st.divider()



    # ======================================
    # TABLA CLIENTES
    # ======================================

    st.subheader(
        "📋 Pagos actuales"
    )


    columnas = [

        "nombre_completo",
        "cedula",
        "fecha_ingreso",
        "valor_pagado",
        "metodo_pago",
        "fecha_vencimiento"

    ]



    disponibles = [

        columna

        for columna in columnas

        if columna in clientes.columns

    ]



    st.dataframe(

        clientes[disponibles],

        use_container_width=True

    )



    st.divider()



    # ======================================
    # NUEVO PAGO
    # ======================================

    st.subheader(
        "➕ Registrar nuevo pago"
    )



    cliente_pago = st.selectbox(

        "Cliente",

        clientes["nombre_completo"].tolist()

    )



    valor = st.number_input(

        "Valor del pago",

        min_value=0,

        step=1000

    )



    concepto = st.selectbox(

        "Concepto",

        [

            "Pago Personalizado",

            "Abono mensualidad",

            "Otro"

        ]

    )



    if st.button(
        "Guardar pago"
    ):


        cliente = clientes[
            clientes["nombre_completo"]
            ==
            cliente_pago
        ].iloc[0]



        resultado = registrar_pago(

            cliente["cedula"],

            cliente["nombre_completo"],

            valor,

            concepto

        )



        if resultado.get("status") == "success":


            st.success(
                "✅ Pago guardado correctamente"
            )


            st.cache_data.clear()



        else:


            st.error(
                resultado
            )
