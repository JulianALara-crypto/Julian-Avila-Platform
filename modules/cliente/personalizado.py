import streamlit as st
from datetime import datetime

from database.planes import buscar_plan_cliente



# ==========================================
# MI PLAN PERSONALIZADO CLIENTE
# ==========================================

def mostrar_personalizado():


    st.header(
        "🏋️ Mi Entrenamiento Personalizado"
    )



    usuario = st.session_state["usuario"]



    cedula = str(
        usuario["cedula"]
    )



    # ======================================
    # BUSCAR PLAN
    # ======================================

    plan = buscar_plan_cliente(
        cedula
    )



    if plan.empty:


        st.info(
            "Actualmente no tienes un plan personalizado activo."
        )

        return



    datos = plan.iloc[-1]



    st.subheader(
        "📋 Información del plan"
    )



    tipo_plan = datos.get(
        "tipo_plan",
        "Personal Training"
    )


    fecha_inicio = datos.get(
        "fecha_inicio",
        ""
    )


    fecha_fin = datos.get(
        "fecha_fin",
        ""
    )


    estado = datos.get(
        "estado",
        "Activo"
    )


    observaciones = datos.get(
        "observaciones",
        ""
    )



    # ======================================
    # DATOS PRINCIPALES
    # ======================================


    col1,col2,col3 = st.columns(3)



    col1.metric(
        "🏋️ Tipo de Plan",
        tipo_plan
    )


    col2.metric(
        "📅 Inicio",
        fecha_inicio
    )


    col3.metric(
        "⏳ Finaliza",
        fecha_fin
    )



    st.divider()



    # ======================================
    # ESTADO DEL PLAN
    # ======================================


    st.subheader(
        "📌 Estado"
    )


    if estado == "Activo":


        st.success(
            "🟢 Plan activo"
        )


    else:


        st.warning(
            f"Estado: {estado}"
        )




    # ======================================
    # DÍAS RESTANTES
    # ======================================


    try:


        vencimiento = datetime.strptime(
            fecha_fin,
            "%d-%m-%Y"
        ).date()



        hoy = datetime.today().date()



        dias = (
            vencimiento - hoy
        ).days



        if dias < 0:


            st.error(
                "🔴 Tu plan está vencido."
            )


        elif dias <= 5:


            st.warning(
                f"🟡 Tu plan vence en {dias} días."
            )


        else:


            st.success(
                f"🟢 Te quedan {dias} días de entrenamiento."
            )



    except:


        st.info(
            "No fue posible calcular los días restantes."
        )



    st.divider()



    # ======================================
    # OBSERVACIONES
    # ======================================


    st.subheader(
        "📝 Observaciones del entrenador"
    )



    if observaciones:


        st.info(
            observaciones
        )


    else:


        st.write(
            "Sin observaciones registradas."
        )



    st.divider()



    st.caption(
        """
        Tu entrenamiento personalizado es gestionado
        directamente por Julian Avila.
        """
    )
