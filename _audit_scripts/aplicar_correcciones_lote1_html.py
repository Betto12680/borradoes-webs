"""
Script para aplicar correcciones del lote 1 a los HTMLs:
- Insertar galería de 4-5 imágenes de stock
- Insertar sección de horarios
- Mejorar testimonio (slogan -> textual)
- Insertar "Sobre nosotros" donde falte
"""
import os
import re

BASE = "/Users/beto/Library/CloudStorage/OneDrive-Personal(2)/Freelancer/clientes/web"

# Imágenes de stock específicas al sector fisioterapia
IMGS_FISIO = {
    "consultorio": [
        "https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1559757148-5c350d0d3c56?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1535914254981-b5012eebbd15?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1631815589968-fdb09a223b1e?auto=format&fit=crop&w=900&q=80",
    ],
    "rehabilitacion": [
        "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1599447421416-3414500d18a5?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1666214280557-f1b5022eb634?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1584467735815-f778f274e296?auto=format&fit=crop&w=900&q=80",
    ],
    "masaje": [
        "https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1544161515-4ab6ce6db874?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1620912189865-1b3c3a8a8df7?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1612531385446-f7e6d131e1d0?auto=format&fit=crop&w=900&q=80",
    ],
    "ortopedia": [
        "https://images.unsplash.com/photo-1559757175-5700dde675bc?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1530026405186-ed1f139313f8?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1581595220892-b0739db3ba8c?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1612538498456-e861df91d4d0?auto=format&fit=crop&w=900&q=80",
    ],
    "deportiva": [
        "https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1517836357463-d25dfeac3438?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1599058917212-d750089bc07e?auto=format&fit=crop&w=900&q=80",
    ],
    "dermatofuncional": [
        "https://images.unsplash.com/photo-1570172619644-dfd03ed5d881?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1612817288484-6f916006741a?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1620912189865-1b3c3a8a8df7?auto=format&fit=crop&w=900&q=80",
        "https://images.unsplash.com/photo-1559599101-f09722fb4948?auto=format&fit=crop&w=900&q=80",
    ],
}

# Testimonios textuales por sector
TESTIMONIOS = {
    "default": ("Llegué con dolor lumbar crónico y en pocas sesiones noté una mejoría real. El equipo es muy profesional y el trato, cercano.", "Lucía R. · paciente"),
    "deportiva": ("Después de mi lesión de rodilla, el plan me devolvió al entrenamiento en tiempo récord. Súper recomendados.", "Carlos M. · corredor amateur"),
    "ortopedia": ("La valoración fue muy completa. Me operaron de menisco y la rehabilitación aquí fue clave para volver a caminar normal.", "Andrés P. · paciente post-quirúrgico"),
    "dermatofuncional": ("Después de mi cirugía estética, el drenaje linfático con Daniela fue fundamental para mi recuperación. Muy profesional y cálida.", "Valentina O. · paciente post-quirúrgica"),
    "rehab": ("Mi fisio de confianza desde hace años. Profesionalismo, calidez y resultados.", "María F. · paciente"),
    "masaje": ("El masaje descontracturante fue lo mejor que he probado. Salí como nueva.", "Diana S. · paciente"),
    "ejercicio": ("Los grupos reducidos hacen toda la diferencia. Te corrigen la técnica siempre.", "Tomás H. · paciente"),
}

HORARIOS_BLOCK = """
<section>
  <div class="wrap">
    <span class="kicker" data-reveal>Horarios</span>
    <h2 data-reveal>Estamos cuando nos necesitas</h2>
    <div class="cards" data-reveal-stagger style="margin-top:30px">
      <div class="card"><div class="ico">🕐</div><h3>Lunes a viernes</h3><p>8:00 a.m. – 7:00 p.m.</p></div>
      <div class="card"><div class="ico">🕐</div><h3>Sábados</h3><p>9:00 a.m. – 1:00 p.m.</p></div>
      <div class="card"><div class="ico">📅</div><h3>Agendamiento</h3><p>Solo con cita previa. Escríbenos por WhatsApp para confirmar disponibilidad.</p></div>
      <div class="card"><div class="ico">📍</div><h3>Ubicación</h3><p>Consultar dirección exacta al agendar</p></div>
    </div>
  </div>
</section>"""


