# Memoria del proceso — Borradores web para clientes

Este documento explica **cómo se construyen** los borradores de página web de esta carpeta, para que cualquier sesión futura (tuya o de Claude) pueda seguir el mismo estándar sin tener que redescubrirlo. Última actualización: julio 2026, tras la ronda de mejora de las 15 primeras webs (fisioterapeutas de Medellín).

---

## 1. Estructura de carpetas

```
clientes/web/
├── Clientes.xlsx                    ← hoja "EMPRESAS MAPS", fuente de verdad de cada negocio
├── _stock/                          ← banco de fotos libres (Pexels) reutilizables entre clientes del mismo rubro
├── investigaciones web/             ← benchmarks de referentes por sector (ver sección 6)
└── [Nombre Empresa]/
    ├── index.html                   ← una sola página autocontenida (HTML+CSS+JS inline, sin dependencias externas)
    └── img/                         ← fotos reales del negocio + apoyo de _stock si hacía falta
```

**Por qué todo va en un solo `index.html`:** el flujo de entrega es arrastrar la carpeta del cliente a Netlify Drop ("Add new site → Deploy manually"). Un archivo autocontenido evita romper rutas relativas y facilita mandar la carpeta comprimida por WhatsApp/correo si hace falta.

---

## 2. Cómo se consiguen las fotos

1. Se abre el perfil de Google Maps del negocio (o el CID / link de búsqueda de la hoja de cálculo).
2. Se extraen las URLs de foto reales vía JS en el navegador (`document.querySelectorAll('img')` filtrando `googleusercontent.com`), no capturas de pantalla.
3. Se descargan con `curl` a `img/` dentro de la carpeta del cliente, pidiendo la resolución más alta disponible (`=w1400-h...`).
4. **Regla de oro:** revisar cada foto antes de usarla. Google Maps mezcla a veces fotos de negocios vecinos — se descartó más de una foto que resultó ser de otra empresa (ej. una marca "DMO" que apareció en el perfil de Activ Fisioterapia).
5. Si el negocio no tiene fotos propias utilizables, se usa banco de imágenes libres (Pexels, sin atribución requerida) guardado en `_stock/` para reutilizar entre clientes del mismo rubro y no descargar la misma imagen 15 veces.

---

## 3. Colores de marca — cómo se investigan

**No inventar la paleta a ojo si se puede verificar.** Proceso:

1. Buscar la página de **Facebook** del negocio (`site:facebook.com "nombre del negocio"` en Google, o el handle si ya se conoce de investigaciones previas).
2. En la página de Facebook, extraer vía JS las URLs de imagen que contienen `scontent`/`fbcdn` y no sean iconos (`rsrc.php`). La foto de perfil (`t39.30808-1`) suele ser el **logo real**.
3. Descargar el logo y **mirarlo** (con la herramienta de lectura de imágenes) — no asumir el color por el nombre de la marca.
4. Si hace falta el hex exacto, usar cuantización de color con PIL (`Image.quantize()`) filtrando neutros (blancos/negros/grises de bajo saturación) para sacar el color dominante real.
5. Si el negocio tiene web propia activa (aunque no se le vaya a construir un borrador), revisar esa web también — a veces confirma o corrige el hallazgo de Facebook.
6. Si no hay Facebook/Instagram con logo identificable (perfil personal, solo fotos de la persona), **no inventar una marca falsa**: se mantiene una paleta profesional coherente con la especialidad, y se documenta explícitamente que no hay color verificado (ver tabla de la sección 5).

**Aprendizaje clave de esta ronda:** de 15 negocios, 7 tenían logo verificable en redes y **la mitad tenía un color de marca real distinto al que se había asumido** en el primer borrador (ej. BMS resultó ser rojo/negro, no teal; Centro de Ortopedia resultó navy+naranja, no vino). Vale la pena investigar antes de diseñar, no después.

---

## 4. El "kit de mejora" — animación + SEO reutilizable

Todo borrador nuevo debe incluir este kit, copiado tal cual (ya probado en las 15 webs) y solo ajustando nombres de variables de color:

### 4.1 CSS de animación (scroll-reveal + micro-interacciones)

