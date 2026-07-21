"""
Script para extraer datos de los briefs del lote 2 y generar
los archivos _CORRECCIONES.md de cada web.
"""
import os
import re
import json

BASE = "/Users/beto/Library/CloudStorage/OneDrive-Personal(2)/Freelancer/clientes/web"

# 23 webs con brief
WEBS_LOTE2 = [
    "centro-bewusst-machen",
    "cercardio-especialidades-medicas",
    "clinica-dental-amsterdent",
    "clinica-dental-dentale",
    "clinica-dental-godiental",
    "clinica-dental-proboca",
    "clinica-dental-rehabilitarte",
    "clinica-fisioterapia-santillan",
    "clinica-medica-palmas-dra-yanina-rubio",
    "clinica-odontologica-dentalcenter",
    "dental-studio-mx",
    "ds-consultorio-dental",
    "fisioterapia-y-rehabilitacion-vertiz",
    "grupo-sonrie-mx",
    "kintsu-dental",
    "klinikdent-mexico",
    "odontologia-biologica-dra-yulianna-suarez",
    "podologia-fisioterapia-pies-alegres",
    "rehavilita-fisioterapia",
    "saludent-sas",
    "sca-clinica-de-fisioterapia",
    "seishi-centro-de-atencion-psicologica",
    "vitalmente-centro-medico-psicologia",
]


def parse_brief(ruta_brief):
    """Extrae datos del brief en formato markdown."""
    with open(ruta_brief, "r", encoding="utf-8") as f:
        contenido = f.read()
    datos = {}
    # Nombre
    m = re.search(r'\*\*Nombre\*\*:\s*(.+)', contenido)
    datos["nombre"] = m.group(1).strip() if m else "N/D"
    # Nicho
    m = re.search(r'\*\*Nicho\*\*:\s*(.+)', contenido)
    datos["nicho"] = m.group(1).strip() if m else "N/D"
    # Ciudad
    m = re.search(r'\*\*Ciudad\*\*:\s*(.+)', contenido)
    datos["ciudad"] = m.group(1).strip() if m else "CDMX"
    # Teléfono
    m = re.search(r'\*\*Teléfono de Contacto\*\*:\s*(.+)', contenido)
    datos["telefono_full"] = m.group(1).strip() if m else ""
    m = re.search(r'WhatsApp:\s*(\d+)', contenido)
    datos["whatsapp"] = m.group(1).strip() if m else ""
    # Rating
    m = re.search(r'\*\*Calificación en Google Maps\*\*:\s*([\d.]+)\s*Estrellas', contenido)
    datos["rating"] = m.group(1) if m else "5.0"
    # Reseñas
    m = re.search(r'\*\*Cantidad de Reseñas\*\*:\s*(\d+)\s*reseñas', contenido)
    datos["reseñas"] = m.group(1) if m else "0"
    # Paleta
    m = re.search(r'-\s*\*\*Primario\*\*:\s*(#[a-fA-F0-9]+)', contenido)
    datos["color_primario"] = m.group(1) if m else "#2563eb"
    m = re.search(r'-\s*\*\*Secundario\*\*:\s*(#[a-fA-F0-9]+)', contenido)
    datos["color_secundario"] = m.group(1) if m else "#60a5fa"
    m = re.search(r'-\s*\*\*Fondo Oscuro \(Hero\)\*\*:\s*(#[a-fA-F0-9]+)', contenido)
    datos["color_oscuro"] = m.group(1) if m else "#1e3a8a"
    # Hero titular
    m = re.search(r'-\s*\*\*Hero Titular\*\*:\s*(.+)', contenido)
    datos["hero_titular"] = m.group(1).strip() if m else datos["nombre"]
    # Hero subtítulo
    m = re.search(r'-\s*\*\*Hero Subtítulo\*\*:\s*(.+)', contenido)
    datos["hero_subtitulo"] = m.group(1).strip() if m else ""
    # Servicios
    servicios_match = re.findall(r'^\s*(\d+)\.\s+(.+)$', contenido[contenido.find("Servicios Principales"):], re.MULTILINE)
    if servicios_match:
        # Filtrar líneas que no sean servicios (buscamos que el siguiente bloque sea el prompt maestro)
        servicios = []
        for num, texto in servicios_match:
            if "PROMPT MAESTRO" in texto or "---" in texto:
                break
            servicios.append(texto.strip())
        datos["servicios"] = servicios[:4]
    else:
        datos["servicios"] = []
    return datos


