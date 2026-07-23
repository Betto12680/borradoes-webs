# Brief de Desarrollo Web: Dr. Rodrigo Mata González - Cirugía

## 1. Información del Cliente
- **Nombre**: Dr. Rodrigo Mata González - Cirugía
- **Nicho**: Clínica Médica / Especialidades
- **Ciudad**: Guadalajara
- **Teléfono de Contacto**: +52 33 3616 5678 (WhatsApp: 523336165678)
- **Calificación en Google Maps**: 4.9 Estrellas
- **Cantidad de Reseñas**: 60 reseñas

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
- **Hero Titular**: Atención Médica de Excelencia en Guadalajara
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
3. **CERO Emojis**: NUNCA utilizar emojis en los textos ni botones. Utilizar viñetas animadas (pulse-bullet-dot) o iconos vectoriales SVG limpios.
4. **Secciones Obligatorias**:
   - Header sticky con efecto Glassmorphism (blur) y botón de contacto.
   - Hero Section dividido (Split layout) con imagen de alta calidad, copy persuasivo, y badge de calificaciones.
   - Barra de Estadísticas Animada (Contadores).
   - Sección de Servicios en formato Tarjetas con viñetas animadas de pulso (`pulse-bullet-dot`).
   - Carrusel/Slider de Instalaciones o Antes/Después (implementado nativamente en JS).
   - Sección de Preguntas Frecuentes (Acordeón interactivo).
   - Botón Flotante de WhatsApp con animación de "latido/pulso" y vector SVG.
5. **Animaciones**: Implementar `IntersectionObserver` para revelar elementos suavemente al hacer scroll (`fade-in-up`).
6. **Responsividad**: Perfecto en dispositivos móviles (flexbox/grid).
7. **Contenido**: Insertar exactamente los textos de este brief. Añadir sutilmente al footer: "*Este es un diseño borrador de propuesta.*"

**OUTPUT ESPERADO:**
Genera el código completo en un solo bloque HTML que integre todo el CSS y JS necesario para que funcione inmediatamente al abrirlo en el navegador. Reemplaza el `index.html` en esta carpeta con este nuevo código.