```css
@media (prefers-reduced-motion: no-preference){
  [data-reveal]{opacity:0;transform:translateY(28px);transition:opacity .8s cubic-bezier(.16,.84,.44,1),transform .8s cubic-bezier(.16,.84,.44,1)}
  [data-reveal].is-visible{opacity:1;transform:translateY(0)}
  [data-reveal-stagger]>*{opacity:0;transform:translateY(22px);transition:opacity .6s ease,transform .6s ease}
  [data-reveal-stagger].is-visible>*{opacity:1;transform:translateY(0)}
  [data-reveal-stagger].is-visible>*:nth-child(1){transition-delay:.04s}
  [data-reveal-stagger].is-visible>*:nth-child(2){transition-delay:.11s}
  [data-reveal-stagger].is-visible>*:nth-child(3){transition-delay:.18s}
  [data-reveal-stagger].is-visible>*:nth-child(4){transition-delay:.25s}
  .kenburns{animation:kenburns 24s ease-in-out infinite alternate}
  @keyframes kenburns{from{transform:scale(1)}to{transform:scale(1.07)}}
}
nav{transition:box-shadow .3s ease}
nav.is-scrolled{box-shadow:0 6px 24px rgba(0,0,0,.1)}
.zoom-wrap{overflow:hidden;border-radius:XXpx}
.zoom-wrap img{transition:transform .6s ease}
.zoom-wrap:hover img{transform:scale(1.06)}
.wa-float .pulse{position:absolute;inset:0;border-radius:50%;background:inherit;animation:wapulse 2.4s ease-out infinite;z-index:-1}
@keyframes wapulse{0%{transform:scale(1);opacity:.55}100%{transform:scale(2.1);opacity:0}}
.faq-item{border-bottom:1px solid VAR_LINEA;padding:22px 0}
.faq-item summary{cursor:pointer;font-weight:700;font-size:1.02rem;display:flex;justify-content:space-between;align-items:center;list-style:none}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary::after{content:"+";font-size:1.4rem;color:VAR_ACENTO;transition:transform .25s ease;flex:none;margin-left:16px}
.faq-item[open] summary::after{transform:rotate(45deg)}
.faq-item p{margin-top:12px;color:VAR_GRIS;font-size:.95rem;max-width:680px}
```

**Uso:**
- `data-reveal` en cualquier bloque que deba aparecer al hacer scroll (título de sección, columna de texto, tarjeta de contacto...).
- `data-reveal-stagger` en el contenedor de una grilla (`.cards`, `.gal-grid`, `.step-grid`) para que sus hijos aparezcan en cascada.
- `zoom-wrap` envolviendo **solo la `<img>`** (nunca un badge o texto superpuesto encima, o quedará recortado por `overflow:hidden`) para el efecto de zoom al hover.
- `kenburns` en la imagen del hero para el zoom lento automático (o en un div `.hero-bg` si el hero usa `background-image` en vez de `<img>`).

### 4.2 JavaScript (una sola vez, antes de `</body>`)

```html
<script>
(function(){
  var els = document.querySelectorAll('[data-reveal],[data-reveal-stagger]');
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){ if(e.isIntersecting){ e.target.classList.add('is-visible'); io.unobserve(e.target);} });
    },{threshold:.12,rootMargin:'0px 0px -60px 0px'});
    els.forEach(function(e){io.observe(e)});
  } else { els.forEach(function(e){e.classList.add('is-visible')}); }
  var nav = document.querySelector('nav');
  if(nav){ window.addEventListener('scroll', function(){ nav.classList.toggle('is-scrolled', window.scrollY>30); }, {passive:true}); }
  document.querySelectorAll('.count-up').forEach(function(el){
    var target = parseFloat(el.getAttribute('data-count'));
    var done=false;
    var obs = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if(entry.isIntersecting && !done){
          done=true;
          var start=null, dur=1300, isDecimal = el.hasAttribute('data-decimal');
          function step(ts){ if(!start)start=ts; var p=Math.min((ts-start)/dur,1); var eased=1-Math.pow(1-p,3);
            el.textContent = isDecimal ? (eased*target).toFixed(1) : Math.floor(eased*target).toLocaleString('es-CO');
            if(p<1) requestAnimationFrame(step); else el.textContent = isDecimal ? target.toFixed(1) : target.toLocaleString('es-CO'); }
          requestAnimationFrame(step);
          obs.unobserve(el);
        }
      });
    },{threshold:.4});
    obs.observe(el);
  });
})();
</script>
```

**⚠️ Trampa ya resuelta:** el contador `.count-up` debe usar `parseFloat` (no `parseInt`) y el atributo `data-count` debe llevar el **valor decimal completo** (ej. `data-count="4.4"`, no `data-count="4"`) cuando `data-decimal` está presente. Con `parseInt` truncaba 4.4 a 4 y el contador terminaba mostrando "4.0" en vez de "4.4".

Ejemplo de uso del contador en el hero:
```html
<span class="count-up" data-count="4.9" data-decimal="1">4.9</span> · <span class="count-up" data-count="66">66</span> reseñas en Google
```

### 4.3 SEO en `<head>`

Por cada web se agrega, además del `<title>` y `<meta description>` ya existentes:
- `<meta name="robots" content="index, follow">`
- `<meta name="keywords">` con 3-4 términos de búsqueda reales (servicio + barrio/ciudad)
- Open Graph completo (`og:type`, `og:title`, `og:description`, `og:image`, `og:locale content="es_CO"`)
- `<meta name="twitter:card" content="summary_large_image">`
- **JSON-LD** con `@type` según el rubro (`PhysicalTherapy`, `MedicalClinic`, `HealthClub`, etc.), incluyendo `telephone`, `address` (PostalAddress con `addressCountry:"CO"`), y **`aggregateRating`** con el rating/reviewCount real tomado de la hoja de Excel — esto es lo que permite que Google muestre estrellas ⭐ en el resultado de búsqueda.

