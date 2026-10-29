import math
import os
import urllib.parse
from datetime import datetime, date

import pandas as pd
import requests
import streamlit as st
from PIL import Image


# ============================================================
# CONFIGURACIÓN GENERAL
# ============================================================

URL_API = ("https://script.google.com/macros/s/AKfycbzEqkRmWqqSKuK_ILnRMdTbnj8cUsD4DQ4FpHK-6zHirPKFJ5z3aEjsrrMXsWh_Eaw/exec")


# ============================================================
# SESIÓN HTTP REUTILIZABLE
# Evita crear una conexión HTTP nueva en cada operación.
# ============================================================
API_SESSION = requests.Session()

def api_get(*args, **kwargs):
    return API_SESSION.get(*args, **kwargs)

def api_post(*args, **kwargs):
    return API_SESSION.post(*args, **kwargs)

def invalidar_cache_datos():
    """Invalida únicamente los cachés de datos de la aplicación."""
    try:
        cargar_usuarios_login.clear()
    except Exception:
        pass
    try:
        cargar_bd.clear()
    except Exception:
        pass


# ============================================================
# RUTA SEGURA DEL LOGO
# ============================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

ruta_logo = os.path.join(
    BASE_DIR,
    "logo.png"
)


# ============================================================
# CARGAR LOGO
# ============================================================

icono_pestana = None

if os.path.isfile(ruta_logo):
    try:
        icono_pestana = Image.open(
            ruta_logo
        )
    except Exception:
        icono_pestana = None


# ============================================================
# CONFIGURACIÓN STREAMLIT
# ============================================================

st.set_page_config(
    page_title="Gestor Gimnasio · Julian Avila",
    page_icon=icono_pestana,
    layout="wide",
)


# ============================================================
# ESTILOS
# ============================================================

st.markdown(
    """
    <style>

    .stApp {
        background-color: #000000;
    }

    h1, h2, h3, h4 {
        color: #ffffff !important;
        text-align: center;
    }

    p, label, .stMarkdown {
        color: #dddddd !important;
    }

    div[data-testid="stDecoration"] {
        display: none;
    }

    .clase-card {
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #333333;
        background-color: #111111;
        margin-bottom: 15px;
    }

    .ui-section-title {
        color: #ffffff !important;
        text-align: center !important;
        font-weight: 700 !important;
        letter-spacing: 0.3px;
        margin-top: 0.7rem;
        margin-bottom: 1rem;
    }

    .ui-section-title .fi { color: #ffffff; }

    .ui-module-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 14px;
        padding: 12px 18px;
        margin: 10px 0 18px 0;
        border: 1px solid #252525;
        border-radius: 16px;
        background: linear-gradient(180deg, #111111 0%, #080808 100%);
        box-shadow: 0 6px 18px rgba(0,0,0,0.28);
    }

    .ui-module-icon {
        width: 58px;
        height: 58px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 15px;
        border: 1px solid #333333;
        background: #151515;
    }

    .ui-module-icon .fi { color: #ffffff; margin-right: 0 !important; }

    .ui-module-title {
        color: #ffffff;
        font-size: 1.35rem;
        font-weight: 700;
        line-height: 1.2;
    }

    .ui-attribution {
        display:none !important;
        text-align: center;
        color: #777777;
        font-size: 0.75rem;
        margin-top: 30px;
        padding: 12px 0;
        border-top: 1px solid #222222;
    }

    .ui-attribution a { color: #aaaaaa !important; text-decoration: none; }

    
    /* ==========================================================
       GLASS/WOW 3D - PALETA POR MÓDULO + CONTROLES DINÁMICOS
       Capa visual. No cambia la lógica de negocio.
       ========================================================== */
    :root {
        --ui-cyan: #22d3ee;
        --ui-blue: #38bdf8;
        --ui-violet: #a78bfa;
        --ui-green: #34d399;
        --ui-amber: #fbbf24;
        --ui-coral: #fb7185;
    }

    section[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at 15% 10%, rgba(34,211,238,.055), transparent 24%),
            radial-gradient(circle at 85% 80%, rgba(167,139,250,.045), transparent 25%),
            linear-gradient(180deg, #08090c 0%, #030405 100%) !important;
        border-right: 1px solid rgba(255,255,255,.075) !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] {
        gap: 7px !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] > label {
        position: relative;
        min-height: 43px;
        padding: 9px 12px !important;
        margin: 0 !important;
        border: 1px solid rgba(255,255,255,.055) !important;
        border-radius: 13px !important;
        background: rgba(255,255,255,.018) !important;
        transition: transform .2s ease, background .2s ease, border-color .2s ease, box-shadow .2s ease !important;
        overflow: hidden;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] > label:hover {
        transform: translateX(3px) !important;
        background: rgba(255,255,255,.045) !important;
        border-color: rgba(255,255,255,.12) !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] > label:has(input:checked) {
        background: linear-gradient(90deg, rgba(34,211,238,.13), rgba(34,211,238,.035)) !important;
        border-color: rgba(34,211,238,.45) !important;
        box-shadow: 0 0 22px rgba(34,211,238,.10), inset 3px 0 0 rgba(34,211,238,.95) !important;
    }

    section[data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(2):has(input:checked) {
        background: linear-gradient(90deg, rgba(167,139,250,.14), rgba(167,139,250,.035)) !important;
        border-color: rgba(167,139,250,.45) !important;
        box-shadow: 0 0 22px rgba(167,139,250,.10), inset 3px 0 0 rgba(167,139,250,.95) !important;
    }
    section[data-testid="stSidebar"] [role="radiogroup"] > label:nth-child(3):has(input:checked) {
        background: linear-gradient(90deg, rgba(52,211,153,.14), rgba(52,211,153,.035)) !important;
        border-color: rgba(52,211,153,.45) !important;
        box-shadow: 0 0 22px rgba(52,211,153,.10), inset 3px 0 0 rgba(52,211,153,.95) !important;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: rgba(34,211,238,.65) !important;
        box-shadow: 0 0 0 1px rgba(34,211,238,.30), 0 0 22px rgba(34,211,238,.09), inset 0 2px 8px rgba(0,0,0,.48) !important;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover,
    div.stDownloadButton > button:hover {
        border-color: rgba(34,211,238,.52) !important;
        box-shadow: 0 14px 32px rgba(0,0,0,.55), 0 0 20px rgba(34,211,238,.08), inset 0 1px 0 rgba(255,255,255,.14) !important;
    }

    div[data-testid="stMetric"] {
        border-top: 2px solid rgba(34,211,238,.72) !important;
    }
    div[data-testid="stMetric"]:nth-child(2) { border-top-color: rgba(167,139,250,.78) !important; }
    div[data-testid="stMetric"]:nth-child(3) { border-top-color: rgba(52,211,153,.78) !important; }
    div[data-testid="stMetric"]:nth-child(4) { border-top-color: rgba(251,191,36,.82) !important; }

    .ui-section-title { text-shadow: 0 0 20px rgba(34,211,238,.06); }
    .ui-section-title .fi { filter: drop-shadow(0 0 9px currentColor); }

    .clase-card { border-left: 3px solid rgba(34,211,238,.72) !important; }
    .clase-card:hover {
        border-left-color: rgba(167,139,250,.95) !important;
        box-shadow: 0 20px 42px rgba(0,0,0,.48), 0 0 22px rgba(167,139,250,.07), inset 0 1px 0 rgba(255,255,255,.07) !important;
    }

    div[data-testid="stDataFrame"] {
        border-color: rgba(255,255,255,.10) !important;
        box-shadow: 0 16px 34px rgba(0,0,0,.35), inset 0 1px 0 rgba(255,255,255,.05) !important;
    }

    /* BARRA DE PROGRESO DINÁMICA */
    .wow-progress-wrap {
        margin: 13px 0 18px 0;
        padding: 14px 16px 13px;
        border-radius: 17px;
        border: 1px solid rgba(255,255,255,.08);
        background: linear-gradient(145deg, rgba(255,255,255,.045), rgba(255,255,255,.012));
        box-shadow: 0 12px 28px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.055);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
    }
    .wow-progress-head { display:flex; align-items:center; justify-content:space-between; gap:12px; margin-bottom:9px; }
    .wow-progress-label { color:#a7a7a7; font-size:12px; font-weight:800; letter-spacing:.7px; text-transform:uppercase; }
    .wow-progress-value { color:#fff; font-size:15px; font-weight:900; text-shadow:0 0 14px rgba(34,211,238,.18); }
    .wow-progress-track {
        position:relative; width:100%; height:13px; overflow:hidden; border-radius:999px;
        background:#090b0f; border:1px solid rgba(255,255,255,.07);
        box-shadow: inset 0 3px 7px rgba(0,0,0,.65), 0 1px 0 rgba(255,255,255,.025);
    }
    .wow-progress-fill {
        position:relative; height:100%; width:var(--progress-width); border-radius:999px;
        background:linear-gradient(90deg, var(--progress-start), var(--progress-mid), var(--progress-end));
        box-shadow:0 0 12px var(--progress-glow), 0 0 25px var(--progress-glow);
        animation: wowProgressIn 1.15s cubic-bezier(.2,.8,.2,1) both;
    }
    .wow-progress-fill::before {
        content:""; position:absolute; inset:0;
        background:linear-gradient(105deg, transparent 0%, rgba(255,255,255,.06) 38%, rgba(255,255,255,.68) 50%, rgba(255,255,255,.06) 62%, transparent 100%);
        transform:translateX(-120%); animation: wowProgressShine 2.8s ease-in-out 1.05s infinite;
    }
    .wow-progress-fill::after {
        content:""; position:absolute; inset:1px 0 auto 0; height:35%; border-radius:999px;
        background:linear-gradient(180deg, rgba(255,255,255,.32), transparent); opacity:.65;
    }
    .wow-progress-scale { display:flex; justify-content:space-between; margin-top:7px; color:#686868; font-size:10px; font-weight:700; }
    @keyframes wowProgressIn { from { width:0; opacity:.35; filter:brightness(.7); } to { width:var(--progress-width); opacity:1; filter:brightness(1); } }
    @keyframes wowProgressShine { 0%,35% { transform:translateX(-120%); } 70%,100% { transform:translateX(120%); } }
    @media (prefers-reduced-motion: reduce) { .wow-progress-fill, .wow-progress-fill::before { animation:none !important; } }

</style>
    """,
    unsafe_allow_html=True,
)

# UIcons de Flaticon: familia consistente para la interfaz.
st.markdown(
    "<link rel=\"stylesheet\" href=\"https://cdn-uicons.flaticon.com/2.6.0/uicons-regular-rounded/css/uicons-regular-rounded.css\">",
    unsafe_allow_html=True,
)

