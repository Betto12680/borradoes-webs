#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline 2: Generador Automático de Webs Borrador y Despliegue en GitHub Pages
Ejecución diaria: 8:00 AM
"""

import os
import re
import sys
import shutil
import subprocess
import openpyxl
from datetime import datetime

BASE_DIR = '/Users/beto/Library/CloudStorage/OneDrive-Personal(2)/Freelancer/clientes/web'
EXCEL_PATH = os.path.join(BASE_DIR, 'Clientes.xlsx')

def slugify(text):
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

def get_niche_template(nombre, tipo, ciudad, tel, resenas, rating, url_demo):
    tipo_lower = str(tipo).lower()
    nombre_lower = str(nombre).lower()
    
    # Colores por defecto según nicho
    if 'odont' in tipo_lower or 'denti' in tipo_lower or 'sonris' in nombre_lower:
        primary = "#0284c7" # Teal / Azul Médico
        accent = "#0ea5e9"
        nicho = "Odontología"
        hero_title = f"Tu Sonrisa en Manos de Especialistas en {ciudad}"
        hero_sub = f"Atención odontológica integral, estética y prevención con la más alta calidad en {ciudad}."
        servicios = [
            ("Diseño de Sonrisa", "Tratamientos estéticos avanzados para lograr la sonrisa natural y brillante que deseas."),
            ("Ortodoncia e Implantes", "Alineación dental y restauración con tecnología de última generación."),
            ("Limpieza y Profilaxis", "Cuidado preventivo profundo para mantener tus dientes y encías sanas."),
            ("Odontología General", "Atención personalizada para toda la familia con el mejor confort.")
        ]
        faqs = [
            ("¿Cómo agendar mi primera cita de valoración?", "Puedes hacer clic en el botón de WhatsApp y nuestro equipo te asignará la fecha y hora disponible de inmediato."),
            ("¿Aceptan urgencias odontológicas?", "Sí, atendemos emergencias dentales con prioridad según disponibilidad de agenda."),
            ("¿Qué métodos de pago manejan?", "Aceptamos efectivo, transferencias bancarias y tarjetas de crédito/débito."),
            ("¿Realizan tratamientos para niños?", "Contamos con odontopediatría especializada para la atención cómoda de los más pequeños.")
        ]
    elif 'glamp' in tipo_lower or 'hotel' in tipo_lower or 'hospedaj' in tipo_lower or 'cabañ' in tipo_lower:
        primary = "#059669" # Verde Naturaleza / Esmeralda
        accent = "#10b981"
        nicho = "Hospedaje & Glamping"
        hero_title = f"Una Experiencia Inolvidable de Descanso en {ciudad}"
        hero_sub = f"Desconéctate de la rutina y disfruta de la naturaleza con el máximo confort y privacidad."
        servicios = [
            ("Alojamiento Exclusivo", "Domos y cabañas totalmente equipadas con vistas panorámicas increíbles."),
            ("Zona de Fogata y Jacuzzi", "Espacios diseñados para relajarte bajo las estrellas con tu pareja o familia."),
            ("Desayunos Campestres", "Gastronomía local preparada con ingredientes frescos de la región."),
            ("Actividades al Aire Libre", "Caminatas ecológicas, avistamiento de aves y recorridos por el paisaje.")
        ]
        faqs = [
            ("¿Cómo puedo consultar disponibilidad y tarifas?", "Haz clic en nuestro botón directo de WhatsApp para responderte en tiempo real con las fechas disponibles."),
            ("¿El alojamiento incluye desayuno?", "Sí, todos nuestros planes incluyen desayuno campestre para dos personas."),
            ("¿Aceptan mascotas (Pet Friendly)?", "Contamos con políticas pet friendly en alojamientos seleccionados."),
            ("¿Qué actividades hay cerca?", "Ofrecemos orientación sobre miradores, senderos ecológicos y atractivos turísticos cercanos.")
        ]
    elif 'fisio' in tipo_lower or 'rehab' in tipo_lower or 'terap' in tipo_lower:
        primary = "#14436c" # Azul Marino Fisioterapia
        accent = "#2ecfb4"
        nicho = "Fisioterapia & Rehabilitación"
        hero_title = f"Alivio del Dolor y Recuperación Física en {ciudad}"
        hero_sub = f"Tratamientos personalizados para devolverte la movilidad y calidad de vida que mereces."
        servicios = [
            ("Rehabilitación Deportiva", "Recuperación acelerada de lesiones musculares y articulares para atletas."),
            ("Fisioterapia Traumatológica", "Tratamiento post-quirúrgico y recuperación de fracturas o esguinces."),
            ("Manejo del Dolor Crónico", "Técnicas avanzadas para aliviar dolores de espalda, cuello y articulaciones."),
            ("Atención a Domicilio", "Sesiones personalizadas en la comodidad de tu hogar con equipos especializados.")
        ]
        faqs = [
            ("¿Necesito orden médica para iniciar tratamiento?", "No es estrictamente necesario. Realizamos una evaluación inicial completa en tu primera sesión."),
            ("¿Cuánto dura cada sesión de fisioterapia?", "Las sesiones tienen una duración aproximada de 45 a 60 minutos según el tratamiento."),
            ("¿Atienden a domicilio?", "Sí, contamos con servicio de fisioterapia domiciliaria adaptada a tus necesidades."),
            ("¿Cómo agendar mi cita?", "Toca el botón de WhatsApp y te asignaremos cita en el horario que mejor te convenga.")
        ]
    else:
        primary = "#2563eb" # Azul Profesional
        accent = "#3b82f6"
        nicho = "Servicios Profesionales"
        hero_title = f"Soluciones Profesionales de Calidad en {ciudad}"
        hero_sub = f"Atención garantizada y excelencia en servicios para clientes exigentes en {ciudad}."
        servicios = [
            ("Atención Personalizada", "Asesoría directa adaptada a los requerimientos específicos de cada cliente."),
            ("Garantía de Calidad", "Procesos respaldados por profesionales con amplia experiencia."),
            ("Respuesta Rápida", "Comunicación fluida y solución ágil a tus solicitudes."),
            ("Cotizaciones Transparentes", "Precios justos y sin costos ocultos.")
        ]
        faqs = [
            ("¿Cómo puedo solicitar una cotización?", "Haz clic en el botón de WhatsApp y déjanos tus datos para enviarte una propuesta detallada."),
            ("¿Cuáles son sus horarios de atención?", "Atendemos de lunes a sábado de 8:00 AM a 6:00 PM."),
            ("¿Dónde están ubicados?", f"Estamos ubicados en {ciudad} con atención presencial y digital."),
            ("¿Qué métodos de pago reciben?", "Transferencias electrónicas, efectivo y pagos digitales seguros.")
        ]

    rating_str = str(rating) if rating and str(rating) != 'N/D' else "4.9"
    resenas_str = str(resenas) if resenas and str(resenas) != 'N/D' else "50"
    tel_clean = re.sub(r'\D', '', str(tel)) if tel and str(tel) != 'N/D' else "573104816153"
    if not tel_clean.startswith('57'): tel_clean = '57' + tel_clean

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{nombre} — {nicho} en {ciudad}</title>
  <meta name="description" content="{nombre}: {hero_sub}">
  <meta name="robots" content="index, follow">
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    :root {{
      --primary: {primary};
      --accent: {accent};
      --bg: #0f172a;
      --card-bg: #1e293b;
      --text: #f8fafc;
      --text-muted: #94a3b8;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Inter', sans-serif; background: var(--bg); color: var(--text); line-height: 1.6; }}
    .container {{ max-width: 1100px; margin: 0 auto; padding: 0 20px; }}
    nav {{ background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(10px); position: fixed; width: 100%; top: 0; z-index: 100; padding: 20px 0; border-bottom: 1px solid #334155; }}
    .nav-inner {{ display: flex; justify-content: space-between; align-items: center; }}
    .logo {{ font-size: 1.25rem; font-weight: 800; color: #fff; text-decoration: none; }}
    .btn-wa {{ background: #25d366; color: #fff; text-decoration: none; padding: 10px 20px; border-radius: 8px; font-weight: 700; display: inline-flex; align-items: center; gap: 8px; transition: transform 0.2s; }}
    .btn-wa:hover {{ transform: scale(1.04); }}
    
    header.hero {{ padding: 160px 0 90px; text-align: center; background: radial-gradient(circle at center, rgba(37,99,235,0.15) 0%, transparent 70%); }}
    .badge-rating {{ display: inline-block; background: #334155; color: #f59e0b; padding: 6px 16px; border-radius: 20px; font-weight: 600; font-size: 0.9rem; margin-bottom: 24px; }}
    h1 {{ font-size: 2.8rem; font-weight: 800; max-width: 800px; margin: 0 auto 20px; line-height: 1.2; }}
    p.lead {{ font-size: 1.15rem; color: var(--text-muted); max-width: 650px; margin: 0 auto 36px; }}
    
    .grid-services {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 24px; margin: 60px 0; }}
    .card-service {{ background: var(--card-bg); border: 1px solid #334155; padding: 28px; border-radius: 16px; transition: border-color 0.2s; }}
    .card-service:hover {{ border-color: var(--primary); }}
    .card-service h3 {{ font-size: 1.2rem; margin-bottom: 12px; color: #fff; }}
    .card-service p {{ color: var(--text-muted); font-size: 0.95rem; }}
    
    .faq-section {{ margin: 80px 0; }}
    .faq-item {{ background: var(--card-bg); border: 1px solid #334155; border-radius: 12px; margin-bottom: 16px; padding: 20px; }}
    .faq-item summary {{ font-weight: 700; cursor: pointer; list-style: none; font-size: 1.05rem; display: flex; justify-content: space-between; }}
    .faq-item p {{ margin-top: 12px; color: var(--text-muted); font-size: 0.95rem; }}
    
    footer {{ text-align: center; padding: 40px 0; border-top: 1px solid #334155; color: var(--text-muted); font-size: 0.9rem; margin-top: 80px; }}
  </style>
</head>
<body>

  <nav>
    <div class="container nav-inner">
      <a href="#" class="logo">{nombre}</a>
      <a href="https://wa.me/{tel_clean}?text=Hola%20{nombre},%20me%20gustar%C3%ADa%20solicitar%20informaci%C3%B3n" class="btn-wa" target="_blank">💬 Agendar por WhatsApp</a>
    </div>
  </nav>

  <header class="hero">
    <div class="container">
      <div class="badge-rating">⭐ {rating_str} en Google Maps ({resenas_str} opiniones)</div>
      <h1>{hero_title}</h1>
      <p class="lead">{hero_sub}</p>
      <a href="https://wa.me/{tel_clean}?text=Hola%20{nombre},%20quiero%20m%C3%A1s%20informaci%C3%B3n" class="btn-wa" style="padding: 14px 28px; font-size: 1.1rem;" target="_blank">👉 Contactar por WhatsApp Ahora</a>
    </div>
  </header>

  <section class="container">
    <h2 style="text-align: center; font-size: 2rem;">Nuestros Servicios Principales</h2>
    <div class="grid-services">
"""
    for s_title, s_desc in servicios:
        html += f"""
      <div class="card-service">
        <h3>{s_title}</h3>
        <p>{s_desc}</p>
      </div>"""

    html += f"""
    </div>
  </section>

  <section class="container faq-section">
    <h2 style="text-align: center; font-size: 2rem; margin-bottom: 30px;">Preguntas Frecuentes</h2>
"""
    for q_title, q_ans in faqs:
        html += f"""
    <details class="faq-item">
      <summary>{q_title}</summary>
      <p>{q_ans}</p>
    </details>"""

    html += f"""
  </section>

  <footer>
    <div class="container">
      <p>&copy; {datetime.now().year} {nombre} — {ciudad}, Colombia/LATAM.</p>
    </div>
  </footer>

</body>
</html>
"""
    return html

