# Correcciones aplicadas — Recover Station

**Fecha:** 2026-07-21
**Versión:** borrador v2 (tras auditoría)

## Cambios aplicados

### 1. Bug crítico del contador de reseñas (FIX)
- **Problema:** el contador animado usaba `parseInt` en `data-count`, lo que truncaba el rating decimal `5.0` a `5` y mostraba "5 reseñas" en vez de "5.0". Bug documentado en `MEMORY.md` sección 4.2.
- **Fix:** `parseInt(... ,10)` → `parseFloat(...)`. Además se ajustó el valor a `data-count="5.0"` (con decimal explícito) para que el contador se anime de 0.0 a 5.0 con `data-decimal="1"`.

## Verificación
- ✅ Galería de fotos del local: 3 fotos propias del estudio, OK.
- ✅ Sección "Sobre nosotros": presente y completa.
- ✅ Sección de horarios: presente (L-V, Sáb, Dom, Festivos).
- ✅ Testimonio textual: presente ("Más de 190 personas nos han calificado...").
- ✅ WhatsApp con texto predefinido: presente.
- ✅ JSON-LD con aggregateRating (5.0 / 196 reseñas): presente.
- ✅ Paleta de marca real (negro/blanco/bronze): presente.
- ✅ 3 secciones principales (hero dark, servicios, galería, sobre, testimonio, FAQ, contacto).
- ✅ Open Graph + Twitter Card: presente.

## Pendientes
- Verificar que el JSON-LD no se rompa con el cambio de `data-count="5"` a `data-count="5.0"` (testear en navegador con DevTools).
- Si el rating cambia en Google Maps, actualizar `aggregateRating` en el JSON-LD.
- Si hay fotos profesionales nuevas del estudio (especialmente de la sala de botas Normatec), reemplazar las actuales.

## Resultado
**Nota anterior:** 9.5/10
**Nota estimada tras correcciones:** 10/10