# ============================================================
# INTERFAZ PREMIUM FITNESS 2.0
# Capa exclusivamente visual: no modifica la lógica de negocio.
# ============================================================
st.markdown(
    """
    <style>

    /* ---------- GLASSMORPHISM PREMIUM 2.0 ---------- */
    .main .block-container {
        position: relative;
    }

    /* Cristal profundo para formularios y paneles */
    div[data-testid="stForm"],
    div[data-testid="stExpander"],
    div[data-testid="stMetric"],
    div[data-testid="stDataFrame"] {
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(18px) saturate(120%);
        -webkit-backdrop-filter: blur(18px) saturate(120%);
    }

    div[data-testid="stForm"]::before,
    div[data-testid="stExpander"]::before,
    div[data-testid="stMetric"]::before,
    .clase-card::before,
    .ui-module-header::before {
        content: "";
        position: absolute;
        left: 0;
        right: 0;
        top: 0;
        height: 1px;
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.32), transparent);
        opacity: 0.72;
        pointer-events: none;
    }

    /* Reflejo diagonal muy sutil, como vidrio real */
    div[data-testid="stMetric"]::after,
    div[data-testid="stForm"]::after,
    .clase-card::after {
        content: "";
        position: absolute;
        width: 55%;
        height: 180%;
        top: -55%;
        left: -28%;
        transform: rotate(24deg);
        background: linear-gradient(90deg, transparent, rgba(255,255,255,0.035), transparent);
        pointer-events: none;
    }

    /* Sombras multicapa para profundidad */
    div[data-testid="stMetric"] {
        box-shadow:
            0 2px 4px rgba(0,0,0,0.50),
            0 10px 24px rgba(0,0,0,0.38),
            0 24px 48px rgba(0,0,0,0.24),
            inset 0 1px 0 rgba(255,255,255,0.075),
            inset 0 -1px 0 rgba(0,0,0,0.65);
    }

    div[data-testid="stForm"] {
        box-shadow:
            0 3px 7px rgba(0,0,0,0.48),
            0 16px 34px rgba(0,0,0,0.40),
            0 30px 65px rgba(0,0,0,0.22),
            inset 0 1px 0 rgba(255,255,255,0.065),
            inset 0 -1px 0 rgba(0,0,0,0.70);
    }

    /* Inputs con sensación de cristal hundido */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        box-shadow:
            inset 0 2px 8px rgba(0,0,0,0.48),
            inset 0 1px 0 rgba(255,255,255,0.035),
            0 2px 8px rgba(0,0,0,0.22) !important;
    }

    /* Botones con volumen y sombra de objeto */
    div.stButton > button,
    div.stFormSubmitButton > button,
    div.stDownloadButton > button {
        position: relative;
        overflow: hidden;
        box-shadow:
            0 2px 4px rgba(0,0,0,0.55),
            0 8px 18px rgba(0,0,0,0.42),
            inset 0 1px 0 rgba(255,255,255,0.09),
            inset 0 -2px 0 rgba(0,0,0,0.45) !important;
    }

    div.stButton > button::before,
    div.stFormSubmitButton > button::before,
    div.stDownloadButton > button::before {
        content: "";
        position: absolute;
        top: 0;
        left: 10%;
        right: 10%;
        height: 1px;
        background: rgba(255,255,255,0.22);
        pointer-events: none;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover,
    div.stDownloadButton > button:hover {
        box-shadow:
            0 3px 5px rgba(0,0,0,0.60),
            0 14px 30px rgba(0,0,0,0.50),
            inset 0 1px 0 rgba(255,255,255,0.13),
            inset 0 -2px 0 rgba(0,0,0,0.38) !important;
    }

    /* Sidebar tipo panel de vidrio oscuro */
    section[data-testid="stSidebar"] {
        backdrop-filter: blur(20px) saturate(120%);
        -webkit-backdrop-filter: blur(20px) saturate(120%);
        box-shadow: 10px 0 35px rgba(0,0,0,0.30);
    }

    /* Encabezados de módulos con cristal */
    .ui-module-header {
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(16px) saturate(120%);
        -webkit-backdrop-filter: blur(16px) saturate(120%);
        box-shadow:
            0 4px 8px rgba(0,0,0,0.42),
            0 16px 32px rgba(0,0,0,0.28),
            inset 0 1px 0 rgba(255,255,255,0.07);
    }

    .ui-module-icon {
        box-shadow:
            0 5px 14px rgba(0,0,0,0.42),
            inset 0 1px 0 rgba(255,255,255,0.07);
    }

    /* Tarjetas de clases más profundas */
    .clase-card {
        position: relative;
        overflow: hidden;
        backdrop-filter: blur(14px) saturate(115%);
        -webkit-backdrop-filter: blur(14px) saturate(115%);
        box-shadow:
            0 3px 6px rgba(0,0,0,0.52),
            0 14px 30px rgba(0,0,0,0.38),
            inset 0 1px 0 rgba(255,255,255,0.06),
            inset 0 -1px 0 rgba(0,0,0,0.62) !important;
    }

    .clase-card:hover {
        box-shadow:
            0 5px 9px rgba(0,0,0,0.55),
            0 20px 38px rgba(0,0,0,0.45),
            inset 0 1px 0 rgba(255,255,255,0.08) !important;
    }

    /* ---------- Fondo y profundidad general ---------- */
    .stApp {
        background:
            radial-gradient(circle at 12% 8%, rgba(255,255,255,0.055), transparent 24%),
            radial-gradient(circle at 88% 18%, rgba(120,120,120,0.045), transparent 22%),
            linear-gradient(135deg, #030303 0%, #080808 48%, #020202 100%) !important;
    }

    .main .block-container {
        max-width: 1450px;
        padding-top: 1.4rem;
        padding-bottom: 3rem;
    }

    /* ---------- Títulos ---------- */
    h1 {
        font-weight: 800 !important;
        letter-spacing: 1.2px !important;
        text-shadow: 0 3px 18px rgba(255,255,255,0.10);
    }

    h2, h3, h4 {
        letter-spacing: 0.35px;
    }

    /* ---------- Botones premium ---------- */
    div.stButton > button,
    div.stFormSubmitButton > button,
    div.stDownloadButton > button {
        border: 1px solid #353535 !important;
        border-radius: 14px !important;
        min-height: 46px !important;
        padding: 0.55rem 1.1rem !important;
        background: linear-gradient(145deg, #202020 0%, #0d0d0d 100%) !important;
        color: #f5f5f5 !important;
        font-weight: 700 !important;
        letter-spacing: 0.25px !important;
        box-shadow: 0 7px 18px rgba(0,0,0,0.38), inset 0 1px 0 rgba(255,255,255,0.06) !important;
        transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease, background 0.18s ease !important;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover,
    div.stDownloadButton > button:hover {
        transform: translateY(-2px) !important;
        border-color: #666666 !important;
        background: linear-gradient(145deg, #2b2b2b 0%, #111111 100%) !important;
        box-shadow: 0 12px 25px rgba(0,0,0,0.52), inset 0 1px 0 rgba(255,255,255,0.09) !important;
    }

    div.stButton > button:active,
    div.stFormSubmitButton > button:active,
    div.stDownloadButton > button:active {
        transform: translateY(1px) scale(0.99) !important;
    }

    /* ---------- Inputs ---------- */
    div[data-baseweb="input"] > div,
    div[data-baseweb="textarea"] > div,
    div[data-baseweb="select"] > div {
        background: linear-gradient(145deg, #151515, #0b0b0b) !important;
        border: 1px solid #303030 !important;
        border-radius: 12px !important;
        box-shadow: inset 0 1px 7px rgba(0,0,0,0.35) !important;
        transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
    }

    div[data-baseweb="input"] > div:focus-within,
    div[data-baseweb="textarea"] > div:focus-within,
    div[data-baseweb="select"] > div:focus-within {
        border-color: #666666 !important;
        box-shadow: 0 0 0 1px #555555, 0 0 18px rgba(255,255,255,0.06) !important;
    }

    input, textarea {
        color: #f2f2f2 !important;
    }

    /* ---------- Métricas ---------- */
    div[data-testid="stMetric"] {
        background: linear-gradient(145deg, rgba(28,28,28,0.96), rgba(8,8,8,0.96));
        border: 1px solid #292929;
        border-radius: 18px;
        padding: 18px 18px 14px 18px;
        box-shadow: 0 10px 28px rgba(0,0,0,0.34), inset 0 1px 0 rgba(255,255,255,0.045);
        transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
    }

    div[data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        border-color: #454545;
        box-shadow: 0 16px 34px rgba(0,0,0,0.48), inset 0 1px 0 rgba(255,255,255,0.07);
    }

    div[data-testid="stMetricLabel"] {
        color: #9f9f9f !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    /* ---------- Formularios / contenedores ---------- */
    div[data-testid="stForm"] {
        background: linear-gradient(145deg, rgba(18,18,18,0.92), rgba(7,7,7,0.92));
        border: 1px solid #262626;
        border-radius: 20px;
        padding: 18px;
        box-shadow: 0 14px 34px rgba(0,0,0,0.34), inset 0 1px 0 rgba(255,255,255,0.035);
    }

    /* ---------- Sidebar ---------- */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #080808 0%, #030303 100%) !important;
        border-right: 1px solid #242424;
    }

    section[data-testid="stSidebar"] div[data-testid="stButton"] button {
        border-radius: 12px !important;
    }

    section[data-testid="stSidebar"] label {
        transition: background 0.18s ease, transform 0.18s ease;
        border-radius: 10px;
        padding: 4px 6px;
    }

    section[data-testid="stSidebar"] label:hover {
        background: rgba(255,255,255,0.045);
        transform: translateX(2px);
    }

    /* ---------- Tarjetas personalizadas existentes ---------- */
    .clase-card {
        background: linear-gradient(145deg, #171717, #080808) !important;
        border: 1px solid #292929 !important;
        border-radius: 18px !important;
        box-shadow: 0 12px 28px rgba(0,0,0,0.38), inset 0 1px 0 rgba(255,255,255,0.04) !important;
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .clase-card:hover {
        transform: translateY(-2px);
        border-color: #444444 !important;
    }

    /* ---------- Separadores ---------- */
    hr {
        border-color: #252525 !important;
    }

    /* ---------- Expander ---------- */
    div[data-testid="stExpander"] {
        border: 1px solid #282828 !important;
        border-radius: 16px !important;
        background: rgba(10,10,10,0.72) !important;
        box-shadow: 0 9px 25px rgba(0,0,0,0.25);
    }

    /* ---------- Dataframes ---------- */
    div[data-testid="stDataFrame"] {
        border: 1px solid #292929;
        border-radius: 14px;
        overflow: hidden;
        box-shadow: 0 10px 25px rgba(0,0,0,0.28);
    }

    /* ---------- Logo ---------- */
    .logo-premium {
        filter: drop-shadow(0 10px 22px rgba(255,255,255,0.08));
    }

    /* ---------- Mobile ---------- */
    @media (max-width: 768px) {
        .main .block-container {
            padding-left: 0.8rem;
            padding-right: 0.8rem;
        }

        .ui-module-header {
            padding: 10px 12px;
        }

        .ui-module-icon {
            width: 48px;
            height: 48px;
        }
    }

\n\n    /* ========================================================\n       GLASS VIVO / MICROANIMACIONES PREMIUM\n       Solo visual: no altera la lógica de Streamlit.\n       ======================================================== */\n\n    .stApp {\n        background:\n            radial-gradient(circle at 12% 18%, rgba(255,255,255,0.075), transparent 20%),\n            radial-gradient(circle at 86% 12%, rgba(130,130,130,0.065), transparent 22%),\n            radial-gradient(circle at 50% 88%, rgba(255,255,255,0.035), transparent 25%),\n            linear-gradient(135deg, #020202 0%, #090909 48%, #020202 100%) !important;\n        background-size: 140% 140%;\n        animation: glassAmbient 18s ease-in-out infinite alternate;\n    }\n\n    @keyframes glassAmbient {\n        0% { background-position: 0% 0%; }\n        50% { background-position: 100% 35%; }\n        100% { background-position: 35% 100%; }\n    }\n\n    /* Luz ambiental muy suave que recorre el cristal */\n    div[data-testid="stMetric"]::after,\n    div[data-testid="stForm"]::after,\n    div[data-testid="stExpander"]::after,\n    .clase-card::after,\n    .ui-module-header::after {\n        animation: glassShimmer 7s ease-in-out infinite;\n    }\n\n    @keyframes glassShimmer {\n        0%, 100% { opacity: 0.18; transform: translateX(-35%) rotate(24deg); }\n        50% { opacity: 0.52; transform: translateX(115%) rotate(24deg); }\n    }\n\n    /* Tarjetas con una pequeña sensación de objeto flotante */\n    div[data-testid="stMetric"] {\n        animation: cardFloat 6s ease-in-out infinite;\n    }\n\n    div[data-testid="stMetric"]:nth-child(2) { animation-delay: -1.2s; }\n    div[data-testid="stMetric"]:nth-child(3) { animation-delay: -2.4s; }\n    div[data-testid="stMetric"]:nth-child(4) { animation-delay: -3.6s; }\n\n    @keyframes cardFloat {\n        0%, 100% { transform: translateY(0px); }\n        50% { transform: translateY(-3px); }\n    }\n\n    div[data-testid="stMetric"]:hover {\n        animation-play-state: paused;\n        transform: translateY(-7px) scale(1.012) !important;\n        border-color: #5a5a5a !important;\n        box-shadow:\n            0 5px 10px rgba(0,0,0,0.58),\n            0 20px 42px rgba(0,0,0,0.52),\n            0 0 28px rgba(255,255,255,0.035),\n            inset 0 1px 0 rgba(255,255,255,0.12) !important;\n    }\n\n    /* Botones con respuesta más viva */\n    div.stButton > button,\n    div.stFormSubmitButton > button,\n    div.stDownloadButton > button {\n        transition: transform 0.2s cubic-bezier(.2,.8,.2,1),\n                    box-shadow 0.2s ease,\n                    border-color 0.2s ease,\n                    background 0.2s ease !important;\n    }\n\n    div.stButton > button:hover,\n    div.stFormSubmitButton > button:hover,\n    div.stDownloadButton > button:hover {\n        transform: translateY(-3px) scale(1.015) !important;\n        border-color: #777777 !important;\n        box-shadow:\n            0 4px 8px rgba(0,0,0,0.62),\n            0 16px 32px rgba(0,0,0,0.52),\n            0 0 20px rgba(255,255,255,0.035),\n            inset 0 1px 0 rgba(255,255,255,0.14) !important;\n    }\n\n    /* Iconos: pequeño pulso elegante al pasar el mouse */\n    .ui-module-icon,\n    .ui-module-header i,\n    .ui-section-title i {\n        transition: transform 0.25s ease, filter 0.25s ease;\n    }\n\n    .ui-module-header:hover .ui-module-icon,\n    .ui-module-header:hover i {\n        transform: translateY(-2px) scale(1.06);\n        filter: drop-shadow(0 5px 10px rgba(255,255,255,0.12));\n    }\n\n    /* Inputs más vivos sin perder el aspecto de cristal */\n    div[data-baseweb="input"] > div:hover,\n    div[data-baseweb="textarea"] > div:hover,\n    div[data-baseweb="select"] > div:hover {\n        border-color: #4b4b4b !important;\n        box-shadow:\n            inset 0 2px 8px rgba(0,0,0,0.48),\n            0 0 16px rgba(255,255,255,0.025) !important;\n    }\n\n    /* Aparición suave de bloques al cargar */\n    .main .block-container > div {\n        animation: softReveal 0.55s ease both;\n    }\n\n    @keyframes softReveal {\n        from { opacity: 0; transform: translateY(7px); }\n        to { opacity: 1; transform: translateY(0); }\n    }\n\n    /* Respeta usuarios que prefieren menos movimiento */\n    @media (prefers-reduced-motion: reduce) {\n        *, *::before, *::after {\n            animation-duration: 0.01ms !important;\n            animation-iteration-count: 1 !important;\n            transition-duration: 0.01ms !important;\n        }\n    }\n    

    /* ==========================================================
       DASHBOARD WOW - GLASS INTERACTIVO
       ========================================================== */
    .dashboard-hero {
        position: relative;
        overflow: hidden;
        margin: 8px 0 24px 0;
        padding: 30px 34px;
        border-radius: 26px;
        border: 1px solid rgba(255,255,255,0.14);
        background:
            radial-gradient(circle at 85% 20%, rgba(255,255,255,0.12), transparent 22%),
            linear-gradient(135deg, rgba(255,255,255,0.075), rgba(255,255,255,0.018));
        backdrop-filter: blur(22px) saturate(125%);
        -webkit-backdrop-filter: blur(22px) saturate(125%);
        box-shadow: 0 24px 55px rgba(0,0,0,0.52), inset 0 1px 0 rgba(255,255,255,0.13);
        transform-style: preserve-3d;
        animation: heroFloat 7s ease-in-out infinite;
    }
    .dashboard-hero::before {
        content: "";
        position: absolute;
        width: 280px;
        height: 280px;
        right: -90px;
        top: -150px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        filter: blur(45px);
        animation: orbMove 9s ease-in-out infinite alternate;
    }
    .dashboard-kicker { color:#aaa; font-size:11px; letter-spacing:3px; font-weight:800; position:relative; z-index:1; }
    .dashboard-title { color:#fff; font-size:34px; font-weight:900; margin-top:5px; position:relative; z-index:1; text-shadow:0 5px 25px rgba(255,255,255,0.12); }
    .dashboard-subtitle { color:#9b9b9b; margin-top:6px; font-size:14px; position:relative; z-index:1; }
    .dashboard-section-title { margin:26px 0 12px; color:#fff; font-size:18px; font-weight:800; letter-spacing:.3px; }
    .glass-panel-title { color:#d7d7d7; font-weight:700; margin:4px 0 8px; }
    .dashboard-card {
        position:relative; overflow:hidden; min-height:145px; padding:20px; border-radius:22px;
        border:1px solid rgba(255,255,255,0.11);
        background:linear-gradient(145deg, rgba(35,35,35,.72), rgba(7,7,7,.74));
        backdrop-filter:blur(18px); -webkit-backdrop-filter:blur(18px);
        box-shadow:0 18px 38px rgba(0,0,0,.48), inset 0 1px 0 rgba(255,255,255,.08);
        transition:transform .28s ease, border-color .28s ease, box-shadow .28s ease;
    }
    .dashboard-card::after {
        content:""; position:absolute; inset:-60% -30%;
        background:linear-gradient(110deg, transparent 40%, rgba(255,255,255,.08) 50%, transparent 60%);
        transform:translateX(-65%) rotate(8deg); transition:transform .7s ease; pointer-events:none;
    }
    .dashboard-card:hover { transform:translateY(-8px) perspective(800px) rotateX(2deg) rotateY(-2deg); border-color:rgba(255,255,255,.24); box-shadow:0 28px 55px rgba(0,0,0,.62), inset 0 1px 0 rgba(255,255,255,.12); }
    .dashboard-card:hover::after { transform:translateX(65%) rotate(8deg); }
    .dash-icon { font-size:25px; margin-bottom:12px; filter:drop-shadow(0 5px 10px rgba(255,255,255,.12)); }
    .dash-label { color:#9c9c9c; font-size:12px; font-weight:700; text-transform:uppercase; letter-spacing:1px; }
    .dash-value { color:#fff; font-size:30px; font-weight:900; margin-top:4px; }
    .dash-note { color:#777; font-size:11px; margin-top:5px; }
    @keyframes heroFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-3px)} }
    @keyframes orbMove { from{transform:translate(-15px,8px) scale(.9)} to{transform:translate(18px,28px) scale(1.15)} }
    @media (prefers-reduced-motion: reduce) { .dashboard-hero,.dashboard-hero::before { animation:none !important; } .dashboard-card { transition:none !important; } }


    /* ========================================================
       PALETA PREMIUM AZUL PETRÓLEO + VERDE OLIVA
       Capa visual: no modifica lógica ni datos.
       ======================================================== */
    .stApp {
        background:
            radial-gradient(circle at 8% 10%, rgba(43, 177, 224, .16), transparent 25%),
            radial-gradient(circle at 88% 14%, rgba(126, 145, 76, .14), transparent 27%),
            radial-gradient(circle at 72% 88%, rgba(49, 155, 119, .09), transparent 24%),
            linear-gradient(135deg, #06121b 0%, #0a222b 48%, #18281f 100%) !important;
        background-size: 150% 150%;
        animation: premiumAmbient 22s ease-in-out infinite alternate;
    }

    @keyframes premiumAmbient {
        0% { background-position: 0% 0%; }
        50% { background-position: 100% 35%; }
        100% { background-position: 35% 100%; }
    }

    /* Glass más luminoso, pero sobrio */
    .dashboard-card,
    div[data-testid="stMetric"],
    .clase-card,
    div[data-testid="stForm"],
    div[data-testid="stExpander"] {
        background:
            linear-gradient(145deg, rgba(255,255,255,.065), rgba(255,255,255,.018)) !important;
        border-color: rgba(185, 224, 218, .12) !important;
        box-shadow:
            0 20px 48px rgba(0,0,0,.30),
            inset 0 1px 0 rgba(255,255,255,.07) !important;
    }

    .dashboard-card:hover,
    div[data-testid="stMetric"]:hover,
    .clase-card:hover {
        border-color: rgba(76, 205, 224, .30) !important;
        box-shadow:
            0 25px 58px rgba(0,0,0,.38),
            0 0 28px rgba(54,185,232,.07),
            inset 0 1px 0 rgba(255,255,255,.10) !important;
    }

    /* Cabeceras de módulos */
    .ui-module-header {
        border-color: rgba(255,255,255,.11) !important;
        background:
            linear-gradient(135deg, rgba(54,185,232,.075), rgba(127,143,82,.065) 55%, rgba(255,255,255,.018)) !important;
        box-shadow:
            0 14px 32px rgba(0,0,0,.25),
            inset 0 1px 0 rgba(255,255,255,.07) !important;
    }

    /* Acentos de iconos por contexto */
    .ui-module-icon { filter: drop-shadow(0 0 10px currentColor); }
    .ui-module-header .fi-rr-users,
    .ui-module-header .fi-rr-user { color:#4fc3e8 !important; }
    .ui-module-header .fi-rr-dumbbell,
    .ui-module-header .fi-rr-chart-histogram { color:#9b8cff !important; }
    .ui-module-header .fi-rr-calendar,
    .ui-module-header .fi-rr-check { color:#55d5aa !important; }
    .ui-module-header .fi-rr-money,
    .ui-module-header .fi-rr-credit-card { color:#e5bd67 !important; }

    /* Botones: color premium, no arcoíris */
    div.stButton > button,
    div.stFormSubmitButton > button,
    div.stDownloadButton > button,
    a[data-testid="stLinkButton"] {
        background: linear-gradient(135deg, rgba(42,164,207,.20), rgba(91,119,68,.18)) !important;
        border-color: rgba(108,203,215,.22) !important;
        box-shadow:
            0 9px 25px rgba(0,0,0,.24),
            inset 0 1px 0 rgba(255,255,255,.08) !important;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover,
    div.stDownloadButton > button:hover,
    a[data-testid="stLinkButton"]:hover {
        background: linear-gradient(135deg, rgba(54,185,232,.30), rgba(127,143,82,.25)) !important;
        border-color: rgba(112,218,226,.48) !important;
        box-shadow:
            0 15px 34px rgba(0,0,0,.30),
            0 0 24px rgba(54,185,232,.10) !important;
    }

    /* Barra de progreso: azul -> violeta -> oliva/verde según avance */
    .wow-progress-wrap {
        background: linear-gradient(145deg, rgba(255,255,255,.065), rgba(255,255,255,.018)) !important;
        border: 1px solid rgba(177,218,207,.13) !important;
        box-shadow:
            0 20px 46px rgba(0,0,0,.30),
            inset 0 1px 0 rgba(255,255,255,.07) !important;
        backdrop-filter: blur(18px);
    }

    .wow-progress-track {
        background: rgba(2,12,17,.62) !important;
        border: 1px solid rgba(255,255,255,.07);
        box-shadow: inset 0 2px 7px rgba(0,0,0,.42) !important;
    }

    .wow-progress-fill {
        background: linear-gradient(90deg, var(--progress-start), var(--progress-mid), var(--progress-end)) !important;
        box-shadow:
            0 0 14px var(--progress-glow),
            0 0 30px var(--progress-glow) !important;
    }

    .wow-progress-fill::after {
        background: linear-gradient(90deg, transparent, rgba(255,255,255,.72), transparent) !important;
        animation: wowProgressShine 2.4s ease-in-out infinite !important;
    }

    @keyframes wowProgressShine {
        0% { transform: translateX(-140%); opacity:0; }
        18% { opacity:1; }
        52% { opacity:.9; }
        100% { transform: translateX(520%); opacity:0; }
    }

    /* Tabla más limpia */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(176,218,211,.11) !important;
        box-shadow: 0 18px 40px rgba(0,0,0,.25) !important;
        border-radius: 16px !important;
    }

    /* Sidebar: azul petróleo con oliva casi imperceptible */
    section[data-testid="stSidebar"] {
        background:
            radial-gradient(circle at 15% 8%, rgba(54,185,232,.09), transparent 28%),
            linear-gradient(180deg, rgba(4,15,22,.98), rgba(14,25,22,.98)) !important;
        border-right: 1px solid rgba(103,194,203,.10) !important;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background: linear-gradient(90deg, rgba(54,185,232,.10), rgba(127,143,82,.07)) !important;
    }
</style>
    """,
    unsafe_allow_html=True,
)