# Mapeo de nicho a schema.org type
SCHEMA_MAP = {
    "Odontología": "Dentist",
    "Clínica Dental": "Dentist",
    "Ortodoncia": "Dentist",
    "Implantes": "Dentist",
    "Rehabilitación Oral": "Dentist",
    "Fisioterapia": "PhysicalTherapy",
    "Rehabilitación Física": "PhysicalTherapy",
    "Clínica Médica": "MedicalClinic",
    "Salud Mental": "MedicalClinic",
    "Terapia Integral": "MedicalClinic",
    "Psicología Clínica": "MedicalClinic",
    "Cardiología": "MedicalClinic",
    "Especialidades Médicas": "MedicalClinic",
    "Podología": "MedicalClinic",
    "Medicina": "MedicalClinic",
    "Odontología Biológica": "Dentist",
}


def get_schema_type(nicho):
    for key, val in SCHEMA_MAP.items():
        if key.lower() in nicho.lower():
            return val
    return "MedicalClinic"


# Prompts de imagen sugeridos por nicho
PROMPTS_POR_NICHO = {
    "dent": [
        "Fachada moderna de clínica dental con letrero iluminado, vidrio y acero, hora dorada, cielo despejado, encuadre frontal arquitectónico, 4K.",
        "Interior de consultorio dental con sillón dental moderno, lámpara quirúrgica LED, luz natural desde ventanal, instrumental visible, sin paciente, 4K.",
        "Detalle de equipo de rayos X dental o escáner intraoral 3D sobre fondo desenfocado, luz cenital, estilo editorial médico, 4K.",
        "Recepción de clínica dental con mostrador blanco, sillas ergonómicas, certificados y diplomas en pared, encuadre 3/4, luz mixta, 4K.",
        "Sala de espera de clínica dental con diseño minimalista, plantas verdes, revistas, luz cálida, 4K.",
        "Retrato editorial de dentista profesional (hombre/mujer 30-50 años) con bata blanca y mascarilla bajada, sonrisa amable, fondo desenfocado, 4K.",
    ],
    "fisiot": [
        "Fachada de clínica de fisioterapia con letrero profesional, acceso para pacientes, hora dorada, 4K.",
        "Interior de sala de rehabilitación con camillas, pesas, bandas elásticas, luz natural, sin pacientes, 4K.",
        "Equipo de electroestimulación o ultrasonido terapéutico sobre fondo desenfocado, luz cenital, 4K.",
        "Recepción de clínica de fisioterapia con escritorio, sillas, decoración cálida profesional, 4K.",
        "Pasillo de clínica de rehabilitación con luz natural, puertas de consultorios, perspectiva lineal, 4K.",
        "Retrato editorial de fisioterapeuta (hombre/mujer 30-50 años) en uniforme clínico, manos sobre camilla vacía, 4K.",
    ],
    "psicol": [
        "Fachada de consultorio psicológico moderno, letrero discreto, entrada acogedora, 4K.",
        "Interior de consultorio psicológico con sillón terapéutico, escritorio con lámpara cálida, diplomas en pared, sin paciente, 4K.",
        "Detalle de materiales terapéuticos (cuadernos, plantas, libros) sobre mesa auxiliar con luz cálida, 4K.",
        "Sala de espera silenciosa con butacas cómodas, mesa baja con revistas, iluminación indirecta, 4K.",
        "Pasillo del centro con luz natural y puertas de consultorios, ambiente sereno, 4K.",
        "Retrato editorial de psicólogo(a) (hombre/mujer 35-55 años) con ropa smart casual, sonrisa profesional, fondo neutro desenfocado, 4K.",
    ],
    "medic": [
        "Fachada de clínica médica con cruz iluminada, acceso principal amplio, 4K.",
        "Interior de consultorio médico con escritorio, estetoscopio, ordenador, diplomas en pared, sin paciente, 4K.",
        "Equipo médico especializado (cardiólogo: electrocardiógrafo; general: tensiómetro) sobre fondo desenfocado, 4K.",
        "Recepción de clínica médica con mostrador, sala de espera visible al fondo, 4K.",
        "Pasillo clínico limpio con luz LED, puertas de consultorios numerados, 4K.",
        "Retrato editorial de médico especialista (hombre/mujer 35-55 años) con bata blanca, estetoscopio, fondo desenfocado, 4K.",
    ],
    "podolog": [
        "Fachada de consultorio de podología con letrero visible, entrada accesible, 4K.",
        "Interior de consultorio podológico con sillón podológico especializado, lámpara LED, instrumental, 4K.",
        "Detalle de equipo de podología (lámpara de aumento, instrumental) sobre fondo desenfocado, 4K.",
        "Recepción de consultorio podológico con mostrador y decoración cálida, 4K.",
        "Zona de espera con sillas cómodas y material informativo, 4K.",
        "Retrato editorial de podólogo(a) con uniforme clínico, 4K.",
    ],
}


