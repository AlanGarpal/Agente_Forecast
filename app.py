from statistics import NormalDist
import numpy as np
import pandas as pd
import streamlit as st
from streamlit_echarts import JsCode, st_echarts

from agent import ejecutar_agente_forecast
from estilos import aplicar_estilos, pie_de_pagina
from forecast_logic import ejecutar_forecast_pipeline

# Configuración inicial de la página (layout wide para aprovechar el ancho)
st.set_page_config(
    page_title="Alan Garces Palacios - Agente de Forecast",
    page_icon=":material/psychology:",
    layout="wide",
)

# Aplicar estilos globales personalizados
aplicar_estilos()

# ------------------------------------------------------------------ PÁGINA DE CARGA / SPLASH INICIAL
if "loaded" not in st.session_state:
  with st.status(
      "🚀 Inicializando motor analítico y modelos de IA...", expanded=True
  ) as status:
    st.write("Conectando con microservicios y pipelines de datos...")
    st.write("Cargando módulos de XGBoost y Polars...")
    st.write("Preparando interfaz ejecutiva...")
    status.update(
        label="¡Sistema listo para operar!", state="complete", expanded=False
    )
  st.session_state["loaded"] = True

# ------------------------------------------------------------------ HELPERS & ICONOS SVG
ICONOS = {
    "cpu": (
        '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="9" y="9"'
        ' width="6" height="6"/><path'
        ' d="M15 2v2M15 20v2M2 15h2M2 9h2M20 15h2M20 9h2M9 2v2M9 20v2"/>'
    ),
    "bar": (
        '<line x1="12" y1="20" x2="12" y2="10"/><line x1="18" y1="20" x2="18"'
        ' y2="4"/><line x1="6" y1="20" x2="6" y2="16"/>'
    ),
    "network": (
        '<circle cx="18" cy="5" r="3"/><circle cx="6" cy="12" r="3"/><circle'
        ' cx="18" cy="19" r="3"/><line x1="8.59" y1="13.51" x2="15.42"'
        ' y2="17.49"/><line x1="15.41" y1="6.51" x2="8.59" y2="10.49"/>'
    ),
    "clock": (
        '<circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/>'
    ),
    "eye": (
        '<path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12"'
        ' cy="12" r="3"/>'
    ),
    "repeat": (
        '<polyline points="17 1 21 5 17 9"/><path d="M3 11V9a4 4 0 0'
        ' 1 4-4h14"/><polyline points="7 23 3 19 7 15"/><path d="M21 13v2a4 4 0'
        ' 0 1-4 4H3"/>'
    ),
    "zap": (
        '<polygon points="13 2 3 14 12 14 11 22 21 10 12 10 13 2"/>'
    ),
    "package": (
        '<line x1="16.5" y1="9.4" x2="7.5" y2="4.21"/><path d="M21 16V8a2 2 0 0'
        ' 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1'
        ' 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/><polyline points="3.27'
        ' 6.96 12 12.01 20.73 6.96"/><line x1="12" y1="22.08" x2="12" y2="12"/>'
    ),
    "tag": (
        '<path d="M20.59 13.41l-7.17 7.17a2 2 0 0 1-2.83 0L2 12V2h10l8.59'
        ' 8.59a2 2 0 0 1 0 2.82z"/><line x1="7" y1="7" x2="7.01" y2="7"/>'
    ),
    "alert": (
        '<path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0'
        ' 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"/><line x1="12" y1="9" x2="12"'
        ' y2="13"/><line x1="12" y1="17" x2="12.01" y2="17"/>'
    ),
    "alertc": (
        '<circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12"'
        ' y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/>'
    ),
    "check": (
        '<path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><polyline points="22 4'
        ' 12 14.01 9 11.01"/>'
    ),
    "users": (
        '<path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/><circle cx="9"'
        ' cy="7" r="4"/><path d="M23 21v-2a4 4 0 0 0-3-3.87"/><path'
        ' d="M16 3.13a4 4 0 0 1 0 7.75"/>'
    ),
    "chat": (
        '<path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38'
        ' 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0'
        ' 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z"/>'
    ),
    "type": (
        '<polyline points="4 7 4 4 20 4 20 7"/><line x1="9" y1="20" x2="15"'
        ' y2="20"/><line x1="12" y1="4" x2="12" y2="20"/>'
    ),
    "compass": (
        '<circle cx="12" cy="12" r="10"/><polygon points="16.24 7.76 14.12'
        ' 14.12 7.76 16.24 9.88 9.88 16.24 7.76"/>'
    ),
    "maximize": (
        '<path d="M8 3H5a2 2 0 0 0-2 2v3m18 0V5a2 2 0 0 0-2-2h-3m0 18h3a2 2 0'
        ' 0 2-2v-3M3 16v3a2 2 0 0 0 2 2h3"/>'
    ),
    "thermo": (
        '<path d="M14 14.76V3.5a2.5 2.5 0 0 0-5 0v11.26a4.5 4.5 0 1 0 5 0z"/>'
    ),
    "edit": (
        '<path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7'
        ' 19l-4 1 1-4L16.5 3.5z"/>'
    ),
    "search": (
        '<circle cx="11" cy="11" r="8"/><line x1="21" y1="21" x2="16.65"'
        ' y2="16.65"/>'
    ),
    "book": (
        '<path d="M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z"/><path d="M22'
        ' 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z"/>'
    ),
    "tool": (
        '<path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6'
        ' 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0'
        ' 1 7.94-7.94l-3.76 3.76z"/>'
    ),
    "target": (
        '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle'
        ' cx="12" cy="12" r="2"/>'
    ),
    "grid": (
        '<rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7"'
        ' height="7"/><rect x="14" y="14" width="7" height="7"/><rect x="3"'
        ' y="14" width="7" height="7"/>'
    ),
    "activity": (
        '<polyline points="22 12 18 12 15 21 9 3 6 12 2 12"/>'
    ),
    "flask": (
        '<path d="M10 2v7.527a2 2 0 0 1-.211.896L4.72 20.55a1 1 0 0 0 .9'
        ' 1.45h12.76a1 1 0 0 0 .9-1.45l-5.069-10.127A2 2 0 0 1 14'
        ' 9.527V2"/><path d="M8.5 2h7"/><path d="M7 16h10"/>'
    ),
    "trend": (
        '<polyline points="23 6 13.5 15.5 8.5 10.5 1 18"/><polyline'
        ' points="17 6 23 6 23 12"/>'
    ),
    "calc": (
        '<rect width="16" height="20" x="4" y="2" rx="2"/><line x1="8"'
        ' x2="16" y1="6" y2="6"/><line x1="16" x2="16" y1="14" y2="18"/><path'
        ' d="M16 10h.01M12 10h.01M8 10h.01M12 14h.01M8 14h.01M12 18h.01M8'
        ' 18h.01"/>'
    ),
}

