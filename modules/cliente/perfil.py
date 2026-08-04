import streamlit as st

from database.usuarios import cargar_usuarios
from database.gimnasio import buscar_cliente_gym
from database.historial import construir_historial_cliente



def formatear_fecha(valor):

    if valor is None:
        return ""

    try:

        fecha = str(valor).split(" ")[0]

        partes = fecha.split("-")

        if len(partes) == 3:

            return f"{partes[2]}-{partes[1]}-{partes[0]}"

        return valor

    except:

        return valor





def mostrar_perfil():


    st.header(
        "👤 Mi Perfil"
    )


    usuario = st.session_state["usuario"]


    cedula = str(
        usuario["cedula"]
    ).strip()



    # =====================================
    # INFORMACIÓN PERSONAL
    # =====================================

    usuarios = cargar_usuarios()



    if usuarios.empty:

        st.warning(
            "No se encontró información del usuario."
        )

        return



    datos = usuarios[

        usuarios["cedula"].astype(str)
        ==
        cedula

    ]



    if datos.empty:

        st.warning(
            "Perfil no encontrado."
        )

        return



    cliente = datos.iloc[0]



    st.subheader(

        cliente.get(
            "nombre_completo",
            "Cliente"
        )

    )



    col1, col2 = st.columns(2)



    with col1:


        st.write(
            "🪪 Cédula"
        )

        st.write(
            cliente.get(
                "cedula",
                ""
            )
        )



        st.write(
            "📱 WhatsApp"
        )

        st.write(
            cliente.get(
                "whatsapp",
                "No registra"
            )
        )



    with col2:


        st.write(
            "🏥 EPS"
        )

        st.write(
            cliente.get(
                "eps",
                "No registra"
            )
        )



        st.write(
            "📅 Fecha registro"
        )

        st.write(
            formatear_fecha(
                cliente.get(
                    "fecha_registro",
                    ""
                )
            )
        )



    st.divider()



    # =====================================
    # INFORMACIÓN MÉDICA
    # =====================================


    st.subheader(
        "🩺 Información médica"
    )



    st.info(

        cliente.get(
            "condiciones_medicas",
            "Sin registros"
        )

    )



    st.divider()



    # =====================================
    # INFORMACIÓN GIMNASIO
    # =====================================


    st.subheader(
        "🏋️ Información de Plan"
    )



    gym = buscar_cliente_gym(
        cedula
    )



    if not gym.empty:


        datos_gym = gym.iloc[0]



        col1, col2, col3 = st.columns(3)



        with col1:

            st.metric(

                "Fecha inicio",

                formatear_fecha(

                    datos_gym.get(

                        "fecha_ingreso",

                        ""

                    )

                )

            )



        with col2:

            st.metric(

                "Vencimiento",

                formatear_fecha(

                    datos_gym.get(

                        "fecha_vencimiento",

                        ""

                    )

                )

            )



        with col3:


            st.metric(

                "Plan",

                datos_gym.get(

                    "tipo_plan",

                    "Membresía"

                )

            )



    else:


        st.info(

            "No tienes una membresía registrada en gimnasio."

        )



    # =====================================
    # PERSONAL TRAINING
    # =====================================


    st.divider()



    st.subheader(
        "💪 Personal Training"
    )



    if "fecha_inicio_personalizado" in cliente.index:



        st.success(

            "Tienes un plan personalizado activo."

        )



        c1, c2 = st.columns(2)



        c1.metric(

            "Inicio",

            formatear_fecha(

                cliente.get(

                    "fecha_inicio_personalizado",

                    ""

                )

            )

        )



        c2.metric(

            "Vencimiento",

            formatear_fecha(

                cliente.get(

                    "fecha_vencimiento_personalizado",

                    ""

                )

            )

        )



    else:


        st.info(

            "No tienes un plan personalizado activo."

        )





    # =====================================
    # HISTORIAL DEL CLIENTE
    # =====================================


    st.divider()



    st.subheader(
        "📜 Historial de actividad"
    )



    historial = construir_historial_cliente(
        cedula
    )



    if not historial.empty:


        historial_visual = historial.copy()



        if "fecha" in historial_visual.columns:


            historial_visual["fecha"] = (

                pd.to_datetime(

                    historial_visual["fecha"],

                    errors="coerce"

                )

                .dt.strftime(

                    "%d-%m-%Y"

                )

            )



        st.dataframe(

            historial_visual,

            use_container_width=True,

            hide_index=True

        )



    else:


        st.info(

            "Todavía no tienes actividad registrada."

        )
