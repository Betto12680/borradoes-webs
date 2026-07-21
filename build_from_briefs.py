#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import subprocess
import glob

BASE_DIR = '/Users/beto/Library/CloudStorage/OneDrive-Personal(2)/Freelancer/clientes/web'

def parse_brief(brief_content):
    data = {}
    
    # 1. Info
    m_nombre = re.search(r'\*\*Nombre\*\*:\s*(.+)', brief_content)
    data['nombre'] = m_nombre.group(1).strip() if m_nombre else 'Clínica'
    
    m_nicho = re.search(r'\*\*Nicho\*\*:\s*(.+)', brief_content)
    data['nicho'] = m_nicho.group(1).strip() if m_nicho else 'Salud'
    
    m_ciudad = re.search(r'\*\*Ciudad\*\*:\s*(.+)', brief_content)
    data['ciudad'] = m_ciudad.group(1).strip() if m_ciudad else 'CDMX'
    
    m_tel = re.search(r'\*\*Teléfono de Contacto\*\*:.*?\(WhatsApp:\s*(\d+)\)', brief_content)
    data['tel_wa'] = m_tel.group(1).strip() if m_tel else '525555551234'
    
    m_rating = re.search(r'\*\*Calificación.*?\*\*:\s*([\d\.]+)', brief_content)
    data['rating'] = m_rating.group(1).strip() if m_rating else '4.9'
    
    m_resenas = re.search(r'\*\*Cantidad de Reseñas\*\*:\s*(\d+)', brief_content)
    data['resenas'] = m_resenas.group(1).strip() if m_resenas else '50'

    # 2. Colors
    m_primary = re.search(r'\*\*Primario\*\*:\s*(#[A-Fa-f0-9]{6})', brief_content)
    data['primary'] = m_primary.group(1) if m_primary else '#2563eb'
    
    m_secondary = re.search(r'\*\*Secundario\*\*:\s*(#[A-Fa-f0-9]{6})', brief_content)
    data['secondary'] = m_secondary.group(1) if m_secondary else '#60a5fa'
    
    m_dark = re.search(r'\*\*Fondo Oscuro \(Hero\)\*\*:\s*(#[A-Fa-f0-9]{6})', brief_content)
    data['dark_bg'] = m_dark.group(1) if m_dark else '#1e3a8a'

    # 3. Images
    m_hero_img = re.search(r'\*\*Hero Image\*\*:\s*(https://[^\s\)]+)', brief_content)
    data['hero_img'] = m_hero_img.group(1) if m_hero_img else ''
    
    imgs = []
    for m in re.finditer(r'\*\*Carrusel \d+\*\*:\s*(https://[^\s\)]+)', brief_content):
        imgs.append(m.group(1))
    data['carousel_imgs'] = imgs if imgs else [data['hero_img']]

    # 4. Texts
    m_hero_title = re.search(r'\*\*Hero Titular\*\*:\s*(.+)', brief_content)
    data['hero_title'] = m_hero_title.group(1).strip() if m_hero_title else 'Atención Especializada'
    
    m_hero_sub = re.search(r'\*\*Hero Subtítulo\*\*:\s*(.+)', brief_content)
    data['hero_sub'] = m_hero_sub.group(1).strip() if m_hero_sub else 'La mejor atención.'
    
    # Extract Services
    servicios = []
    lines = brief_content.splitlines()
    in_services = False
    for line in lines:
        if '**Servicios Principales**' in line:
            in_services = True
            continue
        if in_services:
            if line.strip() == '' or line.startswith('---'):
                break
            m_srv = re.match(r'\s*\d+\.\s*(.+)', line)
            if m_srv:
                servicios.append(m_srv.group(1).strip())
    data['servicios'] = servicios if servicios else ['Consulta Especializada', 'Tratamiento Integral', 'Diagnóstico Preciso', 'Atención Premium']

    return data