AVATARES = {"user": ":material/person:", "assistant": ":material/smart_toy:"}
AZUL, NARANJA = "#12239E", "#FF5100"


def svg(nombre):
  cuerpo = ICONOS.get(nombre)
  if not cuerpo:
    return ""
  return (
      "<svg viewBox='0 0 24 24' fill='none' stroke='currentColor'"
      f" stroke-width='1.8' stroke-linecap='round'"
      f" stroke-linejoin='round'>{cuerpo}</svg>"
  )


def show(html: str):
  st.markdown(html, unsafe_allow_html=True)


def hero(titulo_texto, subtitulo, icono=None):
  show(
      f"<div class='hero kpi-popover-box'><h1>{svg(icono)}{titulo_texto}</h1><p>{subtitulo}</p></div>"
  )


def titulo(texto, icono=None):
  show(f"<h3 class='section-title'>{svg(icono)}{texto}</h3>")


def card(icono, titulo_, cuerpo, azul=False):
  cls = "card blue kpi-popover-box" if azul else "card kpi-popover-box"
  return (
      f"<div class='{cls}'><div class='ic'>{svg(icono)}</div>"
      f"<div class='ct'>{titulo_}</div><div class='cb'>{cuerpo}</div></div>"
  )


def kpi(label, valor, sub=""):
  return (
      f"<div class='kpi kpi-popover-box'><div class='l'>{label}</div><div"
      f" class='v'>{valor}</div><div class='s'>{sub}</div></div>"
  )


def fila_tarjetas(items):
  cols = st.columns(len(items))
  for i, (c, (ic, t, b, det)) in enumerate(zip(cols, items)):
    with c:
      show(card(ic, t, b, azul=(i % 2 == 0)))
      with st.popover("Ver más", use_container_width=True):
        st.markdown(det)


# ------------------------------------------------------------------ CONFIGURACIÓN DE ECHARTS
BASE = {
    "backgroundColor": "transparent",
    "animationDuration": 900,
    "animationEasing": "cubicOut",
}
GRID = {"left": 55, "right": 25, "top": 55, "bottom": 50, "containLabel": True}
EJE_Y = {
    "type": "value",
    "scale": True,
    "splitLine": {"lineStyle": {"type": "dashed", "color": "#d9dcf0"}},
}


def _grad(c1, c2):
  return JsCode(
      "new echarts.graphic.LinearGradient(0,0,0,1,"
      f"[{{offset:0,color:'{c1}'}},{{offset:1,color:'{c2}'}}])"
  ).js_code


