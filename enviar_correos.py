#!/usr/bin/env python3
import os
import sys
import re
import time
import json
import urllib.request
import urllib.error
import getpass

# Configuración de Mailrelay
MAILRELAY_HOST = "trabajandoconia.ipzmarketing.com"
SENDER_EMAIL = "contacto@trabajandoconia.com"
SENDER_NAME = "Edilberto Sarmiento"
HTML_FILE_PATH = "correos-prospeccion.html"

def clean_html_to_text(html_content):
    """
    Convierte el contenido HTML del cuerpo a texto plano para el texto alternativo
    """
    # Reemplazar enlaces <a href="URL">TEXTO</a> por TEXTO (URL) o solo URL si son iguales
    def link_repl(match):
        href = match.group(1)
        text = match.group(2)
        if href.strip() == text.strip():
            return href
        return f"{text} ({href})"
    
    text = re.sub(r'<a\s+[^>]*href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', link_repl, html_content)
    # Reemplazar <br> o <br/> por saltos de línea
    text = re.sub(r'<br\s*/?>', '\n', text)
    # Reemplazar </p> por doble salto de línea
    text = re.sub(r'</p>', '\n\n', text)
    # Eliminar otros tags
    text = re.sub(r'<[^>]+>', '', text)
    # Limpiar espacios repetidos y saltos de línea extras
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()

def parse_emails_html(file_path):
    """
    Parsea correos-prospeccion.html para extraer el asunto global y cada correo individual
    """
    if not os.path.exists(file_path):
        print(f"Error: No se encuentra el archivo {file_path}", file=sys.stderr)
        sys.exit(1)
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Extraer asunto global
    subject_match = re.search(r'<div class="subject-block">.*?<span class="val">([^<]+)</span>', content, re.DOTALL)
    if not subject_match:
        subject_match = re.search(r'Asunto.*?<span class="val">([^<]+)</span>', content, re.DOTALL | re.IGNORECASE)
        
    subject = subject_match.group(1).strip() if subject_match else "¿Sabes cuántos pacientes te buscan y no te encuentran?"
    
    # Extraer cada tarjeta de correo
    cards = re.findall(r'<article class="card"[^>]*>(.*?)</article>', content, re.DOTALL)
    
    emails = []
    for card in cards:
        # 1. Nombre del negocio
        name_match = re.search(r'<h2 class="name">([^<]+)</h2>', card)
        name = name_match.group(1).strip() if name_match else "Negocio sin nombre"
        
        # 2. Correo de destino
        email_match = re.search(r'Para:\s*<b>([^<]+)</b>', card)
        to_email = email_match.group(1).strip() if email_match else None
        
        # 3. Cuerpo del correo (contenido de <div class="letter" id="body\d+"> ... </div>)
        body_match = re.search(r'<div class="letter"[^>]*id="body\d+"[^>]*>(.*?)</div>', card, re.DOTALL)
        body_html = body_match.group(1).strip() if body_match else None
        
        if to_email and to_email != "N/D" and body_html:
            emails.append({
                "name": name,
                "to_email": to_email,
                "body_html": body_html,
                "body_text": clean_html_to_text(body_html)
            })
            
    return subject, emails

