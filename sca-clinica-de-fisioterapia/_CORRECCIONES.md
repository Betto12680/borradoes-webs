# Correcciones — SCA Clínica de Fisioterapia

**Carpeta:** `sca-clinica-de-fisioterapia`
**Fecha:** 2026-07-21
**Versión:** borrador v2 (reescritura profunda)

## Datos del brief

- **Nombre:** SCA Clínica de Fisioterapia
- **Nicho:** Fisioterapia Deportiva
- **Ciudad:** Ciudad de México (CDMX)
- **Teléfono:** +52 55 5693 1200 (WhatsApp: 525556931200)
- **WhatsApp:** +525556931200
- **Rating Google:** 5.0 estrellas
- **Reseñas Google:** 33
- **Paleta:**
  - Primario: `#0d9488`
  - Secundario: `#14b8a6`
  - Fondo hero: `#115e59`

## Hero del brief

- **H1:** Recupera tu Movilidad y Dile Adiós al Dolor en Ciudad de México (CDMX)
- **Subtítulo:** Fisioterapia deportiva, neurológica y traumatológica guiada por especialistas. Recuperación acelerada con la mejor tecnología.

## Servicios del brief

  - 1. Terapia Manual y Liberación Miofascial
  - 2. Rehabilitación Deportiva
  - 3. Fisioterapia Post-Operatoria
  - 4. Punción Seca y Electrólisis

## Cambios a aplicar al index.html

### 1. Agregar SEO schema.org (JSON-LD)
La web actual NO tiene JSON-LD. Agregar `<script type="application/ld+json">` con `@type` específico del nicho (Dentist, PhysicalTherapy, MedicalClinic), incluyendo `name`, `telephone`, `address` (Ciudad de México), `aggregateRating` con rating y reseñas reales del brief.

### 2. Agregar Open Graph + Twitter Card
Agregar meta tags `og:title`, `og:description`, `og:image`, `og:locale=es_MX`, `og:type=business.business` y `twitter:card=summary_large_image`.

### 3. Quitar stats inventadas
La web muestra `1500 pacientes`, `15 años de experiencia`, `100% compromiso` — números falsos. Reemplazar por datos REALES del brief (rating y reseñas de Google) o quitar la sección de stats.

### 4. Reemplazar H1 genérico
El H1 actual es plantilla fija (`Atención Médica de Excelencia en Ciudad de México (CDMX)`) que se repite en TODAS las webs. Reemplazar por el H1 del brief (sección 4) o uno específico del nicho.

### 5. Reescribir copy de servicios (genérico → específico)
Los 4 servicios tienen el mismo párrafo genérico: 'Tratamiento especializado con tecnología de vanguardia y atención personalizada para garantizar tu bienestar en Ciudad de México (CDMX).' Reescribir cada uno con descripción única y relevante al servicio.

### 6. Reemplazar FAQs genéricas
Las 3 preguntas actuales son: 'métodos de pago', 'promociones para pacientes de primera vez', 'cómo agendar cita'. Cambiar por 3-4 FAQs relevantes al nicho del cliente.

### 7. Agregar sección 'Sobre nosotros / Equipo'
La web no tiene bloque de presentación del equipo. Agregar una sección que muestre al profesional/especialistas del negocio (1-2 fotos + bio de 4-6 líneas).

### 8. Agregar horarios de atención
No hay horarios visibles. Agregar bloque con 'Lun a Vie' y 'Sábado' (placeholder razonable a confirmar con el cliente).

### 9. Agregar link a Google Maps
No hay link a la dirección. Agregar un botón 'Cómo llegar' apuntando a búsqueda de Google Maps por nombre del negocio.

### 10. Respetar `prefers-reduced-motion`
Las animaciones (fade-in-up, waPulse) están activas SIEMPRE, sin respetar la preferencia del usuario. Envolver en `@media (prefers-reduced-motion: no-preference)` para accesibilidad.

### 11. Quitar el placeholder 'Este es un diseño borrador de propuesta' del footer
Solo en producción final, o dejarlo sutil si se usa como demo.

## Schema.org sugerido

```json
{
  "@context": "https://schema.org",
  "@type": "PhysicalTherapy",
  "name": "SCA Clínica de Fisioterapia",
  "description": "Fisioterapia deportiva, neurológica y traumatológica guiada por especialistas. Recuperación acelerada con la mejor tecnología.",
  "telephone": "+525556931200",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Ciudad de México",
    "addressRegion": "CDMX",
    "addressCountry": "MX"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "5.0",
    "reviewCount": "33"
  }
}
```

## Prompts de imagen sugeridos (para renderizar con Magnific / GPT Image 2)

Usar para reemplazar las 4 imágenes de stock actuales por 6 imágenes específicas:

1. Fachada de clínica de fisioterapia con letrero profesional, acceso para pacientes, hora dorada, 4K.
2. Interior de sala de rehabilitación con camillas, pesas, bandas elásticas, luz natural, sin pacientes, 4K.
3. Equipo de electroestimulación o ultrasonido terapéutico sobre fondo desenfocado, luz cenital, 4K.
4. Recepción de clínica de fisioterapia con escritorio, sillas, decoración cálida profesional, 4K.
5. Pasillo de clínica de rehabilitación con luz natural, puertas de consultorios, perspectiva lineal, 4K.
6. Retrato editorial de fisioterapeuta (hombre/mujer 30-50 años) en uniforme clínico, manos sobre camilla vacía, 4K.

## Pendientes (post-construcción)

- Verificar la dirección EXACTA del local con Google Maps y actualizar link.
- Confirmar horarios reales con el cliente.
- Si tiene reseñas reales adicionales, actualizar `reviewCount` en el JSON-LD.
- Si el profesional tiene foto en Google Maps, usarla en la sección 'Sobre nosotros'.
- Reemplazar WhatsApp genérico (escrito en el brief) por el número real del cliente cuando esté confirmado.