def get_prompts_imagen(nicho):
    nicho_l = nicho.lower()
    if "odon" in nicho_l or "dent" in nicho_l:
        return PROMPTS_POR_NICHO["dent"]
    if "fisiot" in nicho_l or "rehab" in nicho_l:
        return PROMPTS_POR_NICHO["fisiot"]
    if "psicol" in nicho_l or "psic" in nicho_l:
        return PROMPTS_POR_NICHO["psicol"]
    if "podol" in nicho_l:
        return PROMPTS_POR_NICHO["podolog"]
    return PROMPTS_POR_NICHO["medic"]


# Tareas de corrección estándar para todas las webs del lote 2
CORRECCIONES_LOTE2 = [
    ("Agregar SEO schema.org (JSON-LD)", "La web actual NO tiene JSON-LD. Agregar `<script type=\"application/ld+json\">` con `@type` específico del nicho (Dentist, PhysicalTherapy, MedicalClinic), incluyendo `name`, `telephone`, `address` (Ciudad de México), `aggregateRating` con rating y reseñas reales del brief."),
    ("Agregar Open Graph + Twitter Card", "Agregar meta tags `og:title`, `og:description`, `og:image`, `og:locale=es_MX`, `og:type=business.business` y `twitter:card=summary_large_image`."),
    ("Quitar stats inventadas", "La web muestra `1500 pacientes`, `15 años de experiencia`, `100% compromiso` — números falsos. Reemplazar por datos REALES del brief (rating y reseñas de Google) o quitar la sección de stats."),
    ("Reemplazar H1 genérico", "El H1 actual es plantilla fija (`Atención Médica de Excelencia en Ciudad de México (CDMX)`) que se repite en TODAS las webs. Reemplazar por el H1 del brief (sección 4) o uno específico del nicho."),
    ("Reescribir copy de servicios (genérico → específico)", "Los 4 servicios tienen el mismo párrafo genérico: 'Tratamiento especializado con tecnología de vanguardia y atención personalizada para garantizar tu bienestar en Ciudad de México (CDMX).' Reescribir cada uno con descripción única y relevante al servicio."),
    ("Reemplazar FAQs genéricas", "Las 3 preguntas actuales son: 'métodos de pago', 'promociones para pacientes de primera vez', 'cómo agendar cita'. Cambiar por 3-4 FAQs relevantes al nicho del cliente."),
    ("Agregar sección 'Sobre nosotros / Equipo'", "La web no tiene bloque de presentación del equipo. Agregar una sección que muestre al profesional/especialistas del negocio (1-2 fotos + bio de 4-6 líneas)."),
    ("Agregar horarios de atención", "No hay horarios visibles. Agregar bloque con 'Lun a Vie' y 'Sábado' (placeholder razonable a confirmar con el cliente)."),
    ("Agregar link a Google Maps", "No hay link a la dirección. Agregar un botón 'Cómo llegar' apuntando a búsqueda de Google Maps por nombre del negocio."),
    ("Respetar `prefers-reduced-motion`", "Las animaciones (fade-in-up, waPulse) están activas SIEMPRE, sin respetar la preferencia del usuario. Envolver en `@media (prefers-reduced-motion: no-preference)` para accesibilidad."),
    ("Quitar el placeholder 'Este es un diseño borrador de propuesta' del footer", "Solo en producción final, o dejarlo sutil si se usa como demo."),
]