def send_via_mailrelay_api(api_key, subject, recipient_name, recipient_email, body_html, body_text):
    """
    Envía un correo usando la API v3 (v1/send_emails endpoint) de Mailrelay de forma nativa en Python
    """
    url = f"https://{MAILRELAY_HOST}/api/v1/send_emails"
    
    # Payload estructurado de acuerdo a la API de Mailrelay
    payload = {
        "from": {
            "email": SENDER_EMAIL,
            "name": SENDER_NAME
        },
        "subject": subject,
        "html_part": f"""
        <html>
          <body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; color: #201C16; max-width: 600px; margin: 0 auto; padding: 20px;">
            {body_html}
          </body>
        </html>
        """,
        "text_part": body_text,
        "to": [
            {
                "email": recipient_email,
                "name": recipient_name
            }
        ]
    }
    
    headers = {
        "Content-Type": "application/json",
        "X-AUTH-TOKEN": api_key
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    
    try:
        with urllib.request.urlopen(req) as response:
            res_body = response.read().decode("utf-8")
            res_json = json.loads(res_body)
            # Retorna el JSON de respuesta que suele tener los detalles del envío exitoso
            return True, res_json
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8")
        try:
            err_json = json.loads(err_body)
            err_msg = err_json.get("errors", err_body)
        except:
            err_msg = err_body
        return False, f"HTTP Error {e.code}: {err_msg}"
    except Exception as e:
        return False, str(e)

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Automatiza el envío de correos de prospección desde la API de Mailrelay.")
    parser.add_argument("--dry-run", action="store_true", help="Simula el envío sin mandar correos reales")
    parser.add_argument("--test-self", action="store_true", help="Envía el primer correo de prueba a tu propio correo (sarmi200.1995@gmail.com)")
    
    args = parser.parse_args()
    
    print("=== AUTOMATIZACIÓN DE ENVÍO DE CORREOS DE PROSPECCIÓN (MAILRELAY) ===")
    subject, emails = parse_emails_html(HTML_FILE_PATH)
    
    print(f"Asunto global detectado: '{subject}'")
    print(f"Total correos válidos encontrados: {len(emails)}")
    print("---")
    
    if not emails:
        print("No se encontraron correos para enviar en el archivo HTML.")
        sys.exit(0)
        
    if args.dry_run:
        print("[MODO SIMULACIÓN - DRY RUN] No se enviarán correos reales.")
        for idx, email in enumerate(emails, 1):
            print(f"\n[{idx}/{len(emails)}] Correo para: {email['name']}")
            print(f"Remitente: {SENDER_NAME} <{SENDER_EMAIL}>")
            print(f"Destinatario: {email['to_email']}")
            print(f"Cuerpo (Texto plano):\n{email['body_text']}")
            print("-" * 40)
        print("\nSimulación completada. Todo parece correcto.")
        sys.exit(0)
        
    # Si es prueba personal, reducimos la lista al primer correo pero con destinatario = remitente personal
    if args.test_self:
        print(f"[MODO AUTO-ENVÍO DE PRUEBA]")
        test_email = emails[0].copy()
        # Mandamos a la cuenta de Gmail personal que recibe la redirección
        test_email["to_email"] = "sarmi200.1995@gmail.com"
        test_email["name"] = f"PRUEBA - {test_email['name']}"
        emails_to_send = [test_email]
        print(f"Se enviará una prueba de: '{test_email['name']}' a tu correo de redirección: sarmi200.1995@gmail.com")
    else:
        emails_to_send = emails
        print(f"Se enviarán {len(emails_to_send)} correos reales usando la API de Mailrelay.")
        
    # Obtener API key de forma segura (Prioriza variable de entorno o usa la provista por el usuario)
    api_key = os.environ.get("MAILRELAY_API_KEY")
    if not api_key:
        # Clave por defecto provista para el proyecto
        api_key = "Pk84z15yBRQYsMhj2mug7_af6Anb_gzsS28_qe_r"
        
    enviados_ok = 0
    enviados_fail = 0
    
    for idx, email in enumerate(emails_to_send, 1):
        print(f"[{idx}/{len(emails_to_send)}] Enviando a: {email['name']} ({email['to_email']})... ", end="", flush=True)
        
        success, response = send_via_mailrelay_api(
            api_key=api_key,
            subject=subject,
            recipient_name=email['name'],
            recipient_email=email['to_email'],
            body_html=email['body_html'],
            body_text=email['body_text']
        )
        
        if success:
            print("ENVIADO ✔")
            enviados_ok += 1
        else:
            print(f"FALLÓ ❌ ({response})")
            enviados_fail += 1
            
        # Esperar 8 segundos entre peticiones de API para no saturar
        if idx < len(emails_to_send):
            time.sleep(8)
            
    print("\n=== PROCESO TERMINADO ===")
    print(f"Exitosos: {enviados_ok}")
    print(f"Fallidos: {enviados_fail}")
    
    if enviados_fail > 0:
        sys.exit(2)
    sys.exit(0)

if __name__ == "__main__":
    main()