def generate_html(data):
    # Base background (very dark blue/slate, NEVER black to respect instructions)
    bg_color = "#070f1a"
    card_bg = "#0e1828"
    border = "#1a2a40"

    # Services HTML
    servicios_html = ""
    icon_map = ['🩺', '🔬', '🛡️', '✨', '💎', '🧠', '🧘']
    for idx, srv in enumerate(data['servicios']):
        icon = icon_map[idx % len(icon_map)]
        servicios_html += f"""
        <div class="srv-card fade-in-up">
            <div class="srv-icon">{icon}</div>
            <h3>{srv}</h3>
            <p>Tratamiento especializado con tecnología de vanguardia y atención personalizada para garantizar tu bienestar en {data['ciudad']}.</p>
            <div class="tags"><span class="tag">Especializado</span><span class="tag">Seguro</span></div>
            <a href="https://wa.me/{data['tel_wa']}?text=Hola,%20me%20interesa%20el%20servicio%20de%20{srv}" class="btn-outline">Consultar Detalles</a>
        </div>"""

    # Carousel HTML
    carousel_html = ""
    for idx, img in enumerate(data['carousel_imgs']):
        active = 'active' if idx == 0 else ''
        carousel_html += f"""<div class="carousel-slide {active}"><img src="{img}" alt="Instalaciones {data['nombre']}"></div>"""

    html = f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{data['nombre']} | {data['nicho']}</title>
    <meta name="description" content="{data['hero_sub']}">
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary: {data['primary']};
            --secondary: {data['secondary']};
            --dark-bg: {data['dark_bg']};
            --bg: {bg_color};
            --card-bg: {card_bg};
            --border: {border};
            --text: #f8fafc;
            --text-muted: #94a3b8;
        }}
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}
        body {{ font-family: 'Plus Jakarta Sans', sans-serif; background-color: var(--bg); color: var(--text); overflow-x: hidden; }}
        
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 24px; }}
        
        /* Navbar Glassmorphism */
        nav {{ position: fixed; top: 0; width: 100%; z-index: 1000; background: rgba(7, 15, 26, 0.7); backdrop-filter: blur(12px); -webkit-backdrop-filter: blur(12px); border-bottom: 1px solid rgba(255,255,255,0.05); padding: 16px 0; transition: all 0.3s ease; }}
        .nav-content {{ display: flex; justify-content: space-between; align-items: center; }}
        .brand {{ font-size: 1.5rem; font-weight: 800; color: #fff; text-decoration: none; }}
        .brand span {{ color: var(--secondary); }}
        .btn-wa-header {{ background: var(--primary); color: #fff; padding: 10px 24px; border-radius: 50px; text-decoration: none; font-weight: 700; transition: all 0.3s ease; box-shadow: 0 4px 15px rgba(0,0,0,0.2); }}
        .btn-wa-header:hover {{ background: var(--secondary); transform: translateY(-2px); }}

        /* Hero Split Layout */
        .hero {{ padding: 140px 0 80px; background: radial-gradient(circle at top left, var(--dark-bg) 0%, var(--bg) 70%); }}
        .hero-grid {{ display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 40px; align-items: center; }}
        .hero-badge {{ display: inline-flex; background: rgba(255,255,255,0.1); padding: 8px 16px; border-radius: 20px; font-weight: 700; color: var(--secondary); margin-bottom: 24px; font-size: 0.9rem; border: 1px solid rgba(255,255,255,0.1); }}
        .hero h1 {{ font-size: 3.5rem; font-weight: 800; line-height: 1.1; margin-bottom: 24px; }}
        .hero h1 span {{ color: var(--secondary); }}
        .hero p {{ font-size: 1.1rem; color: var(--text-muted); margin-bottom: 32px; line-height: 1.6; }}
        .hero-cta {{ display: flex; gap: 16px; align-items: center; }}
        .btn-primary {{ background: #25d366; color: #fff; padding: 16px 32px; border-radius: 50px; text-decoration: none; font-weight: 800; font-size: 1.1rem; transition: all 0.3s ease; box-shadow: 0 8px 24px rgba(37, 211, 102, 0.3); }}
        .btn-primary:hover {{ transform: translateY(-3px); box-shadow: 0 12px 32px rgba(37, 211, 102, 0.5); }}
        .hero-rating {{ display: flex; align-items: center; gap: 12px; margin-top: 32px; font-size: 0.9rem; color: var(--text-muted); }}
        .hero-rating strong {{ color: #fbbf24; font-size: 1.1rem; }}
        
        .hero-image-wrap {{ position: relative; border-radius: 24px; overflow: hidden; box-shadow: 0 24px 48px rgba(0,0,0,0.4); border: 1px solid rgba(255,255,255,0.1); }}
        .hero-image-wrap img {{ width: 100%; height: 500px; object-fit: cover; display: block; }}
        
        /* Stats Bar */
        .stats {{ background: var(--card-bg); padding: 40px 0; border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); text-align: center; gap: 20px; }}
        .stat-item h3 {{ font-size: 2.5rem; color: var(--secondary); font-weight: 800; margin-bottom: 8px; }}
        .stat-item p {{ font-size: 0.9rem; color: var(--text-muted); font-weight: 600; text-transform: uppercase; letter-spacing: 1px; }}

        /* Services Cards */
        .section-title {{ text-align: center; margin-bottom: 50px; }}
        .section-title h2 {{ font-size: 2.5rem; font-weight: 800; margin-bottom: 16px; }}
        .section-title p {{ color: var(--text-muted); max-width: 600px; margin: 0 auto; }}
        .services {{ padding: 100px 0; }}
        .srv-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; }}
        .srv-card {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 20px; padding: 32px; transition: all 0.3s ease; position: relative; overflow: hidden; }}
        .srv-card:hover {{ transform: translateY(-10px); border-color: var(--secondary); box-shadow: 0 20px 40px rgba(0,0,0,0.3); }}
        .srv-icon {{ font-size: 2.5rem; margin-bottom: 24px; background: rgba(255,255,255,0.05); width: 64px; height: 64px; display: flex; align-items: center; justify-content: center; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); }}
        .srv-card h3 {{ font-size: 1.3rem; margin-bottom: 16px; font-weight: 700; }}
        .srv-card p {{ color: var(--text-muted); font-size: 0.95rem; margin-bottom: 24px; line-height: 1.6; }}
        .tags {{ display: flex; gap: 8px; margin-bottom: 24px; }}
        .tag {{ font-size: 0.75rem; background: rgba(255,255,255,0.05); padding: 4px 10px; border-radius: 20px; color: var(--secondary); border: 1px solid rgba(255,255,255,0.1); }}
        .btn-outline {{ display: block; text-align: center; border: 1px solid var(--border); padding: 12px; border-radius: 12px; color: #fff; text-decoration: none; font-weight: 600; font-size: 0.9rem; transition: all 0.3s; }}
        .btn-outline:hover {{ background: var(--secondary); border-color: var(--secondary); }}

        /* Carousel JS Native */
        .carousel-sec {{ padding: 100px 0; background: var(--card-bg); border-top: 1px solid var(--border); border-bottom: 1px solid var(--border); }}
        .carousel-wrap {{ position: relative; max-width: 900px; margin: 0 auto; border-radius: 24px; overflow: hidden; box-shadow: 0 20px 50px rgba(0,0,0,0.5); border: 1px solid rgba(255,255,255,0.1); }}
        .carousel-slide {{ display: none; width: 100%; height: 500px; }}
        .carousel-slide.active {{ display: block; animation: fade 0.8s ease-in-out; }}
        .carousel-slide img {{ width: 100%; height: 100%; object-fit: cover; }}
        @keyframes fade {{ from {{opacity: 0.4}} to {{opacity: 1}} }}
        .car-btn {{ position: absolute; top: 50%; transform: translateY(-50%); background: rgba(0,0,0,0.6); color: white; border: 1px solid rgba(255,255,255,0.2); width: 48px; height: 48px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; backdrop-filter: blur(4px); transition: all 0.3s; }}
        .car-btn:hover {{ background: var(--primary); }}
        .car-prev {{ left: 20px; }}
        .car-next {{ right: 20px; }}

        /* FAQs */
        .faqs {{ padding: 100px 0; }}
        .faq-wrap {{ max-width: 800px; margin: 0 auto; }}
        .faq-item {{ background: var(--card-bg); border: 1px solid var(--border); border-radius: 16px; margin-bottom: 16px; }}
        .faq-item summary {{ padding: 24px; font-size: 1.1rem; font-weight: 700; cursor: pointer; list-style: none; display: flex; justify-content: space-between; }}
        .faq-item summary::-webkit-details-marker {{ display: none; }}
        .faq-item summary::after {{ content: '+'; color: var(--secondary); font-size: 1.5rem; }}
        .faq-item[open] summary::after {{ content: '−'; }}
        .faq-item p {{ padding: 0 24px 24px; color: var(--text-muted); border-top: 1px solid rgba(255,255,255,0.05); margin-top: 8px; padding-top: 16px; }}

        /* Floating WhatsApp */
        .wa-float {{ position: fixed; bottom: 30px; right: 30px; background: #25d366; width: 64px; height: 64px; border-radius: 50%; display: flex; justify-content: center; align-items: center; font-size: 2rem; color: white; text-decoration: none; box-shadow: 0 10px 24px rgba(37, 211, 102, 0.4); z-index: 999; }}
        .wa-float::before {{ content: ''; position: absolute; inset: 0; border-radius: 50%; border: 2px solid #25d366; animation: waPulse 2s infinite; }}
        @keyframes waPulse {{ 0% {{ transform: scale(1); opacity: 1; }} 100% {{ transform: scale(1.6); opacity: 0; }} }}

        /* Scroll Animations */
        .fade-in-up {{ opacity: 0; transform: translateY(30px); transition: opacity 0.8s ease, transform 0.8s ease; }}
        .fade-in-up.visible {{ opacity: 1; transform: translateY(0); }}
        
        footer {{ text-align: center; padding: 40px 0; border-top: 1px solid var(--border); color: var(--text-muted); font-size: 0.9rem; }}
        
        @media(max-width: 900px) {{
            .hero-grid {{ grid-template-columns: 1fr; text-align: center; }}
            .hero-cta {{ justify-content: center; }}
            .hero-rating {{ justify-content: center; }}
            .stats-grid {{ grid-template-columns: 1fr 1fr; }}
            .carousel-slide {{ height: 350px; }}
        }}
    </style>
</head>
<body>

    <!-- Nav -->
    <nav>
        <div class="container nav-content">
            <a href="#" class="brand">{data['nombre']}</a>
            <a href="https://wa.me/{data['tel_wa']}" class="btn-wa-header" target="_blank">Contactar</a>
        </div>
    </nav>

    <!-- Hero -->
    <header class="hero">
        <div class="container hero-grid">
            <div class="hero-text fade-in-up">
                <div class="hero-badge">Atención Especializada en {data['ciudad']}</div>
                <h1>{data['hero_title']}</h1>
                <p>{data['hero_sub']}</p>
                <div class="hero-cta">
                    <a href="https://wa.me/{data['tel_wa']}?text=Hola,%20deseo%20agendar%20una%20cita" class="btn-primary" target="_blank">Agendar Cita por WhatsApp</a>
                </div>
                <div class="hero-rating">
                    <span>⭐ <strong>{data['rating']} / 5.0</strong></span>
                    <span>Basado en {data['resenas']} reseñas de pacientes reales</span>
                </div>
            </div>
            <div class="hero-image-wrap fade-in-up" style="transition-delay: 0.2s;">
                <img src="{data['hero_img']}" alt="{data['nombre']}">
            </div>
        </div>
    </header>

    <!-- Stats -->
    <section class="stats">
        <div class="container stats-grid">
            <div class="stat-item fade-in-up"><h3 class="counter" data-target="1500">0</h3><p>Pacientes</p></div>
            <div class="stat-item fade-in-up"><h3 class="counter" data-target="15">0</h3><p>Años Exp.</p></div>
            <div class="stat-item fade-in-up"><h3>100%</h3><p>Compromiso</p></div>
            <div class="stat-item fade-in-up"><h3>{data['rating']}</h3><p>Estrellas</p></div>
        </div>
    </section>

    <!-- Services -->
    <section class="services container">
        <div class="section-title fade-in-up">
            <h2>Nuestros Servicios</h2>
            <p>Descubre todo lo que {data['nombre']} tiene para ofrecerte con la más alta calidad y calidez humana.</p>
        </div>
        <div class="srv-grid">
            {servicios_html}
        </div>
    </section>

    <!-- Carousel -->
    <section class="carousel-sec">
        <div class="container">
            <div class="section-title fade-in-up">
                <h2>Instalaciones de Vanguardia</h2>
                <p>Espacios diseñados para tu máximo confort y bioseguridad.</p>
            </div>
            <div class="carousel-wrap fade-in-up">
                {carousel_html}
                <button class="car-btn car-prev" onclick="moveSlide(-1)">❮</button>
                <button class="car-btn car-next" onclick="moveSlide(1)">❯</button>
            </div>
        </div>
    </section>

    <!-- FAQs -->
    <section class="faqs container">
        <div class="section-title fade-in-up">
            <h2>Preguntas Frecuentes</h2>
        </div>
        <div class="faq-wrap fade-in-up">
            <details class="faq-item">
                <summary>¿Cómo puedo agendar una cita?</summary>
                <p>Es muy sencillo, solo debes hacer clic en el botón de WhatsApp y uno de nuestros asesores te atenderá de inmediato para coordinar el horario que mejor te convenga.</p>
            </details>
            <details class="faq-item">
                <summary>¿Qué métodos de pago aceptan?</summary>
                <p>Aceptamos pagos en efectivo, transferencias bancarias y todas las tarjetas de crédito o débito.</p>
            </details>
            <details class="faq-item">
                <summary>¿Tienen promociones para pacientes de primera vez?</summary>
                <p>Constantemente ofrecemos valoraciones sin costo o descuentos en el primer tratamiento. Contáctanos por WhatsApp para conocer las promociones del mes.</p>
            </details>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <div class="container">
            <p>&copy; 2024 {data['nombre']}. Todos los derechos reservados. | <i>Este es un diseño borrador de propuesta.</i></p>
        </div>
    </footer>

    <!-- Floating WhatsApp -->
    <a href="https://wa.me/{data['tel_wa']}" class="wa-float" target="_blank">💬</a>

    <!-- JS Logic -->
    <script>
        // Scroll Observer
        const observer = new IntersectionObserver((entries) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    entry.target.classList.add('visible');
                }}
            }});
        }}, {{ threshold: 0.1 }});
        document.querySelectorAll('.fade-in-up').forEach(el => observer.observe(el));

        // Stats Counter
        const counters = document.querySelectorAll('.counter');
        const speed = 200;
        const counterObserver = new IntersectionObserver((entries, obs) => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    const counter = entry.target;
                    const target = +counter.getAttribute('data-target');
                    const updateCount = () => {{
                        const count = +counter.innerText;
                        const inc = target / speed;
                        if(count < target) {{
                            counter.innerText = Math.ceil(count + inc);
                            setTimeout(updateCount, 20);
                        }} else {{
                            counter.innerText = target + (target > 100 ? '+' : '');
                        }}
                    }};
                    updateCount();
                    obs.unobserve(counter);
                }}
            }});
        }}, {{ threshold: 0.5 }});
        counters.forEach(c => counterObserver.observe(c));

        // Carousel
        let slideIndex = 0;
        const slides = document.querySelectorAll('.carousel-slide');
        function moveSlide(n) {{
            slides[slideIndex].classList.remove('active');
            slideIndex = (slideIndex + n + slides.length) % slides.length;
            slides[slideIndex].classList.add('active');
        }}
        setInterval(() => moveSlide(1), 5000); // Auto-advance
    </script>