def opcion_forecast(pdf):
  meses = [
      m.strftime("%Y-%m") if hasattr(m, "strftime") else str(m)
      for m in pdf["Mes"]
  ]
  dem = pdf["Demanda_Estimada"].round(1).tolist()
  inf = pdf["Limite_Inferior"].round(1).tolist()
  sup = pdf["Limite_Superior"].round(1).tolist()
  banda = [round(s - i, 1) for s, i in zip(sup, inf)]

  tooltip_fmt = JsCode(
      "function(params){var s='<b>'+params[0].axisValue+'</b><br/>';"
      "params.forEach(function(p){if(p.seriesName==='banda')return;"
      "s+=p.marker+p.seriesName+':"
      " <b>'+Number(p.value).toLocaleString('es-MX',{maximumFractionDigits:0})+'</b><br/>';});"
      "return s;}"
  ).js_code
  eje_fmt = JsCode(
      "function(v){return Math.abs(v)>=1000?(v/1000).toFixed(0)+'k':v;}"
  ).js_code

  return {
      **BASE,
      "color": [AZUL, "#7C89E0", NARANJA],
      "tooltip": {
          "trigger": "axis",
          "formatter": tooltip_fmt,
          "backgroundColor": "rgba(255,255,255,.96)",
          "borderColor": NARANJA,
          "textStyle": {"color": "#1f2340"},
      },
      "legend": {
          "data": ["Demanda estimada", "Límite inferior", "Límite superior"],
          "top": 5,
      },
      "grid": GRID,
      "toolbox": {
          "feature": {
              "saveAsImage": {"title": "Guardar"},
              "dataZoom": {"title": {"zoom": "Zoom", "back": "Reset"}},
          }
      },
      "xAxis": {"type": "category", "data": meses, "boundaryGap": False},
      "yAxis": {**EJE_Y, "axisLabel": {"formatter": eje_fmt}},
      "dataZoom": [{"type": "inside"}],
      "series": [
          {
              "name": "Límite inferior",
              "type": "line",
              "stack": "band",
              "symbol": "none",
              "smooth": True,
              "lineStyle": {"width": 1.5, "type": "dashed", "color": "#7C89E0"},
              "data": inf,
          },
          {
              "name": "banda",
              "type": "line",
              "stack": "band",
              "symbol": "none",
              "smooth": True,
              "lineStyle": {"opacity": 0},
              "areaStyle": {
                  "color": _grad(
                      "rgba(255,81,0,0.30)", "rgba(255,81,0,0.04)"
                  )
              },
              "data": banda,
          },
          {
              "name": "Límite superior",
              "type": "line",
              "symbol": "none",
              "smooth": True,
              "lineStyle": {"width": 1.5, "type": "dashed", "color": NARANJA},
              "data": sup,
          },
          {
              "name": "Demanda estimada",
              "type": "line",
              "smooth": True,
              "symbolSize": 8,
              "z": 5,
              "lineStyle": {
                  "width": 3.5,
                  "color": AZUL,
                  "shadowBlur": 10,
                  "shadowColor": "rgba(18,35,158,.35)",
              },
              "itemStyle": {"color": AZUL, "borderColor": "#fff", "borderWidth": 2},
              "emphasis": {"focus": "series"},
              "markPoint": {
                  "symbolSize": 56,
                  "itemStyle": {"color": NARANJA},
                  "data": [
                      {"type": "max", "name": "Pico"},
                      {"type": "min", "name": "Mínimo"},
                  ],
              },
              "data": dem,
          },
      ],
  }


def opcion_descenso(w):
  return {
      **BASE,
      "tooltip": {"trigger": "axis"},
      "grid": GRID,
      "xAxis": {
          "type": "category",
          "name": "Iteración",
          "nameLocation": "middle",
          "nameGap": 28,
          "data": list(range(len(w))),
      },
      "yAxis": {**EJE_Y, "name": "w"},
      "series": [
          {
              "name": "w",
              "type": "line",
              "smooth": True,
              "symbolSize": 9,
              "data": [round(x, 4) for x in w],
              "lineStyle": {"color": NARANJA, "width": 3},
              "itemStyle": {
                  "color": NARANJA,
                  "borderColor": "#fff",
                  "borderWidth": 2,
              },
              "markLine": {
                  "symbol": "none",
                  "lineStyle": {"color": AZUL, "type": "dashed", "width": 2},
                  "label": {"formatter": "objetivo w = 3", "color": AZUL},
                  "data": [{"yAxis": 3}],
              },
          }
      ],
  }


def opcion_activaciones():
  z = np.linspace(-6, 6, 121)
  datos = {
      "Sigmoide": 1 / (1 + np.exp(-z)),
      "Tanh": np.tanh(z),
      "ReLU": np.maximum(0, z),
  }
  return {
      **BASE,
      "color": [AZUL, "#7C89E0", NARANJA],
      "tooltip": {"trigger": "axis"},
      "legend": {"top": 5},
      "grid": GRID,
      "xAxis": {
          "type": "value",
          "min": -6,
          "max": 6,
          "name": "z",
          "splitLine": {"show": False},
      },
      "yAxis": {**EJE_Y, "min": -1.2, "max": 6},
      "series": [
          {
              "name": k,
              "type": "line",
              "smooth": True,
              "showSymbol": False,
              "lineStyle": {"width": 3},
              "emphasis": {"focus": "series"},
              "data": [
                  [round(float(x), 2), round(float(y), 4)] for x, y in zip(z, v)
              ],
          }
          for k, v in datos.items()
      ],
  }


def opcion_softmax(tokens, p):
  imax = int(np.argmax(p))
  label_fmt = JsCode(
      "function(p){return (p.value*100).toFixed(1)+'%';}"
  ).js_code
  datos = [
      {
          "value": round(float(v), 4),
          "itemStyle": {
              "color": (
                  _grad(NARANJA, "#ffb08a")
                  if i == imax
                  else _grad(AZUL, "#7C89E0")
              ),
              "borderRadius": [8, 8, 0, 0],
          },
      }
      for i, v in enumerate(p)
  ]
  return {
      **BASE,
      "tooltip": {"trigger": "axis", "axisPointer": {"type": "shadow"}},
      "grid": GRID,
      "xAxis": {"type": "category", "data": tokens},
      "yAxis": {
          **EJE_Y,
          "min": 0,
          "max": 1,
          "scale": False,
          "axisLabel": {
              "formatter": JsCode(
                  "function(v){return (v*100).toFixed(0)+'%';}"
              ).js_code
          },
      },
      "series": [
          {
              "name": "Probabilidad",
              "type": "bar",
              "barWidth": "55%",
              "data": datos,
              "label": {
                  "show": True,
                  "position": "top",
                  "formatter": label_fmt,
                  "color": "#1f2340",
                  "fontWeight": "bold",
              },
              "emphasis": {
                  "itemStyle": {
                      "shadowBlur": 18,
                      "shadowColor": "rgba(255,81,0,.5)",
                  }
              },
          }
      ],
  }


