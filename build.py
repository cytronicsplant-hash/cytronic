"""Genera las páginas del sitio de Cytronics Plant.

Uso:  python build.py
Edita los textos aquí (SERVICIOS, PROYECTOS, etc.) y vuelve a ejecutar; se
regeneran index.html y las páginas de servicios/. No edites esos HTML a mano.
"""
from pathlib import Path
from html import escape
from urllib.parse import quote

ROOT = Path(__file__).parent
TELEFONO = "0960071515"
TEL_INTL = "593960071515"
CORREO = "cytronicsplant@gmail.com"
# Formulario: FormSubmit reenvía cada envío al correo. El primer envío llega
# con un enlace de activación que hay que aprobar una sola vez desde ese correo.
FORM_ENDPOINT = f"https://formsubmit.co/ajax/{CORREO}"
WA_URL = f"https://wa.me/{TEL_INTL}"

# ---------------------------------------------------------------- íconos
ICONOS = {
    "asistencia": '<path d="M14.7 6.3a4 4 0 0 0-5.4 5.2L3 17.8V21h3.2l6.3-6.3a4 4 0 0 0 5.2-5.4l-2.6 2.6-2.8-.6-.6-2.8z"/>',
    "diseno": '<rect x="3" y="3" width="18" height="18" rx="1.5"/><path d="M3 9h18M9 9v12M13 13h4M13 17h4"/>',
    "automatizacion": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="8" y="8" width="8" height="8"/><path d="M8 1v3M12 1v3M16 1v3M8 20v3M12 20v3M16 20v3M1 8h3M1 12h3M1 16h3M20 8h3M20 12h3M20 16h3"/>',
    "ia": '<circle cx="12" cy="12" r="3"/><path d="M12 2v4M12 18v4M2 12h4M18 12h4M5 5l2.8 2.8M16.2 16.2 19 19M5 19l2.8-2.8M16.2 7.8 19 5"/>',
    "formacion": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c0 1.7 2.7 3 6 3s6-1.3 6-3v-5M22 9v6"/>',
    "servomotores": '<circle cx="12" cy="12" r="3.2"/><path d="M12 2.5v3M12 18.5v3M2.5 12h3M18.5 12h3M5.3 5.3l2.1 2.1M16.6 16.6l2.1 2.1M5.3 18.7l2.1-2.1M16.6 7.4l2.1-2.1"/><circle cx="12" cy="12" r="7"/>',
    "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
    "flecha": '<path d="M5 12h14M13 6l6 6-6 6"/>',
}


def icono(nombre, clase="icon"):
    return (f'<svg class="{clase}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
            f'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
            f'{ICONOS[nombre]}</svg>')


WA_SVG = ('<svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><path fill="currentColor" d="M16 3C8.8 3 3 8.7 3 15.8c0 2.5.7 4.9 2 7L3 29l6.4-2c2 1.1 4.3 1.7 6.6 1.7 7.2 0 13-5.7 13-12.8S23.2 3 16 3zm0 23.4c-2.1 0-4.1-.6-5.9-1.7l-.4-.3-3.8 1.2 1.2-3.7-.3-.4c-1.2-1.8-1.9-3.9-1.9-6.1C4.9 9.8 9.9 5 16 5s11.1 4.8 11.1 10.8S22.1 26.4 16 26.4zm6.1-8c-.3-.2-2-1-2.3-1.1-.3-.1-.5-.2-.8.2-.2.3-.9 1.1-1.1 1.3-.2.2-.4.3-.7.1-.3-.2-1.4-.5-2.7-1.7-1-.9-1.7-2-1.9-2.3-.2-.3 0-.5.1-.7l.5-.6c.2-.2.2-.3.3-.6.1-.2 0-.4 0-.6l-1-2.5c-.3-.7-.6-.6-.8-.6h-.7c-.2 0-.6.1-.9.4-.3.3-1.2 1.2-1.2 2.9s1.2 3.3 1.4 3.6c.2.2 2.4 3.7 5.9 5.1 2.9 1.1 3.5.9 4.1.9.6-.1 2-.8 2.3-1.6.3-.8.3-1.5.2-1.6-.1-.2-.3-.3-.7-.5z"/></svg>')

