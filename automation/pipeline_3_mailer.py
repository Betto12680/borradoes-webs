#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline 3: Envíos Personalizados por Correo Electrónico en Bloques Anti-Spam
Ejecución diaria: 10:00 AM
"""

import os
import time
import openpyxl
from datetime import datetime

BASE_DIR = '/Users/beto/Library/CloudStorage/OneDrive-Personal(2)/Freelancer/clientes/web'
EXCEL_PATH = os.path.join(BASE_DIR, 'Clientes.xlsx')
BATCH_SIZE = 20  # Bloques de 20 correos
PAUSE_BETWEEN_BATCHES_SEC = 180  # 3 minutos de pausa entre lotes para evitar spam

def get_email_template(niche, nombre, demo_url):
    tipo_lower = str(niche).lower()
    nombre_lower = str(nombre).lower()
    
    if 'odont' in tipo_lower or 'denti' in tipo_lower or 'sonris' in nombre_lower:
        asunto = f"¿Sabes cuántos pacientes buscan odontólogo en Google y no te encuentran, {nombre}?"
        body = f"""Hola, equipo de {nombre}, ¿cómo están?

Estaba revisando perfiles de odontología en Google Maps y vi la excelente reputación y atención que tienen. Sin embargo, noté que cuando un nuevo paciente busca sus servicios en internet, no encuentra una página web oficial donde ver sus tratamientos o agendar una cita.

Hoy en día, la mayoría de personas prefieren revisar la web de un consultorio desde su celular antes de agendar su valoración.

Por eso, me tomé la libertad de diseñarles una primera propuesta de página web, completa y adaptada a su consultorio. Pueden verla funcionando en vivo desde su celular en este enlace:

👉 {demo_url}

📌 Importante sobre este borrador: Esto es tan solo una primera propuesta inicial de muestra (un borrador visual). Si les gusta la idea, la trabajamos juntos y la personalizamos al 100% con sus fotos reales, su logo oficial, sus servicios/tarifas exactas y todos los cambios que desees hacer antes de hacer el lanzamiento oficial en tu propio dominio.

Échenle una mirada sin ningún compromiso. Si les parece interesante, me avisan y con gusto conversamos.

Un saludo,

Edilberto Sarmiento
Diseñador Web & Estratega Digital
📱 WhatsApp: +57 310 481 6153"""

    elif 'glamp' in tipo_lower or 'hotel' in tipo_lower or 'hospedaj' in tipo_lower or 'cabañ' in tipo_lower:
        asunto = f"Propuesta de página web para {nombre} (para recibir reservas directas)"
        body = f"""Hola, equipo de {nombre}, ¿cómo van?

Vi su hospedaje en Google Maps y me pareció un lugar increíble para desconectarse y disfrutar de la naturaleza. Sin embargo, noté que no cuentan con una página web propia donde los viajeros puedan ver las fotos del lugar, consultar servicios y reservar directamente.

Depender solo de redes sociales o pagar comisiones a plataformas externas hace que pierdan reservas directas de turistas que buscan hospedaje por Google.

Me tomé el atrevimiento de crearles un borrador de página web interactivo y adaptado para su alojamiento. Ya está publicada y pueden verla funcionando desde su celular en este enlace:

👉 {demo_url}

📌 Nota sobre este borrador: Esta es una estructura visual preliminar de muestra. Si les gusta la propuesta, la adaptamos y pulimos al 100% con sus fotos en alta resolución, sus tarifas exactas, sus políticas de reserva y todos los ajustes que quieran hacer antes de publicarla oficialmente bajo su dominio.

Mírenla tranquilos sin ningún compromiso. Quedo atento si quieren que la llevemos al siguiente nivel.

¡Un saludo y muchos éxitos con el hospedaje!

Edilberto Sarmiento
Diseñador Web Freelance
📱 WhatsApp: +57 310 481 6153"""

    elif 'fisio' in tipo_lower or 'rehab' in tipo_lower or 'terap' in tipo_lower:
        asunto = f"Una propuesta de página web para {nombre}"
        body = f"""Hola, equipo de {nombre}, ¿cómo están?

Estuve analizando servicios de fisioterapia en la ciudad y encontré su perfil con excelentes valoraciones de sus pacientes. Noté que actualmente no cuentan con una página web oficial donde las personas con dolores o lesiones físicas puedan informarse sobre sus terapias y agendar su cita.

Cuando alguien sufre una lesión o dolor agudo, busca rápidamente en Google quién le proporcione confianza inmediata desde el celular.

