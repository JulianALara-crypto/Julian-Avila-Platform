import streamlit as st

from database.gimnasio import cargar_clientes_gym



def mostrar_dashboard():


    st.header(
        "📊 Dashboard Administrativo"
    )


    clientes = cargar_clientes_gym()


    if clientes.empty:

        st.info(
            "No hay información registrada todavía."
        )

        return



    total_clientes = len(clientes)



    st.metric(
        "👥 Total Clientes",
        total_clientes
    )



    if "valor_pagado" in clientes.columns:


        valores = (
            clientes["valor_pagado"]
            .astype(float)
            .fillna(0)
        )


        total = valores.sum()


        st.metric(
            "💰 Ingresos registrados",
            f"${int(total):,}"
        )



    st.divider()


    st.subheader(
        "Últimos registros"
    )


    st.dataframe(
        clientes,
        use_container_width=True
    )