# ---------------------------------------------------------------- datos
PROYECTOS = {
    "hospital": {
        "cliente": "Hospital San Francisco", "color": "blue",
        "titulo": "Sistema de bombeo de agua automatizado",
        "texto": "Arquitectura maestro-esclavo con dos HMI Delta, interfaz con modo manual/automático, niveles de usuario e historial.",
    },
    "disetec": {
        "cliente": "Disetec", "color": "green",
        "titulo": "Instalación fotovoltaica de 32 paneles",
        "texto": "Montaje, conexión y mantenimiento del sistema solar, dentro de nuestra línea de energía fotovoltaica, almacenamiento y domótica.",
    },
    "bancario": {
        "cliente": "Sector bancario", "color": "blue",
        "titulo": "Monitoreo remoto de combustible en generadores",
        "texto": "Mantenimiento eléctrico en 60 localidades, con diagnóstico de fallas y gestión presupuestaria.",
        "dato": ("35%", "menos tiempo de respuesta ante fallas tras implementar el monitoreo remoto."),
    },
    "robotica": {
        "cliente": "Robótica y control", "color": "green",
        "titulo": "Teleoperación robótica y control de temperatura",
        "texto": "Brazos robóticos teleoperados (ESP32, Raspberry Pi, interfaz Python) y control maestro-esclavo con PLC/HMI Delta y variador.",
    },
}

