#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import re
import openpyxl

BASE_DIR = '/Users/beto/Library/CloudStorage/OneDrive-Personal(2)/Freelancer/clientes/web'
EXCEL_PATH = os.path.join(BASE_DIR, 'Clientes.xlsx')

def slugify(text):
    text = text.lower().strip()
    replacements = {'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u', 'ñ': 'n', 'ü': 'u'}
    for k, v in replacements.items():
        text = text.replace(k, v)
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    return text.strip('-')

PROMPT_MAESTRO_TEMPLATE = """## 🤖 PROMPT MAESTRO PARA GENERACIÓN DE CÓDIGO (PARA LA IA)

**ROLES Y DIRECTRICES:**
Eres un Desarrollador Frontend Senior experto en UX/UI y diseño de alta conversión. Tu objetivo es tomar la información contenida en este brief y generar un archivo `index.html` altamente dinámico, pulido y profesional, basado en el estándar estético de `odontosaludp.com`.

**REGLAS ESTRICTAS DE DISEÑO:**
1. **NO USAR frameworks pesados**: Solo HTML5, CSS3 nativo, y JavaScript vanilla.
2. **CERO colores agresivos**: NUNCA usar rojo, negro absoluto o colores oscuros pesados. Utilizar EXCLUSIVAMENTE la paleta de colores definida en este brief (azules, turquesas, blancos, fondos médicos limpios).
3. **Secciones Obligatorias**:
   - Header sticky con efecto Glassmorphism (blur) y botón de contacto.
   - Hero Section dividido (Split layout) con imagen de alta calidad, copy persuasivo, y badge de calificaciones.
   - Barra de Estadísticas Animada (Contadores).
   - Sección de Servicios en formato Tarjetas con iconos y etiquetas.
   - Carrusel/Slider de Instalaciones o Antes/Después (implementado nativamente en JS o con CDN ligero).
   - Sección de Preguntas Frecuentes (Acordeón interactivo).
   - Botón Flotante de WhatsApp con animación de "latido/pulso".
4. **Animaciones**: Implementar `IntersectionObserver` para revelar elementos suavemente al hacer scroll (`fade-in-up`).
5. **Responsividad**: Perfecto en dispositivos móviles (flexbox/grid).
6. **Contenido**: Insertar exactamente los textos de este brief. Añadir sutilmente al footer: "*Este es un diseño borrador de propuesta.*"

**OUTPUT ESPERADO:**
Genera el código completo en un solo bloque HTML que integre todo el CSS y JS necesario para que funcione inmediatamente al abrirlo en el navegador. Reemplaza el `index.html` en esta carpeta con este nuevo código.
"""

