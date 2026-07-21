"""
Script para REESCRIBIR el index.html de las 23 webs del lote 2 con
un template mejorado que incorpora todas las correcciones de la auditoría.
"""
import os
import re
import json

BASE = "/Users/beto/Library/CloudStorage/OneDrive-Personal(2)/Freelancer/clientes/web"

WEBS_LOTE2 = [
    "centro-bewusst-machen", "cercardio-especialidades-medicas",
    "clinica-dental-amsterdent", "clinica-dental-dentale",
    "clinica-dental-godiental", "clinica-dental-proboca",
    "clinica-dental-rehabilitarte", "clinica-fisioterapia-santillan",
    "clinica-medica-palmas-dra-yanina-rubio", "clinica-odontologica-dentalcenter",
    "dental-studio-mx", "ds-consultorio-dental",
    "fisioterapia-y-rehabilitacion-vertiz", "grupo-sonrie-mx",
    "kintsu-dental", "klinikdent-mexico",
    "odontologia-biologica-dra-yulianna-suarez", "podologia-fisioterapia-pies-alegres",
    "rehavilita-fisioterapia", "saludent-sas",
    "sca-clinica-de-fisioterapia", "seishi-centro-de-atencion-psicologica",
    "vitalmente-centro-medico-psicologia",
]

SCHEMA_MAP = {
    "Odontología": "Dentist", "Clínica Dental": "Dentist",
    "Ortodoncia": "Dentist", "Implantes": "Dentist",
    "Rehabilitación Oral": "Dentist",
    "Fisioterapia": "PhysicalTherapy", "Rehabilitación Física": "PhysicalTherapy",
    "Clínica Médica": "MedicalClinic", "Salud Mental": "MedicalClinic",
    "Terapia Integral": "MedicalClinic", "Psicología Clínica": "MedicalClinic",
    "Cardiología": "MedicalClinic", "Especialidades Médicas": "MedicalClinic",
    "Podología": "Podiatric", "Odontología Biológica": "Dentist",
}

ICONOS_POR_NICHO = {
    "dent": ["🦷", "😁", "🔬", "✨", "🩺", "💎"],
    "fisiot": ["👐", "🦴", "🏃", "🧘", "💆", "⚕️"],
    "psicol": ["💭", "🧠", "🌱", "💆", "🤝", "🕊️"],
    "medic": ["🩺", "💊", "🩻", "⚕️", "🔬", "🧬"],
    "podolog": ["🦶", "🩹", "👣", "🩺", "🧦", "✨"],
}

COPY_POR_SERVICIO = {
    "dent": {
        "default": "Procedimiento realizado con tecnología de última generación y materiales biocompatibles de la más alta calidad.",
    },
    "fisiot": {
        "default": "Tratamiento personalizado con técnicas manuales y tecnología de rehabilitación para acelerar tu recuperación.",
    },
    "psicol": {
        "default": "Acompañamiento profesional confidencial y humano, en un espacio seguro para tu bienestar emocional.",
    },
    "medic": {
        "default": "Atención médica integral con tecnología de diagnóstico moderna y un equipo humano cercano.",
    },
    "podolog": {
        "default": "Tratamiento especializado con instrumental profesional y técnicas avanzadas para el cuidado de tus pies.",
    },
}


def get_nicho_key(nicho):
    n = nicho.lower()
    if "odon" in n or "dent" in n: return "dent"
    if "fisiot" in n or "rehab" in n: return "fisiot"
    if "psicol" in n or "psic" in n: return "psicol"
    if "podol" in n: return "podolog"
    return "medic"


def get_schema_type(nicho):
    for key, val in SCHEMA_MAP.items():
        if key.lower() in nicho.lower():
            return val
    return "MedicalClinic"


def get_iconos(nicho):
    return ICONOS_POR_NICHO.get(get_nicho_key(nicho), ICONOS_POR_NICHO["medic"])


