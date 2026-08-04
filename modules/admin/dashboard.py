import streamlit as st
import pandas as pd
from datetime import datetime

from database.gimnasio import cargar_clientes_gym
from database.pagos import cargar_pagos
from database.planes import cargar_planes
from database.medidas import cargar_medidas


# ==========================================
# DASHBOARD ADMINISTRATIVO
# ==========================================

def mostrar_dashboard():

    st.header(
        "📊 Dashboard Administrativo"
    )

    clientes = cargar_clientes_gym()
    pagos = cargar_pagos()
    planes = cargar_planes()
    medidas = cargar_medidas()

    if clientes.empty:

        st.info(
            "No hay información registrada todavía."
        )

        return

    # ======================================
    # MÉTRICAS PRINCIPALES
    # ======================================

    total_clientes = len(clientes)

    if not pagos.empty and "valor" in pagos.columns:

        ingresos = (
            pd.to_numeric(
                pagos["valor"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

    elif "valor_pagado" in clientes.columns:

        ingresos = (
            pd.to_numeric(
                clientes["valor_pagado"],
                errors="coerce"
            )
            .fillna(0)
            .sum()
        )

    else:

        ingresos = 0

    planes_activos = 0

    if not planes.empty and "estado" in planes.columns:

        planes_activos = len(
            planes[
                planes["estado"]
                .astype(str)
                .str.lower()
                ==
                "activo"
            ]
        )

    total_medidas = len(medidas)

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "👥 Clientes",
        total_clientes
    )

    c2.metric(
        "💰 Ingresos",
        f"${int(ingresos):,}"
    )

    c3.metric(
        "🏋️ Planes activos",
        planes_activos
    )

    c4.metric(
        "📈 Evaluaciones",
        total_medidas
    )

    st.divider()

    # ======================================
    # ÚLTIMOS PAGOS
    # ======================================

    st.subheader(
        "💳 Últimos pagos"
    )

    if pagos.empty:

        st.info(
            "No existen pagos registrados."
        )

    else:

        tabla = pagos.copy()

        if "fecha_pago" in tabla.columns:

            tabla["_fecha"] = pd.to_datetime(
                tabla["fecha_pago"],
                dayfirst=True,
                errors="coerce"
            )

            tabla = (
                tabla
                .sort_values(
                    "_fecha",
                    ascending=False
                )
                .drop(
                    columns="_fecha"
                )
            )

        st.dataframe(
            tabla.head(10),
            use_container_width=True,
            hide_index=True
        )

    st.divider()

    # ======================================
    # PLANES PRÓXIMOS A VENCER
    # ======================================

    st.subheader(
        "⏳ Planes próximos a vencer"
    )

    if planes.empty:

        st.info(
            "No existen planes registrados."
        )

    else:

        hoy = datetime.today()

        proximos = planes.copy()

        if "fecha_fin" in proximos.columns:

            proximos["_fecha"] = pd.to_datetime(
                proximos["fecha_fin"],
                dayfirst=True,
                errors="coerce"
            )

            proximos["dias_restantes"] = (
                proximos["_fecha"] - hoy
            ).dt.days

            proximos = proximos[
                (proximos["dias_restantes"] >= 0)
                &
                (proximos["dias_restantes"] <= 7)
            ]

            proximos = proximos.drop(
                columns="_fecha"
            )

        if proximos.empty:

            st.success(
                "No hay planes próximos a vencer."
            )

        else:

            st.dataframe(
                proximos[
                    [
                        "nombre_completo",
                        "tipo_plan",
                        "fecha_fin",
                        "dias_restantes"
                    ]
                ],
                use_container_width=True,
                hide_index=True
            )

    st.divider()

    # ======================================
    # CLIENTES REGISTRADOS
    # ======================================

    st.subheader(
        "👥 Clientes registrados"
    )

    st.dataframe(
        clientes,
        use_container_width=True,
        hide_index=True
    )
