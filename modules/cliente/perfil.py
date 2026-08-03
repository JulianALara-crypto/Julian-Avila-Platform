import streamlit as st

from database.usuarios import cargar_usuarios
from database.gimnasio import buscar_cliente_gym



def mostrar_perfil():


    st.header(
        "👤 Mi Perfil"
    )


    usuario = st.session_state["usuario"]


    cedula = str(
        usuario["cedula"]
    )



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
        cliente["nombre_completo"]
    )


    col1,col2 = st.columns(2)



    with col1:

        st.write(
            "🪪 Cédula"
        )

        st.write(
            cliente["cedula"]
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
            cliente.get(
                "fecha_registro",
                ""
            )
        )



    st.divider()



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



    # ==============================
    # INFORMACIÓN GYM
    # ==============================


    st.subheader(
        "🏋️ Mi Membresía"
    )



    gym = buscar_cliente_gym(
        cedula
    )



    if not gym.empty:


        datos_gym = gym.iloc[0]


        c1,c2 = st.columns(2)


        c1.metric(
            "Inicio",
            datos_gym["fecha_ingreso"]
        )


        c2.metric(
            "Vencimiento",
            datos_gym["fecha_vencimiento"]
        )


    else:

        st.info(
            "No tienes una membresía registrada."
        )
