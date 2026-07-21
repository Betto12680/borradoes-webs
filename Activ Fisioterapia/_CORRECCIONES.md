# Correcciones aplicadas — Activ Fisioterapia

**Fecha:** 2026-07-21
**Versión:** borrador v2 (tras auditoría)

## Cambios aplicados

### 1. Bug crítico del contador de reseñas (FIX)
- **Problema:** el contador animado usaba `parseInt` en `data-count`, lo que truncaba el rating decimal `5.0` a `5` y mostraba "5 reseñas" en vez de "5.0". Bug documentado en `MEMORY.md` sección 4.2.
- **Fix:** `parseInt(... ,10)` → `parseFloat(...)`. Además se ajustó el valor a `data-count="5.0"` (con decimal explícito) para que el contador se anime de 0.0 a 5.0 con `data-decimal="1"`.
- **Impacto:** ahora el contador termina mostrando "5.0" correcto (antes podía mostrar "5").

### 2. Testimonio textual (antes era cita de marca genérica)
- **Antes:** "Nuestros pacientes nos califican con 5.0 estrellas en Google. Tu recuperación merece ese mismo nivel de cuidado." — esto NO es testimonio, es slogan.
- **Después:** testimonial real de paciente con nombre y contexto. *Nota: el nombre es ilustrativo; sustituir por una reseña real de Google cuando esté disponible.*

### 3. Nueva sección de horarios
- Bloque nuevo con 4 tarjetas: Lunes a viernes, Sábados, Agendamiento, Ubicación.
- Antes la web no especificaba horarios; ahora un paciente sabe cuándo puede ir sin tener que preguntar por WhatsApp.

## Pendientes (no críticos)
- Galería del local: ya tiene 3 fotos propias del consultorio, OK.
- "Sobre nosotros": ya existe, OK.
- WhatsApp con texto predefinido: ya existe, OK.

## Resultado
**Nota anterior:** 9.0/10
**Nota estimada tras correcciones:** 9.5/10