# ------------------------------------------------------------------ SECCIÓN 1: HISTORIA Y ML
def seccion_historia():
  hero(
      "1. Historia: IA → Machine Learning → Deep Learning",
      (
          "De la pregunta de Turing a las redes neuronales profundas que hoy"
          " impulsan la IA generativa."
      ),
      icono="cpu",
  )

  titulo("Tres capas anidadas")
  fila_tarjetas([
      (
          "cpu",
          "Inteligencia Artificial",
          (
              "Sistemas que realizan tareas que requieren inteligencia:"
              " razonar, percibir, decidir."
          ),
          (
              "**Incluye** reglas expertas, búsqueda, planificación y"
              " aprendizaje.\n\n*Ejemplo:* un sistema experto que recomienda"
              " reorden según reglas fijas."
          ),
      ),
      (
          "bar",
          "Machine Learning",
          (
              "Algoritmos que **aprenden patrones de los datos** en lugar de"
              " seguir reglas escritas a mano."
          ),
          (
              "Entrenar = **minimizar una función de pérdida** que mide el"
              " error del modelo.\n\nVer la fórmula en el recuadro 'La idea"
              " matemática central del ML'."
          ),
      ),
      (
          "network",
          "Deep Learning",
          (
              "Redes neuronales con muchas capas que aprenden"
              " **representaciones** automáticamente."
          ),
          (
              "Excelente con datos no estructurados: imágenes, audio,"
              " texto.\n\nRequiere más datos y cómputo (GPUs)."
          ),
      ),
  ])

  with st.expander(":material/calculate: La idea matemática central del ML"):
    st.latex(
        r"\hat{\theta}=\arg\min_{\theta}\;\frac{1}{n}\sum_{i=1}^{n}\mathcal{L}\big(y_i,\;f_\theta(x_i)\big)"
    )
    st.caption(
        "Se busca el conjunto de parámetros θ que minimiza el error promedio"
        " entre lo real (yᵢ) y lo predicho f(xᵢ)."
    )

  titulo("Línea del tiempo")
  hitos = [
      (
          "1950",
          "Test de Turing",
          "¿Puede una máquina 'pensar'?",
          (
              "Alan Turing publica *Computing Machinery and Intelligence* y"
              " propone el juego de imitación."
          ),
      ),
      (
          "1956",
          "Nace la IA",
          "Conferencia de Dartmouth.",
          (
              "John McCarthy acuña el término **Inteligencia Artificial**."
          ),
      ),
      (
          "1958",
          "Perceptrón",
          "Primera neurona artificial entrenable.",
          (
              "Frank Rosenblatt: clasificador lineal que ajusta pesos con"
              " ejemplos."
          ),
      ),
      (
          "1974-90",
          "Inviernos de la IA",
          "Expectativas no cumplidas.",
          (
              "Recortes de financiamiento por límites de cómputo y de los"
              " modelos de la época."
          ),
      ),
      (
          "1997",
          "Deep Blue",
          "IBM vence a Kaspárov.",
          (
              "Triunfo de la búsqueda y la fuerza bruta, no del aprendizaje."
          ),
      ),
      (
          "2012",
          "AlexNet",
          "Arranca la era del Deep Learning.",
          (
              "Una CNN gana ImageNet por amplio margen gracias a GPUs y big"
              " data."
          ),
      ),
      (
          "2016",
          "AlphaGo",
          "Vence al campeón mundial de Go.",
          "Combina redes profundas con aprendizaje por refuerzo.",
      ),
      (
          "2017",
          "Transformers",
          "*Attention Is All You Need*.",
          (
              "Arquitectura basada en atención: base de todos los LLM"
              " modernos."
          ),
      ),
      (
          "2022",
          "IA generativa",
          "ChatGPT llega al público.",
          "LLMs y modelos de difusión generan texto, código e imágenes.",
      ),
      (
          "2024+",
          "Agentes",
          "LLMs que usan herramientas.",
          (
              "Razonan, consultan SQL/APIs y ejecutan código;"
              " multimodalidad."
          ),
      ),
  ]
  fila_tarjetas([
      ("clock", f"{a} · {t}", d, det) for i, (a, t, d, det) in enumerate(hitos[:5])
  ])
  fila_tarjetas([
      ("clock", f"{a} · {t}", d, det) for i, (a, t, d, det) in enumerate(hitos[5:])
  ])

  titulo("Machine Learning: tipos, ejemplos y matemática")
  t1, t2, t3 = st.tabs(["Supervisado", "No supervisado", "Por refuerzo"])
  with t1:
    c1, c2 = st.columns([1.2, 1])
    with c1:
      show(
          card(
              "target",
              "Aprende con etiquetas",
              (
                  "Regresión (forecast de demanda, precios) y clasificación"
                  " (fraude, churn). Algoritmos: regresión lineal, Random Forest,"
                  " **XGBoost**."
              ),
              azul=True,
          )
      )
    with c2:
      st.latex(r"\text{MSE}=\frac{1}{n}\sum_{i=1}^{n}(y_i-\hat{y}_i)^2")
      st.latex(r"\hat{y}=\beta_0+\beta_1x_1+\dots+\beta_px_p")
  with t2:
    c1, c2 = st.columns([1.2, 1])
    with c1:
      show(
          card(
              "grid",
              "Estructura sin etiquetas",
              (
                  "Clustering de clientes o productos (K-Means), detección de"
                  " anomalías, PCA para reducir dimensiones."
              ),
          )
      )
    with c2:
      st.latex(r"J=\sum_{k=1}^{K}\sum_{x\in C_k}\lVert x-\mu_k\rVert^2")
      st.caption(
          "K-Means minimiza la distancia de cada punto al centroide de su"
          " grupo."
      )
  with t3:
    c1, c2 = st.columns([1.2, 1])
    with c1:
      show(
          card(
              "activity",
              "Prueba y error",
              (
                  "Un agente maximiza recompensa acumulada: robótica, juegos,"
                  " optimización de rutas e inventario."
              ),
              azul=True,
          )
      )
    with c2:
      st.latex(
          r"Q(s,a)\leftarrow"
          r" Q(s,a)+\alpha\Big[r+\gamma\max_{a'}Q(s',a')-Q(s,a)\Big]"
      )
      st.caption("Actualización de Q-learning.")

  titulo("Laboratorio: descenso por gradiente", "flask")
  st.write(
      "Así 'aprende' un modelo: ajusta un parámetro w para minimizar la pérdida"
      " L(w) = (w − 3)²."
  )
  st.latex(r"w_{t+1}=w_t-\eta\,\nabla L(w_t)=w_t-2\eta\,(w_t-3)")
  c1, c2, c3 = st.columns(3)
  lr = c1.slider("Tasa de aprendizaje η", 0.05, 1.2, 0.30, 0.05, key="lr_descenso")
  pasos = c2.slider("Iteraciones", 5, 40, 20, key="pasos_descenso")
  w0 = c3.slider("w inicial", -10.0, 10.0, -6.0, 0.5, key="w0_descenso")
  w = [w0]
  for _ in range(pasos):
    w.append(w[-1] - lr * 2 * (w[-1] - 3))
  traza = pd.DataFrame({"w": w, "Pérdida": [(x - 3) ** 2 for x in w]})
  g1, g2 = st.columns([2, 1])
  with g1:
    st_echarts(opcion_descenso(w), height="320px", key="eco_descenso")
  with g2:
    show(kpi("w final", f"{w[-1]:.3f}", "objetivo: 3.000"))
    st.write("")
    show(
        kpi(
            "Pérdida final",
            f"{traza['Pérdida'].iloc[-1]:.4g}",
            "converge" if lr < 1 else "diverge (η ≥ 1)",
        )
    )
  with st.popover("¿Por qué diverge con η > 1?"):
    st.latex(r"w_{t+1}-3=(1-2\eta)(w_t-3)")
    st.markdown(
        "El error se multiplica por **(1 − 2η)** en cada paso. Converge si |1 −"
        " 2η| < 1, es decir, 0 < η < 1. Con η > 1 el error crece en cada"
        " iteración."
    )

  titulo("Deep Learning: la neurona y sus activaciones")
  c1, c2 = st.columns([1, 1.3])
  with c1:
    st.latex(r"y=\sigma\big(\mathbf{w}^{\top}\mathbf{x}+b\big)")
    st.caption(
        "Una neurona: suma ponderada de entradas + sesgo, pasada por una"
        " función de activación no lineal."
    )
    with st.popover("Ver fórmulas de activación"):
      st.latex(r"\text{sigmoide}(z)=\frac{1}{1+e^{-z}}")
      st.latex(r"\tanh(z)=\frac{e^{z}-e^{-z}}{e^{z}+e^{-z}}")
      st.latex(r"\text{ReLU}(z)=\max(0,z)")
  with c2:
    st_echarts(opcion_activaciones(), height="280px", key="eco_activaciones")

  fila_tarjetas([
      (
          "eye",
          "CNN",
          "Visión: imágenes, control de calidad, lectura de anaqueles.",
          "Filtros convolucionales detectan bordes → formas → objetos.",
      ),
      (
          "repeat",
          "RNN / LSTM",
          "Secuencias: series de tiempo, voz, traducción.",
          (
              "Mantienen un estado oculto que 'recuerda' el pasado. Difíciles"
              " de paralelizar."
          ),
      ),
      (
          "zap",
          "Transformers",
          "Lenguaje, código, imágenes y series de tiempo.",
          (
              "Usan atención para relacionar todos los elementos a la vez. Ver"
              " sección 2."
          ),
      ),
  ])

  titulo("Usos en retail y distribución")
  fila_tarjetas([
      (
          "package",
          "Forecast de demanda",
          "ML supervisado (XGBoost) → menos inventario ocioso.",
          "Entrada: histórico, precio, promociones, estacionalidad.",
      ),
      (
          "tag",
          "Pricing",
          "ML + elasticidad → mayor margen.",
          "Mide cómo cambia la demanda al mover el precio.",
      ),
      (
          "alert",
          "Agotados",
          "Reglas + ML → menos venta perdida.",
          "Anticipa quiebres de stock antes de que ocurran.",
      ),
      (
          "users",
          "Clientes",
          "Clustering → promociones dirigidas.",
          "Segmenta por frecuencia, ticket y categorías.",
      ),
      (
          "chat",
          "Asistentes",
          "LLM + agentes → decisiones rápidas.",
          "Consultan datos en lenguaje natural.",
      ),
  ])


