"""
Script para generar archivos _CORRECCIONES.md en cada web del lote 1.
Ejecutar desde: /Users/beto/Library/CloudStorage/OneDrive-Personal(2)/Freelancer/clientes/web/
"""
import os
import sys

lote1 = {
    "Andrea Katich Kurk - Fisioterapeuta": {
        "horario": True, "galeria": True, "sobre": False,
        "testimonio": True, "count_fix": False, "wa_fix": False,
        "direccion": "Calle 7 #39-290, El Poblado, Medellín",
        "telefono": "(604) 352 47 35",
    },
    "Bestrong Fisioterapia": {
        "horario": True, "galeria": True, "sobre": False,
        "testimonio": True, "count_fix": False,
        "direccion": "Tv. 12A #32-116, Castropol, El Poblado",
        "telefono": "+57 324 392 9253",
    },
    "Centro de Ortopedia El Poblado": {
        "horario": True, "galeria": True, "sobre": False,
        "testimonio": True, "count_fix": False,
        "direccion": "Cra. 41 #9-05, El Poblado, Medellín",
        "telefono": "(604) 520 91 20",
    },
    "Centro de Rehabilitacion Fisica BMS": {
        "horario": True, "galeria": True, "sobre": False,
        "testimonio": True, "count_fix": False,
        "direccion": "Cra. 76 #49-86, Laureles-Estadio, Medellín",
        "telefono": "+57 324 297 2587",
    },
    "Fisioterapia Rehab Motion": {
        "horario": True, "galeria": True, "sobre": False,
        "testimonio": True, "count_fix": False,
        "direccion": "El Poblado, Medellín",
        "telefono": "+57 300 000 0000",
    },
    "Fissio T": {
        "horario": True, "galeria": True, "sobre": True,
        "testimonio": True, "count_fix": False,
        "direccion": "Consultar Maps",
        "telefono": "Consultar",
    },
    "Fisioterapeuta Andres Pineros": {
        "horario": True, "galeria": True, "sobre": True,
        "testimonio": True, "count_fix": False,
        "direccion": "El Poblado, Medellín",
        "telefono": "Consultar",
    },
    "Ana Maria Serna y Sandra Vasquez - Fisioterapeutas": {
        "horario": True, "galeria": True, "sobre": True,
        "testimonio": True, "count_fix": False,
        "direccion": "Cra. 48 #17A Sur-47, Cons. 208, Edificio Portugal, El Poblado",
        "telefono": "+57 310 426 8694",
    },
    "Dra Juliana Torne - Fisioterapeuta": {
        "horario": True, "galeria": True, "sobre": False,
        "testimonio": True, "wa_fix": True,
        "direccion": "Consultar Maps",
        "telefono": "Consultar",
    },
    "Dra Maria Andrea Rios - Fisioterapeuta": {
        "horario": True, "galeria": True, "sobre": False,
        "testimonio": True, "count_fix": False,
        "direccion": "El Poblado, Medellín",
        "telefono": "Consultar",
    },
    "Prof Juliana Restrepo - Fisioterapeuta": {
        "horario": True, "galeria": True, "sobre": False,
        "testimonio": True, "wa_fix": True,
        "direccion": "Consultar Maps",
        "telefono": "Consultar",
    },
    "Tatiana Tirado - Fisioterapeuta": {
        "horario": True, "galeria": True, "sobre": True,
        "testimonio": True,
        "direccion": "El Poblado, Medellín",
        "telefono": "Consultar",
    },
    "Daniela Herrera-Dfisio": {
        "horario": True, "galeria": True, "sobre": False,
        "testimonio": True, "wa_fix": True,
        "direccion": "Tv. 32A Sur #31D-49, Envigado",
        "telefono": "Consultar",
    },
}

