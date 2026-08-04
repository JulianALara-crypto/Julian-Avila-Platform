import streamlit as st
import pandas as pd
import urllib.parse
from datetime import timedelta

from database.gimnasio import cargar_clientes_gym
from database.planes import cargar_planes
from database.medidas import cargar_medidas


def mostrar_alertas():
    st.header("🚨 Alertas de vencimiento")

    hoy = pd.Timestamp.today().normalize()
    dias_alerta = st.number_input(
        "Mostrar vencimientos dentro de los próximos días",
        min_value=1,
        value=3,
    )
    limite = hoy + pd.Timedelta(days=int(dias_alerta))

    st.subheader("🏋️ Membresías gimnasio")
    clientes = cargar_clientes_gym()

    if clientes.empty:
        st.info("No hay clientes registrados.")
    else:
        clientes = clientes.copy()
        clientes["fecha_dt"] = pd.to_datetime(
            clientes["fecha_vencimiento"],
            dayfirst=True,
            errors="coerce",
        )
        alertas = clientes[
            clientes["fecha_dt"].notna() &
            (clientes["fecha_dt"] <= limite)
        ]

        if alertas.empty:
            st.success("No hay membresías próximas a vencer.")
        else:
            st.warning(f"{len(alertas)} membresías requieren atención.")
            for _, fila in alertas.iterrows():
                fecha = fila["fecha_dt"]
                estado = "🔴 VENCIDO" if fecha < hoy else "🟡 POR VENCER"
                st.write(f"**{fila['nombre_completo']}**")
                st.write(f"📅 Vence: {fila['fecha_vencimiento']}")
                st.write(estado)

                telefono = str(fila.get("whatsapp", "")).replace(".0", "").strip()
                if telefono:
                    if not telefono.startswith("57"):
                        telefono = "57" + telefono
                    mensaje = f"Hola {fila['nombre_completo']}, tu membresía vence el {fila['fecha_vencimiento']}."
                    url = "https://wa.me/" + telefono + "?text=" + urllib.parse.quote(mensaje)
                    st.link_button("📲 WhatsApp", url)
                st.divider()

    st.subheader("🏋️‍♂️ Planes Personal Training")
    planes = cargar_planes()

    if planes.empty:
        st.info("No existen planes registrados.")
    else:
        planes = planes.copy()
        planes["fecha_dt"] = pd.to_datetime(
            planes["fecha_fin"],
            dayfirst=True,
            errors="coerce",
        )

        alertas = planes[
            planes["fecha_dt"].notna() &
            (planes["fecha_dt"] <= limite)
        ]

        if alertas.empty:
            st.success("No hay planes próximos a vencer.")
        else:
            st.warning(f"{len(alertas)} planes requieren atención.")
            for _, fila in alertas.iterrows():
                fecha = fila["fecha_dt"]
                estado = "🔴 VENCIDO" if fecha < hoy else "🟡 POR VENCER"
                st.write(f"**{fila['nombre_completo']}**")
                st.write(f"🏋️ Plan: {fila['tipo_plan']}")
                st.write(f"📅 Finaliza: {fila['fecha_fin']}")
                st.write(estado)
                st.divider()

    st.subheader("📈 Clientes sin evaluación física")
    medidas = cargar_medidas()
    if clientes.empty:
        st.info("No existen clientes.")
    else:
        if medidas.empty:
            sin = clientes
        else:
            sin = clientes[~clientes["cedula"].astype(str).isin(medidas["cedula"].astype(str))]
        if sin.empty:
            st.success("Todos los clientes tienen evaluación.")
        else:
            st.dataframe(sin[["cedula","nombre_completo","whatsapp"]], hide_index=True, use_container_width=True)

    st.divider()
    st.subheader("💪 Clientes sin Personal Training")
    if clientes.empty:
        st.info("No existen clientes.")
    else:
        if planes.empty:
            sin = clientes
        else:
            sin = clientes[~clientes["cedula"].astype(str).isin(planes["cedula"].astype(str))]
        if sin.empty:
            st.success("Todos los clientes tienen un plan personalizado.")
        else:
            st.dataframe(sin[["cedula","nombre_completo","whatsapp"]], hide_index=True, use_container_width=True)
