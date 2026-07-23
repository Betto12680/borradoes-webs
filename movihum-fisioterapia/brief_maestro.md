# Brief de Desarrollo Web: MOVIHUM Fisioterapia

## 1. Información del Cliente
- **Nombre**: MOVIHUM Fisioterapia
- **Nicho**: Fisioterapia & Osteopatía
- **Ciudad**: Guadalajara
- **Teléfono de Contacto**: +52 33 3642 4567 (WhatsApp: 523336424567)
- **Calificación en Google Maps**: 4.8 Estrellas
- **Cantidad de Reseñas**: 36 reseñas

## 2. Paleta de Colores Autorizada
**IMPORTANTE: NUNCA usar rojo, ni colores relacionados con la sangre, la violencia o el peligro, ni fondos negros puros. Todo debe transmitir limpieza, paz, clínica, salud y profesionalismo.**

- **Primario**: #0d9488 (Turquesa Salud)
- **Secundario**: #14b8a6 (Teal Brillante)
- **Fondo Oscuro (Hero)**: #115e59 (Turquesa Profundo, NUNCA negro)
- **Acentos**: Blanco, gris perla y toques de verde vitalidad.

## 3. Banco de Imágenes de Referencia (Unsplash)

- **Hero Image**: https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?auto=format&fit=crop&w=1200&q=80 (Fisioterapia, terapia manual)
- **Carrusel 1**: https://images.unsplash.com/photo-1519823551278-64ac92734fb1?auto=format&fit=crop&w=1200&q=80
- **Carrusel 2**: https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1200&q=80
- **Carrusel 3**: https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?auto=format&fit=crop&w=1200&q=80

## 4. Estructura y Textos del Borrador
*(Texto borrador inventado)*
- **Hero Titular**: Recupera tu Movilidad y Dile Adiós al Dolor en Guadalajara
- **Hero Subtítulo**: Fisioterapia deportiva, neurológica y traumatológica guiada por especialistas. Recuperación acelerada con la mejor tecnología.
- **Servicios Principales**: 
  1. Terapia Manual y Liberación Miofascial
  2. Rehabilitación Deportiva
  3. Fisioterapia Post-Operatoria
  4. Punción Seca y Electrólisis

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

