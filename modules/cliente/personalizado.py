import streamlit as st
from datetime import datetime, timedelta

from database.gimnasio import buscar_cliente_gym



def mostrar_personalizado():


    st.header(
        "🏋️ Mi Entrenamiento Personalizado"
    )


    usuario = st.session_state["usuario"]


    cedula = str(
        usuario["cedula"]
    )



    cliente = buscar_cliente_gym(
        cedula
    )



    if cliente.empty:

        st.info(
            "Actualmente no tienes un plan personalizado activo."
        )

        return



    datos = cliente.iloc[0]



    st.subheader(
        "Información del plan"
    )



    # --------------------------------
    # PLAN
    # --------------------------------


    plan = datos.get(
        "plan",
        "Personal Training"
    )



    fecha_inicio = datos.get(
        "fecha_inicio",
        ""
    )



    fecha_vencimiento = datos.get(
        "fecha_vencimiento",
        ""
    )



    col1,col2,col3 = st.columns(3)



    col1.metric(
        "🏋️ Tipo de Plan",
        plan
    )


    col2.metric(
        "📅 Inicio",
        fecha_inicio
    )


    col3.metric(
        "⏳ Vencimiento",
        fecha_vencimiento
    )



    st.divider()



    # --------------------------------
    # ESTADO
    # --------------------------------


    try:

        vencimiento = datetime.strptime(
            fecha_vencimiento,
            "%d-%m-%Y"
        ).date()


        hoy = datetime.today().date()


        dias = (
            vencimiento - hoy
        ).days



        if dias < 0:

            st.error(
                "🔴 Tu plan personalizado está vencido."
            )


        elif dias <= 5:

            st.warning(
                f"🟡 Tu plan vence en {dias} días."
            )


        else:

            st.success(
                f"🟢 Plan activo. Restan {dias} días."
            )


    except:

        st.info(
            "Estado pendiente de actualización."
        )



    st.divider()



    st.subheader(
        "Información"
    )


    st.write(
        """
        Tu entrenamiento personalizado es gestionado
        directamente por Julian Avila.

        La fecha de vencimiento corresponde al periodo
        contratado de 30 días.
        """
    )