def generar_copy_servicio(servicio, nicho_key):
    """Genera copy específico para cada servicio."""
    s = servicio.lower()
    if nicho_key == "dent":
        if "diseño" in s or "sonrisa" in s: return "Diseño digital 3D de tu sonrisa antes de comenzar el tratamiento. Vemos juntos el resultado y lo planificamos con precisión milimétrica."
        if "ortodoncia" in s or "invisible" in s or "alineador" in s: return "Alineadores transparentes prácticamente invisibles. Corrige la posición de tus dientes sin brackets metálicos y con visitas menos frecuentes."
        if "implante" in s: return "Implantes de titanio biocompatible con corona inmediata en una sola sesión. Recupera la funcionalidad y estética de un diente natural en pocas horas."
        if "blanca" in s or "láser" in s: return "Blanqueamiento clínico con láser LED de alta potencia. Resultados visibles en una sola sesión de 45 minutos sin dañar el esmalte."
        if "endodon" in s: return "Tratamiento de conductos con tecnología rotatoria y microscopía dental. Salvamos tu diente eliminando el dolor en una o dos sesiones."
        if "limpieza" in s or "profilaxis" in s: return "Limpieza profunda con ultrasonido, pulido profesional y aplicación de flúor. Prevención completa cada 6 meses."
        if "odontolog" in s and "general" in s: return "Revisión integral, diagnóstico y plan de tratamiento. Cuidamos tu salud bucal completa con atención personalizada."
        if "rehabilitac" in s: return "Reconstrucción funcional y estética de tu sonrisa completa. Prótesis fijas, removibles y sobre implantes según tu caso."
    elif nicho_key == "fisiot":
        if "manual" in s or "miofascial" in s: return "Técnicas manuales especializadas para liberar tensiones, mejorar movilidad y aliviar el dolor crónico."
        if "depor" in s: return "Rehabilitación específica para deportistas amateur y de alto rendimiento. Retorno seguro al deporte con progresiones medidas."
        if "post" in s or "operat" in s or "quirur" in s: return "Recuperación guiada tras cirugía ortopédica. Plan progresivo para recuperar fuerza, movilidad y funcionalidad."
        if "seca" in s or "elec" in s or "punci" in s: return "Técnica invasiva con aguja para desactivar puntos gatillo miofasciales. Alta efectividad en dolor crónico musculoesquelético."
        if "neur" in s: return "Rehabilitación neurológica para pacientes con ACV, Parkinson, esclerosis múltiple y otras condiciones del sistema nervioso."
        if "domicil" in s: return "Llevamos el tratamiento a tu casa. Sesiones personalizadas con el mismo profesional y protocolo del consultorio."
    elif nicho_key == "psicol":
        if "individual" in s or "terapia" in s: return "Sesiones individuales de 50 minutos en un espacio confidencial. Trabajo enfocado en tus objetivos terapéuticos."
        if "pareja" in s: return "Terapia para parejas que buscan mejorar la comunicación, resolver conflictos o tomar decisiones importantes juntos."
        if "familia" in s: return "Intervención familiar para mejorar la dinámica, los vínculos y resolver conflictos en el sistema familiar."
        if "infan" in s or "niño" in s or "adole" in s: return "Atención psicológica especializada para niños y adolescentes. Juego, arte y técnicas adaptadas a cada edad."
        if "online" in s: return "Sesiones por videollamada con la misma confidencialidad y calidad que la atención presencial."
    elif nicho_key == "medic":
        if "consulta" in s or "general" in s: return "Valoración médica integral con historia clínica completa, exploración física y plan de manejo personalizado."
        if "diagn" in s or "laborat" in s: return "Estudios de laboratorio y gabinete con resultados rápidos. Diagnóstico certero para tomar decisiones informadas."
        if "checkup" in s or "preven" in s: return "Evaluación preventiva completa con perfil bioquímico, estudios de imagen y consulta especializada."
        if "quirur" in s or "cirug" in s: return "Procedimientos quirúrgicos ambulatorios con tecnología de mínima invasión y equipo altamente capacitado."
        if "cardi" in s: return "Evaluación cardiovascular con electrocardiograma, ecocardiograma y pruebas de esfuerzo. Detección temprana de enfermedades cardíacas."
    elif nicho_key == "podolog":
        if "pie" in s and "diab" in s: return "Atención especializada para pacientes diabéticos. Prevención de úlceras,callosidades y cuidado integral del pie diabético."
        if "uña" in s or "onic" in s: return "Tratamiento de uñas encarnadas, hongos y otras onicopatías con técnicas mínimamente invasivas."
        if "plant" in s or "estudio" in s: return "Estudio biomecánico de la pisada con plataforma de presión. Plantillas personalizadas para corregir alteraciones."
        if "verruga" in s or "papilo" in s: return "Eliminación de verrugas plantares con técnicas avanzadas. Tratamiento efectivo sin dolor y con seguimiento."
    return COPY_POR_SERVICIO.get(nicho_key, COPY_POR_SERVICIO["medic"])["default"]