SERVICIOS = [
    {
        "slug": "asistencia-tecnica", "icono": "asistencia", "img": "area1.jpg",
        "titulo": "Asistencia técnica",
        "corto": "Mantenimiento preventivo y correctivo eléctrico y electrónico. Diagnóstico especializado y soporte en campo.",
        "lead": "Mantenimiento preventivo y correctivo eléctrico y electrónico en equipos e instalaciones industriales, con diagnóstico especializado y soporte en campo para asegurar la continuidad operativa.",
        "incluye": [
            ("Mantenimiento preventivo", "Planes de revisión periódica para anticipar fallas y evitar paradas no programadas."),
            ("Mantenimiento correctivo", "Reparación de fallas eléctricas y electrónicas en equipos e instalaciones."),
            ("Diagnóstico especializado", "Identificamos la causa raíz de la falla antes de intervenir."),
            ("Soporte en campo", "Técnicos en su planta o instalación, donde está el problema."),
            ("Repotenciación de equipos", "Actualización de equipos existentes para extender su vida útil sin reemplazarlos."),
            ("Gestión presupuestaria", "Planificación de trabajos y costos en instalaciones con varias localidades."),
        ],
        "aplicaciones": ["Tableros y circuitos eléctricos", "Generadores y sistemas de respaldo", "Equipos de seguridad", "Instalaciones industriales y comerciales"],
        "tecnologias": ["Instalaciones eléctricas industriales", "Electrónica de potencia y control", "Generadores", "Tableros eléctricos"],
        "proyecto": "bancario",
        "dato_extra": ("45%", "de ahorro en la repotenciación de equipos de seguridad, extendiendo su vida útil 3 años."),
    },
    {
        "slug": "diseno-fabricacion", "icono": "diseno", "img": "area2.jpg",
        "titulo": "Diseño y fabricación",
        "corto": "Tableros eléctricos, máquinas y equipos industriales a medida, con normativas de seguridad.",
        "lead": "Diseño, ingeniería y fabricación de tableros eléctricos, máquinas y equipos industriales a medida, cumpliendo normativas de seguridad y estándares internacionales.",
        "incluye": [
            ("Ingeniería y diseño", "Definimos la solución según su proceso, espacio y requerimientos técnicos."),
            ("Tableros eléctricos", "Fabricación de tableros de control y distribución."),
            ("Máquinas y equipos a medida", "Equipos diseñados para una necesidad específica de su planta."),
            ("Montaje y conexión", "Instalación y cableado en sitio."),
            ("Pruebas y puesta en marcha", "Verificamos el funcionamiento antes de entregar."),
            ("Energía fotovoltaica", "Sistemas solares, almacenamiento y domótica."),
        ],
        "aplicaciones": ["Tableros de control y distribución", "Máquinas especiales", "Sistemas fotovoltaicos", "Equipos de prueba"],
        "tecnologias": ["Normativas de seguridad eléctrica", "Paneles solares y almacenamiento", "Domótica", "Impresión 3D para prototipos"],
        "proyecto": "disetec",
    },
    {
        "slug": "automatizacion-procesos", "icono": "automatizacion", "img": "hero.jpg",
        "titulo": "Automatización de procesos",
        "corto": "Programación de PLC, HMI, variadores y SCADA para optimizar y controlar sus procesos.",
        "lead": "Programación de PLC, HMI, variadores y sistemas SCADA. Integramos hardware y software para optimizar y controlar procesos industriales.",
        "incluye": [
            ("Programación de PLC", "Lógica de control para procesos nuevos o existentes."),
            ("Interfaces HMI", "Pantallas de operación con modo manual/automático, niveles de usuario e historial."),
            ("Variadores de frecuencia", "Configuración y control de motores."),
            ("Sistemas SCADA", "Supervisión y control centralizado del proceso."),
            ("Arquitecturas maestro-esclavo", "Varios controladores trabajando coordinados."),
            ("Integración hardware-software", "Conectamos equipos de distintas marcas en un solo sistema."),
        ],
        "aplicaciones": ["Sistemas de bombeo", "Control de temperatura", "Líneas de producción", "Supervisión de procesos"],
        "tecnologias": ["PLC y HMI Delta", "PLC Siemens", "Variadores de frecuencia", "SCADA"],
        "proyecto": "hospital",
    },
    {
        "slug": "ia-industria-40", "icono": "ia", "img": "area3.jpg",
        "titulo": "Inteligencia artificial e Industria 4.0",
        "corto": "IA, análisis de datos, visión artificial, IoT y gemelos digitales. Datos convertidos en decisiones.",
        "lead": "Implementación de soluciones con IA, análisis de datos, visión artificial, IoT y gemelos digitales. Transformamos datos en decisiones inteligentes.",
        "incluye": [
            ("Análisis de datos", "Convertimos los datos de su proceso en indicadores útiles."),
            ("Visión artificial", "Inspección y reconocimiento con cámaras e IA."),
            ("IoT y monitoreo remoto", "Sensores conectados para ver su proceso desde cualquier lugar."),
            ("Gemelos digitales", "Modelos virtuales para simular y optimizar procesos."),
            ("Robótica y teleoperación", "Control remoto de brazos robóticos."),
            ("Adquisición de datos", "Sistemas embebidos para registrar variables en tiempo real."),
        ],
        "aplicaciones": ["Monitoreo remoto de equipos", "Inspección de calidad", "Robótica", "Mantenimiento predictivo"],
        "tecnologias": ["Python", "ESP32", "Raspberry Pi", "IoT", "Visión artificial"],
        "proyecto": "robotica",
    },
    {
        "slug": "formacion-docencia", "icono": "formacion", "img": None,
        "titulo": "Formación y docencia",
        "corto": "Docencia universitaria, mentorías y capacitaciones en automatización, robótica, control e IA.",
        "lead": "Docencia universitaria, mentorías y capacitaciones especializadas en automatización, robótica, control industrial e inteligencia artificial.",
        "incluye": [
            ("Capacitaciones para empresas", "Formación práctica para el personal técnico de su planta."),
            ("Cursos de automatización", "PLC, HMI, variadores y control industrial."),
            ("Robótica", "Desde fundamentos hasta aplicaciones industriales."),
            ("Inteligencia artificial", "Aplicaciones de IA y datos en procesos productivos."),
            ("Mentorías", "Acompañamiento en proyectos técnicos y de titulación."),
            ("Docencia universitaria", "Experiencia como docentes e investigadores en educación superior."),
        ],
        "aplicaciones": ["Personal de mantenimiento", "Operadores de planta", "Estudiantes técnicos", "Equipos de ingeniería"],
        "tecnologias": ["Automatización industrial", "Robótica", "Control industrial", "Inteligencia artificial"],
        "proyecto": None,
    },
    {
        "slug": "mantenimiento-servomotores", "icono": "servomotores", "img": None,
        "titulo": "Mantenimiento de servomotores industriales",
        "corto": "Diagnóstico, reparación y mantenimiento de servomotores y servodrives, hasta la puesta en marcha.",
        "lead": "Diagnóstico, reparación y mantenimiento preventivo y correctivo de servomotores y servodrives, desde las pruebas iniciales hasta la puesta en marcha.",
        "incluye": [
            ("Diagnóstico", "Evaluación del servomotor y el servodrive para ubicar la falla."),
            ("Pruebas de aislamiento y encoder", "Verificación del estado eléctrico y de la retroalimentación."),
            ("Cambio de rodamientos y retenes", "Reemplazo de componentes mecánicos desgastados."),
            ("Parametrización", "Configuración del servodrive según la aplicación."),
            ("Ajuste de lazos de control", "Sintonía para un movimiento preciso y estable."),
            ("Puesta en marcha", "Pruebas finales con el equipo instalado."),
        ],
        "aplicaciones": ["Máquinas CNC", "Robots industriales", "Líneas de empaque", "Ejes de posicionamiento"],
        "tecnologias": ["Servomotores", "Servodrives", "Encoders", "Control de movimiento"],
        "proyecto": None,
    },
]