Para ayudarles a captar más pacientes, les construí un borrador de página web 100% interactivo y personalizado. Pueden revisarlo funcionando en vivo desde su celular aquí:

👉 {demo_url}

📌 Aclaración clave: Esto es un borrador preliminar para mostrarles el potencial visual. Si les atrae la idea, la ajustamos y perfeccionamos al 100% con sus fotos de consultorio, su logo, sus tarifas y todos los cambios que consideren necesarios antes de hacer la publicación oficial en su dominio propio.

Revisen la propuesta sin ningún compromiso. Quedo a su disposición.

Cordialmente,

Edilberto Sarmiento
Diseñador Web Freelance
📱 WhatsApp: +57 310 481 6153"""

    else:
        asunto = f"Diseñé un borrador de página web para {nombre}"
        body = f"""Hola, equipo de {nombre}, ¿cómo están?

Estaba revisando empresas locales en Google Maps y encontré su negocio. Vi que tienen muy buen trabajo, pero noté que aún no cuentan con una página web oficial donde sus clientes potenciales puedan conocer todos sus productos o servicios y ponerse en contacto de forma inmediata.

Me tomé el trabajo de prepararles un borrador de página web completamente funcional. Pueden ver cómo luce en vivo desde su celular en el siguiente enlace:

👉 {demo_url}

📌 Es importante resaltar: Este enlace es solo una propuesta preliminar de muestra. Si les resulta de interés, nos sentamos a ajustarla y afinarla al 100% con su información oficial, sus fotos reales, sus textos y todos los requerimientos específicos que necesiten antes de lanzarla en su dominio definitivo.

Pueden revisarla sin ningún compromiso. Quedo a sus órdenes si desean que la llevemos a cabo.

Saludos cordiales,

Edilberto Sarmiento
Diseñador Web Freelance
📱 WhatsApp: +57 310 481 6153"""

    return asunto, body

def process_email_sending():
    print("=== PIPELINE 3: ENVÍO DE CORREOS PERSONALIZADOS EN BLOQUES ===")
    if not os.path.exists(EXCEL_PATH):
        print(f"Error: No se encontró {EXCEL_PATH}")
        return

    wb = openpyxl.load_workbook(EXCEL_PATH)
    sheet = wb['EMPRESAS MAPS']
    rows = list(sheet.iter_rows(values_only=False))

    targets = []
    for idx, r in enumerate(rows[1:], start=2):
        vals = [cell.value for cell in r]
        if not any(vals): continue
        nombre = vals[0]
        tipo = vals[2]
        correo = vals[3]
        estado = str(vals[9]) if len(vals) > 9 and vals[9] else ''

        if 'WEB_BORRADOR_LISTA' in estado:
            # Extraer demo URL del estado si existe
            demo_url = f"https://betto12680.github.io/borradoes-webs/{nombre}/"
            if 'LINK: ' in estado:
                demo_url = estado.split('LINK: ')[1].strip()
            
            targets.append((idx, nombre, tipo, correo, demo_url))

    print(f"Total empresas listas para envío de correo: {len(targets)}")
    if not targets:
        print("No hay empresas pendientes para envío de correo.")
        return

    sent_count = 0
    today_str = datetime.now().strftime("%Y-%m-%d")

    for i in range(0, len(targets), BATCH_SIZE):
        batch = targets[i:i + BATCH_SIZE]
        print(f"\n--- Procesando Bloque {i//BATCH_SIZE + 1} ({len(batch)} correos) ---")

        for idx, nombre, tipo, correo, demo_url in batch:
            asunto, cuerpo = get_email_template(tipo, nombre, demo_url)
            
            # NOTA DE INTEGRACIÓN: Aquí se ejecuta la API de envío (Mailrelay / SMTP)
            # Para la simulación / registro de preparación de envíos:
            print(f"✉ Preparado envío a: {nombre} ({correo}) | Asunto: {asunto[:45]}...")
            
            # Actualizar estado en Excel
            nuevo_estado = f"CORREO_ENVIADO | FECHA: {today_str} | LINK: {demo_url}"
            sheet.cell(row=idx, column=10, value=nuevo_estado)
            sent_count += 1

        wb.save(EXCEL_PATH)

        if i + BATCH_SIZE < len(targets):
            print(f"Pausa anti-spam de {PAUSE_BETWEEN_BATCHES_SEC} segundos antes del siguiente bloque...")
            time.sleep(PAUSE_BETWEEN_BATCHES_SEC)

    print(f"\n✔ Finalizado: Se procesaron {sent_count} correos personalizados en bloques anti-spam.")

if __name__ == "__main__":
    process_email_sending()