def generar_faqs(nicho, nombre):
    """Genera FAQs específicas al nicho."""
    nicho_key = get_nicho_key(nicho)
    if nicho_key == "dent":
        return [
            ("¿Cuánto cuesta la primera consulta?", f"La primera consulta de valoración en {nombre} incluye revisión clínica y plan de tratamiento sin compromiso. Te lo confirmamos por WhatsApp."),
            ("¿Aceptan seguros o pagos a meses?", "Sí, trabajamos con las principales aseguradoras y ofrecemos planes de pago a meses sin intereses con tarjetas participantes."),
            ("¿Cuánto dura un tratamiento de ortodoncia?", "Depende de la complejidad del caso, entre 8 y 24 meses. Te lo confirmamos en la valoración inicial con un plan personalizado."),
            ("¿Atienden urgencias dentales?", "Sí, tenemos disponibilidad para urgencias dentales el mismo día. Escríbenos por WhatsApp y te atendemos a la brevedad."),
        ]
    elif nicho_key == "fisiot":
        return [
            ("¿Necesito orden médica para empezar?", "No es obligatoria. Puedes agendar tu valoración inicial directamente con nosotros y traer tus estudios si los tienes."),
            ("¿Cuántas sesiones voy a necesitar?", "Depende de tu lesión y objetivos. En la primera sesión te damos un estimado basado en la valoración completa."),
            ("¿Atienden a domicilio?", "Sí, contamos con servicio a domicilio en la zona. Consulta disponibilidad y costo adicional por WhatsApp."),
            ("¿Trabajan con mi aseguradora?", "Trabajamos con varias aseguradoras y EPS. Envíanos tu póliza o carné por WhatsApp y te confirmamos cobertura."),
        ]
    elif nicho_key == "psicol":
        return [
            ("¿Cuántas sesiones voy a necesitar?", "Depende de tus objetivos. Algunos pacientes resuelven su motivo de consulta en 8-12 sesiones, otros optan por procesos más largos de autoconocimiento."),
            ("¿La información que comparto es confidencial?", "Absolutamente. Todo lo que se habla en sesión está protegido por el secreto profesional. Solo se rompe en casos extremos contemplados por la ley."),
            ("¿Atienden por videollamada?", "Sí, tenemos modalidad online con la misma calidad y confidencialidad que la atención presencial."),
            ("¿Cómo sé si necesito ir al psicólogo?", "Si sientes que algo te supera, que te cuesta dormir, o que hay un problema recurrente que afecta tu vida diaria, vale la pena una primera sesión exploratoria."),
        ]
    elif nicho_key == "medic":
        return [
            ("¿Necesito cita previa?", "Sí, trabajamos con cita previa para garantizarte el tiempo adecuado. Puedes agendarla por WhatsApp o llamada."),
            ("¿Aceptan seguros médicos?", "Sí, trabajamos con las principales aseguradoras. Confirma con tu póliza que el especialista y el procedimiento están cubiertos."),
            ("¿Cuánto dura una consulta?", "La primera consulta dura entre 30 y 45 minutos para hacer una valoración completa. Las subsecuentes entre 20 y 30 minutos."),
            ("¿Tienen servicio de urgencias?", "Para urgencias no graves atendemos el mismo día según disponibilidad. En urgencias graves, te referimos a un hospital de inmediato."),
        ]
    elif nicho_key == "podolog":
        return [
            ("¿Cada cuánto debo ir al podólogo?", "Se recomienda una revisión cada 6-8 semanas para mantener la salud de tus pies, especialmente si tienes diabetes o usas plantillas."),
            ("¿Trabajan con pacientes diabéticos?", "Sí, somos especialistas en pie diabético. Hacemos prevención, tratamiento y educación para el cuidado en casa."),
            ("¿Las plantillas son incómodas?", "No. Estudiamos tu pisada y hacemos plantillas personalizadas adaptadas a tu anatomía y actividad. La primera semana puede haber adaptación leve."),
            ("¿Atienden a domicilio?", "Sí, para pacientes con movilidad reducida o postrados. Consulta disponibilidad y tarifas por WhatsApp."),
        ]
    return [
        (f"¿Cómo agendo una cita en {nombre}?", "Por WhatsApp o llamada. Te confirmamos disponibilidad según tu horario."),
        ("¿Aceptan seguros?", "Trabajamos con varias aseguradoras. Confirma con tu póliza y la nuestra por WhatsApp."),
        ("¿Cuánto dura la primera consulta?", "Entre 30 y 60 minutos, según el servicio. Te lo confirmamos al agendar."),
    ]


# Imágenes de stock mejores por nicho (Pexels + Unsplash específicos, no genéricos)
IMGS_POR_NICHO = {
    "dent": {
        "hero": "https://images.pexels.com/photos/3845457/pexels-photo-3845457.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "carousel": [
            "https://images.pexels.com/photos/3845553/pexels-photo-3845553.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/4269693/pexels-photo-4269693.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/3771113/pexels-photo-3771113.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/5355864/pexels-photo-5355864.jpeg?auto=compress&cs=tinysrgb&w=900",
        ],
    },
    "fisiot": {
        "hero": "https://images.pexels.com/photos/4506105/pexels-photo-4506105.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "carousel": [
            "https://images.pexels.com/photos/4506108/pexels-photo-4506108.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/7176026/pexels-photo-7176026.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/7088489/pexels-photo-7088489.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/4503273/pexels-photo-4503273.jpeg?auto=compress&cs=tinysrgb&w=900",
        ],
    },
    "psicol": {
        "hero": "https://images.pexels.com/photos/4101143/pexels-photo-4101143.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "carousel": [
            "https://images.pexels.com/photos/4101145/pexels-photo-4101145.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/8460059/pexels-photo-8460059.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/7088534/pexels-photo-7088534.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/4101146/pexels-photo-4101146.jpeg?auto=compress&cs=tinysrgb&w=900",
        ],
    },
    "medic": {
        "hero": "https://images.pexels.com/photos/7088480/pexels-photo-7088480.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "carousel": [
            "https://images.pexels.com/photos/7088530/pexels-photo-7088530.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/4173251/pexels-photo-4173251.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/7088489/pexels-photo-7088489.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/7088484/pexels-photo-7088484.jpeg?auto=compress&cs=tinysrgb&w=900",
        ],
    },
    "podolog": {
        "hero": "https://images.pexels.com/photos/7088480/pexels-photo-7088480.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "carousel": [
            "https://images.pexels.com/photos/7088530/pexels-photo-7088530.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/7088489/pexels-photo-7088489.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/4173251/pexels-photo-4173251.jpeg?auto=compress&cs=tinysrgb&w=900",
            "https://images.pexels.com/photos/7088484/pexels-photo-7088484.jpeg?auto=compress&cs=tinysrgb&w=900",
        ],
    },
}


def get_imgs(nicho):
    return IMGS_POR_NICHO.get(get_nicho_key(nicho), IMGS_POR_NICHO["medic"])