def generate_brief(nombre, ciudad, tipo, tel, resenas, rating, slug):
    tipo_lower = tipo.lower()
    
    # Determinar Paleta, Imágenes y Textos por Nicho
    if 'odont' in tipo_lower or 'dent' in tipo_lower:
        paleta = """
- **Primario**: #0284c7 (Azul Médico)
- **Secundario**: #38bdf8 (Cian Suave)
- **Fondo Oscuro (Hero)**: #0c4a6e (Azul Profundo, NUNCA negro)
- **Acentos**: Blanco puro y dorado suave para estrellas de reseñas."""
        
        imagenes = """
- **Hero Image**: https://images.unsplash.com/photo-1606811841689-23dfddce3e95?auto=format&fit=crop&w=1200&q=80 (Clínica limpia y moderna)
- **Carrusel 1**: https://images.unsplash.com/photo-1598256989800-fe5f95da9787?auto=format&fit=crop&w=1200&q=80
- **Carrusel 2**: https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1200&q=80
- **Carrusel 3**: https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&w=1200&q=80"""
        
        textos = f"""*(Texto borrador inventado)*
- **Hero Titular**: Odontología Avanzada y Diseño de Sonrisa en {ciudad}
- **Hero Subtítulo**: Especialistas certificados enfocados en devolverte la confianza al sonreír, con tecnología digital 3D y tratamientos sin dolor.
- **Servicios Principales**: 
  1. Diseño de Sonrisa en 3D
  2. Ortodoncia Invisible
  3. Implantes Dentales de Carga Inmediata
  4. Blanqueamiento Láser Clínico"""

    elif 'fisio' in tipo_lower or 'rehab' in tipo_lower:
        paleta = """
- **Primario**: #0d9488 (Turquesa Salud)
- **Secundario**: #14b8a6 (Teal Brillante)
- **Fondo Oscuro (Hero)**: #115e59 (Turquesa Profundo, NUNCA negro)
- **Acentos**: Blanco, gris perla y toques de verde vitalidad."""
        
        imagenes = """
- **Hero Image**: https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1200&q=80 (Fisioterapia, terapia manual)
- **Carrusel 1**: https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=1200&q=80
- **Carrusel 2**: https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1200&q=80
- **Carrusel 3**: https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=1200&q=80"""
        
        textos = f"""*(Texto borrador inventado)*
- **Hero Titular**: Recupera tu Movilidad y Dile Adiós al Dolor en {ciudad}
- **Hero Subtítulo**: Fisioterapia deportiva, neurológica y traumatológica guiada por especialistas. Recuperación acelerada con la mejor tecnología.
- **Servicios Principales**: 
  1. Terapia Manual y Liberación Miofascial
  2. Rehabilitación Deportiva
  3. Fisioterapia Post-Operatoria
  4. Punción Seca y Electrólisis"""

    else:
        # Default Medical/Salud
        paleta = """
- **Primario**: #2563eb (Azul Clínico Real)
- **Secundario**: #60a5fa (Azul Claro)
- **Fondo Oscuro (Hero)**: #1e3a8a (Azul Marino, NUNCA negro)
- **Acentos**: Blanco, gris claro para fondos de tarjetas."""
        
        imagenes = """
- **Hero Image**: https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=1200&q=80 (Ambiente clínico)
- **Carrusel 1**: https://images.unsplash.com/photo-1551076805-e18690c5e53b?auto=format&fit=crop&w=1200&q=80
- **Carrusel 2**: https://images.unsplash.com/photo-1581056771107-24ca5f033842?auto=format&fit=crop&w=1200&q=80
- **Carrusel 3**: https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1200&q=80"""
        
        textos = f"""*(Texto borrador inventado)*
- **Hero Titular**: Atención Médica de Excelencia en {ciudad}
- **Hero Subtítulo**: Un equipo multidisciplinario comprometido con tu salud integral. Instalaciones de primer nivel y trato humano cálido.
- **Servicios Principales**: 
  1. Consulta Médica Especializada
  2. Diagnóstico y Laboratorio Clínico
  3. Checkups Integrales Preventivos
  4. Especialidades Quirúrgicas"""

    rating_val = str(rating) if rating and str(rating) != 'N/D' else '4.9'
    resenas_val = str(resenas) if resenas and str(resenas) != 'N/D' else '50'
    tel_clean = re.sub(r'\D', '', str(tel)) if tel and str(tel) != 'N/D' else '525555551234'
    if not tel_clean.startswith('52'): tel_clean = '52' + tel_clean

    brief = f"""# Brief de Desarrollo Web: {nombre}

## 1. Información del Cliente
- **Nombre**: {nombre}
- **Nicho**: {tipo}
- **Ciudad**: {ciudad}
- **Teléfono de Contacto**: {tel} (WhatsApp: {tel_clean})
- **Calificación en Google Maps**: {rating_val} Estrellas
- **Cantidad de Reseñas**: {resenas_val} reseñas

## 2. Paleta de Colores Autorizada
**IMPORTANTE: NUNCA usar rojo, ni colores relacionados con la sangre, la violencia o el peligro, ni fondos negros puros. Todo debe transmitir limpieza, paz, clínica, salud y profesionalismo.**
{paleta}

## 3. Banco de Imágenes de Referencia (Unsplash)
{imagenes}

## 4. Estructura y Textos del Borrador
{textos}

---

{PROMPT_MAESTRO_TEMPLATE}
"""
    return brief

def main():
    wb = openpyxl.load_workbook(EXCEL_PATH)
    sheet = wb['EMPRESAS MAPS']
    rows = list(sheet.iter_rows(values_only=False))

    count = 0
    for r in rows[1:]:
        vals = [cell.value for cell in r]
        if not any(vals): continue
        nombre = str(vals[0]).strip()
        ciudad = str(vals[1]).strip()
        tipo = str(vals[2]).strip()
        tel = str(vals[4]).strip() if vals[4] else ''
        resenas = str(vals[6]).strip() if vals[6] else ''
        rating = str(vals[7]).strip() if vals[7] else ''
        estado = str(vals[9]).strip() if len(vals) > 9 and vals[9] else ''

        if 'WEB_BORRADOR_LISTA' in estado or 'PENDIENTE' in estado:
            slug = slugify(nombre)
            site_dir = os.path.join(BASE_DIR, slug)
            if os.path.isdir(site_dir):
                brief_content = generate_brief(nombre, ciudad, tipo, tel, resenas, rating, slug)
                brief_path = os.path.join(site_dir, 'brief_maestro.md')
                with open(brief_path, 'w', encoding='utf-8') as f:
                    f.write(brief_content)
                count += 1
                print(f"Created brief for {nombre}")
    
    print(f"Total briefs creados: {count}")

if __name__ == "__main__":
    main()