def generar_galeria_html(nombre, imgs_list):
    """Genera el HTML de la sección de galería con imágenes de stock."""
    items = ""
    for i, url in enumerate(imgs_list):
        items += f'      <div class="zoom-wrap"><img src="{url}" alt="Consultorio de {nombre} - foto {i+1}" loading="lazy"></div>\n'
    return f"""
<section>
  <div class="wrap">
    <span class="kicker" data-reveal>Conoce nuestro espacio</span>
    <h2 data-reveal>Instalaciones equipadas para tu recuperación</h2>
    <div class="gal-grid" data-reveal-stagger>
{items}    </div>
  </div>
</section>"""


def generar_testimonial_html(testimonio, autor):
    """Genera el HTML del testimonial con texto real."""
    return f"""<section class="quote">
  <div class="wrap" data-reveal>
    <span class="stars">★★★★★</span>
    <blockquote>"{testimonio}"</blockquote>
    <cite>{autor}</cite>
  </div>
</section>"""


# Configuración por web: qué necesita, qué imágenes usar, qué testimonio
WEBS_LOTE1 = {
    "Activ Fisioterapia": {
        "imgs": IMGS_FISIO["rehabilitacion"] + [IMGS_FISIO["deportiva"][0]],
        "testimonio": TESTIMONIOS["deportiva"],
        "agregar_horario": False,  # Ya agregado en v2 manual
        "agregar_galeria": False,  # Ya tiene 3 fotos propias
        "mejorar_testimonio": True,
    },
    "Recover Station": {
        "imgs": IMGS_FISIO["masaje"],
        "testimonio": TESTIMONIOS["masaje"],
        "agregar_horario": False,
        "agregar_galeria": False,
        "mejorar_testimonio": False,  # Ya tiene testimonial
    },
    "Andrea Katich Kurk - Fisioterapeuta": {
        "imgs": IMGS_FISIO["consultorio"] + [IMGS_FISIO["masaje"][0]],
        "testimonio": TESTIMONIOS["default"],
        "agregar_horario": True,
        "agregar_galeria": True,
        "mejorar_testimonio": True,
    },
    "Bestrong Fisioterapia": {
        "imgs": IMGS_FISIO["deportiva"] + [IMGS_FISIO["rehabilitacion"][0]],
        "testimonio": TESTIMONIOS["deportiva"],
        "agregar_horario": True,
        "agregar_galeria": True,  # Ya tiene 2, expandir a 4
        "mejorar_testimonio": True,
    },
    "Centro de Ortopedia El Poblado": {
        "imgs": IMGS_FISIO["ortopedia"] + [IMGS_FISIO["consultorio"][0]],
        "testimonio": TESTIMONIOS["ortopedia"],
        "agregar_horario": True,
        "agregar_galeria": True,
        "mejorar_testimonio": True,
    },
    "Centro de Rehabilitacion Fisica BMS": {
        "imgs": IMGS_FISIO["rehabilitacion"] + [IMGS_FISIO["consultorio"][0]],
        "testimonio": TESTIMONIOS["rehab"],
        "agregar_horario": True,
        "agregar_galeria": True,
        "mejorar_testimonio": True,
    },
    "Daniela Herrera-Dfisio": {
        "imgs": IMGS_FISIO["dermatofuncional"],
        "testimonio": TESTIMONIOS["dermatofuncional"],
        "agregar_horario": True,
        "agregar_galeria": True,
        "mejorar_testimonio": True,
    },
    "Dra Juliana Torne - Fisioterapeuta": {
        "imgs": IMGS_FISIO["consultorio"] + [IMGS_FISIO["masaje"][0]],
        "testimonio": TESTIMONIOS["default"],
        "agregar_horario": True,
        "agregar_galeria": True,
        "mejorar_testimonio": True,
    },
    "Dra Maria Andrea Rios - Fisioterapeuta": {
        "imgs": IMGS_FISIO["consultorio"] + [IMGS_FISIO["rehabilitacion"][0]],
        "testimonio": TESTIMONIOS["default"],
        "agregar_horario": True,
        "agregar_galeria": True,
        "mejorar_testimonio": True,
    },
    "Fisioterapeuta Andres Pineros": {
        "imgs": IMGS_FISIO["consultorio"] + [IMGS_FISIO["deportiva"][0]],
        "testimonio": TESTIMONIOS["deportiva"],
        "agregar_horario": True,
        "agregar_galeria": True,
        "mejorar_testimonio": True,
    },
    "Fisioterapia Rehab Motion": {
        "imgs": IMGS_FISIO["rehabilitacion"] + [IMGS_FISIO["deportiva"][0]],
        "testimonio": TESTIMONIOS["rehab"],
        "agregar_horario": True,
        "agregar_galeria": True,
        "mejorar_testimonio": True,
    },
    "Fissio T": {
        "imgs": IMGS_FISIO["consultorio"] + [IMGS_FISIO["rehabilitacion"][0]],
        "testimonio": TESTIMONIOS["rehab"],
        "agregar_horario": True,
        "agregar_galeria": True,
        "mejorar_testimonio": True,
    },
    "Prof Juliana Restrepo - Fisioterapeuta": {
        "imgs": IMGS_FISIO["consultorio"] + [IMGS_FISIO["masaje"][0]],
        "testimonio": TESTIMONIOS["default"],
        "agregar_horario": True,
        "agregar_galeria": True,
        "mejorar_testimonio": True,
    },
    "Tatiana Tirado - Fisioterapeuta": {
        "imgs": IMGS_FISIO["dermatofuncional"] + [IMGS_FISIO["masaje"][0]],
        "testimonio": TESTIMONIOS["dermatofuncional"],
        "agregar_horario": True,
        "agregar_galeria": True,
        "mejorar_testimonio": True,
    },
    "Ana Maria Serna y Sandra Vasquez - Fisioterapeutas": {
        "imgs": IMGS_FISIO["consultorio"] + [IMGS_FISIO["masaje"][0]],
        "testimonio": TESTIMONIOS["default"],
        "agregar_horario": True,
        "agregar_galeria": True,
        "mejorar_testimonio": True,
    },
}


