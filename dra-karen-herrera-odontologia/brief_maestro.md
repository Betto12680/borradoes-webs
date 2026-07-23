# Brief de Desarrollo Web: Dra. Karen Herrera Odontología

## 1. Información del Cliente
- **Nombre**: Dra. Karen Herrera Odontología
- **Nicho**: Odontología General
- **Ciudad**: Guadalajara
- **Teléfono de Contacto**: +52 33 3615 4567 (WhatsApp: 523336154567)
- **Calificación en Google Maps**: 4.8 Estrellas
- **Cantidad de Reseñas**: 19 reseñas

## 2. Paleta de Colores Autorizada
**IMPORTANTE: NUNCA usar rojo, ni colores relacionados con la sangre, la violencia o el peligro, ni fondos negros puros. Todo debe transmitir limpieza, paz, clínica, salud y profesionalismo.**

- **Primario**: #0284c7 (Azul Médico)
- **Secundario**: #38bdf8 (Cian Suave)
- **Fondo Oscuro (Hero)**: #0c4a6e (Azul Profundo, NUNCA negro)
- **Acentos**: Blanco puro y dorado suave para estrellas de reseñas.

## 3. Banco de Imágenes de Referencia (Unsplash)

- **Hero Image**: https://images.unsplash.com/photo-1606811841689-23dfddce3e95?auto=format&fit=crop&w=1200&q=80 (Clínica limpia y moderna)
- **Carrusel 1**: https://images.unsplash.com/photo-1598256989800-fe5f95da9787?auto=format&fit=crop&w=1200&q=80
- **Carrusel 2**: https://images.unsplash.com/photo-1629909613654-28e377c37b09?auto=format&fit=crop&w=1200&q=80
- **Carrusel 3**: https://images.unsplash.com/photo-1588776814546-1ffcf47267a5?auto=format&fit=crop&w=1200&q=80

## 4. Estructura y Textos del Borrador
*(Texto borrador inventado)*
- **Hero Titular**: Odontología Avanzada y Diseño de Sonrisa en Guadalajara
- **Hero Subtítulo**: Especialistas certificados enfocados en devolverte la confianza al sonreír, con tecnología digital 3D y tratamientos sin dolor.
- **Servicios Principales**: 
  1. Diseño de Sonrisa en 3D
  2. Ortodoncia Invisible
  3. Implantes Dentales de Carga Inmediata
  4. Blanqueamiento Láser Clínico

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

