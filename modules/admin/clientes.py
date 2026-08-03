import streamlit as st

from database.usuarios import cargar_usuarios
from database.gimnasio import buscar_cliente_gym
from database.medidas import obtener_medidas_cliente



def mostrar_clientes():

    st.header(
        "👥 Gestión de Clientes"
    )


    usuarios = cargar_usuarios()


    if usuarios.empty:

        st.warning(
            "No hay usuarios registrados."
        )

        return



    clientes = usuarios[
        usuarios["rol"]
        .astype(str)
        .str.lower()
        ==
        "cliente"
    ]



    if clientes.empty:

        st.info(
            "No existen clientes."
        )

        return



    seleccion = st.selectbox(
        "Buscar cliente:",
        clientes["cedula"].astype(str)
        +
        " - "
        +
        clientes["nombre_completo"]
    )



    cedula = (
        seleccion
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



    col1,col2,col3 = st.columns(3)


    with col1:

        st.write(
            "🪪 Cédula:"
        )

        st.write(
            cedula
        )


        st.write(
            "📱 WhatsApp:"
        )

        st.write(
            cliente.get(
                "whatsapp",
                "No registra"
            )
        )


    with col2:

        st.write(
            "🏥 EPS:"
        )

        st.write(
            cliente.get(
                "eps",
                "No registra"
            )
        )


        st.write(
            "📅 Registro:"
        )

        st.write(
            cliente.get(
                "fecha_registro",
                ""
            )
        )


    with col3:

        st.write(
            "🩺 Condiciones:"
        )

        st.write(
            cliente.get(
                "condiciones_medicas",
                "Ninguna"
            )
        )



    st.divider()



    # ==============================
    # INFORMACIÓN GYM
    # ==============================


    st.subheader(
        "🏋️ Información Gimnasio"
    )


    gym = buscar_cliente_gym(
        cedula
    )


    if not gym.empty:


        datos_gym = gym.iloc[0]


        c1,c2,c3 = st.columns(3)


        c1.metric(
            "Fecha Inicio",
            datos_gym["fecha_ingreso"]
        )


        c2.metric(
            "Vencimiento",
            datos_gym["fecha_vencimiento"]
        )


        c3.metric(
            "Valor Último Pago",
            datos_gym["valor_pagado"]
        )


    else:

        st.info(
            "No tiene registro de gimnasio."
        )



    st.divider()



    # ==============================
    # MEDIDAS
    # ==============================


    st.subheader(
        "📏 Evolución Física"
    )


    medidas = obtener_medidas_cliente(
        cedula
    )


    if not medidas.empty:

        st.dataframe(
            medidas,
            use_container_width=True
        )

    else:

        st.info(
            "Sin evaluaciones físicas."
        )