No se agregó `canonical` porque la URL final de Netlify no se conoce de antemano; se puede añadir cuando el cliente confirme el dominio definitivo.

### 4.4 Contenido — sección FAQ nueva

Cada web ganó una sección de **preguntas frecuentes** (4 preguntas, con `<details>/<summary>` nativos de HTML — sin JS extra, funcionan solos) adaptadas al tipo de negocio:
- Fisioterapia general: orden médica, duración de sesión, tipo de lesiones, qué llevar.
- Domiciliaria: zona de cobertura, si necesitas equipos en casa, cómo agendar.
- Dermatofuncional/postquirúrgica: cuándo empezar el drenaje, cuántas sesiones, si trabaja con cualquier cirujano.

Esto aporta profundidad de contenido real (no relleno) y ayuda al SEO por preguntas long-tail.

---

## 5. Registro de colores por cliente (ronda de fisioterapia, julio 2026)

| Cliente | Fuente del color | Resultado |
|---|---|---|
| Recover Station | Web propia real (recoverstation.com) | Negro/blanco minimalista + acento bronce (antes: sand/bronze genérico) |
| Activ Fisioterapia | Logo en Facebook (Activft) | Azul marino `#14436c` real (antes: azul genérico `#0e5fd8`) |
| Centro de Ortopedia El Poblado | Logo en Facebook (3.3k seguidores) | Navy `#223c55` + naranja `#e2782f` (antes: vino/maroon, completamente distinto) |
| Centro de Rehabilitación BMS | Logo en Facebook | Rojo `#d81f24` + negro/carbón (antes: teal, completamente distinto) |
| Fisioterapeuta Andrés Piñeros | Logo en Facebook (fisioandresp) | Negro + turquesa `#2ecfb4` (antes: verde salvia claro — se mantuvo el tono verde-azulado pero se llevó a fondo oscuro dramático) |
| Rehab Motion | Logo en Facebook | Teal `#1dae9a` — coincidía ya con el borrador, sin cambios de color |
| Fissio T | Web propia real (fissiot.com) | Petróleo `#1c6a7c` + naranja (antes: índigo/lavanda, sin relación) |
| Bestrong Fisioterapia | Foto de fachada (letrero físico) ya en `img/` | Ámbar `#f2a900` + carbón — ya coincidía, sin cambios |
| Ana María Serna / Sandra Vásquez | Solo foto personal en Facebook | Sin marca verificable → se mantuvo paleta petrol/hielo elegida a criterio |
| Dra. Juliana Torné | Solo foto personal en Facebook | Sin marca verificable → se mantuvo paleta coral/arena |
| Andrea Katich Kurk | Página de Facebook fue dada de baja | Sin marca verificable → se mantuvo paleta salvia/hueso |
| Dra. María Andrea Ríos | Sin Facebook encontrado | Sin marca verificable → se mantuvo paleta lila/crema |
| Tatiana Tirado | Sin página de marca en Instagram (solo apariciones en eventos) | Sin marca verificable → se mantuvo paleta magenta/rosa |
| Prof. Juliana Restrepo | Sin Facebook encontrado | Sin marca verificable → se mantuvo paleta azul/celeste |
| Daniela Herrera (D'fisio) | Sin Facebook encontrado | Sin marca verificable → se mantuvo paleta nude/crema |

**Regla para el futuro:** si en una próxima ronda se encuentra el logo real de alguno de los 7 "sin marca verificable", actualizar su paleta siguiendo el mismo proceso de la sección 3.

---

## 6. Carpeta `investigaciones web/`

Contiene benchmarks de 3 sitios referentes por sector (odontología, ópticas, fisioterapia, glamping), con capturas de pantalla y análisis en 6 dimensiones (imagen, efectos, composición, jerarquía, SEO, conversión). Cada informe termina en un **"Playbook"** de puntos concretos a replicar — el kit de la sección 4 de este documento es la implementación práctica de esos playbooks para el sector fisioterapia. Al abordar odontología, ópticas o glamping, releer el informe de ese sector antes de diseñar.

---

## 7. Checklist para la próxima empresa nueva

1. [ ] Sacar fotos reales de Google Maps (verificar que sean del negocio correcto).
2. [ ] Buscar Facebook/Instagram → extraer y mirar el logo real → definir paleta (o documentar "sin marca verificable").
3. [ ] Redactar contenido: hero con promesa (no descripción de servicio), 4 servicios, sección "nosotros/nosotras", testimonio/cita, **FAQ de 4 preguntas**, contacto con WhatsApp.
4. [ ] Pegar el kit de animación CSS + JS de la sección 4.
5. [ ] Añadir bloque SEO completo del `<head>` (OG + Twitter + JSON-LD con rating real de la hoja de Excel).
6. [ ] Marcar `data-reveal` / `data-reveal-stagger` / `zoom-wrap` / `kenburns` en las secciones.
7. [ ] Verificar en navegador: que el hero cargue, que el contador de reseñas termine en el número correcto, que el acordeón FAQ abra/cierre.
8. [ ] Marcar la fila correspondiente en amarillo en `Clientes.xlsx` con nota de estado.