def icono_ui(clase, tamano=28):
    """Icono UI con color contextual por módulo; solo cambia presentación."""
    colores = {
        "fi-rr-user": "#22d3ee",
        "fi-rr-users": "#22d3ee",
        "fi-rr-file-user": "#22d3ee",
        "fi-rr-dashboard": "#38bdf8",
        "fi-rr-apps": "#38bdf8",
        "fi-rr-dumbbell": "#a78bfa",
        "fi-rr-ruler-horizontal": "#a78bfa",
        "fi-rr-clipboard": "#34d399",
        "fi-rr-wallet": "#34d399",
        "fi-rr-credit-card": "#34d399",
        "fi-rr-calendar": "#fbbf24",
        "fi-rr-bell": "#fbbf24",
        "fi-rr-document": "#fb7185",
    }
    color = colores.get(clase, "#e5e7eb")
    return (
        f'<i class="fi {clase}" style="font-size:{tamano}px; color:{color}; '
        'vertical-align:middle; margin-right:10px;"></i>'
    )

def titulo_ui(texto, clase_icono="fi-rr-apps", nivel=2, tamano=30):
    tag = f"h{nivel}"
    st.markdown(
        f'<{tag} class=\"ui-section-title\">{icono_ui(clase_icono, tamano)}{texto}</{tag}>',
        unsafe_allow_html=True,
    )


# ============================================================
# FUNCIÓN FORMATEAR FECHA
# ============================================================

def parsear_fecha(valor_fecha):
    """Convierte fechas de Google Sheets/ISO/DD-MM-YYYY a Timestamp."""
    if valor_fecha is None:
        return pd.NaT

    if isinstance(valor_fecha, (datetime, date)):
        try:
            return pd.Timestamp(valor_fecha)
        except Exception:
            return pd.NaT

    texto = str(valor_fecha).strip()

    if not texto:
        return pd.NaT

    # Formato principal de la aplicación: DD-MM-YYYY
    dt = pd.to_datetime(
        texto,
        format="%d-%m-%Y",
        errors="coerce"
    )

    if not pd.isna(dt):
        return dt

    # ISO generado por Google Apps Script
    dt = pd.to_datetime(
        texto,
        errors="coerce",
        dayfirst=False
    )

    return dt


def formatear_fecha(valor_fecha):
    dt = parsear_fecha(valor_fecha)

    if pd.isna(dt):
        texto = str(valor_fecha).strip() if valor_fecha is not None else ""
        return "" if texto.lower() in ("nan", "nat", "none") else texto

    return dt.strftime("%d-%m-%Y")


# ============================================================
# MOSTRAR LOGO
# ============================================================

if icono_pestana is not None:
    col_l1, col_l2, col_l3 = st.columns(3)

    with col_l2:
        st.image(
            icono_pestana,
            width="stretch"
        )


# ============================================================
# ALIMENTACIÓN RECOMENDADA SEGÚN OBJETIVO
# Utiliza UIcons de Flaticon ya cargados por la aplicación.
# ============================================================

def calcular_recomendacion_alimentaria(row):
    """Calcula una guía orientativa desde la última evaluación disponible."""
    def numero(campos, predeterminado=0.0):
        for campo in campos:
            try:
                valor = float(row.get(campo, 0) or 0)
                if valor > 0:
                    return valor
            except (TypeError, ValueError):
                continue
        return float(predeterminado)

    peso = numero(["peso_kg", "peso"], 70.0)
    calorias = numero(["calorias_objetivo"], 0.0)
    meta = str(row.get("meta", row.get("objetivo", "Mantenimiento"))).strip().lower()

    if "ganar" in meta or "músc" in meta or "mus" in meta:
        objetivo, factor_proteina, grasa_pct, color = "Ganar músculo", 1.8, 0.27, "#35d0ba"
        enfoque = "Prioriza proteína suficiente, carbohidratos para apoyar el entrenamiento y alimentos variados."
    elif "perder" in meta or "grasa" in meta or "peso" in meta:
        objetivo, factor_proteina, grasa_pct, color = "Perder peso / grasa", 1.8, 0.28, "#ff7185"
        enfoque = "Prioriza proteína, verduras, fibra y porciones ajustadas a tu objetivo energético."
    else:
        objetivo, factor_proteina, grasa_pct, color = "Mantenimiento", 1.6, 0.30, "#69aefc"
        enfoque = "Busca una alimentación equilibrada que ayude a mantener tu peso, energía y rendimiento."

    if calorias <= 0:
        calorias = max(1200.0, peso * 30.0)

    proteina = round(peso * factor_proteina)
    grasa = round((calorias * grasa_pct) / 9)
    carbohidratos = max(50, round((calorias - proteina * 4 - grasa * 9) / 4))

    distribucion = [
        {"nombre": "Desayuno", "icono": "fi-rr-sun", "kcal": 0.25, "p": 0.25, "c": 0.25, "g": 0.22,
         "alimentos": "Huevos o yogur griego, avena o pan integral y una fruta."},
        {"nombre": "Almuerzo", "icono": "fi-rr-utensils", "kcal": 0.32, "p": 0.30, "c": 0.35, "g": 0.32,
         "alimentos": "Pollo, pescado, huevos o legumbres; arroz, papa o pasta; verduras y una porción de grasa saludable."},
        {"nombre": "Merienda / entrenamiento", "icono": "fi-rr-dumbbell", "kcal": 0.15, "p": 0.18, "c": 0.17, "g": 0.16,
         "alimentos": "Yogur alto en proteína o una alternativa equivalente, fruta y avena o pan integral según preferencia."},
        {"nombre": "Cena", "icono": "fi-rr-moon", "kcal": 0.28, "p": 0.27, "c": 0.23, "g": 0.30,
         "alimentos": "Pescado, pollo, huevos, tofu o legumbres; una porción de papa, arroz u otro cereal y verduras."},
    ]
    comidas = []
    for item in distribucion:
        comidas.append({
            **item,
            "kcal_total": round(calorias * item["kcal"]),
            "proteina": round(proteina * item["p"]),
            "carbohidratos": round(carbohidratos * item["c"]),
            "grasa": round(grasa * item["g"]),
        })

    return {
        "objetivo": objetivo, "color": color, "enfoque": enfoque,
        "calorias": round(calorias), "proteina": proteina,
        "carbohidratos": carbohidratos, "grasa": grasa, "comidas": comidas,
    }


def mostrar_alimentacion_recomendada(row, nombre_cliente="Cliente"):
    """Muestra macros y ejemplos de comidas del cliente seleccionado."""
    if row is None or not hasattr(row, "index") or len(row.index) == 0:
        st.info("Todavía no hay una evaluación disponible para generar la guía alimentaria.")
        return

    plan = calcular_recomendacion_alimentaria(row)
    color = plan["color"]
    st.markdown("---")
    titulo_ui("Alimentación recomendada", "fi-rr-restaurant", 3, 26)
    st.caption(
        "Guía orientativa calculada con el peso, el objetivo y las calorías de la última evaluación. "
        "No sustituye una valoración individual de nutrición."
    )

    st.markdown(
        f"""<div style="background:linear-gradient(135deg,rgba(255,255,255,.085),rgba(255,255,255,.025));
        border:1px solid {color}77;border-radius:20px;padding:20px;margin:8px 0 16px;
        box-shadow:0 10px 32px rgba(0,0,0,.20);">
        <div style="font-size:13px;opacity:.78;">PLAN ORIENTATIVO · {nombre_cliente}</div>
        <div style="font-size:26px;font-weight:800;color:{color};margin:6px 0;">{plan['objetivo']}</div>
        <div style="font-size:14px;opacity:.9;">{plan['enfoque']}</div></div>""",
        unsafe_allow_html=True,
    )

    columnas = st.columns(4)
    tarjetas = [
        ("fi-rr-bolt", "Energía", f"{plan['calorias']:,} kcal/día", "#f6c85f"),
        ("fi-rr-egg", "Proteína", f"{plan['proteina']} g/día", "#35d0ba"),
        ("fi-rr-wheat", "Carbohidratos", f"{plan['carbohidratos']} g/día", "#69aefc"),
        ("fi-rr-apple-whole", "Grasas", f"{plan['grasa']} g/día", "#c49bff"),
    ]
    for col, (icono, etiqueta, valor, tono) in zip(columnas, tarjetas):
        with col:
            st.markdown(
                f"""<div style="height:100%;min-height:112px;padding:15px 12px;border-radius:16px;
                border:1px solid {tono}66;background:rgba(255,255,255,.045);text-align:center;">
                <div style="font-size:22px;color:{tono};"><i class="fi {icono}"></i></div>
                <div style="font-size:12px;opacity:.8;margin-top:5px;">{etiqueta}</div>
                <div style="font-size:19px;font-weight:800;color:{tono};margin-top:4px;">{valor}</div></div>""",
                unsafe_allow_html=True,
            )

    st.markdown("#### Distribución sugerida por comida")
    for comida in plan["comidas"]:
        st.markdown(
            f"""<div style="background:linear-gradient(145deg,rgba(255,255,255,.07),rgba(255,255,255,.025));
            border:1px solid rgba(255,255,255,.11);border-radius:17px;padding:17px;margin:10px 0;">
            <div style="display:flex;justify-content:space-between;align-items:center;gap:12px;flex-wrap:wrap;">
            <div style="font-size:19px;font-weight:800;"><i class="fi {comida['icono']}" style="color:{color};"></i>
            &nbsp;{comida['nombre']}</div><div style="font-weight:800;color:{color};">≈ {comida['kcal_total']} kcal</div></div>
            <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:13px;">
            <span style="padding:7px 10px;border-radius:9px;background:rgba(53,208,186,.12);">Proteína: <b>{comida['proteina']} g</b></span>
            <span style="padding:7px 10px;border-radius:9px;background:rgba(105,174,252,.12);">Carbohidratos: <b>{comida['carbohidratos']} g</b></span>
            <span style="padding:7px 10px;border-radius:9px;background:rgba(196,155,255,.12);">Grasas: <b>{comida['grasa']} g</b></span></div>
            <div style="margin-top:12px;font-size:14px;opacity:.9;"><b>Ideas de alimentos:</b> {comida['alimentos']}</div></div>""",
            unsafe_allow_html=True,
        )

    st.info(
        "Las cantidades de macronutrientes por comida son aproximadas y no equivalen a gramos de cada alimento. "
        "Las porciones reales deben ajustarse a preferencias, alergias, salud y entrenamiento; consulta a un profesional "
        "si necesitas una dieta individualizada."
    )


# ============================================================
# CALCULAR MÉTRICAS (CORREGIDO Y AJUSTADO MATEMÁTICAMENTE)
# ============================================================

def calcular_metricas(
    peso,
    estatura_cm,
    edad,
    sexo,
    cuello,
    cintura,
    cadera,
    meta,
):
    """Calcula IMC, % de grasa, calorías objetivo y edad metabólica estimada.

    La ecuación de densidad tipo US Navy utilizada aquí aplica sus
    coeficientes sobre medidas en centímetros. La fórmula se mantiene
    consistente con los resultados históricos esperados por la aplicación.

    La edad metabólica es solamente una estimación orientativa; no es
    una medida clínica universal.
    """
    peso = float(peso)
    estatura_cm = float(estatura_cm)
    edad = int(edad)
    cuello = float(cuello)
    cintura = float(cintura)
    cadera = float(cadera)

    if peso <= 0:
        raise ValueError("El peso debe ser mayor que cero.")
    if estatura_cm <= 0:
        raise ValueError("La estatura debe ser mayor que cero.")
    if edad <= 0:
        raise ValueError("La edad debe ser mayor que cero.")
    if cuello <= 0 or cintura <= 0 or cadera <= 0:
        raise ValueError("Cuello, cintura y cadera deben ser mayores que cero.")

    # ============================================================
    # IMC
    # ============================================================
    estatura_m = estatura_cm / 100.0
    imc = peso / (estatura_m ** 2)

    # ============================================================
    # % GRASA - ECUACIÓN TIPO US NAVY
    #
    # Estos coeficientes de densidad se aplican directamente a
    # centímetros. No convertir a pulgadas aquí.
    # ============================================================
    if sexo == "Masculino":
        circunferencia = cintura - cuello

        if circunferencia <= 0:
            raise ValueError("La cintura debe ser mayor que el cuello.")

        densidad = (
            1.0324
            - 0.19077 * math.log10(circunferencia)
            + 0.15456 * math.log10(estatura_cm)
        )

    else:
        circunferencia = cintura + cadera - cuello

        if circunferencia <= 0:
            raise ValueError(
                "La combinación cintura + cadera - cuello no es válida."
            )

        densidad = (
            1.29579
            - 0.35004 * math.log10(circunferencia)
            + 0.22100 * math.log10(estatura_cm)
        )

    pct_grasa = (495.0 / densidad) - 450.0
    pct_grasa = max(3.0, min(pct_grasa, 60.0))

    # ============================================================
    # TMB - MIFFLIN-ST JEOR
    # ============================================================
    if sexo == "Masculino":
        tmb = (
            10 * peso
            + 6.25 * estatura_cm
            - 5 * edad
            + 5
        )
    else:
        tmb = (
            10 * peso
            + 6.25 * estatura_cm
            - 5 * edad
            - 161
        )

    # ============================================================
    # MANTENIMIENTO Y CALORÍAS OBJETIVO
    # ============================================================
    mantenimiento = tmb * 1.375

    if meta == "Perder Grasa":
        calorias = mantenimiento - 400
    elif meta == "Ganar Músculo":
        calorias = mantenimiento + 350
    else:
        calorias = mantenimiento

    calorias = max(800, calorias)

    # ============================================================
    # EDAD METABÓLICA - ESTIMACIÓN ORIENTATIVA
    #
    # Se utiliza la composición corporal para obtener una TMB por
    # Katch-McArdle y luego se calcula una edad equivalente con
    # Mifflin-St Jeor. Para evitar que la diferencia entre ambas
    # ecuaciones produzca valores exagerados, el resultado se acerca
    # de forma conservadora a la edad real del cliente.
    #
    # IMPORTANTE: es un indicador orientativo, no una medición clínica.
    # ============================================================
    masa_magra = peso * (1.0 - pct_grasa / 100.0)
    tmb_composicion = 370.0 + (21.6 * masa_magra)

    if sexo == "Masculino":
        constante_sexo = 5.0
    else:
        constante_sexo = -161.0

    edad_equivalente = (
        10 * peso
        + 6.25 * estatura_cm
        + constante_sexo
        - tmb_composicion
    ) / 5.0

    # Suavizado conservador: solo el 35 % de la diferencia se refleja
    # en la edad metabólica para reducir el efecto de error acumulado
    # entre las ecuaciones de composición corporal y TMB.
    diferencia_edad = edad_equivalente - edad
    diferencia_edad = max(-10.0, min(diferencia_edad, 10.0))
    edad_metabolica = edad + (diferencia_edad * 0.35)

    edad_metabolica = int(round(edad_metabolica))
    edad_metabolica = max(18, min(edad_metabolica, 80))

    return (
        round(imc, 2),
        round(pct_grasa, 2),
        int(round(calorias)),
        edad_metabolica,
    )


