import html
from datetime import datetime

import streamlit as st

# ======================================================================
# DATOS DEL PIE DE PÁGINA  ->  cambia solo estas tres líneas
# ======================================================================
NOMBRE = "Pablo Alan Garces Palacios"
GITHUB_URL = "https://github.com/AlanGarpal"
LINKEDIN_URL = "https://www.linkedin.com/in/pablo-alan-garces-palacios-42172825a/"

# Siluetas oficiales (monocromas) de GitHub y LinkedIn
_SVG_GITHUB = (
    "<svg viewBox='0 0 16 16' aria-hidden='true'><path fill-rule='evenodd' d='M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 "
    "6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28"
    "-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64"
    "-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 "
    "1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 "
    "1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z'/></svg>"
)
_SVG_LINKEDIN = (
    "<svg viewBox='0 0 24 24' aria-hidden='true'><path d='M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037"
    "-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 "
    "4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 "
    "2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 "
    "1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z'/>"
    "</svg>"
)

# ======================================================================
# CSS
# ======================================================================
_CSS = """
:root {
    /* Paleta sobria: azul corporativo + un solo acento naranja */
    --azul: #12239E;
    --azul-profundo: #0B1659;
    --acento: #FF5100;
    --acento-oscuro: #CC4706;

    --tinta: #102342;
    --texto-suave: #53627a;
    --texto-tenue: #8a94a5;

    --fondo: #f6f7fb;
    --blanco: #ffffff;
    --borde: #e3e7ef;
    --verde: #1b8a4b;
    --rojo: #c8323c;

    --radio: 12px;
    --sombra: 0 1px 2px rgba(16, 35, 66, 0.05), 0 4px 14px rgba(16, 35, 66, 0.06);
    --sombra-hover: 0 10px 28px rgba(18, 35, 158, 0.16);

    /* Alias para no romper tus otros dashboards */
    --rosa-principal: var(--acento);
    --rosa-oscuro: var(--acento-oscuro);
    --rosa-claro: #F5905F;
    --rosa-borde: var(--acento);
    --azul-texto: var(--tinta);
    --azul-secundario: var(--texto-suave);
    --sombra-legacy: var(--sombra);
}

/* Tipografía (sin tocar los <span> para no romper los iconos Material) */
.stApp, .stApp p, .stApp li, .stApp label, .stApp input, .stApp textarea, .stApp button,
.stApp h1, .stApp h2, .stApp h3, .stApp h4, .stApp td, .stApp th {
    font-family: Inter, "Segoe UI", Arial, sans-serif;
}
[data-testid="stIconMaterial"], [class*="material-symbols"] {
    font-family: "Material Symbols Rounded" !important;
}

.stApp { background: var(--fondo); }
[data-testid="stHeader"] { background: transparent; }
[data-testid="stDecoration"] { display: none; }

.block-container {
    max-width: 1720px;
    padding: 1.25rem 2rem 5rem 2rem;
}

/* ==================== SIDEBAR ==================== */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, var(--azul-profundo) 0%, #101E7E 100%);
    border-right: none;
}
[data-testid="stSidebarContent"] { display: flex !important; flex-direction: column !important; }
[data-testid="stSidebarUserContent"] { order: 1 !important; padding-top: 0.5rem !important; }
[data-testid="stSidebarNav"] { order: 2 !important; }

[data-testid="stSidebar"] * { color: rgba(255, 255, 255, 0.92); }
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] [data-baseweb="select"] * { color: var(--tinta); }
[data-testid="stSidebar"] hr { border-color: rgba(255, 255, 255, 0.14); }

[data-testid="stSidebarNav"] a {
    border-radius: 10px;
    margin: 0.2rem 0.55rem;
    padding: 0.55rem 0.85rem;
    transition: background 0.18s ease;
}
[data-testid="stSidebarNav"] a:hover { background: rgba(255, 255, 255, 0.08); }
[data-testid="stSidebarNav"] a[aria-current="page"] {
    background: rgba(255, 255, 255, 0.12);
    box-shadow: inset 3px 0 0 var(--acento);
}
[data-testid="stSidebarNav"] span { font-weight: 600; }

.marca-sidebar {
    padding: 1rem 1rem 1.2rem 1rem;
    border-bottom: 1px solid rgba(255, 255, 255, 0.14);
    margin-bottom: 0.8rem;
}
.marca-sidebar-titulo { font-size: 1rem; font-weight: 700; letter-spacing: 0.02rem; }
.marca-sidebar-subtitulo { font-size: 0.76rem; opacity: 0.75; margin-top: 0.18rem; }

/* ==================== TÍTULOS ==================== */
.encabezado-pagina { display: flex; align-items: center; gap: 0.7rem; padding: 0.15rem 0 1.25rem 0; }
.encabezado-punto {
    width: 10px; height: 10px; flex: 0 0 10px;
    border-radius: 999px;
    background: var(--acento);
}
.titulo-principal {
    color: var(--tinta);
    font-size: 1.85rem; line-height: 1.1; font-weight: 700; letter-spacing: -0.03rem;
}
.titulo-secundario { color: var(--texto-suave); font-size: 0.95rem; margin-top: 0.35rem; }
.titulo-bloque { color: var(--tinta); font-size: 1rem; line-height: 1.2; font-weight: 700; }
.subtitulo-bloque { color: var(--texto-tenue); font-size: 0.77rem; margin-top: 0.18rem; }
.etiqueta-seccion { color: var(--texto-suave); font-size: 0.74rem; font-weight: 600; margin-bottom: 0.35rem; }

.espacio-seccion { height: 0.65rem; }
.espacio-insight { height: 1rem; }
.espacio-seccion-grande { height: 1.15rem; }
.separador-suave { height: 1px; margin: 0.65rem 0 0.85rem 0; background: var(--borde); }

/* ==================== CONTENEDORES ==================== */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: var(--blanco);
    border: 1px solid var(--borde);
    border-radius: var(--radio);
    box-shadow: var(--sombra);
    padding: 0.25rem;
}
div[data-testid="stExpander"] {
    background: var(--blanco);
    border: 1px solid var(--borde);
    border-radius: var(--radio);
    box-shadow: var(--sombra);
}
div[data-testid="stExpander"] summary { color: var(--tinta); font-weight: 600; }

/* ==================== FILTROS ==================== */
div[data-testid="stSelectbox"] label,
div[data-testid="stMultiSelect"] label,
div[data-testid="stTextInput"] label,
div[data-testid="stDateInput"] label {
    color: var(--tinta) !important;
    font-size: 0.75rem !important;
    font-weight: 600 !important;
}
div[data-baseweb="select"] > div,
div[data-testid="stTextInput"] input,
div[data-testid="stDateInput"] input {
    min-height: 42px;
    border-radius: 8px !important;
    border-color: #d9dfea !important;
    background: var(--blanco) !important;
    color: var(--tinta) !important;
    box-shadow: none !important;
}
div[data-testid="stTextInput"] input::placeholder { color: #a1a9b7; }
div[data-baseweb="select"] > div:focus-within,
div[data-testid="stTextInput"] input:focus,
div[data-testid="stDateInput"] input:focus {
    border-color: var(--azul) !important;
    box-shadow: 0 0 0 3px rgba(18, 35, 158, 0.10) !important;
}

/* ==================== BOTONES ==================== */
div.stButton > button,
div[data-testid="stPopover"] button {
    width: 100%;
    min-height: 40px;
    border-radius: 8px;
    border: 1px solid #cfd6e4;
    background: var(--blanco);
    color: var(--azul);
    font-weight: 600;
    transition: background 0.18s ease, color 0.18s ease, border-color 0.18s ease;
}
div.stButton > button:hover,
div[data-testid="stPopover"] button:hover {
    background: var(--azul);
    color: var(--blanco);
    border-color: var(--azul);
}
div.stButton > button[kind="primary"] {
    background: var(--azul);
    color: var(--blanco);
    border-color: var(--azul);
}
div.stButton > button[kind="primary"]:hover {
    background: var(--acento);
    border-color: var(--acento);
}

/* ==================== KPI (genérico) ==================== */
.kpi-card {
    min-height: 150px; height: 100%;
    padding: 1.05rem 1rem 0.9rem 1rem;
    border-radius: var(--radio);
    border: 1px solid var(--borde);
    background: var(--blanco);
    box-shadow: var(--sombra);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.kpi-card:hover { transform: translateY(-2px); box-shadow: var(--sombra-hover); }
.kpi-fila-superior { display: flex; align-items: center; gap: 0.8rem; }

/* Iconos de KPI: planos y discretos (se conservan los nombres de clase) */
.kpi-icono {
    width: 44px; height: 44px; flex: 0 0 44px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.15rem; font-weight: 700;
    background: #eef1fb; color: var(--azul);
}
.kpi-icono.azul, .kpi-icono.morado, .kpi-icono.cian { background: #eef1fb; color: var(--azul); }
.kpi-icono.rosa, .kpi-icono.naranja { background: #fff0e9; color: var(--acento-oscuro); }
.kpi-icono.verde { background: #e9f6ee; color: var(--verde); }

.kpi-titulo {
    color: var(--texto-suave);
    font-size: 0.68rem; line-height: 1.2; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.04rem;
}
.kpi-valor {
    color: var(--tinta);
    font-size: 1.45rem; line-height: 1.2; font-weight: 700;
    margin-top: 0.26rem; white-space: nowrap;
}
.kpi-subtitulo { color: var(--texto-tenue); font-size: 0.68rem; margin-top: 0.28rem; }

/* Variación (antes estaba definida 3 veces) */
.kpi-variacion {
    display: flex; align-items: center; gap: 0.35rem;
    margin-top: 0.5rem; font-size: 0.72rem; font-weight: 700;
}
.kpi-variacion.verde, .kpi-variacion-valor.positivo { color: var(--verde); }
.kpi-variacion.rojo, .kpi-variacion-valor.negativo { color: var(--rojo); }
.kpi-variacion-valor { font-weight: 700; }
.kpi-variacion span, .kpi-variacion-texto { color: var(--texto-tenue); font-weight: 500; }

/* ==================== INSIGHT ==================== */
.insight-card {
    display: flex; align-items: center; gap: 1rem;
    min-height: 82px;
    padding: 1.1rem 1.25rem;
    border-radius: var(--radio);
    border: 1px solid var(--borde);
    border-left: 3px solid var(--acento);
    background: var(--blanco);
    box-shadow: var(--sombra);
}
.insight-icono {
    width: 46px; height: 46px; flex: 0 0 46px;
    border-radius: 10px;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.2rem;
    background: #fff0e9; color: var(--acento-oscuro);
}
.insight-titulo { color: var(--tinta); font-weight: 700; font-size: 0.9rem; }
.insight-texto { color: var(--texto-suave); font-size: 0.78rem; line-height: 1.6; margin-top: 0.22rem; }

/* ==================== TABLAS / GRÁFICAS / ALERTAS ==================== */
div[data-testid="stDataFrame"] { border: none; border-radius: 10px; overflow: hidden; }
div[data-testid="stDataFrame"] thead tr th {
    background: #f8f9fc !important;
    color: var(--texto-suave) !important;
    font-size: 0.7rem !important; font-weight: 700 !important;
    text-transform: uppercase;
    border-bottom: 1px solid var(--borde) !important;
}
div[data-testid="stDataFrame"] tbody td { color: var(--tinta) !important; border-bottom: 1px solid #edf0f5 !important; }
div[data-testid="stPlotlyChart"] { border-radius: 10px; overflow: hidden; }
div[data-testid="stAlert"] { border-radius: var(--radio); }

/* ==================== KPI PRINCIPALES / SECUNDARIOS / DOBLE ==================== */
.kpi-principal-card, .kpi-doble-card {
    min-height: 108px; height: auto;
    display: flex; align-items: center; gap: 0.8rem;
    padding: 0.85rem 1rem;
    border: 1px solid var(--borde);
    border-radius: var(--radio);
    background: var(--blanco);
    box-shadow: var(--sombra);
    overflow: hidden;
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.kpi-principal-card:hover, .kpi-doble-card:hover { transform: translateY(-2px); box-shadow: var(--sombra-hover); }

.kpi-principal-icono, .kpi-doble-icono {
    width: 56px !important; height: 56px !important;
    min-width: 56px !important; max-width: 56px !important; flex: 0 0 56px !important;
    display: flex; align-items: center; justify-content: center;
    border-radius: 12px;
    font-size: 1.3rem; font-weight: 700;
    color: var(--blanco);
    background: var(--azul) !important;
}
.kpi-principal-contenido, .kpi-doble-contenido { flex: 1; min-width: 0; width: auto; }
.kpi-principal-titulo, .kpi-doble-titulo-general {
    color: var(--azul);
    font-size: 0.76rem; line-height: 1.1; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.03rem;
    margin: 0 0 0.3rem 0;
}
.kpi-principal-valor {
    color: var(--tinta);
    font-size: 1.5rem; line-height: 1.05; font-weight: 700;
    margin: 0; white-space: nowrap;
}
.kpi-principal-subtitulo { color: var(--texto-tenue); font-size: 0.66rem; line-height: 1.2; margin-top: 0.28rem; }

.kpi-doble-metricas { width: 100%; display: grid; grid-template-columns: 1fr 1px 1fr; align-items: center; gap: 0.75rem; }
.kpi-doble-metrica { min-width: 0; }
.kpi-doble-etiqueta { color: var(--texto-suave); font-size: 0.61rem; line-height: 1.15; font-weight: 600; text-transform: uppercase; }
.kpi-doble-valor { color: var(--tinta); font-size: 1.3rem; line-height: 1.05; font-weight: 700; margin-top: 0.18rem; white-space: nowrap; }
.kpi-doble-separador { width: 1px; height: 34px; background: var(--borde); }
.kpi-doble-subtitulo { color: var(--texto-tenue); font-size: 0.66rem; line-height: 1.2; margin-top: 0.4rem; }

.kpi-secundaria-card {
    min-height: 82px;
    display: flex; align-items: center; gap: 0.75rem;
    padding: 0.75rem 0.9rem;
    background: var(--blanco);
    border: 1px solid var(--borde);
    border-radius: var(--radio);
    box-shadow: var(--sombra);
    transition: transform 0.18s ease, box-shadow 0.18s ease;
}
.kpi-secundaria-card:hover { transform: translateY(-2px); box-shadow: var(--sombra-hover); }
.kpi-secundaria-icono {
    width: 42px; height: 42px; min-width: 42px; max-width: 42px; flex: 0 0 42px;
    display: flex; align-items: center; justify-content: center;
    border-radius: 10px;
    font-size: 1rem; font-weight: 700;
    background: #eef1fb; color: var(--azul);
}
.kpi-secundaria-contenido { flex: 1; }
.kpi-secundaria-titulo { color: var(--texto-suave); font-size: 0.64rem; font-weight: 700; text-transform: uppercase; margin-bottom: 0.15rem; }
.kpi-secundaria-valor { color: var(--tinta); font-size: 1.1rem; font-weight: 700; line-height: 1; }
.kpi-secundaria-subtitulo { color: var(--texto-tenue); font-size: 0.63rem; margin-top: 0.18rem; }

/* ==================== COMPONENTES DE LA APP IA ==================== */
.hero {
    background: linear-gradient(120deg, var(--azul-profundo) 0%, var(--azul) 100%);
    color: #fff;
    padding: 24px 30px;
    border-radius: var(--radio);
    border-bottom: 3px solid var(--acento);
    box-shadow: var(--sombra);
    margin-bottom: 22px;
}
.hero h1 {
    color: #fff; margin: 0; padding: 0;
    font-size: 1.75rem; font-weight: 700; letter-spacing: -0.02rem;
    display: flex; align-items: center; gap: 12px;
}
.hero h1 svg { width: 30px; height: 30px; flex-shrink: 0; opacity: 0.9; }
.hero p { margin: 6px 0 0 0; opacity: 0.85; font-size: 0.98rem; }

.card {
    background: var(--blanco); color: var(--tinta);
    border: 1px solid var(--borde);
    border-top: 3px solid var(--azul);
    border-radius: var(--radio);
    padding: 16px 18px; min-height: 150px; margin-bottom: 8px;
    box-shadow: var(--sombra);
}
.card .ic { color: var(--azul); line-height: 1; transition: color 0.2s ease; }
.card .ic svg { width: 26px; height: 26px; }
.card .ct { font-weight: 700; color: var(--azul); margin: 6px 0 4px 0; font-size: 1rem; }
.card .cb { font-size: 0.9rem; line-height: 1.4; color: #3a4660; }

.badge { background: var(--azul); color: #fff; padding: 2px 10px; border-radius: 20px; font-weight: 600; font-size: 0.78rem; }

.kpi {
    background: var(--blanco); color: var(--tinta);
    border: 1px solid var(--borde);
    border-left: 4px solid var(--azul);
    border-radius: var(--radio);
    padding: 14px 18px;
    box-shadow: var(--sombra);
}
.kpi .l { font-size: 0.74rem; color: var(--texto-suave); text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600; }
.kpi .v { font-size: 1.7rem; font-weight: 700; color: var(--azul); line-height: 1.2; }
.kpi .s { font-size: 0.78rem; color: var(--texto-tenue); font-weight: 500; }

.section-title {
    color: var(--azul); font-weight: 700; font-size: 1.2rem;
    border-bottom: 2px solid var(--acento);
    display: inline-block; padding-bottom: 3px; margin: 20px 0 12px 0;
    transition: color 0.2s ease, transform 0.2s ease;
}
.section-title:hover { color: var(--acento); transform: translateY(-2px); }
.section-title svg { width: 18px; height: 18px; vertical-align: -3px; margin-right: 8px; }

/* Efecto hover compartido (versión sobria de .kpi-popover-box) */
.kpi-popover-box { transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease; }
.kpi-popover-box:hover {
    transform: translateY(-3px);
    border-color: var(--acento) !important;
    box-shadow: var(--sombra-hover) !important;
    border-left-color: var(--acento-oscuro);
}
.kpi-popover-box:hover .ic { color: var(--acento); }

/* ==================== PIE DE PÁGINA ==================== */
.pie-pagina {
    margin-top: 3rem; padding: 1.4rem 0 0.6rem 0;
    border-top: 1px solid var(--borde);
    text-align: center;
}
.pie-nombre { color: var(--tinta); font-weight: 600; font-size: 0.9rem; }
.pie-copy { color: var(--texto-tenue); font-size: 0.72rem; margin-top: 0.15rem; }
.pie-enlaces { display: flex; justify-content: center; gap: 12px; margin-top: 0.8rem; }
.pie-enlaces a {
    width: 38px; height: 38px;
    display: inline-flex; align-items: center; justify-content: center;
    border-radius: 50%;
    border: 1px solid var(--borde);
    background: var(--blanco);
    color: var(--texto-suave);
    text-decoration: none;
    transition: color 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
}
.pie-enlaces a:hover { color: var(--acento); border-color: var(--acento); transform: translateY(-2px); }
.pie-enlaces svg { width: 18px; height: 18px; fill: currentColor; }

/* ==================== RESPONSIVO ==================== */
.st-key-kpi_principales [data-testid="stHorizontalBlock"],
.st-key-kpi_secundarios [data-testid="stHorizontalBlock"] { display: flex; flex-wrap: wrap; align-items: stretch; }

.st-key-kpi_principales [data-testid="column"], .st-key-kpi_principales [data-testid="stColumn"] { flex: 1 1 280px !important; min-width: 280px !important; }
.st-key-kpi_secundarios [data-testid="column"], .st-key-kpi_secundarios [data-testid="stColumn"] { flex: 1 1 220px !important; min-width: 220px !important; }

.kpi-principal-titulo, .kpi-secundaria-titulo, .kpi-doble-titulo-general, .kpi-doble-etiqueta { word-break: normal; overflow-wrap: normal; white-space: normal; }
.kpi-principal-valor, .kpi-secundaria-valor, .kpi-doble-valor { word-break: normal; overflow-wrap: normal; white-space: nowrap; }

@media screen and (max-width: 1350px) {
    .kpi-card { min-height: 160px; padding-left: 0.8rem; padding-right: 0.8rem; }
    .kpi-icono { width: 40px; height: 40px; flex-basis: 40px; }
    .kpi-valor { font-size: 1.25rem; }
}
@media screen and (max-width: 1250px) {
    .st-key-kpi_principales [data-testid="column"], .st-key-kpi_principales [data-testid="stColumn"] { flex: 1 1 calc(50% - 1rem) !important; min-width: 320px !important; }
    .st-key-kpi_secundarios [data-testid="column"], .st-key-kpi_secundarios [data-testid="stColumn"] { flex: 1 1 calc(33.333% - 1rem) !important; min-width: 250px !important; }
}
@media screen and (max-width: 1100px) {
    .block-container { padding-left: 1rem; padding-right: 1rem; }
    .titulo-principal { font-size: 1.6rem; }
    .kpi-card { min-height: 138px; }
}
@media screen and (max-width: 900px) {
    div[data-testid="stExpander"] div[data-testid="stHorizontalBlock"] { flex-wrap: wrap; }
    div[data-testid="stExpander"] div[data-testid="column"], div[data-testid="stExpander"] div[data-testid="stColumn"] { flex: 1 1 280px !important; min-width: 280px !important; }
}
@media screen and (max-width: 760px) {
    .block-container { padding-left: 0.75rem; padding-right: 0.75rem; }
    .st-key-kpi_principales [data-testid="column"], .st-key-kpi_principales [data-testid="stColumn"],
    .st-key-kpi_secundarios [data-testid="column"], .st-key-kpi_secundarios [data-testid="stColumn"] { flex: 1 1 100% !important; min-width: 100% !important; }
    .kpi-principal-card, .kpi-doble-card { min-height: auto; padding: 1rem; }
    .kpi-principal-valor { font-size: 1.6rem; }
    .kpi-secundaria-card { min-height: auto; }
    .hero { padding: 18px 20px; }
    .hero h1 { font-size: 1.4rem; }
}
@media screen and (max-width: 600px) {
    div[data-testid="stExpander"] div[data-testid="column"], div[data-testid="stExpander"] div[data-testid="stColumn"] { flex: 1 1 100% !important; min-width: 100% !important; }
}
@media screen and (max-width: 480px) {
    .kpi-principal-card, .kpi-doble-card { align-items: flex-start; flex-direction: column; }
    .titulo-principal { font-size: 1.4rem; }
}
"""


def aplicar_estilos() -> None:
    """Inyecta el CSS global. Llamar justo después de st.set_page_config()."""
    st.markdown("<style>" + _CSS + "</style>", unsafe_allow_html=True)


def pie_de_pagina(nombre: str = NOMBRE, github: str = GITHUB_URL, linkedin: str = LINKEDIN_URL) -> None:
    """Pie con nombre y logotipos de GitHub y LinkedIn. Llamar al final de cada página."""
    n, g, l = html.escape(nombre), html.escape(github, quote=True), html.escape(linkedin, quote=True)
    st.markdown(
        "<div class='pie-pagina'>"
        f"<div class='pie-nombre'>{n}</div>"
        f"<div class='pie-copy'>© {datetime.now().year}</div>"
        "<div class='pie-enlaces'>"
        f"<a href='{g}' target='_blank' rel='noopener noreferrer' aria-label='GitHub' title='GitHub'>{_SVG_GITHUB}</a>"
        f"<a href='{l}' target='_blank' rel='noopener noreferrer' aria-label='LinkedIn' title='LinkedIn'>{_SVG_LINKEDIN}</a>"
        "</div></div>",
        unsafe_allow_html=True,
    )