def generar_correcciones_md(nombre_carpeta, datos):
    schema_type = get_schema_type(datos["nicho"])
    prompts = get_prompts_imagen(datos["nicho"])
    servicios_md = "\n".join([f"  - {i+1}. {s}" for i, s in enumerate(datos["servicios"])])

    contenido = f"""# Correcciones — {datos['nombre']}

**Carpeta:** `{nombre_carpeta}`
**Fecha:** 2026-07-21
**Versión:** borrador v2 (reescritura profunda)

## Datos del brief

- **Nombre:** {datos['nombre']}
- **Nicho:** {datos['nicho']}
- **Ciudad:** {datos['ciudad']}
- **Teléfono:** {datos['telefono_full']}
- **WhatsApp:** +{datos['whatsapp']}
- **Rating Google:** {datos['rating']} estrellas
- **Reseñas Google:** {datos['reseñas']}
- **Paleta:**
  - Primario: `{datos['color_primario']}`
  - Secundario: `{datos['color_secundario']}`
  - Fondo hero: `{datos['color_oscuro']}`

## Hero del brief

- **H1:** {datos['hero_titular']}
- **Subtítulo:** {datos['hero_subtitulo']}

## Servicios del brief

{servicios_md}

## Cambios a aplicar al index.html

"""
    for i, (titulo, accion) in enumerate(CORRECCIONES_LOTE2, 1):
        contenido += f"### {i}. {titulo}\n{accion}\n\n"

    contenido += f"""## Schema.org sugerido

```json
{{
  "@context": "https://schema.org",
  "@type": "{schema_type}",
  "name": "{datos['nombre']}",
  "description": "{datos['hero_subtitulo'][:150]}",
  "telephone": "+{datos['whatsapp']}",
  "priceRange": "$$",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "{datos['ciudad'].replace(' (CDMX)', '')}",
    "addressRegion": "CDMX",
    "addressCountry": "MX"
  }},
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "{datos['rating']}",
    "reviewCount": "{datos['reseñas']}"
  }}
}}
```

## Prompts de imagen sugeridos (para renderizar con Magnific / GPT Image 2)

Usar para reemplazar las 4 imágenes de stock actuales por 6 imágenes específicas:

"""
    for i, p in enumerate(prompts, 1):
        contenido += f"{i}. {p}\n"

    contenido += f"""
## Pendientes (post-construcción)

- Verificar la dirección EXACTA del local con Google Maps y actualizar link.
- Confirmar horarios reales con el cliente.
- Si tiene reseñas reales adicionales, actualizar `reviewCount` en el JSON-LD.
- Si el profesional tiene foto en Google Maps, usarla en la sección 'Sobre nosotros'.
- Reemplazar WhatsApp genérico (escrito en el brief) por el número real del cliente cuando esté confirmado.
"""
    return contenido


def main():
    print(f"Procesando {len(WEBS_LOTE2)} webs del lote 2...\n")
    creados = 0
    for carpeta in WEBS_LOTE2:
        ruta_brief = os.path.join(BASE, carpeta, "brief_maestro.md")
        ruta_corr = os.path.join(BASE, carpeta, "_CORRECCIONES.md")
        if not os.path.exists(ruta_brief):
            print(f"--  {carpeta} (sin brief)")
            continue
        datos = parse_brief(ruta_brief)
        contenido = generar_correcciones_md(carpeta, datos)
        with open(ruta_corr, "w", encoding="utf-8") as f:
            f.write(contenido)
        print(f"OK  {carpeta}  (schema={get_schema_type(datos['nicho'])}, rating={datos['rating']}, reseñas={datos['reseñas']})")
        creados += 1
    print(f"\nTotal: {creados} archivos _CORRECCIONES.md creados.")


if __name__ == "__main__":
    main()