# ============================================================
# WHATSAPP
# ============================================================

def link_whatsapp(
    num_celular,
    nombre_cliente,
    mensaje=""
):
    num_limpio = (
        str(num_celular)
        .strip()
        .replace(" ", "")
        .replace("-", "")
        .replace(".", "")
    )

    if not num_limpio.startswith("57"):
        num_limpio = "57" + num_limpio

    if not mensaje:
        mensaje = (
            f"💪 ¡Hola {nombre_cliente}! "
            "Te saludamos de tu plan de "
            "Entrenamiento Personalizado. "
            "¡Queremos revisar cómo van "
            "tus avances!"
        )

    return (
        "https://wa.me/"
        f"{num_limpio}"
        "?text="
        + urllib.parse.quote(mensaje)
    )


# ============================================================
# NORMALIZAR CÉDULA
# ============================================================

def normalizar_cedula(valor):
    if pd.isna(valor):
        return ""
    return str(valor).replace(".0", "").strip()


# ============================================================
# CONVERTIR RESPUESTAS DE GOOGLE SHEETS A DATAFRAME
# ============================================================

def construir_dataframe(raw, columnas_default):
    """
    Acepta respuestas de Apps Script en cualquiera de estos formatos:
    1) Matriz: [headers, fila1, fila2, ...]
    2) Lista de diccionarios: [{...}, {...}]
    3) Diccionario con data/rows/values
    """
    if raw is None:
        return pd.DataFrame(columns=columnas_default)

    # Si Apps Script devuelve un objeto, buscar el contenedor de filas.
    if isinstance(raw, dict):
        for clave in ("data", "rows", "values", "items", "result"):
            if clave in raw and isinstance(raw[clave], (list, tuple)):
                raw = raw[clave]
                break
        else:
            # Un único registro como diccionario.
            raw = [raw]

    if not isinstance(raw, (list, tuple)) or len(raw) == 0:
        return pd.DataFrame(columns=columnas_default)

    # Lista de diccionarios.
    if isinstance(raw[0], dict):
        df = pd.DataFrame(list(raw))
        df.columns = [str(c).strip().lower() for c in df.columns]
        return df

    # Matriz de Google Sheets: primera fila = encabezados.
    if isinstance(raw[0], (list, tuple)):
        headers = [str(c).strip().lower() for c in raw[0]]
        rows = list(raw[1:])
        if not headers:
            return pd.DataFrame(columns=columnas_default)

        # Evita errores si alguna fila tiene menos/más columnas.
        ancho = len(headers)
        filas_limpias = []
        for row in rows:
            row = list(row) if isinstance(row, (list, tuple)) else [row]
            if len(row) < ancho:
                row += [""] * (ancho - len(row))
            elif len(row) > ancho:
                row = row[:ancho]
            filas_limpias.append(row)

        df = pd.DataFrame(filas_limpias, columns=headers)
        df = df.loc[:, ~df.columns.duplicated()]
        return df

    return pd.DataFrame(columns=columnas_default)


# ============================================================
# CARGAR SOLO USUARIOS PARA LOGIN / REGISTRO
# ============================================================

@st.cache_data(ttl=5)
def cargar_usuarios_login():
    """
    Consulta únicamente la hoja Usuarios mediante el endpoint
    action=usuarios. Esto evita descargar Historial, Pagos y Clases
    cada vez que alguien intenta iniciar sesión.

    Retorna: (df_usuarios, error)
    error = None si la consulta fue exitosa.
    """
    try:
        respuesta = api_get(
            URL_API,
            params={"action": "usuarios"},
            timeout=15,
        )
        respuesta.raise_for_status()
        res = respuesta.json()

        if not isinstance(res, dict):
            return pd.DataFrame(), "La API no devolvió una respuesta válida."

        if str(res.get("status", "success")).lower() == "error":
            return pd.DataFrame(), str(
                res.get("message", "Error desconocido de Google Apps Script.")
            )

        usuarios_raw = res.get("usuarios", [])
        df_u = construir_dataframe(
            usuarios_raw,
            [
                "cedula",
                "nombre_completo",
                "whatsapp",
                "eps",
                "condiciones_medicas",
                "rol",
                "password",
                "fecha_registro",
            ],
        )

        if not df_u.empty and "cedula" in df_u.columns:
            df_u["cedula"] = df_u["cedula"].apply(normalizar_cedula)

        return df_u, None

    except requests.exceptions.Timeout:
        return (
            pd.DataFrame(),
            "Google Apps Script tardó demasiado en responder. Intenta nuevamente en unos segundos.",
        )
    except requests.exceptions.RequestException as e:
        return pd.DataFrame(), f"No fue posible conectar con Google Apps Script: {e}"
    except ValueError:
        return pd.DataFrame(), "Google Apps Script devolvió una respuesta que no es JSON válido."
    except Exception as e:
        return pd.DataFrame(), f"Error procesando usuarios: {e}"


# ============================================================
# CARGAR BASE DE DATOS COMPLETA
# ============================================================

@st.cache_data(ttl=20)
def cargar_bd():
    try:
        respuesta = api_get(
            URL_API,
            timeout=30
        )
        respuesta.raise_for_status()
        res = respuesta.json()

        # ====================================================
        # USUARIOS
        # ====================================================
        usuarios_raw = res.get("usuarios", [])
        df_u = construir_dataframe(
            usuarios_raw,
            [
                "cedula",
                "nombre_completo",
                "whatsapp",
                "eps",
                "condiciones_medicas",
                "rol",
                "password",
                "fecha_registro",
            ],
        )

        # ====================================================
        # HISTORIAL DE MEDIDAS
        # ====================================================
        historial_raw = res.get("historial", [])
        df_m = construir_dataframe(
            historial_raw,
            ['id_registro', 'fecha_evaluacion', 'cedula', 'edad', 'sexo', 'meta', 'peso_kg', 'estatura_cm', 'cuello_cm', 'hombros_cm', 'bicep_der_cm', 'bicep_izq_cm', 'pecho_cm', 'cintura_cm', 'cadera_cm', 'pierna_der_cm', 'pierna_izq_cm', 'gemelo_der_cm', 'gemelo_izq_cm', 'imc', 'porcentaje_grasa', 'calorias_objetivo', 'edad_metabolica'],
        )

        # ====================================================
        # PAGOS
        # ====================================================
        pagos_raw = res.get("pagos", [])
        df_p = construir_dataframe(
            pagos_raw,
            ['id_pago', 'cedula', 'fecha_pago', 'valor', 'concepto', 'valor_mensualidad'],
        )

        # ====================================================
        # PLANES
        # Se aprovecha la misma respuesta completa de la API para
        # evitar una segunda petición HTTP exclusiva para Planes.
        # ====================================================
        planes_raw = res.get("planes", [])
        df_planes = construir_dataframe(
            planes_raw,
            [
                "cedula",
                "nombre_completo",
                "tipo_plan",
                "fecha_inicio",
                "fecha_fin",
                "estado",
                "observaciones",
                "clases_incluidas",
                "id_plan",
            ],
        )

        # ====================================================
        # CLASES
        # ====================================================
        clases_raw = res.get("clases", [])
        df_c = construir_dataframe(
            clases_raw,
            ['id_clase', 'cedula', 'nombre_completo', 'fecha_clase', 'tipo_plan', 'periodo', 'estado', 'id_plan'],
        )

        # ====================================================
        # LIMPIAR CÉDULAS
        # ====================================================
        for dataframe in (df_u, df_m, df_p, df_planes, df_c):
            if not dataframe.empty and "cedula" in dataframe.columns:
                dataframe["cedula"] = dataframe["cedula"].apply(normalizar_cedula)

        # ====================================================
        # NUMÉRICOS DE MEDIDAS
        # ====================================================
        columnas_numericas_medidas = [
            "edad",
            "peso_kg",
            "estatura_cm",
            "cuello_cm",
            "hombros_cm",
            "bicep_der_cm",
            "bicep_izq_cm",
            "pecho_cm",
            "cintura_cm",
            "cadera_cm",
            "pierna_der_cm",
            "pierna_izq_cm",
            "gemelo_der_cm",
            "gemelo_izq_cm",
            "imc",
            "porcentaje_grasa",
            "calorias_objetivo",
            "edad_metabolica",
        ]

        for columna in columnas_numericas_medidas:
            if columna in df_m.columns:
                df_m[columna] = pd.to_numeric(df_m[columna], errors="coerce")

        # ====================================================
        # NUMÉRICOS DE PAGOS
        # ====================================================
        for columna in ["valor", "valor_mensualidad"]:
            if columna in df_p.columns:
                df_p[columna] = pd.to_numeric(df_p[columna], errors="coerce")

        # ====================================================
        # NUMÉRICOS DE PLANES Y CLASES
        # ====================================================
        if not df_planes.empty and "clases_incluidas" in df_planes.columns:
            df_planes["clases_incluidas"] = pd.to_numeric(
                df_planes["clases_incluidas"], errors="coerce"
            ).fillna(0)

        if not df_c.empty and "periodo" in df_c.columns:
            df_c["periodo"] = pd.to_numeric(df_c["periodo"], errors="coerce")

        # ====================================================
        # FECHAS
        # ====================================================
        if not df_u.empty and "fecha_registro" in df_u.columns:
            df_u["fecha_registro"] = df_u["fecha_registro"].apply(formatear_fecha)

        if not df_m.empty and "fecha_evaluacion" in df_m.columns:
            df_m["fecha_evaluacion"] = df_m["fecha_evaluacion"].apply(formatear_fecha)

        if not df_p.empty and "fecha_pago" in df_p.columns:
            df_p["fecha_pago"] = df_p["fecha_pago"].apply(formatear_fecha)

        if not df_planes.empty and "fecha_inicio" in df_planes.columns:
            df_planes["_fecha_inicio_dt"] = df_planes["fecha_inicio"].apply(parsear_fecha)
        else:
            df_planes["_fecha_inicio_dt"] = pd.NaT

        if not df_c.empty and "fecha_clase" in df_c.columns:
            df_c["fecha_clase"] = df_c["fecha_clase"].apply(formatear_fecha)

        if not df_c.empty and "fecha_registro" in df_c.columns:
            df_c["fecha_registro"] = df_c["fecha_registro"].apply(formatear_fecha)

        return (
            df_u,
            df_m,
            df_p,
            df_c,
            df_planes,
        )

    except Exception as e:
        st.error(f"Error procesando base de datos: {e}")
        return (
            pd.DataFrame(),
            pd.DataFrame(),
            pd.DataFrame(),
            pd.DataFrame(),
            pd.DataFrame()
        )


# ============================================================
# GRÁFICOS
# ============================================================

def mostrar_resumen_metricas_evolucion(df_filtrado):
    """Muestra de forma persistente los resultados de la última evaluación."""
    if df_filtrado is None or df_filtrado.empty:
        return

    datos = df_filtrado.copy()
    if "fecha_evaluacion" in datos.columns:
        datos["_fecha_evolucion"] = datos["fecha_evaluacion"].apply(parsear_fecha)
        datos = datos.sort_values("_fecha_evolucion", na_position="first")
    actual = datos.iloc[-1]

    def numero(columnas, default=0.0):
        for columna in columnas:
            if columna in actual.index:
                try:
                    valor = float(actual[columna])
                    if pd.notna(valor):
                        return valor
                except (TypeError, ValueError):
                    continue
        return float(default)

    imc = numero(["imc"])
    grasa = numero(["porcentaje_grasa", "grasa"])
    calorias = numero(["calorias_objetivo"])
    edad_metabolica = numero(["edad_metabolica"])

    titulo_ui("Resultados de tu última evaluación", "fi-rr-chart-line-up", 3, 24)
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("IMC", f"{imc:.2f}")
    c2.metric("% Grasa Estimada", f"{grasa:.2f}%")
    c3.metric("Calorías Recomendadas", f"{calorias:,.0f} kcal".replace(",", "."))
    c4.metric("Edad Metabólica", f"{edad_metabolica:.0f} años")


def mostrar_resumen_evolucion_actual(row):
    """Muestra permanentemente los resultados de la última evaluación física."""
    def numero(keys, default=0.0):
        for key in keys:
            if key in row.index:
                try:
                    valor = float(row[key])
                    if pd.notna(valor):
                        return valor
                except (TypeError, ValueError):
                    pass
        return default

    imc = numero(["imc"], 0.0)
    grasa = numero(["porcentaje_grasa", "grasa"], 0.0)
    calorias = numero(["calorias_objetivo"], 0.0)
    edad_metabolica = numero(["edad_metabolica"], 0.0)

    st.markdown("### 📊 Resultados de tu última evaluación")
    r1, r2, r3, r4 = st.columns(4)
    r1.metric("IMC", f"{imc:.2f}")
    r2.metric("% Grasa Estimada", f"{grasa:.2f}%")
    r3.metric("Calorías Recomendadas", f"{calorias:,.0f} kcal".replace(",", "."))
    r4.metric("Edad Metabólica", f"{edad_metabolica:.0f} años")

def mostrar_graficos_evolucion(df_filtrado):
    if df_filtrado.empty:
        return

    # Las 4 métricas principales quedan visibles permanentemente en
    # cualquier pantalla que utilice el módulo de Evolución Física.
    mostrar_resumen_metricas_evolucion(df_filtrado)

    df_graficos = df_filtrado.copy()

    columnas_num = [
        "peso_kg", "porcentaje_grasa", "cintura_cm", "pecho_cm", "cadera_cm",
        "bicep_der_cm", "bicep_izq_cm", "pierna_der_cm", "pierna_izq_cm",
        "gemelo_der_cm", "gemelo_izq_cm",
    ]

    for col in columnas_num:
        if col in df_graficos.columns:
            df_graficos[col] = pd.to_numeric(df_graficos[col], errors="coerce")

    df_graficos["fecha_dt"] = pd.to_datetime(
        df_graficos["fecha_evaluacion"], format="%d-%m-%Y", errors="coerce"
    )
    if df_graficos["fecha_dt"].isna().any():
        df_graficos["fecha_dt"] = pd.to_datetime(
            df_graficos["fecha_evaluacion"], errors="coerce"
        )

    df_graficos = (
        df_graficos.dropna(subset=["fecha_dt"]).sort_values(by="fecha_dt")
    )
    if df_graficos.empty:
        st.info("No hay fechas válidas para construir las gráficas.")
        return

    df_graficos["Fecha"] = df_graficos["fecha_dt"].dt.strftime("%d-%m-%Y")

    titulo_ui("Gráficas de Evolución Temporal", "fi-rr-chart-line-up", 3, 24)

    tab1, tab2, tab3, tab4 = st.tabs([
        "Peso y Composición",
        "Perímetros Principales",
        "Extremidades Superiores",
        "Piernas y Glúteos",
    ])

    with tab1:
        col_g1, col_g2 = st.columns(2)
        with col_g1:
            st.markdown("<p style='text-align:center;'>Evolución del Peso Corporal (kg)</p>", unsafe_allow_html=True)
            if "peso_kg" in df_graficos.columns:
                st.line_chart(
                    df_graficos.set_index("Fecha")[["peso_kg"]].rename(columns={"peso_kg": "Peso (kg)"})
                )
        with col_g2:
            st.markdown("<p style='text-align:center;'>Evolución del % de Grasa Corporal</p>", unsafe_allow_html=True)
            if "porcentaje_grasa" in df_graficos.columns:
                st.line_chart(
                    df_graficos.set_index("Fecha")[["porcentaje_grasa"]].rename(columns={"porcentaje_grasa": "% Grasa"})
                )

    with tab2:
        st.markdown("<p style='text-align:center;'>Evolución de Torso y Cintura (cm)</p>", unsafe_allow_html=True)
        cols, names = [], {}
        for col, name in [("cintura_cm", "Cintura"), ("pecho_cm", "Pecho"), ("cadera_cm", "Cadera / Glúteos")]:
            if col in df_graficos.columns:
                cols.append(col); names[col] = name
        if cols:
            st.line_chart(df_graficos.set_index("Fecha")[cols].rename(columns=names))
        else:
            st.info("No hay perímetros registrados.")

    with tab3:
        st.markdown("<p style='text-align:center;'>Evolución de Brazos (cm)</p>", unsafe_allow_html=True)
        cols, names = [], {}
        for col, name in [("bicep_der_cm", "Bícep Derecho"), ("bicep_izq_cm", "Bícep Izquierdo")]:
            if col in df_graficos.columns:
                cols.append(col); names[col] = name
        if cols:
            st.line_chart(df_graficos.set_index("Fecha")[cols].rename(columns=names))
        else:
            st.info("No hay medidas de brazos registradas.")

    with tab4:
        st.markdown("<p style='text-align:center;'>Comparativa de Piernas (cm)</p>", unsafe_allow_html=True)
        cols, names = [], {}
        for col, name in [("pierna_der_cm", "Pierna Derecha"), ("pierna_izq_cm", "Pierna Izquierda")]:
            if col in df_graficos.columns:
                cols.append(col); names[col] = name
        if cols:
            st.line_chart(df_graficos.set_index("Fecha")[cols].rename(columns=names))
        else:
            st.info("No hay medidas de piernas registradas.")

        st.markdown("<p style='text-align:center;'>Comparativa de Glúteos y Gemelos (cm)</p>", unsafe_allow_html=True)
        cols, names = [], {}
        for col, name in [
            ("cadera_cm", "Glúteos / Cadera"),
            ("gemelo_der_cm", "Gemelo Derecho"),
            ("gemelo_izq_cm", "Gemelo Izquierdo"),
        ]:
            if col in df_graficos.columns:
                cols.append(col); names[col] = name
        if cols:
            st.line_chart(df_graficos.set_index("Fecha")[cols].rename(columns=names))
        else:
            st.info("No hay medidas de glúteos/cadera o gemelos registradas.")