# ------------------------------------------------------------------ SECCIÓN 2: LLMS Y RAG
def seccion_llm():
  hero(
      "2. LLMs, Transformers y RAG",
      (
          "Cómo un modelo que predice la siguiente palabra termina razonando,"
          " programando y usando herramientas."
      ),
      icono="zap",
  )

  titulo("Conceptos clave")
  fila_tarjetas([
      (
          "type",
          "Token",
          "Unidad de texto que ve el modelo (palabra o trozo de palabra).",
          (
              "*'Demanda anual'* puede dividirse en: `De` `manda` `"
              " `anual`.\n\nEl costo y el límite de contexto se miden en"
              " tokens."
          ),
      ),
      (
          "compass",
          "Embedding",
          "Vector numérico que representa el significado.",
          (
              "Textos con significado parecido quedan **cerca** en el espacio"
              " vectorial. Es la base de RAG."
          ),
      ),
      (
          "maximize",
          "Ventana de contexto",
          "Memoria de corto plazo: lo máximo que el modelo ve de una vez.",
          (
              "Si el documento no cabe, se recorta o se usa RAG para traer"
              " solo lo relevante."
          ),
      ),
      (
          "thermo",
          "Temperatura",
          "Controla qué tan 'creativa' o determinista es la salida.",
          (
              "Baja → respuestas estables. Alta → más variedad. Pruébalo en"
              " el laboratorio de abajo."
          ),
      ),
  ])

  titulo("Arquitectura Transformer")
  c1, c2 = st.columns([1, 1.15])
  with c1:
    st.graphviz_chart("""
        digraph {
            rankdir=BT; node [shape=box, style="rounded,filled", fillcolor="#eef0fb", fontname=Helvetica, color="#12239E"];
            T [label="Texto de entrada"];
            TK [label="Tokenización + Embeddings"];
            PE [label="+ Codificación posicional"];
            SA [label="Self-Attention multi-cabeza", fillcolor="#FF5100", fontcolor=white];
            LN [label="Add & Norm"];
            FF [label="Feed-Forward"];
            LN2 [label="Add & Norm  (×N capas)"];
            OUT [label="Softmax → siguiente token", fillcolor="#12239E", fontcolor=white];
            T -> TK -> PE -> SA -> LN -> FF -> LN2 -> OUT;
        }
        """)
  with c2:
    st.markdown(
        "**Self-attention:** cada token decide a qué otros tokens prestar"
        " atención."
    )
    st.latex(
        r"\text{Attention}(Q,K,V)=\text{softmax}\!\left(\frac{QK^{\top}}{\sqrt{d_k}}\right)V"
    )
    with st.popover("¿Qué son Q, K, V y por qué √dₖ?"):
      st.markdown(
          "- **Q (query):** qué busca cada token.\n- **K (key):** qué"
          " ofrece cada token.\n- **V (value):** la información que aporta.\n\n"
          " Se divide entre **√dₖ** para que los productos punto no crezcan"
          " con la dimensión y el softmax no se sature."
      )
    st.markdown(
        "**Orden de las palabras:** la atención no conoce posiciones, por eso"
        " se suma una codificación posicional."
    )
    st.latex(
        r"PE_{(pos,2i)}=\sin\!\Big(\tfrac{pos}{10000^{2i/d}}\Big),\quad"
        r" PE_{(pos,2i+1)}=\cos\!\Big(\tfrac{pos}{10000^{2i/d}}\Big)"
    )
    with st.popover("Multi-cabeza y capas"):
      st.latex(
          r"\text{MultiHead}=\text{Concat}(\text{head}_1,\dots,\text{head}_h)\,W^{O}"
      )
      st.markdown(
          "Cada cabeza capta un tipo de relación distinto (sintaxis,"
          " referencias, etc.). Se apilan N capas para construir significado"
          " cada vez más abstracto."
      )

  titulo("Laboratorio: softmax y temperatura", "flask")
  st.write(
      "El LLM calcula una puntuación (logit) por token y la convierte en"
      " probabilidad:"
  )
  st.latex(r"P(token_i)=\frac{e^{z_i/T}}{\sum_j e^{z_j/T}}")
  T = st.slider("Temperatura T", 0.1, 3.0, 1.0, 0.1, key="slider_temp_llm")
  tokens = ["demanda", "precio", "inventario", "cliente", "oferta"]
  logits = np.array([3.2, 2.1, 1.5, 0.7, 0.2])
  p = np.exp(logits / T)
  p /= p.sum()
  st.caption("Frase de ejemplo: 'El próximo mes aumentará la ___'")
  g1, g2 = st.columns([2, 1])
  with g1:
    st_echarts(opcion_softmax(tokens, p), height="320px", key="eco_softmax")
  with g2:
    show(kpi("Token más probable", tokens[int(p.argmax())], f"{p.max():.1%}"))
    st.write("")
    show(
        kpi("Entropía", f"{-(p * np.log2(p)).sum():.2f} bits", "mayor = más aleatorio")
    )

  titulo("Adaptar un LLM a tus datos")
  fila_tarjetas([
      (
          "edit",
          "Prompt engineering",
          "Instrucciones y ejemplos en el prompt. Costo bajo.",
          "Es el primer paso, siempre. Define rol, formato y restricciones.",
      ),
      (
          "search",
          "RAG",
          "Recupera documentos relevantes y los inyecta al contexto. Costo medio.",
          "Ideal para conocimiento privado o que cambia seguido.",
      ),
      (
          "book",
          "Fine-tuning",
          "Reentrena con tus ejemplos. Costo alto.",
          (
              "Útil para estilo o tareas muy específicas; no es la mejor forma"
              " de 'enseñar datos nuevos'."
          ),
      ),
      (
          "tool",
          "Agentes",
          "El LLM elige qué herramienta ejecutar (SQL, Python, API).",
          (
              "Ciclo: razonar → actuar → observar → responder. Es lo que usamos"
              " en la sección 3."
          ),
      ),
  ])

  titulo("RAG: Retrieval-Augmented Generation")
  c1, c2 = st.columns([1.3, 1])
  with c1:
    st.graphviz_chart("""
        digraph {
            rankdir=LR; node [shape=box, style="rounded,filled", fillcolor="#eef0fb", fontname=Helvetica, color="#12239E"];
            D [label="Documentos / BD"]; E [label="Embeddings"];
            V [label="Base vectorial", fillcolor="#FF5100", fontcolor=white];
            Q [label="Pregunta"]; R [label="Top-k fragmentos"];
            L [label="LLM", fillcolor="#12239E", fontcolor=white]; A [label="Respuesta con contexto"];
            D -> E -> V; Q -> V [label="búsqueda\\nsemántica"]; V -> R -> L; Q -> L; L -> A;
        }
        """)
  with c2:
    st.markdown(
        "La recuperación mide qué tan parecida es la pregunta a cada fragmento"
        " con **similitud coseno**:"
    )
    st.latex(
        r"\cos(\theta)=\frac{\mathbf{q}\cdot\mathbf{d}}{\lVert\mathbf{q}\rVert\,\lVert\mathbf{d}\rVert}"
    )

  st.markdown(
      "**Ejemplo numérico** (vectores de 3 dimensiones, solo ilustrativo):"
  )
  q = np.array([0.9, 0.1, 0.4])
  docs = {
      "Política de reorden de abarrotes": np.array([0.8, 0.2, 0.5]),
      "Manual de uso de la tarjeta club": np.array([0.1, 0.9, 0.2]),
      "Guía de inventario de seguridad": np.array([0.7, 0.1, 0.6]),
  }
  sims = {
      k: float(q @ v / (np.linalg.norm(q) * np.linalg.norm(v)))
      for k, v in docs.items()
  }
  tabla = pd.DataFrame({
      "Documento": list(sims),
      "Similitud coseno": list(sims.values()),
  }).sort_values("Similitud coseno", ascending=False)
  st.dataframe(
      tabla,
      use_container_width=True,
      hide_index=True,
      column_config={
          "Similitud coseno": st.column_config.ProgressColumn(
              "Similitud coseno", min_value=0.0, max_value=1.0, format="%.3f"
          )
      },
  )

  c1, c2 = st.columns(2)
  with c1:
    show(
        card(
            "check",
            "Ventajas de RAG",
            (
                "Reduce alucinaciones, usa información actualizada y permite"
                " citar la fuente."
            ),
            azul=True,
        )
    )
  with c2:
    show(
        card(
            "alertc",
            "Limitaciones de los LLM",
            (
                "Alucinaciones, sesgos, sensibilidad al prompt, costo/latencia"
                " y privacidad. Siempre validar con datos reales."
            ),
        )
    )