# Prompts de imagen base compartidos
PROMPTS_BASE = [
    "Fachada exterior del consultorio de fisioterapia con letrero visible del negocio, hora dorada, encuadre frontal a la altura de los ojos, estilo arquitectónico comercial limpio, sin gente, cielo nublado suave, resolución 4K.",
    "Interior de la sala de atención principal con camilla profesional y equipo de rehabilitación visible, luz natural desde ventana grande, sin pacientes (solo el espacio decorado de forma clínica), encuadre 3/4, tonos cálidos.",
    "Detalle del equipo de rehabilitación más característico (ultrasonido, electroestimulador, bandas elásticas o camilla hidráulica) sobre fondo desenfocado, luz cenital, estilo editorial de producto médico.",
    "Recepción o zona de espera con sillas cómodas, mesa de centro con revistas, logotipo o marco del negocio en pared, encuadre 3/4 desde la entrada, luz mixta natural-artificial.",
    "Pasillo o zona de transición entre consultorios con luz natural, perspectiva lineal y puertas de consultorios a los lados, piso limpio.",
    "Retrato editorial del profesional de la salud (mujer/hombre 30-45 años) en bata blanca, con estetoscopio o en plena consulta sin paciente visible, fondo desenfocado de consultorio, sonrisa profesional.",
]


def generar_contenido(nombre, cambios):
    aplicar = []
    if cambios.get("horario"):
        aplicar.append(("Agregar sección de horarios", "Bloque nuevo con clase `cards` después de la sección de testimonio, 4 tarjetas: Lunes a viernes, Sábados, Agendamiento, Ubicación."))
    if cambios.get("galeria"):
        aplicar.append(("Expandir galería de fotos del local", "La web actual tiene 0-2 fotos genéricas o ninguna. Generar 4-6 imágenes específicas con Magnific usando los prompts de abajo."))
    if cambios.get("sobre"):
        aplicar.append(("Agregar sección 'Sobre nosotros/mí'", "Bloque nuevo tipo `about` con foto del profesional y bio de 4-6 líneas personalizadas."))
    if cambios.get("testimonio"):
        aplicar.append(("Mejorar testimonio textual", "El `blockquote` actual es slogan de marca, no testimonio real. Reemplazar por testimonial con nombre de paciente + contexto concreto de tratamiento."))
    if cambios.get("wa_fix"):
        aplicar.append(("Agregar WhatsApp como canal principal", "La web actual usa `tel:` en CTAs. Cambiar a `wa.me/` con texto predefinido. Teléfono queda como canal secundario."))
    if cambios.get("count_fix"):
        aplicar.append(("Fix bug contador `parseInt` → `parseFloat`", "Bug conocido: truncaba decimales del rating. Ya documentado en `MEMORY.md` 4.2."))

    secciones = []
    for i, (titulo, accion) in enumerate(aplicar, 1):
        secciones.append(f"### {i}. {titulo}\n{accion}\n")

    contenido = f"""# Correcciones — {nombre}

**Fecha:** 2026-07-21
**Versión:** borrador v2 (tras auditoría)
**Dirección:** {cambios.get('direccion', 'Consultar Maps')}
**Teléfono:** {cambios.get('telefono', 'Consultar')}

## Cambios a aplicar

{chr(10).join(secciones)}

## Prompts de imagen sugeridos (para renderizar con Magnific / GPT Image 2)

Usar como base para la galería de 4-6 fotos:

1. **Fachada exterior** — {PROMPTS_BASE[0]}
2. **Sala principal** — {PROMPTS_BASE[1]}
3. **Equipo destacado** — {PROMPTS_BASE[2]}
4. **Recepción/espera** — {PROMPTS_BASE[3]}
5. **Pasillo/zona de transición** — {PROMPTS_BASE[4]}
6. **Retrato del profesional** — {PROMPTS_BASE[5]}

## Pendientes
- Si el cliente confirma WhatsApp, actualizar todos los `tel:` y `href="tel:..."` por `wa.me/` con texto predefinido.
- Si hay reseñas reales adicionales en Google Maps, actualizar `aggregateRating` del JSON-LD.
- Reemplazar foto del profesional con retrato profesional (verificar con Google Maps que sea del profesional real, no de otra persona).
"""
    return contenido


def main():
    base = "/Users/beto/Library/CloudStorage/OneDrive-Personal(2)/Freelancer/clientes/web"
    creados = 0
    for w, cambios in lote1.items():
        ruta_corr = os.path.join(base, w, "_CORRECCIONES.md")
        if os.path.exists(os.path.join(base, w, "index.html")):
            with open(ruta_corr, "w", encoding="utf-8") as f:
                f.write(generar_contenido(w, cambios))
            print(f"OK  {w}")
            creados += 1
        else:
            print(f"--  {w} (no tiene index.html)")
    print(f"\nTotal: {creados} archivos _CORRECCIONES.md creados.")


if __name__ == "__main__":
    main()