PASOS = [
    ("Visita técnica sin costo", "Evaluamos su instalación en sitio."),
    ("Diagnóstico", "Identificamos oportunidades de mejora y riesgos."),
    ("Propuesta a medida", "Alcance, tiempos y costos claros."),
    ("Ejecución y soporte", "Implementamos y damos continuidad operativa."),
]

# ---------------------------------------------------------------- partes comunes


def head(titulo, descripcion, r):
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{escape(titulo)}</title>
  <meta name="description" content="{escape(descripcion)}">
  <meta name="theme-color" content="#0a1442">
  <meta property="og:title" content="{escape(titulo)}">
  <meta property="og:description" content="{escape(descripcion)}">
  <meta property="og:image" content="{r}img/hero.jpg">
  <meta property="og:type" content="website">
  <link rel="icon" href="{r}img/favicon.png" type="image/png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Inter+Tight:wght@600;700&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{r}styles.css">
</head>
<body>
"""


def header(r, activo=None):
    inicio = f"{r}index.html"
    sub = "\n".join(
        f'            <a href="{r}servicios/{s["slug"]}.html"{" aria-current=\"page\"" if activo == s["slug"] else ""}>'
        f'{icono(s["icono"], "icon icon--sm")}<span>{s["titulo"]}</span></a>'
        for s in SERVICIOS)
    return f"""
  <a class="skip" href="#main">Saltar al contenido</a>
  <header class="header">
    <div class="container header__inner">
      <a href="{inicio}" class="header__logo" aria-label="Cytronics Plant, inicio">
        <img src="{r}img/logo.png" alt="Cytronics Plant" width="1200" height="226">
      </a>
      <button class="nav-toggle" aria-expanded="false" aria-controls="nav" aria-label="Abrir menú">
        <span></span><span></span><span></span>
      </button>
      <nav class="nav" id="nav">
        <a href="{inicio}#nosotros">Nosotros</a>
        <div class="nav__group">
          <a href="{inicio}#servicios" class="nav__parent{" is-current" if activo else ""}">Servicios
            <svg class="nav__caret" viewBox="0 0 12 12" aria-hidden="true"><path d="M3 4.5l3 3 3-3" fill="none" stroke="currentColor" stroke-width="1.6"/></svg>
          </a>
          <div class="nav__dropdown">
{sub}
          </div>
        </div>
        <a href="{inicio}#proyectos">Proyectos</a>
        <a href="{inicio}#valores">Valores</a>
        <a href="#contacto" class="btn btn--primary btn--sm">Contáctenos</a>
      </nav>
    </div>
  </header>