</body>
</html>"""
    return html

def audit_html(html):
    issues = []
    lower_html = html.lower()
    
    # 1. Color check (Aggressive colors)
    forbidden = ['#ff0000', '#f00', 'color: red', 'color:red', 'background: red', 'background:red', '#000000', '#000;']
    for f in forbidden:
        if f in lower_html:
            issues.append(f"Forbidden color/string found: {f}")
            
    # 2. Component check
    if 'intersectionobserver' not in lower_html:
        issues.append("Missing IntersectionObserver for animations.")
    if 'function moveslide' not in lower_html:
        issues.append("Missing native JS Carousel logic.")
    if 'backdrop-filter: blur' not in lower_html:
        issues.append("Missing Glassmorphism CSS.")
    
    return issues

def main():
    brief_files = glob.glob(os.path.join(BASE_DIR, '*/brief_maestro.md'))
    success_count = 0
    fail_count = 0
    
    for brief_path in brief_files:
        folder = os.path.dirname(brief_path)
        with open(brief_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        data = parse_brief(content)
        html = generate_html(data)
        
        # AUDIT
        issues = audit_html(html)
        if issues:
            print(f"[FAIL] Audit failed for {os.path.basename(folder)}: {issues}")
            fail_count += 1
            continue
            
        # Write
        out_path = os.path.join(folder, 'index.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(html)
        success_count += 1
        print(f"[OK] Generado y Auditado: {os.path.basename(folder)}")
        
    print(f"\n--- RESUMEN ---")
    print(f"Webs Construidas Exitosamente: {success_count}")
    print(f"Auditorías Fallidas: {fail_count}")

    if success_count > 0:
        print("Subiendo a GitHub...")
        try:
            subprocess.run(["git", "add", "."], cwd=BASE_DIR, check=True)
            subprocess.run(["git", "commit", "-m", "Generación final de webs auditadas desde briefs maestros"], cwd=BASE_DIR, check=True)
            subprocess.run(["git", "push"], cwd=BASE_DIR, check=True)
            print("✔ Despliegue en GitHub Pages completado exitosamente.")
        except Exception as e:
            print(f"Error en Git push: {e}")

if __name__ == "__main__":
    main()
