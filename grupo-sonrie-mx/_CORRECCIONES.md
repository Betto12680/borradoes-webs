# Correcciones — Grupo Sonríe Mx

**Carpeta:** `grupo-sonrie-mx`
**Fecha:** 2026-07-21
**Versión:** borrador v2 (reescritura profunda)

## Datos del brief

- **Nombre:** Grupo Sonríe Mx
- **Nicho:** Odontología Estética
- **Ciudad:** Ciudad de México (CDMX)
- **Teléfono:** +52 55 5207 6543 (WhatsApp: 525552076543)
- **WhatsApp:** +525552076543
- **Rating Google:** 4.9 estrellas
- **Reseñas Google:** 28
- **Paleta:**
  - Primario: `#0284c7`
  - Secundario: `#38bdf8`
  - Fondo hero: `#0c4a6e`

## Hero del brief

- **H1:** Odontología Avanzada y Diseño de Sonrisa en Ciudad de México (CDMX)
- **Subtítulo:** Especialistas certificados enfocados en devolverte la confianza al sonreír, con tecnología digital 3D y tratamientos sin dolor.

## Servicios del brief

  - 1. Diseño de Sonrisa en 3D
  - 2. Ortodoncia Invisible
  - 3. Implantes Dentales de Carga Inmediata
  - 4. Blanqueamiento Láser Clínico

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
  "@type": "Dentist",
  "name": "Grupo Sonríe Mx",
  "description": "Especialistas certificados enfocados en devolverte la confianza al sonreír, con tecnología digital 3D y tratamientos sin dolor.",
  "telephone": "+525552076543",
  "priceRange": "$$",
  "address": {
    "@type": "PostalAddress",
    "addressLocality": "Ciudad de México",
    "addressRegion": "CDMX",
    "addressCountry": "MX"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "reviewCount": "28"
  }
}
```

## Prompts de imagen sugeridos (para renderizar con Magnific / GPT Image 2)

Usar para reemplazar las 4 imágenes de stock actuales por 6 imágenes específicas:

1. Fachada moderna de clínica dental con letrero iluminado, vidrio y acero, hora dorada, cielo despejado, encuadre frontal arquitectónico, 4K.
2. Interior de consultorio dental con sillón dental moderno, lámpara quirúrgica LED, luz natural desde ventanal, instrumental visible, sin paciente, 4K.
3. Detalle de equipo de rayos X dental o escáner intraoral 3D sobre fondo desenfocado, luz cenital, estilo editorial médico, 4K.
4. Recepción de clínica dental con mostrador blanco, sillas ergonómicas, certificados y diplomas en pared, encuadre 3/4, luz mixta, 4K.
5. Sala de espera de clínica dental con diseño minimalista, plantas verdes, revistas, luz cálida, 4K.
6. Retrato editorial de dentista profesional (hombre/mujer 30-50 años) con bata blanca y mascarilla bajada, sonrisa amable, fondo desenfocado, 4K.

## Pendientes (post-construcción)

- Verificar la dirección EXACTA del local con Google Maps y actualizar link.
- Confirmar horarios reales con el cliente.
- Si tiene reseñas reales adicionales, actualizar `reviewCount` en el JSON-LD.
- Si el profesional tiene foto en Google Maps, usarla en la sección 'Sobre nosotros'.
- Reemplazar WhatsApp genérico (escrito en el brief) por el número real del cliente cuando esté confirmado.