"""


def formulario(r, servicio=None):
    opciones = "\n".join(
        f'              <option{" selected" if servicio == s["titulo"] else ""}>{s["titulo"]}</option>'
        for s in SERVICIOS)
    asunto = f"Nueva solicitud web – {servicio}" if servicio else "Nueva solicitud desde la web"
    return f"""
    <section class="cta" id="contacto">
      <div class="cta__circle" aria-hidden="true"></div>
      <div class="container cta__inner">
        <div class="cta__intro">
          <span class="cta__bar" aria-hidden="true"></span>
          <h2>Construyamos juntos<br>la Industria 4.0</h2>
          <p class="cta__lead">Agende una visita técnica sin costo: evaluamos su instalación, identificamos oportunidades de mejora y le presentamos una propuesta a medida.</p>
          <ul class="contact-list">
            <li><a href="{WA_URL}?text=Hola%20Cytronics%20Plant%2C%20quisiera%20agendar%20una%20visita%20t%C3%A9cnica." target="_blank" rel="noopener">
              <span class="contact-list__label">WhatsApp</span><span class="contact-list__value">{TELEFONO}</span></a></li>
            <li><a href="mailto:{CORREO}">
              <span class="contact-list__label">Correo</span><span class="contact-list__value">{CORREO}</span></a></li>
            <li><a href="tel:+{TEL_INTL}">
              <span class="contact-list__label">Llamar</span><span class="contact-list__value">+593 96 007 1515</span></a></li>
            <li><span class="contact-list__label">Ubicación</span><span class="contact-list__value">Quito · Ecuador</span></li>
          </ul>
        </div>

        <form class="form" action="{FORM_ENDPOINT}" method="POST" data-form novalidate>
          <h3 class="form__title">Solicite información o una visita técnica</h3>
          <input type="hidden" name="_subject" value="{escape(asunto)}">
          <input type="hidden" name="_template" value="table">
          <input type="text" name="_honey" class="form__hp" tabindex="-1" autocomplete="off" aria-hidden="true">
          <div class="form__row">
            <label class="field"><span>Nombre *</span>
              <input type="text" name="nombre" autocomplete="name" required></label>
            <label class="field"><span>Empresa</span>
              <input type="text" name="empresa" autocomplete="organization"></label>
          </div>
          <div class="form__row">
            <label class="field"><span>Correo *</span>
              <input type="email" name="email" autocomplete="email" required></label>
            <label class="field"><span>Teléfono</span>
              <input type="tel" name="telefono" autocomplete="tel" inputmode="tel"></label>
          </div>
          <label class="field"><span>Servicio de interés</span>
            <select name="servicio">
              <option value="">Seleccione una opción</option>
{opciones}
              <option>Otro</option>
            </select></label>
          <label class="field"><span>Mensaje *</span>
            <textarea name="mensaje" rows="4" required placeholder="Cuéntenos brevemente qué necesita"></textarea></label>
          <button type="submit" class="btn btn--accent form__submit">Enviar solicitud</button>
          <p class="form__status" role="status" aria-live="polite"></p>
        </form>
      </div>
    </section>
"""


def footer(r):
    links = "\n".join(f'          <li><a href="{r}servicios/{s["slug"]}.html">{s["titulo"]}</a></li>' for s in SERVICIOS)
    return f"""
  <footer class="footer">
    <div class="container footer__grid">
      <div>
        <div class="footer__logo"><img src="{r}img/logo.png" alt="Cytronics Plant" loading="lazy" width="1200" height="226"></div>
        <p class="footer__about">Automatización, mantenimiento eléctrico y electrónico, diseño y fabricación de equipos industriales e integración de inteligencia artificial.</p>
      </div>
      <div>
        <h4>Servicios</h4>
        <ul>
{links}
        </ul>
      </div>
      <div>
        <h4>Contacto</h4>
        <ul>
          <li><a href="{WA_URL}" target="_blank" rel="noopener">WhatsApp {TELEFONO}</a></li>
          <li><a href="mailto:{CORREO}">{CORREO}</a></li>
          <li>Quito · Ecuador</li>
        </ul>
      </div>
    </div>
    <div class="container footer__bottom">
      <p>© <span data-year>2026</span> Cytronics Plant</p>
      <p class="footer__tag">Automatización · Integración · Inteligencia · Innovación</p>
    </div>
  </footer>

  <a class="wa-float" href="{WA_URL}?text=Hola%20Cytronics%20Plant%2C%20quisiera%20m%C3%A1s%20informaci%C3%B3n." target="_blank" rel="noopener" aria-label="Escribir por WhatsApp">
    {WA_SVG}
  </a>

  <script src="{r}script.js"></script>
