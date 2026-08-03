import streamlit as st
from datetime import datetime, timedelta

from database.gimnasio import cargar_clientes_gym
from database.planes import (
    cargar_planes,
    crear_plan,
    renovar_plan
)
from database.resumen_cliente import resumen_cliente



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
    # RESUMEN FÍSICO DEL CLIENTE
    # ======================================


    resumen = resumen_cliente(
        cedula
    )



    if "actual" in resumen:


        actual = resumen["actual"]

        inicial = resumen["inicial"]



        st.divider()


        st.subheader(
            "📊 Estado físico actual"
        )



        col1,col2,col3,col4 = st.columns(4)



        try:

            cambio_peso = (

                float(actual.get("peso_kg",0))

                -

                float(inicial.get("peso_kg",0))

            )

        except:

            cambio_peso = 0



        try:

            cambio_grasa = (

                float(actual.get("porcentaje_grasa",0))

                -

                float(inicial.get("porcentaje_grasa",0))

            )

        except:

            cambio_grasa = 0



        try:

            cambio_cintura = (

                float(actual.get("cintura_cm",0))

                -

                float(inicial.get("cintura_cm",0))

            )

        except:

            cambio_cintura = 0




        col1.metric(

            "⚖️ Peso",

            f"{actual.get('peso_kg','')} kg",

            f"{cambio_peso:.1f}"

        )



        col2.metric(

            "🔥 % Grasa",

            f"{actual.get('porcentaje_grasa','')} %",

            f"{cambio_grasa:.1f}"

        )



        col3.metric(

            "📏 Cintura",

            f"{actual.get('cintura_cm','')} cm",

            f"{cambio_cintura:.1f}"

        )



        col4.metric(

            "📊 IMC",

            actual.get(
                "imc",
                ""
            )

        )



    else:


        st.info(

            "Este cliente todavía no tiene evaluaciones físicas."

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

            plan_actual.get(

                "tipo_plan",

                "Sin nombre"

            )

        )



        col1,col2 = st.columns(2)



        col1.write(

            f"📅 Inicio: {plan_actual.get('fecha_inicio','')}"

        )



        col2.write(

            f"⏳ Fin: {plan_actual.get('fecha_fin','')}"

        )



        st.write(

            f"Estado: {plan_actual.get('estado','Activo')}"

        )



        if plan_actual.get("observaciones"):


            st.write(
                "📝 Observaciones:"
            )


            st.info(

                plan_actual["observaciones"]

            )



    else:



        st.info(

            "Cliente sin plan personalizado."

        )




    st.divider()



    # ======================================
    # CREAR PLAN
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

            timedelta(days=int(dias))

        )



        nuevo_plan = {


            "cedula":

                str(cedula),



            "nombre_completo":

                datos["nombre_completo"],



            "tipo_plan":

                tipo_plan,



            "fecha_inicio":

                fecha_inicio.strftime(

                    "%d-%m-%Y"

                ),



            "fecha_fin":

                fecha_fin.strftime(

                    "%d-%m-%Y"

                ),



            "estado":

                "Activo",



            "observaciones":

                observaciones

        }




        resultado = crear_plan(

            nuevo_plan

        )



        if isinstance(resultado, dict) and resultado.get("status") == "success":


            st.success(

                "✅ Plan guardado correctamente."

            )


            cargar_planes.clear()


            st.rerun()



        else:


            st.error(

                f"❌ Error guardando plan: {resultado}"

            )