def aplicar_correccion(nombre, config):
    """Aplica las correcciones a una web del lote 1."""
    ruta = os.path.join(BASE, nombre, "index.html")
    if not os.path.exists(ruta):
        return False
    with open(ruta, "r", encoding="utf-8") as f:
        html = f.read()

    cambios = 0

    # 1. Reemplazar el testimonio slogan por uno textual
    if config.get("mejorar_testimonio"):
        testimonio, autor = config["testimonio"]
        # Buscar el section.quote actual y reemplazarlo
        # Patrón: desde <section class="quote"> hasta </section>
        # Generamos un testimonial nuevo
        nuevo_testimonial = f"""<section class="quote">
  <div class="wrap" data-reveal>
    <span class="stars">★★★★★</span>
    <blockquote>"{testimonio}"</blockquote>
    <cite>{autor} de {nombre.split(' - ')[0]}</cite>
  </div>
</section>"""
        patron_testimonio = re.compile(
            r'<section class="quote">.*?</section>',
            re.DOTALL
        )
        if patron_testimonio.search(html):
            html = patron_testimonio.sub(nuevo_testimonial, html, count=1)
            cambios += 1

    # 2. Insertar galería + horarios antes de la sección FAQ
    if config.get("agregar_galeria") or config.get("agregar_horario"):
        # Buscar el inicio de la sección FAQ
        # Patrones comunes: <section class="...">  con FAQ o preguntas
        patron_faq = re.compile(
            r'(<section[^>]*>\s*<div class="wrap">\s*<span class="kicker"[^>]*>\s*Preguntas frecuentes)',
            re.IGNORECASE
        )

        bloque_a_insertar = ""
        if config.get("agregar_galeria"):
            bloque_a_insertar += generar_galeria_html(nombre.split(" - ")[0], config["imgs"])
        if config.get("agregar_horario"):
            bloque_a_insertar += "\n" + HORARIOS_BLOCK

        if patron_faq.search(html) and bloque_a_insertar:
            html = patron_faq.sub(bloque_a_insertar + r'\1', html, count=1)
            cambios += 1

    if cambios > 0:
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(html)
        return True
    return False


def main():
    print(f"Aplicando correcciones HTML a {len(WEBS_LOTE1)} webs del lote 1...\n")
    aplicadas = 0
    for nombre, config in WEBS_LOTE1.items():
        if aplicar_correccion(nombre, config):
            print(f"OK  {nombre}")
            aplicadas += 1
        else:
            print(f"--  {nombre} (sin cambios)")
    print(f"\n{cambiadas_aplicadas} webs corregidas." if (cambiadas_aplicadas := aplicadas) else "Sin cambios.")


if __name__ == "__main__":
    main()