</body>
</html>
"""


def circuito():
    """Línea con resistencia y nodo, como en el logo."""
    return """<svg class="circuit" viewBox="0 0 420 40" aria-hidden="true">
          <path class="circuit__line" d="M0 20H70l6-14 10 28 10-28 10 28 10-28 6 14H405"/>
          <circle class="circuit__node" cx="410" cy="20" r="6"/>
        </svg>"""


def proyecto_card(key, r):
    p = PROYECTOS[key]
    return f"""          <article class="project">
            <p class="project__client c-{p["color"]}">{p["cliente"]}</p>
            <h3>{p["titulo"]}</h3>
            <p>{p["texto"]}</p>
          </article>"""


# ---------------------------------------------------------------- inicio


def pagina_inicio():
    r = ""
    tarjetas = "\n".join(f"""          <a class="svc-card" href="servicios/{s["slug"]}.html">
            <span class="svc-card__num">{i:02d}</span>
            <span class="svc-card__icon">{icono(s["icono"])}</span>
            <h3>{s["titulo"]}</h3>
            <p>{s["corto"]}</p>
            <span class="svc-card__more">Ver servicio {icono("flecha", "icon icon--sm")}</span>
          </a>""" for i, s in enumerate(SERVICIOS, 1))
    proyectos = "\n".join(proyecto_card(k, r) for k in PROYECTOS)

    return head("Cytronics Plant | Automatización e Industria 4.0 en Quito",
                "Automatización, mantenimiento eléctrico y electrónico, diseño y fabricación de equipos industriales e integración de inteligencia artificial para procesos productivos. Quito, Ecuador.", r) \
        + header(r) + f"""
  <main id="main">

    <section class="hero">
      <div class="hero__bg" aria-hidden="true"></div>
      <div class="container hero__inner">
        <p class="eyebrow eyebrow--light anim" style="--d:0">Automatización · Integración · Inteligencia · Innovación</p>
        <h1 class="anim" style="--d:1">Su aliado estratégico<br>hacia la <span class="accent">Industria 4.0</span></h1>
        <div class="anim" style="--d:2">{circuito()}</div>
        <p class="hero__lead anim" style="--d:3">Automatización, mantenimiento eléctrico y electrónico, diseño y fabricación de equipos industriales e integración de inteligencia artificial para procesos productivos.</p>
        <div class="hero__actions anim" style="--d:4">
          <a href="#contacto" class="btn btn--accent">Agendar visita técnica</a>
          <a href="#servicios" class="btn btn--ghost">Ver servicios</a>
        </div>
      </div>
      <div class="hero__chips container anim" style="--d:5">
        <span>PLC · HMI · SCADA</span><span>Mantenimiento eléctrico</span><span>Visión artificial e IoT</span><span>Servomotores</span>
      </div>
    </section>

    <section class="section" id="nosotros">
      <div class="container">
        <div class="about">
          <div class="about__text">
            <p class="eyebrow">Quiénes somos</p>
            <h2>Experiencia técnica y visión académica en un mismo equipo</h2>
            <p class="lead">En Cytronics Plant brindamos soluciones integrales en automatización, mantenimiento eléctrico y electrónico, diseño y fabricación de equipos industriales, e integración de inteligencia artificial para llevar los procesos de nuestros clientes hacia la Industria 4.0.</p>
            <p>Combinamos experiencia técnica con tecnología avanzada para optimizar, conectar y hacer más inteligentes los sistemas productivos, aumentando la eficiencia, reduciendo costos y asegurando la continuidad operativa.</p>
            <p>Además de nuestro enfoque industrial, aportamos una visión académica y formativa: como docentes e investigadores, compartimos conocimiento, impulsamos el talento y formamos profesionales listos para la transformación digital.</p>
          </div>
          <figure class="about__img">
            <img src="img/area3.jpg" alt="Técnicos revisando brazos robóticos industriales" loading="lazy" width="612" height="407">
          </figure>
        </div>

        <div class="stats">
          <div class="stat"><strong class="c-blue"><span data-count="15" data-prefix="+">+15</span></strong><span>años de experiencia</span></div>
          <div class="stat"><strong class="c-green"><span data-count="6">6</span></strong><span>áreas de trabajo integradas</span></div>
          <div class="stat"><strong><span data-count="8">8</span></strong><span>ingenieros, tecnólogos y docentes</span></div>
        </div>

        <div class="mv">
          <article class="mv__card mv__card--dark">
            <p class="eyebrow eyebrow--mint">Misión</p>
            <p>Brindar soluciones integrales en automatización, mantenimiento eléctrico y electrónico, diseño y fabricación de equipos industriales, e integración de inteligencia artificial, combinando experiencia técnica y visión académica para ayudar a nuestros clientes a transformar sus procesos productivos hacia la Industria 4.0, generando eficiencia, continuidad operativa y valor sostenible.</p>
          </article>
          <article class="mv__card">
            <p class="eyebrow eyebrow--blue">Visión</p>
            <p>Ser el aliado estratégico líder en Ecuador para la transformación digital industrial, reconocidos por diseñar, implementar y mantener soluciones inteligentes en automatización e Industria 4.0 que generen valor real y sostenible, mientras formamos el talento técnico que impulsará la industria del futuro.</p>
          </article>
        </div>
      </div>
    </section>

    <section class="section section--muted" id="servicios">
      <div class="container">
        <div class="section__head">
          <div>
            <p class="eyebrow">Áreas de trabajo</p>
            <h2>Cómo generamos valor</h2>
          </div>
          <p class="section__sub">Seis áreas, un mismo objetivo: procesos más eficientes, conectados e inteligentes.</p>
        </div>
        <div class="svc-grid">
{tarjetas}
        </div>
      </div>
    </section>

    <section class="section" id="proyectos">
      <div class="container">
        <p class="eyebrow">Proyectos realizados</p>
        <h2>Trabajo entregado en campo</h2>
        <div class="projects">
{proyectos}
        </div>
        <div class="results">
          <div class="result">
            <strong class="c-blue"><span data-count="35" data-suffix="%">35%</span></strong>
            <span>menos tiempo de respuesta ante fallas tras implementar el monitoreo remoto de combustible.</span>
          </div>
          <div class="result">
            <strong class="c-green"><span data-count="45" data-suffix="%">45%</span></strong>
            <span>de ahorro en la repotenciación de equipos de seguridad, extendiendo su vida útil 3 años.</span>
          </div>
        </div>
      </div>
    </section>

    <section class="section section--muted" id="valores">
      <div class="container">
        <p class="eyebrow">Nuestros valores</p>
        <h2>Lo que nos guía en cada proyecto</h2>
        <div class="values">
          <div class="value value--navy"><h3>Soluciones a medida</h3><p>Cada cliente y cada proceso es distinto; diseñamos a su medida.</p></div>
          <div class="value value--blue"><h3>Tecnología inteligente</h3><p>Aplicamos automatización e IA con criterio técnico y resultados medibles.</p></div>
          <div class="value value--green"><h3>Compromiso y confianza</h3><p>Cumplimos lo que ofrecemos, con respaldo y continuidad operativa.</p></div>
          <div class="value value--navy"><h3>Experiencia y conocimiento</h3><p>Formación académica e industria de la mano en cada proyecto.</p></div>
        </div>
      </div>
    </section>
{formulario(r)}
  </main>
