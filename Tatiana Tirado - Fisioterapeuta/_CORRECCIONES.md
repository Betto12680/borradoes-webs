# Correcciones — Tatiana Tirado - Fisioterapeuta

**Fecha:** 2026-07-21
**Versión:** borrador v2 (tras auditoría)
**Dirección:** El Poblado, Medellín
**Teléfono:** Consultar

## Cambios a aplicar

### 1. Agregar sección de horarios
Bloque nuevo con clase `cards` después de la sección de testimonio, 4 tarjetas: Lunes a viernes, Sábados, Agendamiento, Ubicación.

### 2. Expandir galería de fotos del local
La web actual tiene 0-2 fotos genéricas o ninguna. Generar 4-6 imágenes específicas con Magnific usando los prompts de abajo.

### 3. Agregar sección 'Sobre nosotros/mí'
Bloque nuevo tipo `about` con foto del profesional y bio de 4-6 líneas personalizadas.

### 4. Mejorar testimonio textual
El `blockquote` actual es slogan de marca, no testimonio real. Reemplazar por testimonial con nombre de paciente + contexto concreto de tratamiento.


## Prompts de imagen sugeridos (para renderizar con Magnific / GPT Image 2)

Usar como base para la galería de 4-6 fotos:

1. **Fachada exterior** — Fachada exterior del consultorio de fisioterapia con letrero visible del negocio, hora dorada, encuadre frontal a la altura de los ojos, estilo arquitectónico comercial limpio, sin gente, cielo nublado suave, resolución 4K.
2. **Sala principal** — Interior de la sala de atención principal con camilla profesional y equipo de rehabilitación visible, luz natural desde ventana grande, sin pacientes (solo el espacio decorado de forma clínica), encuadre 3/4, tonos cálidos.
3. **Equipo destacado** — Detalle del equipo de rehabilitación más característico (ultrasonido, electroestimulador, bandas elásticas o camilla hidráulica) sobre fondo desenfocado, luz cenital, estilo editorial de producto médico.
4. **Recepción/espera** — Recepción o zona de espera con sillas cómodas, mesa de centro con revistas, logotipo o marco del negocio en pared, encuadre 3/4 desde la entrada, luz mixta natural-artificial.
5. **Pasillo/zona de transición** — Pasillo o zona de transición entre consultorios con luz natural, perspectiva lineal y puertas de consultorios a los lados, piso limpio.
6. **Retrato del profesional** — Retrato editorial del profesional de la salud (mujer/hombre 30-45 años) en bata blanca, con estetoscopio o en plena consulta sin paciente visible, fondo desenfocado de consultorio, sonrisa profesional.

## Pendientes
- Si el cliente confirma WhatsApp, actualizar todos los `tel:` y `href="tel:..."` por `wa.me/` con texto predefinido.
- Si hay reseñas reales adicionales en Google Maps, actualizar `aggregateRating` del JSON-LD.
- Reemplazar foto del profesional con retrato profesional (verificar con Google Maps que sea del profesional real, no de otra persona).
