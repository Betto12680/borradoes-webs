# Brief de Desarrollo Web: Seishi Centro de Atención Psicológica

## 1. Información del Cliente
- **Nombre**: Seishi Centro de Atención Psicológica
- **Nicho**: Salud Mental / Clínica Psicológica
- **Ciudad**: Ciudad de México (CDMX)
- **Teléfono de Contacto**: +52 55 5574 3311 (WhatsApp: 525555743311)
- **Calificación en Google Maps**: 4.8 Estrellas
- **Cantidad de Reseñas**: 18 reseñas

## 2. Paleta de Colores Autorizada
**IMPORTANTE: NUNCA usar rojo, ni colores relacionados con la sangre, la violencia o el peligro, ni fondos negros puros. Todo debe transmitir limpieza, paz, clínica, salud y profesionalismo.**

- **Primario**: #2563eb (Azul Clínico Real)
- **Secundario**: #60a5fa (Azul Claro)
- **Fondo Oscuro (Hero)**: #1e3a8a (Azul Marino, NUNCA negro)
- **Acentos**: Blanco, gris claro para fondos de tarjetas.

## 3. Banco de Imágenes de Referencia (Unsplash)

- **Hero Image**: https://images.unsplash.com/photo-1516549655169-df83a0774514?auto=format&fit=crop&w=1200&q=80 (Ambiente clínico)
- **Carrusel 1**: https://images.unsplash.com/photo-1551076805-e18690c5e53b?auto=format&fit=crop&w=1200&q=80
- **Carrusel 2**: https://images.unsplash.com/photo-1581056771107-24ca5f033842?auto=format&fit=crop&w=1200&q=80
- **Carrusel 3**: https://images.unsplash.com/photo-1579684385127-1ef15d508118?auto=format&fit=crop&w=1200&q=80

## 4. Estructura y Textos del Borrador
*(Texto borrador inventado)*
- **Hero Titular**: Atención Médica de Excelencia en Ciudad de México (CDMX)
- **Hero Subtítulo**: Un equipo multidisciplinario comprometido con tu salud integral. Instalaciones de primer nivel y trato humano cálido.
- **Servicios Principales**: 
  1. Consulta Médica Especializada
  2. Diagnóstico y Laboratorio Clínico
  3. Checkups Integrales Preventivos
  4. Especialidades Quirúrgicas

---

## 🤖 PROMPT MAESTRO PARA GENERACIÓN DE CÓDIGO (PARA LA IA)

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

