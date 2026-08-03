# ==========================================
# CONTROL DE PERMISOS
# JULIAN AVILA PLATFORM
# ==========================================


PERMISOS = {


    "Admin": [

        "📊 Dashboard",

        "👥 Clientes",

        "💳 Pagos y Contabilidad",

        "🏋️ Personal Training",

        "📈 Evolución Física",

        "🚨 Alertas de Vencimiento",

        "📄 Documentos",

        "⚙️ Configuración"

    ],



    "Cliente": [

        "👤 Mi Perfil",

        "📏 Mis Medidas",

        "📈 Mi Evolución",

        "🏋️ Mi Plan Personalizado",

        "📄 Documentos"

    ]

}



def obtener_menu(rol):

    return PERMISOS.get(
        rol,
        []
    )



def puede_ver(rol, modulo):

    if modulo in obtener_menu(rol):

        return True

    return False