def build_pending_sites():
    print("=== PIPELINE 2: GENERADOR AUTOMÁTICO DE WEBS BORRADOR ===")
    if not os.path.exists(EXCEL_PATH):
        print(f"Error: No se encontró el archivo {EXCEL_PATH}")
        return

    wb = openpyxl.load_workbook(EXCEL_PATH)
    sheet = wb['EMPRESAS MAPS']
    rows = list(sheet.iter_rows(values_only=False))

    header = [cell.value for cell in rows[0]]
    pending_count = 0

    for idx, r in enumerate(rows[1:], start=2):
        vals = [cell.value for cell in r]
        if not any(vals): continue
        nombre = vals[0]
        ciudad = vals[1]
        tipo = vals[2]
        correo = vals[3]
        tel = vals[4]
        resenas = vals[6]
        rating = vals[7]
        estado = str(vals[9]) if len(vals) > 9 and vals[9] else ''

        if 'PENDIENTE_BORRADOR' in estado or estado == 'Prospecto' or 'PENDIENTE' in estado:
            slug = slugify(str(nombre))
            if not slug: continue
            
            site_dir = os.path.join(BASE_DIR, slug)
            os.makedirs(site_dir, exist_ok=True)
            
            demo_url = f"https://betto12680.github.io/borradoes-webs/{slug}/"
            html_content = get_niche_template(nombre, tipo, ciudad, tel, resenas, rating, demo_url)
            
            with open(os.path.join(site_dir, 'index.html'), 'w', encoding='utf-8') as f:
                f.write(html_content)
                
            # Actualizar estado en el Excel
            nuevo_estado = f"WEB_BORRADOR_LISTA | LINK: {demo_url}"
            sheet.cell(row=idx, column=10, value=nuevo_estado)
            print(f"✔ Web borrador generada para: {nombre} -> {demo_url}")
            pending_count += 1

    if pending_count > 0:
        wb.save(EXCEL_PATH)
        print(f"\n{pending_count} sitios webs generados. Desplegando en GitHub Pages...")
        
        # Git Commit & Push
        try:
            subprocess.run(["git", "add", "."], cwd=BASE_DIR, check=True)
            subprocess.run(["git", "commit", "-m", f"Automático: Despliegue diario de {pending_count} webs borrador"], cwd=BASE_DIR, check=True)
            subprocess.run(["git", "push"], cwd=BASE_DIR, check=True)
            print("✔ Despliegue en GitHub completado con éxito.")
        except Exception as e:
            print(f"Error en Git push: {e}")
    else:
        print("No hay empresas pendientes para generar borrador web hoy.")

if __name__ == "__main__":
    build_pending_sites()
