
import os
import unicodedata
import html
from datetime import date, datetime, timedelta

import requests
import streamlit as st
from dotenv import load_dotenv

# ==========================================
# CONFIGURACIÓN
# ==========================================

load_dotenv()

API_KEY = os.getenv("API_FOOTBALL_KEY")
BASE_URL = "https://v3.football.api-sports.io"

st.set_page_config(
    page_title="FutbolSpleef",
    page_icon="🍆",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# DISEÑO
# ==========================================

st.markdown("""
<style>
.stApp {
    background: #0b1711;
    color: #e8eee9;
}

header[data-testid="stHeader"] {
    background: #0b1711;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

section[data-testid="stSidebar"] {
    background: #102219;
    border-right: 1px solid #294632;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: #edf3ed !important;
}

h1, h2, h3, h4 {
    color: #edf3ed !important;
    letter-spacing: -0.4px;
}

p, label, span {
    color: #c2d0c5;
}

[data-testid="stCaptionContainer"] p {
    color: #84998a;
}

/* ENCABEZADO */

.hero {
    background: linear-gradient(110deg, #193b29, #102319);
    border: 1px solid #426344;
    border-radius: 14px;
    padding: 25px 28px;
    margin-bottom: 24px;
}

.hero-label {
    color: #c5a65a;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.hero-title {
    color: #d8b75d;
    font-size: 30px;
    font-weight: 750;
    margin: 0;
}

.hero-subtitle {
    color: #b4c6b8;
    font-size: 14px;
    margin-top: 7px;
}

/* TARJETAS DE PARTIDOS */

div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #14271c;
    border: 1px solid #31533a !important;
    border-radius: 12px !important;
    transition: border-color 0.15s ease;
}

div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    border-color: #b99a4e !important;
}

.match-league {
    color: #d1b66d;
    font-size: 12px;
    font-weight: 650;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    padding-bottom: 12px;
    border-bottom: 1px solid #294432;
    margin-bottom: 15px;
}

.team-name {
    color: #edf3ed;
    font-size: 15px;
    font-weight: 650;
    line-height: 1.3;
    margin-top: 7px;
}

.team-role {
    color: #819989;
    font-size: 10px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.score {
    color: #d8b75d;
    font-size: 29px;
    font-weight: 750;
    text-align: center;
    letter-spacing: 1px;
    padding-top: 8px;
}

.score-label {
    color: #819989;
    font-size: 10px;
    text-align: center;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.match-footer {
    border-top: 1px solid #294432;
    margin-top: 15px;
    padding-top: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 10px;
}

.status {
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.4px;
    text-transform: uppercase;
}

.status-live {
    color: #ed7777;
}

.status-finished {
    color: #91a596;
}

.status-scheduled {
    color: #d8b75d;
}

.status-other {
    color: #d5a96c;
}

.match-time {
    color: #b6c7ba;
    font-size: 12px;
    font-weight: 600;
}

/* MÉTRICAS */

div[data-testid="stMetric"] {
    background: #14271c;
    border: 1px solid #31533a;
    border-radius: 10px;
    padding: 14px 16px;
}

div[data-testid="stMetricLabel"] {
    color: #a5b8a9;
}

div[data-testid="stMetricValue"] {
    color: #edf3ed;
    font-size: 22px;
}

/* BOTONES */

.stButton button {
    background: #1c3826;
    color: #e6eee7;
    border: 1px solid #45664b;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.15s ease;
}

.stButton button:hover {
    background: #294b33;
    border-color: #c5a65a;
    color: white;
}

/* SELECTORES */

div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    background: #14271c;
    border-color: #45664b;
}

/* SEPARADORES */

hr {
    border-color: #263345;
}

/* COMPETICIONES */

.competition-card {
    background: #14271c;
    border: 1px solid #31533a;
    border-radius: 10px;
    padding: 18px;
    min-height: 145px;
}

.competition-title {
    color: #d8b75d;
    font-size: 15px;
    font-weight: 700;
    margin-bottom: 12px;
}

.competition-item {
    color: #b4c6b8;
    font-size: 13px;
    margin: 6px 0;
}

/* PIE */

.footer {
    color: #84998a;
    font-size: 11px;
    text-align: center;
    padding: 18px 0;
}
</style>
""", unsafe_allow_html=True)


# ==========================================
# FUNCIONES
# ==========================================

@st.cache_data(ttl=300, show_spinner=False)
def obtener_partidos(fecha_seleccionada):

    if not API_KEY:
        raise ValueError(
            "No se encontró API_FOOTBALL_KEY en el archivo .env."
        )

    respuesta = requests.get(
        f"{BASE_URL}/fixtures",
        headers={"x-apisports-key": API_KEY},
        params={
            "date": fecha_seleccionada,
            "timezone": "America/Argentina/Buenos_Aires"
        },
        timeout=25
    )

    respuesta.raise_for_status()
    datos = respuesta.json()

    errores = datos.get("errors")

    if errores:
        raise RuntimeError(str(errores))

    return datos.get("response", [])


def normalizar(texto):

    texto = str(texto or "").lower()
    texto = unicodedata.normalize("NFD", texto)

    texto = "".join(
        c for c in texto
        if unicodedata.category(c) != "Mn"
    )

    return texto.strip()


def pertenece_a_competicion(nombre, seleccion):

    nombre = normalizar(nombre)

    equivalencias = {
        "Liga Profesional Argentina": [
            "liga profesional argentina",
            "primera division argentina"
        ],
        "Copa Libertadores": ["libertadores"],
        "Copa Sudamericana": ["sudamericana"],
        "Premier League": ["premier league"],
        "LaLiga": ["la liga", "laliga"],
        "Serie A": ["serie a"],
        "Bundesliga": ["bundesliga"],
        "Ligue 1": ["ligue 1"],
        "Champions League": [
            "uefa champions league",
            "champions league"
        ],
        "Europa League": [
            "uefa europa league",
            "europa league"
        ],
        "Conference League": [
            "uefa conference league",
            "conference league"
        ],
        "Mundial": ["world cup", "fifa world cup"],
        "Copa Argentina": ["copa argentina"]
    }

    opciones = equivalencias.get(
        seleccion,
        [normalizar(seleccion)]
    )

    return any(opcion in nombre for opcion in opciones)


def informacion_estado(codigo):

    codigo = str(codigo or "").upper()

    estados = {
        "NS": ("Programado", "scheduled"),
        "TBD": ("Horario por confirmar", "scheduled"),
        "1H": ("En vivo · Primer tiempo", "live"),
        "HT": ("Entretiempo", "live"),
        "2H": ("En vivo · Segundo tiempo", "live"),
        "ET": ("Tiempo extra", "live"),
        "BT": ("Descanso extra", "live"),
        "P": ("Penales en curso", "live"),
        "LIVE": ("En vivo", "live"),
        "INT": ("Interrumpido", "other"),
        "FT": ("Finalizado", "finished"),
        "AET": ("Finalizado · Tiempo extra", "finished"),
        "PEN": ("Finalizado · Penales", "finished"),
        "PST": ("Aplazado", "other"),
        "CANC": ("Cancelado", "other"),
        "ABD": ("Abandonado", "other"),
        "AWD": ("Victoria administrativa", "finished"),
        "WO": ("Walkover", "finished")
    }

    return estados.get(
        codigo,
        (codigo or "Desconocido", "other")
    )


def es_en_vivo(codigo):

    return codigo in [
        "1H", "HT", "2H", "ET", "BT", "P", "LIVE", "INT"
    ]


def es_finalizado(codigo):

    return codigo in ["FT", "AET", "PEN", "AWD", "WO"]


def es_programado(codigo):

    return codigo in ["NS", "TBD"]


# ==========================================
# TARJETA DE PARTIDO
# ==========================================

def mostrar_partido(partido):

    fixture = partido.get("fixture", {})
    liga = partido.get("league", {})
    equipos = partido.get("teams", {})
    goles = partido.get("goals", {})

    local = equipos.get("home", {})
    visitante = equipos.get("away", {})

    codigo = fixture.get("status", {}).get("short", "")

    estado_texto, tipo_estado = informacion_estado(codigo)

    fecha_partido = fixture.get("date", "")

    try:
        hora = datetime.fromisoformat(
            fecha_partido.replace("Z", "+00:00")
        ).strftime("%H:%M")
    except (ValueError, TypeError):
        hora = "--:--"

    marcador_local = goles.get("home")
    marcador_visitante = goles.get("away")

    if marcador_local is None:
        marcador_local = "-"

    if marcador_visitante is None:
        marcador_visitante = "-"

    nombre_liga = html.escape(
        str(liga.get("name", "Competición"))
    )

    pais_liga = html.escape(
        str(liga.get("country", ""))
    )

    nombre_local = html.escape(
        str(local.get("name", "Local"))
    )

    nombre_visitante = html.escape(
        str(visitante.get("name", "Visitante"))
    )

    estadio = fixture.get("venue", {}).get("name")

    if estadio:
        estadio = html.escape(str(estadio))

    with st.container(border=True):

        st.markdown(
            f"""
            <div class="match-league">
                {nombre_liga} · {pais_liga}
            </div>
            """,
            unsafe_allow_html=True
        )

        col_local, col_marcador, col_visitante = st.columns(
            [2.7, 1.3, 2.7],
            vertical_alignment="center"
        )

        with col_local:

            if local.get("logo"):
                st.image(local["logo"], width=48)

            st.markdown(
                f"""
                <div class="team-role">Local</div>
                <div class="team-name">{nombre_local}</div>
                """,
                unsafe_allow_html=True
            )

        with col_marcador:

            st.markdown(
                f"""
                <div class="score">
                    {marcador_local} - {marcador_visitante}
                </div>
                <div class="score-label">Marcador</div>
                """,
                unsafe_allow_html=True
            )

        with col_visitante:

            if visitante.get("logo"):
                st.image(visitante["logo"], width=48)

            st.markdown(
                f"""
                <div class="team-role">Visitante</div>
                <div class="team-name">{nombre_visitante}</div>
                """,
                unsafe_allow_html=True
            )

        st.markdown(
            f"""
            <div class="match-footer">
                <span class="status status-{tipo_estado}">
                    {estado_texto}
                </span>
                <span class="match-time">{hora} hs</span>
            </div>
            """,
            unsafe_allow_html=True
        )

        if estadio:
            st.caption(f"Estadio: {estadio}")


# ==========================================
# COMPETICIONES
# ==========================================

COMPETICIONES = [
    "Todas",
    "Liga Profesional Argentina",
    "Copa Argentina",
    "Copa Libertadores",
    "Copa Sudamericana",
    "Premier League",
    "LaLiga",
    "Serie A",
    "Bundesliga",
    "Ligue 1",
    "Champions League",
    "Europa League",
    "Conference League",
    "Mundial"
]


# ==========================================
# ESTADO DE FECHA
# ==========================================

if "fecha_actual" not in st.session_state:
    st.session_state.fecha_actual = date.today()


# ==========================================
# BARRA LATERAL
# ==========================================

st.sidebar.markdown("## 🍆 FutbolSpleef")
st.sidebar.caption("CENTRO DE PARTIDOS Y RESULTADOS")
st.sidebar.divider()

st.sidebar.markdown("### Filtros")

competicion = st.sidebar.selectbox(
    "Competición",
    COMPETICIONES
)

estado = st.sidebar.selectbox(
    "Estado del encuentro",
    ["Todos", "Programados", "En vivo", "Finalizados"]
)

fecha = st.sidebar.date_input(
    "Fecha",
    value=st.session_state.fecha_actual
)

st.session_state.fecha_actual = fecha

if st.sidebar.button(
    "Actualizar partidos",
    use_container_width=True
):
    obtener_partidos.clear()
    st.rerun()

st.sidebar.divider()
st.sidebar.caption("FutbolSpleef v1.0")
st.sidebar.caption("Fuente de datos: API-Football")


# ==========================================
# ENCABEZADO PRINCIPAL
# ==========================================

# st.html interpreta el contenido como HTML.
# Así evitamos que aparezcan las etiquetas como texto.

st.html("""
<div class="hero">
    <div class="hero-label">FOOTBALL MATCH CENTER</div>
    <div class="hero-title">🍆 FutbolSpleef</div>
    <div class="hero-subtitle">
        Calendario, horarios y resultados de las principales
        competiciones de fútbol.
    </div>
</div>
""")


# ==========================================
# RESUMEN
# ==========================================

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(
        "Fecha seleccionada",
        fecha.strftime("%d/%m/%Y")
    )

with col2:

    st.metric("Competición", competicion)

with col3:

    st.metric("Estado", estado)

st.divider()


# ==========================================
# NAVEGACIÓN DE FECHAS
# ==========================================

st.subheader("Calendario")

col_anterior, col_fecha, col_siguiente = st.columns(
    [1, 2, 1]
)

with col_anterior:

    if st.button(
        "← Día anterior",
        use_container_width=True
    ):

        st.session_state.fecha_actual = fecha - timedelta(days=1)
        st.rerun()

with col_fecha:

    st.markdown(
        f"""
        <h3 style="text-align:center; margin-top:5px;">
            {fecha.strftime("%d de %B de %Y")}
        </h3>
        """,
        unsafe_allow_html=True
    )

with col_siguiente:

    if st.button(
        "Día siguiente →",
        use_container_width=True
    ):

        st.session_state.fecha_actual = fecha + timedelta(days=1)
        st.rerun()


# ==========================================
# PARTIDOS DEL DÍA
# ==========================================

st.divider()

st.subheader("Partidos del día")

st.caption(
    f"Encuentros del {fecha.strftime('%d/%m/%Y')}"
)

fecha_api = fecha.strftime("%Y-%m-%d")

try:

    with st.spinner("Consultando encuentros..."):
        partidos = obtener_partidos(fecha_api)

    if not partidos:

        st.info(
            "No se encontraron partidos para esta fecha."
        )

    else:

        partidos_filtrados = []

        for partido in partidos:

            liga = partido.get("league", {})

            codigo = (
                partido.get("fixture", {})
                .get("status", {})
                .get("short", "")
            )

            if competicion != "Todas":

                if not pertenece_a_competicion(
                    liga.get("name", ""),
                    competicion
                ):
                    continue

            if estado == "Programados" and not es_programado(codigo):
                continue

            if estado == "En vivo" and not es_en_vivo(codigo):
                continue

            if estado == "Finalizados" and not es_finalizado(codigo):
                continue

            partidos_filtrados.append(partido)

        st.metric(
            "Encuentros encontrados",
            len(partidos_filtrados)
        )

        if not partidos_filtrados:

            st.info(
                "No hay encuentros que coincidan con los filtros."
            )

        else:

            for partido in partidos_filtrados:
                mostrar_partido(partido)


except requests.exceptions.HTTPError as error:

    codigo_http = (
        error.response.status_code
        if error.response else "desconocido"
    )

    st.error(
        f"API-Football devolvió un error HTTP {codigo_http}."
    )

    if codigo_http == 401:

        st.warning("La API rechazó la clave de acceso.")

    elif codigo_http == 403:

        st.warning(
            "Tu plan no permite acceder a este recurso "
            "o fecha solicitada."
        )

    elif codigo_http == 429:

        st.warning(
            "Se alcanzó el límite de solicitudes de la API."
        )


except requests.exceptions.Timeout:

    st.error(
        "La API tardó demasiado en responder. "
        "Intentá nuevamente."
    )


except requests.exceptions.RequestException:

    st.error(
        "No se pudo conectar con API-Football. "
        "Revisá tu conexión."
    )


except (ValueError, RuntimeError) as error:

    mensaje = str(error)

    if "Free plans do not have access to this date" in mensaje:

        st.warning(
            "Tu plan gratuito de API-Football no permite "
            "consultar esa fecha. Revisá el rango habilitado "
            "por tu suscripción."
        )

    else:

        st.error(mensaje)


except Exception as error:

    st.error(f"Se produjo un error inesperado: {error}")


# ==========================================
# COMPETICIONES DESTACADAS
# ==========================================

st.divider()
st.subheader("Competiciones destacadas")

col1, col2, col3 = st.columns(3)

with col1:

    st.markdown("""
    <div class="competition-card">
        <div class="competition-title">Argentina</div>
        <div class="competition-item">Liga Profesional</div>
        <div class="competition-item">Copa Argentina</div>
    </div>
    """, unsafe_allow_html=True)

with col2:

    st.markdown("""
    <div class="competition-card">
        <div class="competition-title">Europa</div>
        <div class="competition-item">Champions League</div>
        <div class="competition-item">Europa League</div>
        <div class="competition-item">Conference League</div>
    </div>
    """, unsafe_allow_html=True)

with col3:

    st.markdown("""
    <div class="competition-card">
        <div class="competition-title">Internacional</div>
        <div class="competition-item">Copa Libertadores</div>
        <div class="competition-item">Copa Sudamericana</div>
        <div class="competition-item">Mundial</div>
    </div>
    """, unsafe_allow_html=True)


# ==========================================
# PIE DE PÁGINA
# ==========================================

st.divider()

st.markdown(
    """
    <div class="footer">
        🍆 FUTBOLSPLEEF · CALENDARIO Y RESULTADOS DE FÚTBOL
    </div>
    """,
    unsafe_allow_html=True
)