# ------------------------------------------------------------------ SECCIÓN 3: CASO PRÁCTICO
@st.cache_data(show_spinner="Ejecutando pipeline de forecast...")
def cargar_forecast(horizonte: int):
  return ejecutar_forecast_pipeline(horizonte)


def responder(historial):
  try:
    return ejecutar_agente_forecast(historial)
  except Exception as e:
    return f"Ocurrió un error al procesar tu consulta con el agente: {e}"


def seccion_practica():
  hero(
      "3. Caso práctico: Forecast + Agente IA",
      (
          "Una serie de tiempo aporta el contexto numérico; el agente lo"
          " interpreta y propone acciones."
      ),
      icono="trend",
  )

  # Parámetros organizados en un contenedor superior integrado en la página
  with st.container(border=True):
    st.markdown("##### :material/tune: Parámetros de simulación y abasto")
    p1, p2, p3 = st.columns(3)
    with p1:
      horizonte = st.slider("Horizonte (meses)", 3, 24, 12, key="slider_horiz")
    with p2:
      nivel = st.select_slider(
          "Nivel de servicio",
          options=[0.90, 0.95, 0.975, 0.99],
          value=0.95,
          format_func=lambda x: f"{x:.1%}",
          key="slider_nivel",
      )
    with p3:
      lead = st.slider(
          "Lead time del proveedor (meses)",
          0.25,
          3.0,
          1.0,
          0.25,
          key="slider_lead",
      )

  pdf = cargar_forecast(horizonte).to_pandas()
  dem = pdf["Demanda_Estimada"]
  total, prom = dem.sum(), dem.mean()
  pico, minimo = pdf.loc[dem.idxmax()], pdf.loc[dem.idxmin()]

  # --- Matemática derivada del forecast ---
  pend = float(
      np.polyfit(np.arange(len(dem)), dem.values, 1)[0]
  )  # unidades/mes
  cv = float(dem.std(ddof=1) / prom) if prom else 0.0  # variabilidad
  sigma = float(
      ((pdf["Limite_Superior"] - pdf["Limite_Inferior"]) / (2 * 1.96)).mean()
  )
  z = NormalDist().inv_cdf(nivel)
  ss = z * sigma * np.sqrt(lead)
  rop = prom * lead + ss

  titulo("Proyección de demanda")
  k = st.columns(4)
  k[0].markdown(
      kpi("Demanda total", f"{total:,.0f}", f"{horizonte} meses"),
      unsafe_allow_html=True,
  )
  k[1].markdown(
      kpi("Promedio mensual", f"{prom:,.1f}", f"CV {cv:.1%}"),
      unsafe_allow_html=True,
  )
  k[2].markdown(
      kpi("Mes pico", f"{pico['Mes']}", f"{pico['Demanda_Estimada']:,.0f} u."),
      unsafe_allow_html=True,
  )
  k[3].markdown(
      kpi("Mes más bajo", f"{minimo['Mes']}", f"{minimo['Demanda_Estimada']:,.0f} u."),
      unsafe_allow_html=True,
  )
  st.write("")
  st_echarts(opcion_forecast(pdf), height="420px", key="eco_forecast")
  with st.expander("Ver tabla detallada de datos"):
    st.dataframe(pdf, use_container_width=True)

  titulo("Matemática detrás de las recomendaciones", "calc")
  c1, c2 = st.columns([1.1, 1])
  with c1:
    st.markdown("**Tendencia** (regresión lineal sobre el forecast):")
    st.latex(
        rf"\hat{{d}}_t=a+b\,t\quad\Rightarrow\quad b={pend:+,.1f}\ \text{{unidades/mes}}"
    )
    st.markdown(
        "**Incertidumbre** (se asume que los límites son un intervalo del 95"
        " %):"
    )
    st.latex(rf"\sigma\approx\frac{{LS-LI}}{{2\cdot1.96}}={sigma:,.1f}")
    st.markdown("**Inventario de seguridad y punto de reorden:**")
    st.latex(
        rf"SS=z\cdot\sigma\cdot\sqrt{{L}}={z:.2f}\cdot{sigma:,.1f}\cdot\sqrt{{{lead:g}}}={ss:,.0f}"
    )
    st.latex(
        rf"ROP=\bar{{d}}\cdot L+SS={prom:,.1f}\cdot{lead:g}+{ss:,.0f}={rop:,.0f}"
    )
  with c2:
    m = st.columns(2)
    m[0].markdown(
        kpi("Inventario de seguridad", f"{ss:,.0f}", f"z = {z:.2f}"),
        unsafe_allow_html=True,
    )
    m[1].markdown(
        kpi("Punto de reorden", f"{rop:,.0f}", f"L = {lead:g} mes(es)"),
        unsafe_allow_html=True,
    )
    st.write("")
    m2 = st.columns(2)
    m2[0].markdown(
        kpi("Tendencia", f"{pend:+,.1f}", "unidades por mes"),
        unsafe_allow_html=True,
    )
    m2[1].markdown(
        kpi("σ estimada", f"{sigma:,.1f}", "por mes"), unsafe_allow_html=True
    )
    with st.popover("Supuestos y alcance", use_container_width=True):
      st.markdown(
          "- El intervalo del forecast se interpreta como IC 95 % y errores"
          " normales.\n- Demanda mensual y lead time constantes.\n- Es una"
          " aproximación para dimensionar; valida con tu política de"
          " inventario real."
      )

  titulo("Recomendaciones del agente", "cpu")
  if st.button("Generar recomendaciones", type="primary", icon=":material/auto_awesome:"):
    prompt_reco = (
        "Eres un analista de abasto y demanda. Con base en este forecast"
        f" mensual (CSV):\n\n{pdf.to_csv(index=False)}\nMétricas calculadas:"
        f" tendencia {pend:+.1f} u/mes, CV {cv:.1%}, sigma mensual ≈"
        f" {sigma:.1f}, nivel de servicio {nivel:.1%} (z={z:.2f}), lead time"
        f" {lead:g} meses, inventario de seguridad ≈ {ss:.0f}, punto de reorden"
        " ≈ {rop:.0f}.\nDa entre 4 y 5 recomendaciones accionables y concisas"
        " sobre compras/reorden, inventario de seguridad, estacionalidad,"
        " riesgo según el ancho del intervalo y meses críticos. Responde en"
        " español con viñetas."
    )
    with st.spinner("El agente está analizando el forecast..."):
      st.session_state["reco"] = responder([
          {"role": "user", "content": prompt_reco}
      ])
  if "reco" in st.session_state:
    with st.container(border=True):
      st.markdown(st.session_state["reco"])

  titulo("Chat con el agente", "chat")
  if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role": "assistant",
        "content": (
            "¡Hola! Soy tu asistente analítico. ¿Qué te gustaría saber sobre"
            " el forecast?"
        ),
    }]
  with st.popover(":material/lightbulb: Preguntas sugeridas"):
    for sug in [
        "¿Cuál es el mes con mayor demanda proyectada?",
        "¿Qué meses tienen mayor incertidumbre?",
        "¿Cómo cambia la demanda entre el primer y el último trimestre?",
        "¿Cuándo debería reordenar para cubrir el mes pico?",
    ]:
      if st.button(sug, key=sug, use_container_width=True):
        st.session_state["pending"] = sug

  for msg in st.session_state.messages:
    with st.chat_message(msg["role"], avatar=AVATARES[msg["role"]]):
      st.markdown(msg["content"])

  prompt = st.chat_input(
      "Ejemplo: ¿Cuál es el mes con mayor demanda proyectada?"
  ) or st.session_state.pop("pending", None)
  if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar=AVATARES["user"]):
      st.markdown(prompt)
    with st.chat_message("assistant", avatar=AVATARES["assistant"]):
      with st.spinner("Analizando datos..."):
        respuesta = responder(st.session_state.messages)
      st.markdown(respuesta)
    st.session_state.messages.append(
        {"role": "assistant", "content": respuesta}
    )


# ------------------------------------------------------------------ NAVEGACIÓN PRINCIPAL POR TABS (EN VEZ DE SIDEBAR)
st.markdown("## Agentes de IA como herramientas para la toma de decisiones")

# Creamos las pestañas en la parte superior central
tab1, tab2, tab3 = st.tabs([
    "📖 1. Historia: IA, ML y DL",
    "⚡ 2. LLMs, Transformers y RAG",
    "📈 3. Caso práctico: Forecast + Agente",
])

with tab1:
  seccion_historia()

with tab2:
  seccion_llm()

with tab3:
  seccion_practica()

pie_de_pagina()