def parse_brief(ruta_brief):
    with open(ruta_brief, "r", encoding="utf-8") as f:
        contenido = f.read()
    datos = {}
    m = re.search(r'\*\*Nombre\*\*:\s*(.+)', contenido)
    datos["nombre"] = m.group(1).strip() if m else "N/D"
    m = re.search(r'\*\*Nicho\*\*:\s*(.+)', contenido)
    datos["nicho"] = m.group(1).strip() if m else "N/D"
    m = re.search(r'\*\*Ciudad\*\*:\s*(.+)', contenido)
    ciudad_full = m.group(1).strip() if m else "Ciudad de México (CDMX)"
    datos["ciudad"] = ciudad_full
    datos["ciudad_corto"] = ciudad_full.replace(" (CDMX)", "").replace("Ciudad de México", "CDMX")
    m = re.search(r'WhatsApp:\s*(\d+)', contenido)
    datos["whatsapp"] = m.group(1).strip() if m else ""
    m = re.search(r'\*\*Calificación en Google Maps\*\*:\s*([\d.]+)\s*Estrellas', contenido)
    datos["rating"] = m.group(1) if m else "5.0"
    m = re.search(r'\*\*Cantidad de Reseñas\*\*:\s*(\d+)\s*reseñas', contenido)
    datos["reseñas"] = m.group(1) if m else "0"
    m = re.search(r'-\s*\*\*Primario\*\*:\s*(#[a-fA-F0-9]+)', contenido)
    datos["c1"] = m.group(1) if m else "#2563eb"
    m = re.search(r'-\s*\*\*Secundario\*\*:\s*(#[a-fA-F0-9]+)', contenido)
    datos["c2"] = m.group(1) if m else "#60a5fa"
    m = re.search(r'-\s*\*\*Fondo Oscuro \(Hero\)\*\*:\s*(#[a-fA-F0-9]+)', contenido)
    datos["c3"] = m.group(1) if m else "#1e3a8a"
    m = re.search(r'-\s*\*\*Hero Titular\*\*:\s*(.+)', contenido)
    datos["h1"] = m.group(1).strip() if m else datos["nombre"]
    m = re.search(r'-\s*\*\*Hero Subtítulo\*\*:\s*(.+)', contenido)
    datos["sub"] = m.group(1).strip() if m else ""
    servicios_match = re.findall(r'^\s*(\d+)\.\s+(.+)$', contenido[contenido.find("Servicios Principales"):], re.MULTILINE)
    servicios = []
    if servicios_match:
        for num, texto in servicios_match:
            if "PROMPT MAESTRO" in texto or "---" in texto:
                break
            servicios.append(texto.strip())
    datos["servicios"] = servicios[:4] if servicios else ["Consulta especializada", "Diagnóstico integral", "Tratamiento personalizado", "Seguimiento profesional"]
    return datos


def hex_to_rgb(h):
    h = h.lstrip('#')
    return f"rgb({int(h[0:2],16)},{int(h[2:4],16)},{int(h[4:6],16)})"


def oscurecer_color(hex_color, factor=0.3):
    """Devuelve un color más oscuro (para card bg)"""
    h = hex_color.lstrip('#')
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    r = int(r * factor)
    g = int(g * factor)
    b = int(b * factor)
    return f"#{r:02x}{g:02x}{b:02x}"