""" + footer(r)


# ---------------------------------------------------------------- servicio


def pagina_servicio(s):
    r = "../"
    bg = (f'<div class="page-hero__bg" style="background-image:url(\'{r}img/{s["img"]}\')" aria-hidden="true"></div>'
          if s["img"] else "")
    incluye = "\n".join(f"""          <div class="feature">
            <span class="feature__icon">{icono("check")}</span>
            <div><h3>{t}</h3><p>{d}</p></div>
          </div>""" for t, d in s["incluye"])
    apps = "\n".join(f"            <li>{a}</li>" for a in s["aplicaciones"])
    tecs = "\n".join(f"            <span>{t}</span>" for t in s["tecnologias"])
    pasos = "\n".join(f"""          <li class="step"><span class="step__num">{i}</span><h3>{t}</h3><p>{d}</p></li>"""
                      for i, (t, d) in enumerate(PASOS, 1))
    otros = "\n".join(f"""          <a class="mini-card" href="{o["slug"]}.html">{icono(o["icono"])}<span>{o["titulo"]}</span></a>"""
                      for o in SERVICIOS if o is not s)

    bloque_proyecto = ""
    if s["proyecto"] or s.get("dato_extra"):
        partes = []
        if s["proyecto"]:
            partes.append(proyecto_card(s["proyecto"], r))
        datos = []
        p = PROYECTOS.get(s["proyecto"]) if s["proyecto"] else None
        if p and p.get("dato"):
            datos.append(p["dato"])
        if s.get("dato_extra"):
            datos.append(s["dato_extra"])
        dato_html = "\n".join(f"""            <div class="result"><strong class="c-{"blue" if i == 0 else "green"}">{n}</strong><span>{t}</span></div>"""
                              for i, (n, t) in enumerate(datos))
        bloque_proyecto = f"""
    <section class="section">
      <div class="container">
        <p class="eyebrow">Experiencia en campo</p>
        <h2>Proyecto relacionado</h2>
        <div class="svc-project">
{"".join(partes)}
          <div class="results results--stack">
{dato_html}
          </div>
        </div>
      </div>
    </section>"""

    return head(f"{s['titulo']} | Cytronics Plant", s["lead"], r) + header(r, s["slug"]) + f"""
  <main id="main">

    <section class="page-hero{" page-hero--img" if s["img"] else ""}">
      {bg}
      <div class="container page-hero__inner">
        <nav class="crumbs anim" style="--d:0" aria-label="Ruta"><a href="{r}index.html">Inicio</a><span>/</span><a href="{r}index.html#servicios">Servicios</a><span>/</span><span aria-current="page">{s["titulo"]}</span></nav>
        <span class="page-hero__icon anim" style="--d:1">{icono(s["icono"])}</span>
        <h1 class="anim" style="--d:1">{s["titulo"]}</h1>
        <p class="page-hero__lead anim" style="--d:2">{s["lead"]}</p>
        <div class="hero__actions anim" style="--d:3">
          <a href="#contacto" class="btn btn--accent">Solicitar cotización</a>
          <a href="{WA_URL}?text={quote('Hola Cytronics Plant, quisiera información sobre ' + s['titulo'])}" target="_blank" rel="noopener" class="btn btn--ghost">Consultar por WhatsApp</a>
        </div>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <p class="eyebrow">Qué incluye</p>
        <h2>Alcance del servicio</h2>
        <div class="features">
{incluye}
        </div>
      </div>
    </section>

    <section class="section section--muted">
      <div class="container two-col">
        <div>
          <p class="eyebrow">Aplicaciones</p>
          <h2>Dónde lo aplicamos</h2>
          <ul class="checklist">
{apps}
          </ul>
        </div>
        <div>
          <p class="eyebrow">Tecnologías</p>
          <h2>Con qué trabajamos</h2>
          <div class="chips">
{tecs}
          </div>
        </div>
      </div>
    </section>
{bloque_proyecto}
    <section class="section section--muted">
      <div class="container">
        <p class="eyebrow">Cómo trabajamos</p>
        <h2>De la visita técnica a la puesta en marcha</h2>
        <ol class="steps">
{pasos}
        </ol>
      </div>
    </section>

    <section class="section">
      <div class="container">
        <p class="eyebrow">Otras áreas</p>
        <h2>Más servicios de Cytronics Plant</h2>
        <div class="mini-grid">
{otros}
        </div>
      </div>
    </section>
{formulario(r, s["titulo"])}
  </main>
""" + footer(r)


def main():
    (ROOT / "servicios").mkdir(exist_ok=True)
    (ROOT / "index.html").write_text(pagina_inicio(), encoding="utf-8")
    for s in SERVICIOS:
        (ROOT / "servicios" / f"{s['slug']}.html").write_text(pagina_servicio(s), encoding="utf-8")
    print(f"Generadas: index.html + {len(SERVICIOS)} páginas de servicios")


if __name__ == "__main__":
    main()