# ============================================================
# INFORME DE EVOLUCIÓN EN PDF
# ============================================================

def _numero_seguro(valor):
    try:
        if pd.isna(valor):
            return None
        return float(valor)
    except Exception:
        return None


def generar_informe_evolucion_pdf(df_historial_cliente, nombre_cliente, cedula_cliente, logo_path=None, incluir_alimentacion=False):
    """Genera un informe PDF de evolución y, opcionalmente, una guía alimentaria basada en la última evaluación."""
    try:
        from io import BytesIO
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER, TA_LEFT
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import cm
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle,
            Image as RLImage,
            PageBreak,
            KeepTogether,
        )
    except ImportError:
        raise RuntimeError(
            "Para generar el PDF debes agregar 'reportlab' a requirements.txt "
            "y volver a desplegar la aplicación."
        )

    if df_historial_cliente is None or df_historial_cliente.empty:
        raise ValueError("El cliente no tiene evaluaciones registradas para generar el informe.")

    df = df_historial_cliente.copy()
    df["_fecha_dt"] = df["fecha_evaluacion"].apply(parsear_fecha)
    df = df.sort_values("_fecha_dt", ascending=True, na_position="last").reset_index(drop=True)

    # Si hay fechas no válidas, igual conservar los registros y mostrar su texto original.
    if df.empty:
        raise ValueError("No fue posible preparar las evaluaciones del cliente.")

    inicial = df.iloc[0]
    actual = df.iloc[-1]

    def valor_fila(row, columna):
        return _numero_seguro(row[columna]) if columna in row.index else None

    def fmt_num(v, dec=1):
        if v is None:
            return "—"
        return f"{v:,.{dec}f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def fmt_cambio(v, dec=1, sufijo=""):
        if v is None:
            return "—"
        signo = "+" if v > 0 else ""
        return f"{signo}{fmt_num(v, dec)}{sufijo}"

    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=1.35 * cm,
        leftMargin=1.35 * cm,
        topMargin=1.25 * cm,
        bottomMargin=1.25 * cm,
        title=f"Informe de Evolución - {nombre_cliente}",
        author="Julian Avila - Personal Training & Evolution Tracker",
    )

    styles = getSampleStyleSheet()
    titulo = ParagraphStyle(
        "TituloInforme", parent=styles["Title"], fontName="Helvetica-Bold",
        fontSize=20, leading=23, alignment=TA_CENTER, textColor=colors.HexColor("#111111"),
        spaceAfter=5,
    )
    subtitulo = ParagraphStyle(
        "Subtitulo", parent=styles["Normal"], fontName="Helvetica",
        fontSize=10, leading=13, alignment=TA_CENTER, textColor=colors.HexColor("#555555"),
        spaceAfter=10,
    )
    h2 = ParagraphStyle(
        "H2Informe", parent=styles["Heading2"], fontName="Helvetica-Bold",
        fontSize=13, leading=16, textColor=colors.HexColor("#111111"), spaceBefore=7, spaceAfter=7,
    )
    normal = ParagraphStyle(
        "NormalInforme", parent=styles["Normal"], fontName="Helvetica",
        fontSize=8.5, leading=11, textColor=colors.HexColor("#222222"),
    )
    small = ParagraphStyle(
        "SmallInforme", parent=normal, fontSize=7.5, leading=9.5,
    )
    # Estilo específico para encabezados de tablas.
    # Las tablas tienen fondo negro, por lo que el texto debe ser blanco.
    table_header = ParagraphStyle(
        "TableHeaderInforme", parent=small, fontName="Helvetica-Bold",
        textColor=colors.white, alignment=TA_CENTER,
    )
    note = ParagraphStyle(
        "NotaInforme", parent=normal, fontSize=7.5, leading=10,
        textColor=colors.HexColor("#555555"),
    )

    story = []

    # Logo
    if logo_path and os.path.isfile(logo_path):
        try:
            logo = RLImage(logo_path)
            max_w = 6.2 * cm
            max_h = 2.0 * cm
            ratio = min(max_w / logo.imageWidth, max_h / logo.imageHeight)
            logo.drawWidth = logo.imageWidth * ratio
            logo.drawHeight = logo.imageHeight * ratio
            logo.hAlign = "CENTER"
            story.append(logo)
            story.append(Spacer(1, 0.18 * cm))
        except Exception:
            pass

    story.append(Paragraph("INFORME DE EVOLUCIÓN FÍSICA", titulo))
    story.append(Paragraph("Personal Training & Evolution Tracker · Julian Avila", subtitulo))

    fecha_generacion = datetime.today().strftime("%d-%m-%Y %H:%M")
    info_data = [
        [Paragraph("<b>Cliente</b>", normal), Paragraph(str(nombre_cliente), normal),
         Paragraph("<b>Cédula / ID</b>", normal), Paragraph(str(cedula_cliente), normal)],
        [Paragraph("<b>Evaluación inicial</b>", normal), Paragraph(formatear_fecha(inicial.get("fecha_evaluacion", "")), normal),
         Paragraph("<b>Evaluación actual</b>", normal), Paragraph(formatear_fecha(actual.get("fecha_evaluacion", "")), normal)],
        [Paragraph("<b>Evaluaciones registradas</b>", normal), Paragraph(str(len(df)), normal),
         Paragraph("<b>Informe generado</b>", normal), Paragraph(fecha_generacion, normal)],
    ]
    info_table = Table(info_data, colWidths=[3.0*cm, 6.2*cm, 3.0*cm, 5.0*cm])
    info_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F3F3F3")),
        ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#BBBBBB")),
        ("INNERGRID", (0,0), (-1,-1), 0.3, colors.HexColor("#D5D5D5")),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 0.28 * cm))

    # Resumen de indicadores principales
    story.append(Paragraph("1. Resumen de indicadores", h2))
    resumen_campos = [
        ("Peso", "peso_kg", "kg", 1),
        ("% Grasa corporal", "porcentaje_grasa", "%", 2),
        ("IMC", "imc", "", 2),
        ("Calorías objetivo", "calorias_objetivo", "kcal", 0),
        ("Edad metabólica estimada", "edad_metabolica", "años", 0),
    ]
    resumen_data = [[
        Paragraph("Indicador", table_header), Paragraph("Inicial", table_header),
        Paragraph("Actual", table_header), Paragraph("Cambio", table_header)
    ]]
    for etiqueta, campo, sufijo, dec in resumen_campos:
        vi = valor_fila(inicial, campo)
        va = valor_fila(actual, campo)
        cambio = (va - vi) if vi is not None and va is not None else None
        resumen_data.append([
            Paragraph(etiqueta, small),
            Paragraph((fmt_num(vi, dec) + (" " + sufijo if sufijo else "")), small),
            Paragraph((fmt_num(va, dec) + (" " + sufijo if sufijo else "")), small),
            Paragraph((fmt_cambio(cambio, dec, (" " + sufijo if sufijo else ""))), small),
        ])
    resumen_table = Table(resumen_data, colWidths=[6.0*cm, 3.4*cm, 3.4*cm, 4.4*cm], repeatRows=1)
    resumen_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#171717")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#CCCCCC")),
        ("BACKGROUND", (0,1), (-1,-1), colors.white),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F7F7F7")]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
    ]))
    story.append(resumen_table)
    story.append(Spacer(1, 0.18 * cm))
    story.append(Paragraph(
        "Los cambios se muestran de forma descriptiva entre la primera y la última evaluación registrada. "
        "La interpretación debe considerar el objetivo individual y el contexto de cada evaluación.", note
    ))
    story.append(Paragraph(
        "La edad metabólica es un indicador estimado y orientativo calculado a partir de ecuaciones antropométricas y de metabolismo basal. "
        "No constituye una medición clínica ni debe interpretarse de forma aislada.", note
    ))

    # Tabla antropométrica completa
    story.append(Paragraph("2. Comparativa antropométrica completa", h2))
    antropometricos = [
        ("Cuello", "cuello_cm"),
        ("Hombros", "hombros_cm"),
        ("Pecho", "pecho_cm"),
        ("Cintura / Abdomen", "cintura_cm"),
        ("Cadera / Glúteos", "cadera_cm"),
        ("Bíceps Derecho", "bicep_der_cm"),
        ("Bíceps Izquierdo", "bicep_izq_cm"),
        ("Pierna Derecha", "pierna_der_cm"),
        ("Pierna Izquierda", "pierna_izq_cm"),
        ("Gemelo Derecho", "gemelo_der_cm"),
        ("Gemelo Izquierdo", "gemelo_izq_cm"),
    ]
    ant_data = [[
        Paragraph("Medida", table_header), Paragraph("Inicial (cm)", table_header),
        Paragraph("Actual (cm)", table_header), Paragraph("Cambio (cm)", table_header)
    ]]
    for etiqueta, campo in antropometricos:
        vi = valor_fila(inicial, campo)
        va = valor_fila(actual, campo)
        cambio = (va - vi) if vi is not None and va is not None else None
        ant_data.append([
            Paragraph(etiqueta, small),
            Paragraph(fmt_num(vi, 1), small),
            Paragraph(fmt_num(va, 1), small),
            Paragraph(fmt_cambio(cambio, 1), small),
        ])
    ant_table = Table(ant_data, colWidths=[7.0*cm, 3.1*cm, 3.1*cm, 4.0*cm], repeatRows=1)
    ant_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#171717")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F7F7F7")]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 6),
        ("RIGHTPADDING", (0,0), (-1,-1), 6),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(ant_table)

    # Guía de alimentación opcional: toma automáticamente el objetivo y datos
    # de la última evaluación guardada; nunca solicita elegir perder grasa/ganar músculo.
    if incluir_alimentacion:
        try:
            plan_alimentario = calcular_recomendacion_alimentaria(actual)
            story.append(PageBreak())
            story.append(Paragraph("GUÍA DE ALIMENTACIÓN ORIENTATIVA", titulo))
            story.append(Paragraph(
                "Generada automáticamente con los datos y el objetivo registrados en la última evaluación.",
                subtitulo,
            ))
            story.append(Paragraph(f"Objetivo registrado: {plan_alimentario['objetivo']}", h2))
            story.append(Paragraph(plan_alimentario["enfoque"], normal))
            story.append(Spacer(1, 0.18 * cm))

            macros_data = [
                [Paragraph("Energía diaria", table_header), Paragraph("Proteína", table_header),
                 Paragraph("Carbohidratos", table_header), Paragraph("Grasas", table_header)],
                [Paragraph(f"{plan_alimentario['calorias']} kcal", normal),
                 Paragraph(f"{plan_alimentario['proteina']} g", normal),
                 Paragraph(f"{plan_alimentario['carbohidratos']} g", normal),
                 Paragraph(f"{plan_alimentario['grasa']} g", normal)],
            ]
            macros_table = Table(macros_data, colWidths=[4.1*cm, 4.1*cm, 4.1*cm, 4.1*cm])
            macros_table.setStyle(TableStyle([
                ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#171717")),
                ("BACKGROUND", (0,1), (-1,1), colors.HexColor("#F3F3F3")),
                ("GRID", (0,0), (-1,-1), 0.35, colors.HexColor("#CCCCCC")),
                ("ALIGN", (0,0), (-1,-1), "CENTER"),
                ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
                ("TOPPADDING", (0,0), (-1,-1), 8),
                ("BOTTOMPADDING", (0,0), (-1,-1), 8),
            ]))
            story.append(macros_table)
            story.append(Spacer(1, 0.35 * cm))
            story.append(Paragraph("Distribución sugerida por comida", h2))

            for comida in plan_alimentario["comidas"]:
                comida_data = [
                    [Paragraph(f"<b>{comida['nombre']}</b> · aproximadamente {comida['kcal_total']} kcal", normal)],
                    [Paragraph(
                        f"Proteína: {comida['proteina']} g · Carbohidratos: {comida['carbohidratos']} g · "
                        f"Grasas: {comida['grasa']} g", small)],
                    [Paragraph(f"<b>Ideas de alimentos:</b> {comida['alimentos']}", normal)],
                ]
                comida_table = Table(comida_data, colWidths=[16.4*cm])
                comida_table.setStyle(TableStyle([
                    ("BACKGROUND", (0,0), (-1,-1), colors.HexColor("#F7F7F7")),
                    ("BOX", (0,0), (-1,-1), 0.5, colors.HexColor("#D5D5D5")),
                    ("LINEBELOW", (0,0), (-1,0), 0.4, colors.HexColor("#B8B8B8")),
                    ("LEFTPADDING", (0,0), (-1,-1), 8),
                    ("RIGHTPADDING", (0,0), (-1,-1), 8),
                    ("TOPPADDING", (0,0), (-1,-1), 5),
                    ("BOTTOMPADDING", (0,0), (-1,-1), 5),
                ]))
                story.append(KeepTogether([comida_table, Spacer(1, 0.18*cm)]))

            story.append(Spacer(1, 0.15*cm))
            story.append(Paragraph(
                "Importante: esta guía es orientativa. Los macronutrientes por comida son aproximados y no equivalen "
                "a gramos de cada alimento. Ajusta las porciones a preferencias, alergias y necesidades personales; "
                "no sustituye una valoración individual de nutrición.", note
            ))
        except Exception as exc:
            raise ValueError(f"No se pudo generar la guía alimentaria con los datos guardados: {exc}")

    # Historial completo de evaluaciones
    story.append(PageBreak())
    story.append(Paragraph("3. Historial de evaluaciones", h2))
    historia_campos = [
        ("Fecha", "fecha_evaluacion"),
        ("Peso (kg)", "peso_kg"),
        ("% Grasa", "porcentaje_grasa"),
        ("IMC", "imc"),
        ("Cintura (cm)", "cintura_cm"),
        ("Cadera (cm)", "cadera_cm"),
        ("Pierna D (cm)", "pierna_der_cm"),
        ("Pierna I (cm)", "pierna_izq_cm"),
        ("Gemelo D (cm)", "gemelo_der_cm"),
        ("Gemelo I (cm)", "gemelo_izq_cm"),
    ]
    hist_data = [[Paragraph(x[0], table_header) for x in historia_campos]]
    for _, row in df.iterrows():
        fila = []
        for etiqueta, campo in historia_campos:
            if campo == "fecha_evaluacion":
                valor = formatear_fecha(row.get(campo, ""))
            else:
                n = valor_fila(row, campo)
                valor = fmt_num(n, 1) if n is not None else "—"
            fila.append(Paragraph(str(valor), small))
        hist_data.append(fila)
    hist_widths = [2.2*cm, 1.7*cm, 1.7*cm, 1.6*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm, 1.8*cm]
    hist_table = Table(hist_data, colWidths=hist_widths, repeatRows=1)
    hist_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#171717")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F7F7F7")]),
        ("ALIGN", (1,1), (-1,-1), "CENTER"),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 3),
        ("RIGHTPADDING", (0,0), (-1,-1), 3),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(hist_table)

    # Datos complementarios de las evaluaciones
    story.append(Spacer(1, 0.25 * cm))
    story.append(Paragraph("4. Datos complementarios", h2))
    comp_data = [[
        Paragraph("Fecha", table_header), Paragraph("Edad", table_header), Paragraph("Sexo", table_header),
        Paragraph("Meta", table_header), Paragraph("Calorías", table_header), Paragraph("Edad metabólica", table_header)
    ]]
    for _, row in df.iterrows():
        comp_data.append([
            Paragraph(formatear_fecha(row.get("fecha_evaluacion", "")), small),
            Paragraph(fmt_num(valor_fila(row, "edad"), 0), small),
            Paragraph(str(row.get("sexo", "—")), small),
            Paragraph(str(row.get("meta", "—")), small),
            Paragraph(fmt_num(valor_fila(row, "calorias_objetivo"), 0), small),
            Paragraph(fmt_num(valor_fila(row, "edad_metabolica"), 0), small),
        ])
    comp_table = Table(comp_data, colWidths=[2.3*cm, 1.6*cm, 2.4*cm, 4.0*cm, 2.3*cm, 3.2*cm], repeatRows=1)
    comp_table.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (-1,0), colors.HexColor("#171717")),
        ("TEXTCOLOR", (0,0), (-1,0), colors.white),
        ("GRID", (0,0), (-1,-1), 0.3, colors.HexColor("#CCCCCC")),
        ("ROWBACKGROUNDS", (0,1), (-1,-1), [colors.white, colors.HexColor("#F7F7F7")]),
        ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
        ("LEFTPADDING", (0,0), (-1,-1), 4),
        ("RIGHTPADDING", (0,0), (-1,-1), 4),
        ("TOPPADDING", (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
    ]))
    story.append(comp_table)

    story.append(Spacer(1, 0.3 * cm))
    story.append(Paragraph(
        "Nota: IMC, porcentaje de grasa, calorías objetivo y edad metabólica son cálculos/estimaciones "
        "generados por la aplicación a partir de los datos registrados. Este informe es de seguimiento "
        "deportivo y no sustituye una valoración médica o clínica.", note
    ))

    def pie_pagina(canvas, doc_obj):
        canvas.saveState()
        canvas.setStrokeColor(colors.HexColor("#DDDDDD"))
        canvas.line(1.35*cm, 0.9*cm, A4[0]-1.35*cm, 0.9*cm)
        canvas.setFont("Helvetica", 7)
        canvas.setFillColor(colors.HexColor("#666666"))
        canvas.drawString(1.35*cm, 0.55*cm, "Julian Avila · Personal Training & Evolution Tracker")
        canvas.drawRightString(A4[0]-1.35*cm, 0.55*cm, f"Página {doc_obj.page}")
        canvas.restoreState()

    doc.build(story, onFirstPage=pie_pagina, onLaterPages=pie_pagina)
    buffer.seek(0)
    return buffer.getvalue()