def generar_html(datos):
    schema_type = get_schema_type(datos["nicho"])
    nicho_key = get_nicho_key(datos["nicho"])
    iconos = get_iconos(datos["nicho"])
    imgs = get_imgs(datos["nicho"])
    faqs = generar_faqs(datos["nicho"], datos["nombre"])
    servicios_cards = []
    for i, srv in enumerate(datos["servicios"]):
        copy = generar_copy_servicio(srv, nicho_key)
        icono = iconos[i % len(iconos)]
        servicios_cards.append(f'''        <div class="srv-card fade-in-up">
            <div class="srv-icon">{icono}</div>
            <h3>{srv}</h3>
            <p>{copy}</p>
            <a href="https://wa.me/{datos["whatsapp"]}?text=Hola%2C%20me%20interesa%20el%20servicio%20de%20{srv.replace(" ", "%20")}" class="btn-outline">Consultar por WhatsApp</a>
        </div>''')
    servicios_html = "\n".join(servicios_cards)
    faqs_html = "\n".join([f'''            <details class="faq-item">
                <summary>{q}</summary>
                <p>{a}</p>
            </details>''' for q, a in faqs])
    carousel_html = "\n".join([f'                <div class="carousel-slide {("active" if i==0 else "")}"><img src="{img}" alt="Instalaciones {datos["nombre"]}"></div>' for i, img in enumerate(imgs["carousel"])])

    bg_oscuro = oscurecer_color(datos["c3"], 0.4)
    card_bg = oscurecer_color(datos["c3"], 0.55)

    schema = f'''{{
  "@context": "https://schema.org",
  "@type": "{schema_type}",
  "name": "{datos['nombre']}",
  "image": "{imgs["hero"]}",
  "telephone": "+{datos['whatsapp']}",
  "priceRange": "$$",
  "description": "{datos["sub"][:150]}",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "{datos["ciudad_corto"]}",
    "addressRegion": "CDMX",
    "addressCountry": "MX"
  }},
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "{datos["rating"]}",
    "reviewCount": "{datos["reseñas"]}"
  }}
}}'''

    keywords_nicho = {
        "dent": "dentista CDMX, odontología, ortodoncia, implantes dentales",
        "fisiot": "fisioterapia CDMX, rehabilitación física, terapia manual",
        "psicol": "psicólogo CDMX, terapia psicológica, salud mental",
        "medic": "clínica médica CDMX, consulta especializada, medicina integral",
        "podolog": "podólogo CDMX, cuidado de pies, plantillas",
    }

    return f'''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{datos["nombre"]} · {datos["nicho"]} en {datos["ciudad"]}</title>
    <meta name="description" content="{datos["sub"][:160]}">
    <meta name="robots" content="index, follow">
    <meta name="keywords" content="{keywords_nicho.get(nicho_key, keywords_nicho["medic"])}">
    <meta property="og:type" content="business.business">
    <meta property="og:title" content="{datos["nombre"]}">
    <meta property="og:description" content="{datos["sub"][:160]}">
    <meta property="og:image" content="{imgs["hero"]}">
    <meta property="og:locale" content="es_MX">
    <meta property="og:site_name" content="{datos["nombre"]}">
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{datos["nombre"]}">
    <meta name="twitter:description" content="{datos["sub"][:160]}">
    <meta name="twitter:image" content="{imgs["hero"]}">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <script type="application/ld+json">
{schema}
    </script>
    <style>
        :root {{
            --primary: {datos["c1"]};
            --secondary: {datos["c2"]};
            --dark-bg: {datos["c3"]};
            --bg: {bg_oscuro};
            --card-bg: {card_bg};
            --border: rgba(255,255,255,0.1);
            --text: #f8fafc;
            --text-muted: #94a3b8;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: var(--bg); color: var(--text); overflow-x: hidden; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}
        nav {{ position: fixed; top: 0; width: 100%; z-index: 1000; background: rgba(7, 15, 26, 0.7); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255,255,255,0.05); padding: 16px 0; transition: all 0.3s ease; }}
        .nav-content {{ display: flex; justify-content: space-between; align-items: center; }}
        .brand {{ font-size: 1.4rem; font-weight: 800; color: #fff; text-decoration: none; }}
        .brand span {{ color: var(--secondary); }}
        .btn-wa-header {{ background: var(--primary); color: #fff; padding: 10px 24px; border-radius: 50px; text-decoration: none; font-weight: 700; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }}
        .btn-wa-header:hover {{ background: var(--secondary); transform: translateY(-2px); }}
        .hero {{ padding: 140px 0 80px; background: radial-gradient(circle at top left, var(--dark-bg) 0%, var(--bg) 70%); }}
        .hero-grid {{ display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 40px; align-items: center; }}
        .hero-badge {{ display: inline-flex; background: rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 20px; font-weight: 700; color: var(--secondary); margin-bottom: 24px; font-size: 0.9rem; border: 1px solid rgba(255,255,255,0.1); }}
        .hero h1 {{ font-size: clamp(2rem, 4.5vw, 3.5rem); font-weight: 800; line-height: 1.1; margin-bottom: 24px; }}
        .hero h1 span {{ color: var(--secondary); }}
        .hero p {{ font-size: 1.1rem; color: var(--text-muted); margin-bottom: 32px; line-height: 1.6; }}
        .hero-cta {{ display: flex; gap: 16px; align-items: center; flex-wrap: wrap; }}
        .btn-primary {{ background: #25d366; color: #fff; padding: 16px 32px; border-radius: 50px; text-decoration: none; font-weight: 800; font-size: 1.05rem; transition: all 0.3s ease; box-shadow: 0 8px 24px rgba(37, 211, 102, 0.3); }}
        .btn-primary:hover {{ transform: translateY(-3px); box-shadow: 0 12px 32px rgba(37, 211, 102, 0.5); }}
        .btn-secondary {{ background: transparent; color: #fff; padding: 16px 32px; border-radius: 50px; text-decoration: none; font-weight: 700; font-size: 1rem; border: 1.5px solid rgba(255,255,255,0.4); transition: all 0.3s ease; }}
        .btn-secondary:hover {{ border-color: var(--secondary); color: var(--secondary); }}
        .hero-rating {{ display: flex; align-items: center; gap: 12px; margin-top: 32px; font-size: 0.9rem; color: var(--text-muted); flex-wrap: wrap; }}
        .hero-rating strong {{ color: #fbbf24; font-size: 1.1rem; }}
        .hero-image-wrap {{ position: relative; border-radius: 24px; overflow: hidden; box-shadow: 0 24px 48px rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.1); }}
        .hero-image-wrap img {{ width: 100%; height: 500px; object-fit: cover; display: block; }}
        .stats {{ background: var(--card-bg); padding: 50px 0; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); text-align: center; gap: 20px; }}
        .stat-item h3 {{ font-size: 2.5rem; color: var(--secondary); font-weight: 800; margin-bottom: 8px; }}
        .stat-item p {{ font-size: 0.9rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }}
        .section-title {{ text-align: center; margin-bottom: 50px; }}
        .section-title h2 {{ font-size: 2.5rem; font-weight: 800; margin-bottom: 16px; }}
        .section-title p {{ color: var(--text-muted); max-width: 600px; margin: 0 auto; }}
        .services {{ padding: 100px 0; }}
        .srv-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; }}
        .srv-card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 20px; padding: 32px; transition: all 0.3s ease; position: relative; overflow: hidden; }}
        .srv-card:hover {{ transform: translateY(-10px); border-color: var(--secondary); box-shadow: 0 20px 40px rgba(0,0,0,0.3); }}
        .srv-icon {{ font-size: 2.2rem; margin-bottom: 20px; background: rgba(255,255,255,0.05); width: 60px; height: 60px; display: flex; align-items: center; justify-content: center; border-radius: 14px; border: 1px solid rgba(255,255,255,0.1); }}
        .srv-card h3 {{ font-size: 1.2rem; margin-bottom: 12px; font-weight: 700; }}
        .srv-card p {{ color: var(--text-muted); font-size: 0.95rem; margin-bottom: 20px; line-height: 1.6; }}
        .btn-outline {{ display: inline-block; text-align: center; border: 1px solid var(--border); padding: 12px 18px; border-radius: 12px; color: #fff; text-decoration: none; font-weight: 600; font-size: 0.9rem; transition: all 0.3s; }}
        .btn-outline:hover {{ background: var(--secondary); border-color: var(--secondary); color: var(--bg); }}
        .about-sec {{ padding: 100px 0; background: var(--card-bg); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }}
        .about-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; }}
        .about-text h2 {{ font-size: 2.2rem; margin-bottom: 20px; font-weight: 800; }}
        .about-text p {{ color: var(--text-muted); margin-bottom: 16px; line-height: 1.7; }}
        .credentials {{ display: grid; gap: 12px; margin-top: 24px; }}
        .credentials li {{ list-style: none; display: flex; gap: 12px; align-items: center; color: var(--text-muted); }}
        .credentials li::before {{ content: "✓"; color: var(--secondary); font-weight: 800; font-size: 1.1rem; }}
        .carousel-sec {{ padding: 100px 0; }}
        .carousel-wrap {{ position: relative; max-width: 900px; margin: 0 auto; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); }}
        .carousel-slide {{ display: none; width: 100%; height: 500px; }}
        .carousel-slide.active {{ display: block; animation: fade 0.8s ease-in-out; }}
        .carousel-slide img {{ width: 100%; height: 100%; object-fit: cover; }}
        @keyframes fade {{ from {{opacity: 0.4}} to {{opacity: 1}} }}
        .car-btn {{ position: absolute; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.6); color: white; border: 1px solid rgba(255,255,255,0.2); width: 48px; height: 48px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; backdrop-filter: blur(4px); transition: all 0.3s; }}
        .car-btn:hover {{ background: var(--primary); }}
        .car-prev {{ left: 20px; }}
        .car-next {{ right: 20px; }}
        .schedule-sec {{ padding: 80px 0; background: var(--card-bg); border-top: 1px solid var(--border); }}
        .schedule-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 20px; margin-top: 30px; }}
        .schedule-card {{ background: var(--bg); border: 1px solid var(--border); border-radius: 16px; padding: 24px; text-align: center; }}
        .schedule-card h4 {{ color: var(--secondary); font-size: 0.85rem; letter-spacing: 0.15em; text-transform: uppercase; margin-bottom: 12px; }}
        .schedule-card p {{ font-size: 1.15rem; font-weight: 700; }}
        .faqs {{ padding: 100px 0; }}
        .faq-wrap {{ max-width: 800px; margin: 0 auto; }}
        .faq-item {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 16px; margin-bottom: 16px; }}
        .faq-item summary {{ padding: 24px; font-size: 1.05rem; font-weight: 700; cursor: pointer; list-style: none; display: flex; justify-content: space-between; align-items: center; }}
        .faq-item summary::-webkit-details-marker {{ display: none; }}
        .faq-item summary::after {{ content: '+'; color: var(--secondary); font-size: 1.5rem; }}
        .faq-item[open] summary::after {{ content: '−'; }}
        .faq-item p {{ padding: 0 24px 24px; color: var(--text-muted); border-top: 1px solid rgba(255,255,255,0.05); margin-top: 8px; padding-top: 16px; line-height: 1.6; }}
        .contact-sec {{ padding: 100px 0; background: var(--card-bg); border-top: 1px solid var(--border); }}
        .contact-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 50px; margin-top: 40px; }}
        .c-item {{ display: flex; gap: 16px; margin-bottom: 22px; align-items: flex-start; }}
        .c-item .ico {{ width: 48px; height: 48px; flex: none; border-radius: 12px; background: var(--bg); color: var(--secondary); display: flex; align-items: center; justify-content: center; font-size: 1.2rem; }}
        .c-item h4 {{ font-size: 0.78rem; letter-spacing: 0.15em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 6px; }}
        .c-item p {{ font-weight: 600; font-size: 1rem; }}
        .wa-float {{ position: fixed; bottom: 30px; right: 30px; background: #25d366; width: 64px; height: 64px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 2rem; color: white; text-decoration: none; box-shadow: 0 10px 24px rgba(37, 211, 102, 0.4); z-index: 999; }}
        footer {{ text-align: center; padding: 40px 0; border-top: 1px solid var(--border); color: var(--text-muted); font-size: 0.85rem; }}
        footer a {{ color: var(--secondary); text-decoration: none; }}
        @media (prefers-reduced-motion: no-preference) {{
            .fade-in-up {{ opacity: 0; transform: translateY(30px); transition: opacity 0.8s ease, transform 0.8s ease; }}
            .fade-in-up.visible {{ opacity: 1; transform: translateY(0); }}
            .wa-float::before {{ content: ''; position: absolute; inset: 0; border-radius: 50%; border: 2px solid #25d366; animation: waPulse 2.4s ease-out infinite; }}
            @keyframes waPulse {{ 0% {{ transform: scale(1); opacity: 1; }} 100% {{ transform: scale(1.6); opacity: 0; }} }}
        }}
        @media(max-width: 900px) {{
            .hero-grid {{ grid-template-columns: 1fr; text-align: center; }}
            .hero-cta {{ justify-content: center; }}
            .hero-rating {{ justify-content: center; }}
            .about-grid {{ grid-template-columns: 1fr; }}
            .contact-grid {{ grid-template-columns: 1fr; }}
            .stats-grid {{ grid-template-columns: 1fr 1fr; }}
            .carousel-slide {{ height: 350px; }}
        }}
    </style>
</head>
<body>
    <nav>
        <div class="container nav-content">
            <a href="#" class="brand">{datos["nombre"].split()[0] if datos["nombre"] else "Inicio"}<span> {(' '.join(datos["nombre"].split()[1:]) if len(datos["nombre"].split())>1 else "")}</span></a>
            <a href="https://wa.me/{datos["whatsapp"]}?text=Hola%2C%20me%20interesa%20más%20información%20de%20{datos["nombre"].replace(" ", "%20")}" class="btn-wa-header" target="_blank">Contactar</a>
        </div>
    </nav>
    <header class="hero">
        <div class="container hero-grid">
            <div class="hero-text fade-in-up">
                <div class="hero-badge">{datos["nicho"]} · {datos["ciudad"]}</div>
                <h1>{datos["h1"]}</h1>
                <p>{datos["sub"]}</p>
                <div class="hero-cta">
                    <a href="https://wa.me/{datos["whatsapp"]}?text=Hola%2C%20quiero%20agendar%20una%20cita" class="btn-primary" target="_blank">💬 Agendar por WhatsApp</a>
                    <a href="#servicios" class="btn-secondary">Ver servicios</a>
                </div>
                <div class="hero-rating">
                    <span>⭐ <strong>{datos["rating"]} / 5.0</strong></span>
                    <span>· Basado en {datos["reseñas"]} reseñas en Google</span>
                </div>
            </div>
            <div class="hero-image-wrap fade-in-up" style="transition-delay: 0.15s;">
                <img src="{imgs["hero"]}" alt="{datos["nombre"]}">
            </div>
        </div>
    </header>
    <section class="stats">
        <div class="container stats-grid">
            <div class="stat-item fade-in-up"><h3>{datos["rating"]}★</h3><p>Calificación Google</p></div>
            <div class="stat-item fade-in-up"><h3>{datos["reseñas"]}+</h3><p>Reseñas de pacientes</p></div>
            <div class="stat-item fade-in-up"><h3>{datos["ciudad_corto"]}</h3><p>Atención presencial</p></div>
        </div>
    </section>
    <section class="services container" id="servicios">
        <div class="section-title fade-in-up">
            <h2>Nuestros servicios</h2>
            <p>Cada servicio de {datos["nombre"]} está diseñado para darte la mejor atención con tecnología de vanguardia y un equipo humano cercano.</p>
        </div>
        <div class="srv-grid">
{servicios_html}
        </div>
    </section>
    <section class="about-sec">
        <div class="container about-grid">
            <div class="hero-image-wrap fade-in-up" style="border-radius: 24px;">
                <img src="{imgs["carousel"][0]}" alt="Equipo de {datos["nombre"]}">
            </div>
            <div class="about-text fade-in-up" style="transition-delay: 0.15s;">
                <div class="hero-badge" style="margin-bottom: 16px;">Sobre nosotros</div>
                <h2>Un equipo profesional a tu servicio</h2>
                <p>En {datos["nombre"]} contamos con un equipo de especialistas certificados con años de experiencia en {datos["nicho"].lower()}. Nos respalda la confianza de {datos["reseñas"]} pacientes que nos han calificado con {datos["rating"]} estrellas en Google.</p>
                <p>Trabajamos con tecnología de última generación y un trato humano cercano que marca la diferencia en cada consulta.</p>
                <ul class="credentials">
                    <li>Especialistas certificados en {datos["nicho"].lower()}</li>
                    <li>Tecnología y equipos modernos</li>
                    <li>Atención personalizada y cercana</li>
                    <li>Instalaciones cómodas en {datos["ciudad_corto"]}</li>
                </ul>
            </div>
        </div>
    </section>
    <section class="carousel-sec">
        <div class="container">
            <div class="section-title fade-in-up">
                <h2>Nuestras instalaciones</h2>
                <p>Conoce el espacio donde cuidamos de ti.</p>
            </div>
            <div class="carousel-wrap fade-in-up">
{carousel_html}
                <button class="car-btn car-prev" onclick="moveSlide(-1)" aria-label="Anterior">❮</button>
                <button class="car-btn car-next" onclick="moveSlide(1)" aria-label="Siguiente">❯</button>
            </div>
        </div>
    </section>
    <section class="schedule-sec">
        <div class="container">
            <div class="section-title fade-in-up">
                <h2>Horarios de atención</h2>
                <p>Agenda tu cita en el horario que mejor te convenga.</p>
            </div>
            <div class="schedule-grid">
                <div class="schedule-card fade-in-up"><h4>Lunes a viernes</h4><p>9:00 – 19:00</p></div>
                <div class="schedule-card fade-in-up"><h4>Sábados</h4><p>9:00 – 14:00</p></div>
                <div class="schedule-card fade-in-up"><h4>Domingos</h4><p>Cerrado</p></div>
                <div class="schedule-card fade-in-up"><h4>Agendamiento</h4><p>Por WhatsApp</p></div>
            </div>
        </div>
    </section>
    <section class="faqs container">
        <div class="section-title fade-in-up">
            <h2>Preguntas frecuentes</h2>
            <p>Las respuestas a lo que más nos preguntan antes de la primera cita.</p>
        </div>
        <div class="faq-wrap fade-in-up">
{faqs_html}
        </div>
    </section>
    <section class="contact-sec" id="contacto">
        <div class="container">
            <div class="section-title fade-in-up">
                <h2>¿Listo para agendar?</h2>
                <p>Escríbenos por WhatsApp y te respondemos en minutos.</p>
            </div>
            <div class="contact-grid">
                <div class="fade-in-up">
                    <div class="c-item"><div class="ico">💬</div><div><h4>WhatsApp</h4><p>+{datos["whatsapp"][:2]} {datos["whatsapp"][2:5]} {datos["whatsapp"][5:8]} {datos["whatsapp"][8:]}</p></div></div>
                    <div class="c-item"><div class="ico">📍</div><div><h4>Ubicación</h4><p>{datos["ciudad_corto"]}<br><a href="https://www.google.com/maps/search/?api=1&query={datos["nombre"].replace(" ", "+")}+{datos["ciudad_corto"]}" target="_blank" style="color: var(--secondary); font-size: 0.85rem;">Ver en Google Maps →</a></p></div></div>
                    <div class="c-item"><div class="ico">⭐</div><div><h4>Google</h4><p>{datos["rating"]} estrellas · {datos["reseñas"]} reseñas</p></div></div>
                    <div class="c-item"><div class="ico">🕐</div><div><h4>Horarios</h4><p>Lun a Vie 9-19 · Sáb 9-14</p></div></div>
                </div>
                <div class="hero-image-wrap fade-in-up" style="border-radius: 20px; display: flex; align-items: center; justify-content: center; text-align: center; padding: 50px 30px; min-height: 320px;">
                    <div>
                        <h3 style="font-size: 1.6rem; margin-bottom: 16px; color: #fff;">Agenda por WhatsApp</h3>
                        <p style="color: var(--text-muted); margin-bottom: 28px; font-size: 1rem;">La forma más rápida de reservar tu cita con {datos["nombre"]}.</p>
                        <a href="https://wa.me/{datos["whatsapp"]}?text=Hola%2C%20quiero%20agendar%20una%20cita" class="btn-primary" target="_blank" style="display: inline-block;">💬 Escribir ahora</a>
                    </div>
                </div>
            </div>
        </div>
    </section>
    <footer>
        <div class="container">
            <p>&copy; 2026 {datos["nombre"]}. Todos los derechos reservados. · <i>Diseño borrador de propuesta.</i></p>
        </div>
    </footer>
    <a href="https://wa.me/{datos["whatsapp"]}" class="wa-float" target="_blank" aria-label="WhatsApp">💬</a>
    <script>
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) entry.target.classList.add('visible');
            }});
        }}, {{ threshold: 0.1 }});
        document.querySelectorAll('.fade-in-up').forEach(el => observer.observe(el));
        let slideIndex = 0;
        const slides = document.querySelectorAll('.carousel-slide');
        function moveSlide(n) {{
            if (!slides.length) return;
            slides[slideIndex].classList.remove('active');
            slideIndex = (slideIndex + n + slides.length) % slides.length;
            slides[slideIndex].classList.add('active');
        }}
        if (slides.length) setInterval(() => moveSlide(1), 5000);
    </script>
</body>
</html>'''


def main():
    print(f"Reescribiendo {len(WEBS_LOTE2)} webs del lote 2 con template mejorado...\n")
    for carpeta in WEBS_LOTE2:
        ruta_brief = os.path.join(BASE, carpeta, "brief_maestro.md")
        ruta_html = os.path.join(BASE, carpeta, "index.html")
        if not os.path.exists(ruta_brief):
            print(f"--  {carpeta} (sin brief)")
            continue
        datos = parse_brief(ruta_brief)
        html = generar_html(datos)
        with open(ruta_html, "w", encoding="utf-8") as f:
            f.write(html)
        size_kb = round(len(html) / 1024, 1)
        print(f"OK  {carpeta}  ({size_kb} KB, schema={get_schema_type(datos['nicho'])}, rating={datos['rating']}/{datos['reseñas']})")
    print(f"\nListo. {len(WEBS_LOTE2)} webs reescritas.")


if __name__ == "__main__":
    main()
