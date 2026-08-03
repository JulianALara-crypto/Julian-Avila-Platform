import streamlit as st
from datetime import datetime, timedelta

from database.gimnasio import cargar_clientes_gym
from database.planes import cargar_planes



# ==========================================
# PLANES DISPONIBLES
# ==========================================

PLANES = [

    "Personalizado Básico",

    "Personalizado Premium",

    "Online",

    "Competición"

]



# ==========================================
# MÓDULO ADMIN PERSONAL TRAINING
# ==========================================

def mostrar_personal_training():


    st.header(
        "🏋️ Gestión Personal Training"
    )



    clientes = cargar_clientes_gym()



    if clientes.empty:

        st.warning(
            "No existen clientes registrados."
        )

        return




    # ======================================
    # BUSCAR CLIENTE
    # ======================================


    cedula = st.text_input(
        "Buscar cliente por cédula"
    )



    if not cedula:


        st.info(
            "Ingrese una cédula para comenzar."
        )

        return




    cliente = clientes[

        clientes["cedula"].astype(str)
        ==
        str(cedula)

    ]



    if cliente.empty:


        st.warning(
            "Cliente no encontrado."
        )

        return




    datos = cliente.iloc[0]



    st.divider()



    st.subheader(
        "👤 Cliente"
    )


    st.write(
        datos["nombre_completo"]
    )



    # ======================================
    # PLAN ACTUAL
    # ======================================


    planes = cargar_planes()



    plan_actual = None



    if not planes.empty:


        encontrado = planes[

            planes["cedula"].astype(str)
            ==
            str(cedula)

        ]


        if not encontrado.empty:

            plan_actual = encontrado.iloc[0]




    st.divider()



    st.subheader(
        "🏋️ Plan actual"
    )



    if plan_actual is not None:


        st.success(
            plan_actual["tipo_plan"]
        )


        col1,col2 = st.columns(2)


        col1.write(
            f"Inicio: {plan_actual['fecha_inicio']}"
        )


        col2.write(
            f"Fin: {plan_actual['fecha_fin']}"
        )


        st.write(
            f"Estado: {plan_actual['estado']}"
        )



    else:


        st.info(
            "Cliente sin plan personalizado."
        )




    st.divider()



    # ======================================
    # CREAR / ACTUALIZAR PLAN
    # ======================================


    st.subheader(
        "➕ Asignar nuevo plan"
    )



    tipo_plan = st.selectbox(

        "Tipo de plan",

        PLANES

    )



    dias = st.number_input(

        "Duración (días)",

        min_value=1,

        value=30

    )



    observaciones = st.text_area(

        "Observaciones del entrenador"

    )



    if st.button(
        "Guardar Plan",
        use_container_width=True
    ):



        fecha_inicio = datetime.today()

        fecha_fin = (
            fecha_inicio
            +
            timedelta(days=dias)
        )



        st.info(
            "Conexión preparada. Siguiente paso: guardar en Google Sheets."
        )


        st.write({

            "cedula":cedula,

            "nombre":datos["nombre_completo"],

            "plan":tipo_plan,

            "inicio":
                fecha_inicio.strftime("%d-%m-%Y"),

            "fin":
                fecha_fin.strftime("%d-%m-%Y"),

            "observaciones":
                observaciones

        })