def cargar_solo_planes():
    """
    Reutiliza la hoja Planes que ya viene en la respuesta completa de la API.
    Evita una petición HTTP adicional y comparte la misma caché de cargar_bd.
    """
    try:
        datos = cargar_bd()
        if isinstance(datos, (tuple, list)) and len(datos) >= 5:
            return datos[4]
        return pd.DataFrame()
    except Exception:
        # El resumen de clases no debe tumbar toda la aplicación si Planes
        # no responde temporalmente.
        return pd.DataFrame()


def obtener_resumen_clases(df_clases, cedula):
    """
    Obtiene el último plan activo del cliente y cuenta sus clases.

    Compatible con la estructura actual de Google Sheets:
    Planes: 8 columnas, sin id_plan.
    Clases: 7 columnas, sin id_plan.

    Si existe id_plan en una versión futura de la hoja, también lo utiliza.
    """
    resultado = {
        "plan": "Sin plan registrado",
        "id_plan": "",
        "fecha_inicio": pd.NaT,
        "clases_contratadas": 0,
        "clases_tomadas": 0,
        "clases_restantes": 0,
        "porcentaje": 0.0,
        "registros": pd.DataFrame(),
    }

    cedula_str = normalizar_cedula(cedula)
    if not cedula_str:
        return resultado

    # ------------------------------------------------------------
    # 1. Obtener el último plan ACTIVO del cliente
    # ------------------------------------------------------------
    df_planes = cargar_solo_planes()

    if not df_planes.empty and "cedula" in df_planes.columns:
        planes = df_planes.copy()
        planes["_cedula_norm"] = planes["cedula"].apply(normalizar_cedula)

        if "estado" not in planes.columns:
            planes["estado"] = "Activo"

        activos = planes[
            (planes["_cedula_norm"] == cedula_str)
            & (
                planes["estado"]
                .astype(str)
                .str.strip()
                .str.lower()
                .isin(["activo", "activa"])
            )
        ].copy()

        if not activos.empty:
            if "_fecha_inicio_dt" not in activos.columns:
                activos["_fecha_inicio_dt"] = activos["fecha_inicio"].apply(parsear_fecha)

            activos = activos.sort_values(
                by="_fecha_inicio_dt",
                ascending=True,
                na_position="first",
            )
            plan_activo = activos.iloc[-1]

            resultado["plan"] = str(plan_activo.get("tipo_plan", "")).strip()
            resultado["id_plan"] = str(plan_activo.get("id_plan", "")).strip()
            resultado["fecha_inicio"] = parsear_fecha(plan_activo.get("fecha_inicio"))

            try:
                resultado["clases_contratadas"] = int(
                    float(
                        pd.to_numeric(
                            plan_activo.get("clases_incluidas", 0),
                            errors="coerce",
                        )
                    )
                )
            except Exception:
                resultado["clases_contratadas"] = 0

    # ------------------------------------------------------------
    # 2. Filtrar clases del cliente
    # ------------------------------------------------------------
    if df_clases is not None and not df_clases.empty and "cedula" in df_clases.columns:
        clases = df_clases.copy()
        clases["_cedula_norm"] = clases["cedula"].apply(normalizar_cedula)

        if "estado" not in clases.columns:
            clases["estado"] = "Tomada"

        registros = clases[
            (clases["_cedula_norm"] == cedula_str)
            & (
                clases["estado"]
                .astype(str)
                .str.strip()
                .str.lower()
                == "tomada"
            )
        ].copy()

        # --------------------------------------------------------
        # 3. Asociar las clases al ciclo actual.
        #    - Si hay id_plan en ambas tablas, usarlo.
        #    - Si no existe (estructura actual), usar fecha_inicio.
        # --------------------------------------------------------
        id_plan_actual = resultado["id_plan"]

        if id_plan_actual and "id_plan" in registros.columns:
            registros["_id_plan_norm"] = (
                registros["id_plan"].fillna("").astype(str).str.strip()
            )
            registros = registros[
                registros["_id_plan_norm"] == id_plan_actual
            ].copy()
            registros = registros.drop(columns=["_id_plan_norm"], errors="ignore")

        elif not pd.isna(resultado["fecha_inicio"]) and "fecha_clase" in registros.columns:
            registros["_fecha_clase_dt"] = registros["fecha_clase"].apply(parsear_fecha)
            registros = registros[
                registros["_fecha_clase_dt"].notna()
                & (registros["_fecha_clase_dt"] >= resultado["fecha_inicio"])
            ].copy()
            registros = registros.drop(columns=["_fecha_clase_dt"], errors="ignore")

        elif id_plan_actual:
            # Hay ID de plan, pero las clases no lo traen: no mezclar históricos.
            registros = registros.iloc[0:0].copy()

        resultado["clases_tomadas"] = len(registros)
        resultado["registros"] = registros.drop(
            columns=["_cedula_norm"],
            errors="ignore",
        )

    # ------------------------------------------------------------
    # 4. Totales
    # ------------------------------------------------------------
    resultado["clases_restantes"] = max(
        resultado["clases_contratadas"] - resultado["clases_tomadas"],
        0,
    )

    if resultado["clases_contratadas"] > 0:
        resultado["porcentaje"] = min(
            (
                resultado["clases_tomadas"]
                / resultado["clases_contratadas"]
            )
            * 100,
            100,
        )

    return resultado


# ============================================================
# MOSTRAR RESUMEN DE CLASES
# ============================================================

def mostrar_resumen_clases(
    df_clases,
    cedula,
    titulo="Clases Personalizadas"
):
    resumen = obtener_resumen_clases(df_clases, cedula)

    titulo_ui(titulo, "fi-rr-dumbbell", 3, 24)

    if resumen["clases_contratadas"] <= 0:
        st.info("Este cliente todavía no tiene un plan de clases configurado.")
        return

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Plan", resumen["plan"])
    c2.metric("Clases contratadas", resumen["clases_contratadas"])
    c3.metric("Clases tomadas", resumen["clases_tomadas"])
    c4.metric("Clases restantes", resumen["clases_restantes"])

    porcentaje = float(resumen["porcentaje"])
    if porcentaje < 50:
        p_start, p_mid, p_end, p_glow = "#38bdf8", "#22d3ee", "#34d399", "#22d3ee"
    elif porcentaje < 80:
        p_start, p_mid, p_end, p_glow = "#22d3ee", "#a78bfa", "#fbbf24", "#a78bfa"
    else:
        p_start, p_mid, p_end, p_glow = "#fbbf24", "#fb7185", "#ef4444", "#fb7185"

    porcentaje_seguro = max(0.0, min(porcentaje, 100.0))
    st.markdown(
        f"""
        <div class="wow-progress-wrap">
            <div class="wow-progress-head">
                <span class="wow-progress-label">Progreso del plan · {resumen['clases_tomadas']} de {resumen['clases_contratadas']} clases</span>
                <span class="wow-progress-value">{porcentaje:.1f}%</span>
            </div>
            <div class="wow-progress-track" role="progressbar" aria-valuenow="{porcentaje_seguro:.1f}" aria-valuemin="0" aria-valuemax="100">
                <div class="wow-progress-fill" style="--progress-width:{porcentaje_seguro:.2f}%; --progress-start:{p_start}; --progress-mid:{p_mid}; --progress-end:{p_end}; --progress-glow:{p_glow};"></div>
            </div>
            <div class="wow-progress-scale"><span>0 clases</span><span>{resumen['clases_restantes']} restantes</span><span>Plan completo</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ============================================================
# ESTADO DE SESIÓN
# ============================================================

# ============================================================
# DASHBOARD ADMINISTRADOR - CAPA VISUAL
# ============================================================
def mostrar_dashboard_admin(df_usuarios, df_historial, df_pagos, df_clases):
    clientes = df_usuarios.copy() if not df_usuarios.empty else pd.DataFrame()
    if not clientes.empty and "rol" in clientes.columns:
        clientes = clientes[clientes["rol"].astype(str).str.lower() == "cliente"].copy()

    total_clientes = len(clientes)
    total_clases = len(df_clases) if not df_clases.empty else 0
    clases_tomadas = 0
    if not df_clases.empty and "estado" in df_clases.columns:
        clases_tomadas = int((df_clases["estado"].astype(str).str.lower() == "tomada").sum())

    total_ingresos = 0.0
    if not df_pagos.empty and "valor" in df_pagos.columns:
        total_ingresos = pd.to_numeric(df_pagos["valor"], errors="coerce").fillna(0).sum()

    ultima_evaluacion = "Sin registros"
    if not df_historial.empty and "fecha_evaluacion" in df_historial.columns:
        fechas = pd.to_datetime(df_historial["fecha_evaluacion"], errors="coerce")
        if fechas.notna().any():
            ultima_evaluacion = fechas.max().strftime("%d-%m-%Y")

    st.markdown(
        '<div class="dashboard-hero">'
        '<div class="dashboard-glow"></div>'
        '<div class="dashboard-kicker">PERSONAL TRAINING · CONTROL CENTER</div>'
        '<div class="dashboard-title">Dashboard General</div>'
        '<div class="dashboard-subtitle">Visión rápida de clientes, clases, ingresos y evolución.</div>'
        '</div>',
        unsafe_allow_html=True,
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Clientes", f"{total_clientes:,}")
    c2.metric("Clases tomadas", f"{clases_tomadas:,}")
    c3.metric("Ingresos registrados", f"${total_ingresos:,.0f}")
    c4.metric("Última evaluación", ultima_evaluacion)

    st.markdown('<div class="dashboard-section-title">Actividad de la plataforma</div>', unsafe_allow_html=True)
    left, right = st.columns([1.15, 0.85])

    with left:
        if not df_clases.empty and "fecha_clase" in df_clases.columns:
            actividad = df_clases.copy()
            actividad["fecha"] = pd.to_datetime(actividad["fecha_clase"], errors="coerce")
            actividad = actividad.dropna(subset=["fecha"])
            if not actividad.empty:
                actividad = actividad.groupby(actividad["fecha"].dt.strftime("%d-%m"), sort=False).size().tail(14)
                st.markdown('<div class="glass-panel-title">Clases por día</div>', unsafe_allow_html=True)
                st.line_chart(actividad, use_container_width=True)
            else:
                st.info("Aún no hay fechas de clases para mostrar.")
        else:
            st.info("Aún no hay clases registradas.")

    with right:
        if not df_pagos.empty and "valor" in df_pagos.columns:
            pagos = df_pagos.copy()
            pagos["valor_num"] = pd.to_numeric(pagos["valor"], errors="coerce").fillna(0)
            if "fecha_pago" in pagos.columns:
                pagos["fecha"] = pd.to_datetime(pagos["fecha_pago"], errors="coerce")
                pagos = pagos.dropna(subset=["fecha"])
                if not pagos.empty:
                    resumen = pagos.groupby(pagos["fecha"].dt.strftime("%b")).agg(Ingresos=("valor_num", "sum"))
                    st.markdown('<div class="glass-panel-title">Ingresos registrados</div>', unsafe_allow_html=True)
                    st.bar_chart(resumen, use_container_width=True)
                else:
                    st.metric("Total histórico", f"${total_ingresos:,.0f}")
            else:
                st.metric("Total histórico", f"${total_ingresos:,.0f}")
        else:
            st.info("Aún no hay pagos registrados.")

    st.markdown('<div class="dashboard-section-title">Resumen operativo</div>', unsafe_allow_html=True)
    r1, r2, r3 = st.columns(3)

    with r1:
        st.markdown(
            f'<div class="dashboard-card"><div class="dash-icon">👥</div>'
            f'<div class="dash-label">Clientes registrados</div><div class="dash-value">{total_clientes}</div>'
            f'<div class="dash-note">Usuarios con rol Cliente</div></div>',
            unsafe_allow_html=True,
        )
    with r2:
        st.markdown(
            f'<div class="dashboard-card"><div class="dash-icon">🏋️</div>'
            f'<div class="dash-label">Clases registradas</div><div class="dash-value">{total_clases}</div>'
            f'<div class="dash-note">Incluye historial de clases</div></div>',
            unsafe_allow_html=True,
        )
    with r3:
        st.markdown(
            f'<div class="dashboard-card"><div class="dash-icon">💳</div>'
            f'<div class="dash-label">Movimientos de pago</div><div class="dash-value">{len(df_pagos) if not df_pagos.empty else 0}</div>'
            f'<div class="dash-note">Ingresos registrados en sistema</div></div>',
            unsafe_allow_html=True,
        )


if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
    st.session_state["rol"] = None
    st.session_state["cedula"] = None
    st.session_state["nombre"] = None


# ============================================================
# TÍTULO
# ============================================================

st.title("GESTOR GIMNASIO · JULIAN AVILA")


# ============================================================
# LOGIN / REGISTRO
# ============================================================

if not st.session_state["autenticado"]:
    col1, col2 = st.columns(2)

    # LOGIN
    with col1:
        titulo_ui("Iniciar Sesión", "fi-rr-lock", 2, 28)

        cedula_ingreso = st.text_input(
            "Número de Cédula / ID:"
        ).strip()

        pass_ingreso = st.text_input(
            "Contraseña:",
            type="password"
        ).strip()

        if st.button("Ingresar", use_container_width=True):
            if cedula_ingreso == "admin" and pass_ingreso == "admin123456":
                st.session_state["autenticado"] = True
                st.session_state["rol"] = "Admin"
                st.session_state["cedula"] = "ADMIN"
                st.session_state["nombre"] = "JULIAN AVILA"
                st.rerun()
            else:
                # Para iniciar sesión consultamos únicamente Usuarios.
                # No descargamos Historial, Pagos ni Clases hasta que
                # la autenticación haya sido confirmada.
                df_usuarios, error_usuarios = cargar_usuarios_login()

                if error_usuarios:
                    st.error(f"⚠️ {error_usuarios}")
                elif df_usuarios.empty or "cedula" not in df_usuarios.columns:
                    st.error("❌ No fue posible verificar los usuarios en este momento. Intenta nuevamente.")
                elif normalizar_cedula(cedula_ingreso) in df_usuarios["cedula"].values:
                    u = df_usuarios[df_usuarios["cedula"] == normalizar_cedula(cedula_ingreso)].iloc[0]

                    if str(u["password"]).strip() == pass_ingreso:
                        st.session_state["autenticado"] = True
                        st.session_state["rol"] = u.get("rol", "Cliente")
                        st.session_state["cedula"] = str(u["cedula"])
                        st.session_state["nombre"] = u["nombre_completo"]
                        st.rerun()
                    else:
                        st.error("❌ Contraseña incorrecta.")
                else:
                    st.error("❌ Cédula no registrada.")

    # REGISTRO
    with col2:
        titulo_ui("Crear Cuenta Nueva", "fi-rr-user-add", 2, 28)

        with st.form("form_registro"):
            reg_cedula = st.text_input("Número de Cédula / ID:").strip()
            reg_nombre = st.text_input("Nombre Completo:").strip()
            reg_whatsapp = st.text_input(
                "Número de Whatsapp (10 dígitos):",
                placeholder="310......."
            ).strip()
            reg_eps = st.text_input("EPS :").strip()
            reg_condiciones = st.text_area(
                "Condiciones Médicas / Lesiones / Cirugías:"
            ).strip()
            reg_pass = st.text_input("Crea tu Contraseña:", type="password").strip()

            if st.form_submit_button("Crear Perfil"):
                # Para validar duplicados consultamos únicamente Usuarios.
                df_usuarios, error_usuarios = cargar_usuarios_login()

                if error_usuarios:
                    st.error(f"⚠️ {error_usuarios}")
                elif not reg_cedula or not reg_nombre or not reg_pass:
                    st.error("⚠️ Cédula, Nombre y Contraseña son obligatorios.")
                elif not df_usuarios.empty and normalizar_cedula(reg_cedula) in df_usuarios["cedula"].values:
                    st.error("❌ Esta cédula ya está registrada.")
                else:
                    datos_usuario = {
                        "action": "registrar_usuario",
                        "cedula": str(reg_cedula).strip(),
                        "nombre_completo": str(reg_nombre).strip(),
                        "whatsapp": str(reg_whatsapp).strip(),
                        "eps": reg_eps if reg_eps else "NINGUNA",
                        "condiciones_medicas": (
                            reg_condiciones
                            if reg_condiciones
                            else "NINGUNA"
                        ),
                        "rol": "Cliente",
                        "password": str(reg_pass),
                        "fecha_registro": datetime.today().strftime("%d-%m-%Y"),
                    }

                    try:
                        respuesta_registro = api_post(
                            URL_API,
                            json=datos_usuario,
                            timeout=30,
                        )
                        respuesta_registro.raise_for_status()

                        try:
                            resultado_registro = respuesta_registro.json()
                        except Exception:
                            resultado_registro = {}

                        if str(resultado_registro.get("status", "")).lower() == "error":
                            st.error(
                                "❌ Google Apps Script reportó un error: "
                                + str(
                                    resultado_registro.get(
                                        "message",
                                        "No fue posible registrar el usuario.",
                                    )
                                )
                            )
                        else:
                            invalidar_cache_datos()
                            st.success(
                                "✅ Perfil creado correctamente. "
                                "Ya puedes iniciar sesión con tu cédula y contraseña."
                            )

                    except Exception as e:
                        st.error(f"❌ Error al guardar usuario: {e}")



# ============================================================
# PLATAFORMA UNIFICADA PARA GIMNASIO
# Integra las funcionalidades completas de app_1 y la estructura
# modular planteada en app_2, sin depender de carpetas externas.
# ============================================================

def _clientes(df_usuarios):
    if df_usuarios is None or df_usuarios.empty:
        return pd.DataFrame()
    if "rol" in df_usuarios.columns:
        return df_usuarios[df_usuarios["rol"].astype(str).str.strip().str.lower() == "cliente"].copy()
    return df_usuarios.copy()


def _selector_cliente(clientes, key):
    if clientes.empty:
        st.info("No hay clientes registrados actualmente.")
        return None, None
    opciones = clientes["cedula"].astype(str) + " - " + clientes["nombre_completo"].astype(str)
    seleccionado = st.selectbox("Seleccionar Cliente", opciones.tolist(), key=key)
    cedula = str(seleccionado.split(" - ", 1)[0]).strip()
    nombre = str(seleccionado.split(" - ", 1)[1]).strip()
    return cedula, nombre


def mostrar_clientes_gym(df_usuarios, df_clases, df_pagos, df_historial):
    titulo_ui("Gestión de Clientes", "fi-rr-users", 2, 28)
    clientes = _clientes(df_usuarios)
    cedula, nombre = _selector_cliente(clientes, "gym_cliente_general")
    if not cedula:
        return
    fila = clientes[clientes["cedula"].astype(str) == cedula]
    if fila.empty:
        return
    u = fila.iloc[0]

    st.markdown(f"### {u.get('nombre_completo', nombre)}")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Cédula / ID", cedula)
    c2.metric("WhatsApp", str(u.get("whatsapp", "No registra")))
    c3.metric("EPS", str(u.get("eps", "No registra")))
    c4.metric("Registro", str(u.get("fecha_registro", "No registra")))
    st.info(f"Condiciones / lesiones: {u.get('condiciones_medicas', 'Ninguna')}")

    ws = link_whatsapp(u.get("whatsapp", ""), u.get("nombre_completo", nombre))
    if u.get("whatsapp", ""):
        st.markdown(f"[📲 Enviar mensaje de seguimiento por WhatsApp]({ws})")

    st.markdown("---")
    mostrar_resumen_clases(df_clases, cedula, "Resumen del Plan")

    pagos_cliente = df_pagos[df_pagos["cedula"] == cedula].copy() if not df_pagos.empty and "cedula" in df_pagos.columns else pd.DataFrame()
    st.markdown("---")
    titulo_ui("Resumen de Pagos", "fi-rr-credit-card", 3, 23)
    if pagos_cliente.empty:
        st.info("Este cliente todavía no tiene pagos registrados.")
    else:
        total = pd.to_numeric(pagos_cliente.get("valor", 0), errors="coerce").fillna(0).sum()
        ultimo = pagos_cliente.iloc[-1]
        st.metric("Total histórico pagado", f"${total:,.0f}")
        st.caption(f"Último movimiento: {formatear_fecha(ultimo.get('fecha_pago', ''))} · {ultimo.get('concepto', 'Pago')}")


def _estado_pago_cliente(df_pagos, cedula):
    hoy = pd.Timestamp.today().normalize()
    pagos = df_pagos[df_pagos["cedula"] == cedula].copy() if not df_pagos.empty and "cedula" in df_pagos.columns else pd.DataFrame()
    if pagos.empty:
        return 0.0, 0.0, 0.0, "🔴 PENDIENTE", pagos
    if "fecha_pago" in pagos.columns:
        pagos["_fecha_dt"] = pagos["fecha_pago"].apply(parsear_fecha)
        mes = pagos[(pagos["_fecha_dt"].notna()) & (pagos["_fecha_dt"].dt.year == hoy.year) & (pagos["_fecha_dt"].dt.month == hoy.month)].copy()
    else:
        mes = pd.DataFrame()
    mensualidad = 0.0
    if "valor_mensualidad" in pagos.columns:
        vals = pd.to_numeric(pagos["valor_mensualidad"], errors="coerce").dropna()
        if not vals.empty:
            mensualidad = float(vals.iloc[-1])
    if mensualidad <= 0:
        mensualidad = 400000.0
    pagado = float(pd.to_numeric(mes.get("valor", 0), errors="coerce").fillna(0).sum()) if not mes.empty else 0.0
    saldo = max(mensualidad - pagado, 0.0)
    estado = "🟢 PAGADO" if saldo <= 0.001 else ("🟡 ABONO" if pagado > 0 else "🔴 PENDIENTE")
    return mensualidad, pagado, saldo, estado, pagos


def mostrar_pagos_gym(df_usuarios, df_pagos):
    titulo_ui("Pagos y Contabilidad", "fi-rr-credit-card", 2, 28)
    clientes = _clientes(df_usuarios)
    cedula, nombre = _selector_cliente(clientes, "gym_cliente_pagos")
    if not cedula:
        return
    mensualidad, pagado, saldo, estado, pagos_cliente = _estado_pago_cliente(df_pagos, cedula)
    p1, p2, p3, p4 = st.columns(4)
    p1.metric("Mensualidad", f"${mensualidad:,.0f}")
    p2.metric("Pagado este mes", f"${pagado:,.0f}")
    p3.metric("Saldo pendiente", f"${saldo:,.0f}")
    p4.metric("Estado", estado)
    st.caption(f"Estado de pagos de {nombre} · {datetime.today().strftime('%B').capitalize()} de {datetime.today().year}.")

    with st.expander("➕ Registrar nuevo pago / abono", expanded=saldo > 0):
        with st.form(f"gym_pago_{cedula}"):
            valor_mensualidad = st.number_input("Valor de la mensualidad ($)", min_value=1.0, value=float(mensualidad), step=5000.0, format="%.0f")
            saldo_nuevo = max(float(valor_mensualidad) - pagado, 0.0)
            valor_pago_default = saldo_nuevo if saldo_nuevo > 0 else 1.0
            valor_pago = st.number_input("Valor del pago / abono ($)", min_value=1.0, value=float(valor_pago_default), step=5000.0, format="%.0f")
            concepto = st.text_input("Concepto", value="Abono mensualidad").strip()
            guardar = st.form_submit_button("Registrar Pago", use_container_width=True)
            if guardar:
                if valor_pago > saldo_nuevo + 0.001:
                    st.error(f"❌ El abono supera el saldo pendiente. Saldo disponible: ${saldo_nuevo:,.0f}.")
                    st.stop()
                id_pago = f"{cedula}_{datetime.today().strftime('%Y%m%d%H%M%S%f')}"
                try:
                    r = api_post(URL_API, json={
                        "action": "guardar_pago", "id_pago": id_pago, "cedula": cedula,
                        "fecha_pago": datetime.today().strftime('%d-%m-%Y'), "valor": float(valor_pago),
                        "concepto": concepto or "Abono mensualidad", "valor_mensualidad": float(valor_mensualidad)
                    }, timeout=30)
                    r.raise_for_status(); resultado = r.json()
                    if resultado.get("status") == "error":
                        st.error("❌ Google Apps Script reportó un error: " + str(resultado.get("message", "Error desconocido")))
                    else:
                        invalidar_cache_datos(); st.success("✅ Pago registrado correctamente."); st.rerun()
                except Exception as e:
                    st.error(f"❌ Error registrando el pago: {e}")

    if not pagos_cliente.empty:
        titulo_ui("Historial de Pagos", "fi-rr-receipt", 3, 22)
        tabla = pagos_cliente.copy()
        if "fecha_pago" in tabla.columns:
            tabla["_fecha"] = tabla["fecha_pago"].apply(parsear_fecha)
            tabla = tabla.sort_values("_fecha", ascending=False).drop(columns=["_fecha"])
        cols = [c for c in ["fecha_pago", "valor", "concepto", "valor_mensualidad"] if c in tabla.columns]
        tabla = tabla[cols].copy()
        for c in ["valor", "valor_mensualidad"]:
            if c in tabla.columns:
                tabla[c] = pd.to_numeric(tabla[c], errors="coerce").fillna(0).map(lambda x: f"${x:,.0f}")
        tabla = tabla.rename(columns={"fecha_pago":"Fecha", "valor":"Pago", "concepto":"Concepto", "valor_mensualidad":"Mensualidad"})
        st.dataframe(tabla, use_container_width=True, hide_index=True)


def mostrar_alertas_gym(df_usuarios, df_pagos, df_clases, df_planes):
    titulo_ui("Alertas de Vencimiento", "fi-rr-bell", 2, 28)
    clientes = _clientes(df_usuarios)
    if clientes.empty:
        st.info("No hay clientes para revisar.")
        return
    filas = []
    for _, u in clientes.iterrows():
        cedula = str(u.get("cedula", "")).strip()
        nombre = str(u.get("nombre_completo", "Cliente"))
        mensualidad, pagado, saldo, estado, _ = _estado_pago_cliente(df_pagos, cedula)
        resumen = obtener_resumen_clases(df_clases, cedula)
        alerta = "🟢 Al día"
        if saldo > 0:
            alerta = "🔴 Pago pendiente" if pagado <= 0 else "🟡 Pago incompleto"
        elif resumen["clases_contratadas"] > 0 and resumen["clases_restantes"] <= 2:
            alerta = "🟠 Pocas clases restantes"
        filas.append({"Cliente": nombre, "Cédula": cedula, "Pago": estado, "Saldo": f"${saldo:,.0f}", "Clases restantes": resumen["clases_restantes"], "Alerta": alerta})
    alertas = pd.DataFrame(filas)
    solo_alertas = alertas[alertas["Alerta"].str.startswith(("🔴", "🟡", "🟠"))]
    st.metric("Clientes con alerta", len(solo_alertas))
    st.dataframe((solo_alertas if not solo_alertas.empty else alertas), use_container_width=True, hide_index=True)


def mostrar_personal_training_gym(df_usuarios, df_clases):
    titulo_ui("Personal Training", "fi-rr-dumbbell", 2, 28)
    clientes = _clientes(df_usuarios)
    cedula, nombre = _selector_cliente(clientes, "gym_cliente_training")
    if not cedula:
        return
    mostrar_resumen_clases(df_clases, cedula)
    resumen = obtener_resumen_clases(df_clases, cedula)

    st.markdown("---")
    titulo_ui("Configurar nuevo plan", "fi-rr-file-plus", 3, 22)
    with st.form(f"gym_plan_{cedula}"):
        c1, c2 = st.columns(2)
        with c1:
            plan = st.text_input("Tipo / nombre del plan", value="" if resumen["plan"] == "Sin plan registrado" else resumen["plan"]).strip()
        with c2:
            clases = st.number_input("Número de clases contratadas", min_value=1, max_value=500, value=resumen["clases_contratadas"] if resumen["clases_contratadas"] > 0 else 20, step=1)
        guardar = st.form_submit_button("Registrar nuevo plan", use_container_width=True)
        if guardar:
            if not plan:
                st.error("❌ Debes indicar el tipo o nombre del plan.")
                st.stop()
            try:
                r = api_post(URL_API, json={
                    "action":"guardar_plan", "cedula":cedula, "nombre_completo":nombre, "tipo_plan":plan,
                    "fecha_inicio":datetime.today().strftime('%d-%m-%Y'), "fecha_fin":"", "estado":"Activo",
                    "observaciones":"Nueva contratación", "clases_incluidas":int(clases)
                }, timeout=30)
                r.raise_for_status(); resultado = r.json()
                if resultado.get("status") == "error":
                    st.error("❌ Google Apps Script reportó un error: " + str(resultado.get("message", "Error desconocido")))
                else:
                    invalidar_cache_datos(); st.success("✅ Nuevo plan registrado correctamente."); st.rerun()
            except Exception as e:
                st.error(f"❌ Error registrando el plan: {e}")

    st.markdown("---")
    titulo_ui("Registrar clase tomada", "fi-rr-calendar-plus", 3, 22)
    if resumen["clases_contratadas"] > 0 and resumen["clases_tomadas"] >= resumen["clases_contratadas"]:
        st.warning("⚠️ Este cliente ya utilizó todas las clases contratadas.")
    with st.form(f"gym_clase_{cedula}"):
        fecha_clase = st.date_input("Fecha de la clase tomada", value=date.today(), max_value=date.today(), format="DD-MM-YYYY")
        registrar = st.form_submit_button("Registrar Clase Tomada", use_container_width=True)
        if registrar:
            if resumen["clases_contratadas"] <= 0:
                st.error("❌ Primero debes configurar el plan y el número de clases contratadas."); st.stop()
            if resumen["clases_tomadas"] >= resumen["clases_contratadas"]:
                st.error("❌ El cliente ya utilizó todas las clases de su plan."); st.stop()
            fecha_str = fecha_clase.strftime("%d-%m-%Y")
            if not resumen["registros"].empty and "fecha_clase" in resumen["registros"].columns:
                existentes = resumen["registros"]["fecha_clase"].apply(formatear_fecha).astype(str).str.strip().tolist()
                if fecha_str in existentes:
                    st.error(f"❌ Ya existe una clase registrada para este cliente el {fecha_str}."); st.stop()
            id_clase = f"{cedula}CLASE{fecha_clase.strftime('%Y%m%d')}_{datetime.today().strftime('%H%M%S%f')}"
            try:
                r = api_post(URL_API, json={
                    "action":"guardar_clase", "id_clase":id_clase, "cedula":cedula, "nombre_completo":nombre,
                    "fecha_clase":fecha_str, "tipo_plan":resumen["plan"], "periodo":resumen["clases_tomadas"] + 1, "estado":"Tomada"
                }, timeout=30)
                r.raise_for_status(); resultado = r.json()
                if resultado.get("status") == "error":
                    st.error("❌ Google Apps Script reportó un error: " + str(resultado.get("message", "Error desconocido")))
                else:
                    invalidar_cache_datos(); st.success("✅ Clase registrada correctamente."); st.rerun()
            except Exception as e:
                st.error(f"❌ Error registrando la clase: {e}")

    st.markdown("---")
    titulo_ui("Historial de clases", "fi-rr-clipboard", 3, 22)
    registros = obtener_resumen_clases(df_clases, cedula)["registros"]
    if registros.empty:
        st.info("Este cliente todavía no tiene clases registradas.")
    else:
        tabla = registros.copy()
        if "fecha_clase" in tabla.columns:
            tabla["_fecha"] = tabla["fecha_clase"].apply(parsear_fecha); tabla = tabla.sort_values("_fecha", ascending=False).drop(columns=["_fecha"])
        cols = [c for c in ["fecha_clase","tipo_plan","periodo","estado"] if c in tabla.columns]
        tabla = tabla[cols].rename(columns={"fecha_clase":"Fecha Clase","tipo_plan":"Plan","periodo":"Periodo","estado":"Estado"})
        st.dataframe(tabla.astype(str), use_container_width=True, hide_index=True)


def mostrar_evolucion_admin_gym(df_usuarios, df_historial):
    titulo_ui("Evolución Física", "fi-rr-chart-line-up", 2, 28)
    clientes = _clientes(df_usuarios)
    cedula, nombre = _selector_cliente(clientes, "gym_cliente_evolucion")
    if not cedula:
        return
    h = df_historial[df_historial["cedula"] == cedula].copy() if not df_historial.empty and "cedula" in df_historial.columns else pd.DataFrame()
    if h.empty:
        st.info("Este cliente todavía no tiene evaluaciones físicas.")
        return
    h["_fecha_dt"] = h["fecha_evaluacion"].apply(parsear_fecha)
    h = h.sort_values("_fecha_dt").drop(columns=["_fecha_dt"])
    mostrar_graficos_evolucion(h)
    mostrar_alimentacion_recomendada(h.iloc[-1], nombre)
    st.markdown("---")
    incluir = st.checkbox("Incluir guía de alimentación en el PDF", value=False, key=f"gym_pdf_nut_{cedula}")
    if st.button("Generar Informe PDF del Cliente", use_container_width=True, key=f"gym_pdf_{cedula}"):
        try:
            pdf = generar_informe_evolucion_pdf(h, nombre, cedula, ruta_logo, incluir_alimentacion=incluir)
            safe = "".join(ch for ch in nombre if ch.isalnum() or ch in " _-").strip().replace(" ", "_")
            st.download_button("⬇️ Descargar Informe PDF", data=pdf, file_name=f"Informe_Evolucion_{safe}.pdf", mime="application/pdf", use_container_width=True, key=f"gym_pdf_dl_{cedula}")
        except Exception as e:
            st.error(f"❌ No fue posible generar el informe PDF: {e}")
    titulo_ui("Historial de evaluaciones", "fi-rr-clipboard", 3, 22)
    st.dataframe(h.astype(str), use_container_width=True, hide_index=True)


def mostrar_perfil_cliente_gym(df_usuarios):
    titulo_ui("Mi Perfil", "fi-rr-user", 2, 28)
    cedula = str(st.session_state.get("cedula", "")).strip()
    if df_usuarios.empty:
        st.info("No hay información de perfil disponible."); return
    filas = df_usuarios[df_usuarios["cedula"].astype(str) == cedula]
    if filas.empty:
        st.info("No se encontró tu perfil."); return
    u = filas.iloc[0]
    c1,c2,c3 = st.columns(3)
    c1.metric("Nombre", str(u.get("nombre_completo", "")))
    c2.metric("Cédula / ID", cedula)
    c3.metric("WhatsApp", str(u.get("whatsapp", "No registra")))
    st.info(f"EPS: {u.get('eps','No registra')} · Condiciones / lesiones: {u.get('condiciones_medicas','Ninguna')}")


def mostrar_evolucion_cliente_gym(df_historial):
    titulo_ui("Mi Evolución", "fi-rr-chart-line-up", 2, 28)
    cedula = str(st.session_state.get("cedula", "")).strip()
    h = df_historial[df_historial["cedula"] == cedula].copy() if not df_historial.empty and "cedula" in df_historial.columns else pd.DataFrame()
    if h.empty:
        st.info("Aún no has registrado ninguna evaluación física."); return
    h["_fecha_dt"] = h["fecha_evaluacion"].apply(parsear_fecha); h = h.sort_values("_fecha_dt").drop(columns=["_fecha_dt"])
    mostrar_graficos_evolucion(h)
    mostrar_alimentacion_recomendada(h.iloc[-1], st.session_state.get("nombre", "Cliente"))
    st.markdown("---")
    incluir = st.checkbox("Incluir guía de alimentación en el PDF", value=False, key="gym_pdf_cliente_nut")
    if st.button("Generar Informe de Evolución en PDF", use_container_width=True, key="gym_pdf_cliente"):
        try:
            pdf = generar_informe_evolucion_pdf(h, st.session_state.get("nombre", "Cliente"), cedula, ruta_logo, incluir_alimentacion=incluir)
            safe = "".join(ch for ch in st.session_state.get("nombre", "Cliente") if ch.isalnum() or ch in " _-").strip().replace(" ", "_")
            st.download_button("⬇️ Descargar Informe PDF", data=pdf, file_name=f"Informe_Evolucion_{safe}.pdf", mime="application/pdf", use_container_width=True, key="gym_pdf_cliente_dl")
        except Exception as e:
            st.error(f"❌ No fue posible generar el informe PDF: {e}")


def mostrar_registro_medidas_cliente_gym(df_historial):
    # Conserva el flujo de registro de app_1, incluyendo los cálculos y la API existente.
    st.subheader("Registro de Evaluación Antropométrica")
    with st.form("form_medidas_gym"):
        c1,c2,c3 = st.columns(3)
        peso=c1.number_input("Peso (kg)",30.0,200.0,70.0,0.5)
        estatura=c2.number_input("Estatura (cm)",100.0,220.0,170.0,1.0)
        edad=c3.number_input("Edad (años)",10,90,25)
        sexo=c1.selectbox("Sexo Fisiológico",["Masculino","Femenino"])
        meta=c2.selectbox("Objetivo Principal",["Perder Grasa","Ganar Músculo","Mantenimiento"])
        st.markdown("---")
        titulo_ui("Medidas Corporales (cm)","fi-rr-ruler-horizontal",3,24)
        a,b=st.columns(2)
        with a:
            cuello=st.number_input("Cuello",20.0,60.0,38.0); hombros=st.number_input("Hombros",50.0,180.0,110.0); pecho=st.number_input("Pecho",50.0,180.0,95.0); cintura=st.number_input("Cintura / Abdomen",40.0,180.0,80.0); cadera=st.number_input("Glúteos / Cadera",40.0,180.0,95.0)
        with b:
            bder=st.number_input("Bícep Derecho",15.0,60.0,32.0); bizq=st.number_input("Bícep Izquierdo",15.0,60.0,32.0); pder=st.number_input("Pierna Derecha",20.0,90.0,55.0); pizq=st.number_input("Pierna Izquierda",20.0,90.0,55.0); gder=st.number_input("Gemelo Derecho",15.0,60.0,35.0); gizq=st.number_input("Gemelo Izquierdo",15.0,60.0,35.0)
        guardar=st.form_submit_button("Guardar Evaluación",use_container_width=True)
        if guardar:
            try:
                imc,grasa,cals,edad_bio=calcular_metricas(peso,estatura,edad,sexo,cuello,cintura,cadera,meta)
                id_reg=f"{st.session_state['cedula']}_{datetime.today().strftime('%Y%m%d%H%M%S')}"; fecha=datetime.today().strftime('%d-%m-%Y')
                datos={"action":"guardar_medidas","id_registro":id_reg,"fecha_evaluacion":fecha,"cedula":str(st.session_state['cedula']).strip(),"edad":int(edad),"sexo":sexo,"meta":meta,"peso_kg":float(peso),"estatura_cm":float(estatura),"cuello_cm":float(cuello),"hombros_cm":float(hombros),"bicep_der_cm":float(bder),"bicep_izq_cm":float(bizq),"pecho_cm":float(pecho),"cintura_cm":float(cintura),"cadera_cm":float(cadera),"pierna_der_cm":float(pder),"pierna_izq_cm":float(pizq),"gemelo_der_cm":float(gder),"gemelo_izq_cm":float(gizq),"imc":float(imc),"porcentaje_grasa":float(grasa),"calorias_objetivo":int(cals),"edad_metabolica":int(edad_bio)}
                r=api_post(URL_API,json=datos,timeout=30); r.raise_for_status(); resultado=r.json()
                if resultado.get("status")=="error": st.error("❌ Google Apps Script reportó un error: "+str(resultado.get("message","Error desconocido")))
                else: invalidar_cache_datos(); st.success("¡Medidas guardadas con éxito!"); st.rerun()
            except Exception as e: st.error(f"❌ Error calculando o guardando las medidas: {e}")

# ============================================================
# EJECUCIÓN PRINCIPAL UNIFICADA
# ============================================================

if "autenticado" not in st.session_state:
    st.session_state["autenticado"] = False
    st.session_state["rol"] = None
    st.session_state["cedula"] = None
    st.session_state["nombre"] = None

st.title("GESTOR GIMNASIO · JULIAN AVILA")

if not st.session_state["autenticado"]:
    col1,col2=st.columns(2)
    with col1:
        titulo_ui("Iniciar Sesión","fi-rr-lock",2,28)
        cedula_ingreso=st.text_input("Número de Cédula / ID:").strip()
        pass_ingreso=st.text_input("Contraseña:",type="password").strip()
        if st.button("Ingresar",use_container_width=True):
            if cedula_ingreso=="admin" and pass_ingreso=="admin123456":
                st.session_state.update({"autenticado":True,"rol":"Admin","cedula":"ADMIN","nombre":"JULIAN AVILA"}); st.rerun()
            else:
                df_u,error=cargar_usuarios_login()
                if error: st.error(f"⚠️ {error}")
                elif df_u.empty or "cedula" not in df_u.columns: st.error("❌ No fue posible verificar los usuarios en este momento.")
                elif normalizar_cedula(cedula_ingreso) in df_u["cedula"].values:
                    u=df_u[df_u["cedula"]==normalizar_cedula(cedula_ingreso)].iloc[0]
                    if str(u.get("password","")).strip()==pass_ingreso:
                        st.session_state.update({"autenticado":True,"rol":u.get("rol","Cliente"),"cedula":str(u["cedula"]),"nombre":u.get("nombre_completo","Cliente")}); st.rerun()
                    else: st.error("❌ Contraseña incorrecta.")
                else: st.error("❌ Cédula no registrada.")
    with col2:
        titulo_ui("Crear Cuenta Nueva","fi-rr-user-add",2,28)
        with st.form("form_registro_gym"):
            reg_cedula=st.text_input("Número de Cédula / ID:").strip(); reg_nombre=st.text_input("Nombre Completo:").strip(); reg_whatsapp=st.text_input("Número de WhatsApp:").strip(); reg_eps=st.text_input("EPS:").strip(); reg_cond=st.text_area("Condiciones Médicas / Lesiones / Cirugías:").strip(); reg_pass=st.text_input("Crea tu Contraseña:",type="password").strip()
            if st.form_submit_button("Crear Perfil"):
                df_u,error=cargar_usuarios_login()
                if error: st.error(f"⚠️ {error}")
                elif not reg_cedula or not reg_nombre or not reg_pass: st.error("⚠️ Cédula, Nombre y Contraseña son obligatorios.")
                elif not df_u.empty and normalizar_cedula(reg_cedula) in df_u["cedula"].values: st.error("❌ Esta cédula ya está registrada.")
                else:
                    try:
                        r=api_post(URL_API,json={"action":"registrar_usuario","cedula":reg_cedula,"nombre_completo":reg_nombre,"whatsapp":reg_whatsapp,"eps":reg_eps or "NINGUNA","condiciones_medicas":reg_cond or "NINGUNA","rol":"Cliente","password":reg_pass,"fecha_registro":datetime.today().strftime('%d-%m-%Y')},timeout=30); r.raise_for_status(); resultado=r.json()
                        if resultado.get("status")=="error": st.error("❌ Google Apps Script reportó un error: "+str(resultado.get("message","No fue posible registrar el usuario.")))
                        else: invalidar_cache_datos(); st.success("✅ Perfil creado correctamente. Ya puedes iniciar sesión.")
                    except Exception as e: st.error(f"❌ Error al guardar usuario: {e}")
else:
    st.sidebar.markdown(f"### {icono_ui('fi-rr-user',22)}{st.session_state['nombre']}",unsafe_allow_html=True)
    st.sidebar.caption(f"Rol: {st.session_state['rol']}")
    if st.sidebar.button("Cerrar Sesión",use_container_width=True):
        st.session_state.clear(); st.rerun()

    df_usuarios,df_historial,df_pagos,df_clases,df_planes_bd=cargar_bd()

    if str(st.session_state.get("rol","Cliente")).strip().lower()=="admin":
        st.sidebar.markdown("### 🏋️ GESTIÓN DEL GIMNASIO")
        opcion_admin=st.sidebar.radio("MENÚ",[
            "📊 Dashboard","👥 Clientes","💳 Pagos y Contabilidad","🚨 Alertas de Vencimiento","🏋️ Personal Training","📈 Evolución Física"
        ],key="menu_admin_gym")
        if opcion_admin=="📊 Dashboard": mostrar_dashboard_admin(df_usuarios,df_historial,df_pagos,df_clases)
        elif opcion_admin=="👥 Clientes": mostrar_clientes_gym(df_usuarios,df_clases,df_pagos,df_historial)
        elif opcion_admin=="💳 Pagos y Contabilidad": mostrar_pagos_gym(df_usuarios,df_pagos)
        elif opcion_admin=="🚨 Alertas de Vencimiento": mostrar_alertas_gym(df_usuarios,df_pagos,df_clases,df_planes_bd)
        elif opcion_admin=="🏋️ Personal Training": mostrar_personal_training_gym(df_usuarios,df_clases)
        elif opcion_admin=="📈 Evolución Física": mostrar_evolucion_admin_gym(df_usuarios,df_historial)
    else:
        st.sidebar.markdown("### 👤 ÁREA DEL CLIENTE")
        opcion_cliente=st.sidebar.radio("MENÚ",[
            "👤 Mi Perfil","📏 Registrar Medidas Hoy","📈 Mi Evolución","🥗 Mi Alimentación","🏋️ Mis Clases"
        ],key="menu_cliente_gym")
        if opcion_cliente=="👤 Mi Perfil": mostrar_perfil_cliente_gym(df_usuarios)
        elif opcion_cliente=="📏 Registrar Medidas Hoy": mostrar_registro_medidas_cliente_gym(df_historial)
        elif opcion_cliente=="📈 Mi Evolución": mostrar_evolucion_cliente_gym(df_historial)
        elif opcion_cliente=="🥗 Mi Alimentación":
            cedula=str(st.session_state.get("cedula","")).strip(); h=df_historial[df_historial["cedula"]==cedula].copy() if not df_historial.empty else pd.DataFrame()
            if h.empty: st.info("Aún no tienes una evaluación física registrada.")
            else:
                h["_fecha_dt"]=h["fecha_evaluacion"].apply(parsear_fecha); h=h.sort_values("_fecha_dt").drop(columns=["_fecha_dt"]); mostrar_alimentacion_recomendada(h.iloc[-1],st.session_state.get("nombre","Cliente"))
        elif opcion_cliente=="🏋️ Mis Clases":
            titulo_ui("Mis Clases","fi-rr-dumbbell",2,28); mostrar_resumen_clases(df_clases,st.session_state["cedula"])
            resumen=obtener_resumen_clases(df_clases,st.session_state["cedula"])
            if not resumen["registros"].empty:
                tabla=resumen["registros"].copy(); cols=[c for c in ["fecha_clase","tipo_plan","periodo","estado"] if c in tabla.columns]; tabla=tabla[cols].rename(columns={"fecha_clase":"Fecha de Clase","tipo_plan":"Plan","periodo":"Periodo","estado":"Estado"}); st.dataframe(tabla.astype(str),use_container_width=True,hide_index=True)

st.markdown('<div class="ui-attribution">Iconos de interfaz: <a href="https://www.flaticon.com/uicons" target="_blank">Uicons by Flaticon</a></div>',unsafe_allow_html=True)
