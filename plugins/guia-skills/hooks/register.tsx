import type { Register } from 'claude-code'

const PANE = 'guia-skills'
const TITLE = 'Skills por tarea'

// [tarea, skill(s), ejemplo de pedido]. Varias skills en una fila: separarlas con " · ".
// ponytail: lista fija; edítala a mano para sumar o quitar filas.
const GUIA: [string, [string, string, string][]][] = [
  ['Código', [
    ['Idea o feature nueva', 'superpowers:brainstorming', '"quiero hacer X" / "I want to build X"'],
    ['Proyecto grande (plan escrito)', 'egm:egm-draft', '"/egm:egm-draft"'],
    ['Un bug', 'superpowers:systematic-debugging', '"esto falla: ..." / "this is broken: ..."'],
    ['Revisar cambios', 'code-review', '"/code-review"'],
    ['Entender un proyecto', 'graphify', '"/graphify"'],
  ]],
  ['Web y diseño', [
    ['Web o landing nueva', 'design-taste-frontend', '"landing para una cafetería"'],
    ['De captura a código', 'image-to-code', '"pasá esta captura a código"'],
    ['Marca, logo, paleta', 'brandkit', '"kit de marca para..."'],
    ['Animaciones', 'improve-animations', '"mejorá las animaciones"'],
    ['UI que se ve "amateur"', 'ux-design:refactoring-ui', '"mi UI se ve rara, arreglala"'],
  ]],
  ['Contenido y redes', [
    ['Calendario de posts', 'ig-content-planner', '"armá el calendario de la semana"'],
    ['Caption', 'ig-caption-writer', '"caption para este reel"'],
    ['Carrusel', 'ig-carousel-planner', '"carrusel sobre 3 errores de..."'],
    ['Ganchos', 'ig-hook-extractor', '"ganchos para este tema"'],
    ['Que no suene a IA', 'humanizer', '"humanizá este texto"'],
  ]],
  ['Video', [
    ['Reel o video', 'hyperframes', '"hacé un video de 15 s sobre..."'],
    ['Música, voz, imágenes', 'media-use', '"ponele música de fondo"'],
    ['Subtítulos', 'embedded-captions', '"subtitulá este video"'],
    ['Video explicativo', 'faceless-explainer', '"video explicativo sobre..."'],
    ['Guion de YouTube', 'youtube-scriptwriting', '"guion de 8 min sobre..."'],
  ]],
  ['Ventas y marketing', [
    ['Email en frío', 'cold-email', '"email de prospección para..."'],
    ['Armar la oferta', 'offers', '"mejorá mi oferta"'],
    ['Textos de la web', 'copywriting', '"reescribí el hero"'],
    ['SEO', 'seo-audit', '"auditá el SEO de la web"'],
    ['Anuncios', 'ad-creative', '"10 variantes de anuncio"'],
  ]],
  ['Investigar', [
    ['Qué se dice hoy', 'last30days', '"qué se dice de X en los últimos 30 días"'],
    ['Investigación larga', 'deep-research', '"investigá a fondo..."'],
    ['Buscar más skills', 'find-skills', '"¿hay una skill para...?"'],
  ]],
  ['Documentos', [
    ['Word, PowerPoint, Excel, PDF', 'docx · pptx · xlsx · pdf', '"pasalo a Word"'],
    ['Presentación', 'frontend-slides', '"presentación sobre..."'],
    ['Revisar un contrato', 'contract-review', '"revisá este contrato"'],
    ['Caso de negocio', 'business-case', '"¿conviene invertir en...?"'],
  ]],
  ['Sesión', [
    ['Pasar a sesión nueva', 'handoff', '"/handoff tema"'],
    ['Cambiar perfil de skills', 'perfiles', '"hoy toca video"'],
  ]],
]

// Palabra clave en el pedido → skill sugerida. La primera que coincide gana.
// Verbo de pedido + objeto cerca: "hacé un reel" sí, "agregaste algo de los videos?" no.
// ponytail: regex, no modelo; si sugiere mal, ajusta la regla acá.
const V = String.raw`(?<!\p{L})(hac[eé]|hacer|haceme|arm[aá]|armar|armame|cre[aá]|crear|gener[aá]|generar|edit[aá]|editar|escrib[ií]|escribir|dise[ñn][aá]|dise[ñn]ar|mejor[aá]|mejorar|reescrib[ií]|pas[aá]|pasar|quiero|necesito|sac[aá]|pon[eé]|agreg[aá]|planific[aá]|audit[aá]|revis[aá]|busc[aá]|make|create|build|write|generate|edit|design|improve|rewrite|convert|need|want|add|plan|audit|review|find)(?!\p{L})`
const pide = (objeto: string) => new RegExp(`${V}.{0,40}(${objeto})`, 'iu')

const REGLAS: [RegExp, string][] = [
  [pide('calendario|content calendar'), 'ig-content-planner'],
  [pide('caption|epígrafe'), 'ig-caption-writer'],
  [pide('carrusel|carousel'), 'ig-carousel-planner'],
  [pide('ganchos?|hooks?'), 'ig-hook-extractor'],
  [/suene (a )?ia|humaniz|sounds? (like )?ai/i, 'humanizer'],
  [pide('subt[ií]tul|subtitles?|captions? for'), 'embedded-captions'],
  [pide('stickman|faceless|explainer'), 'faceless-explainer'],
  [pide('gui[oó]n|script'), 'youtube-scriptwriting'],
  [pide('m[uú]sica|voz|sonido|music|voiceover'), 'media-use'],
  [pide('reel|video'), 'hyperframes'],
  [/captura.{0,30}c[oó]digo|screenshot.{0,30}code/i, 'image-to-code'],
  [pide('logo|paleta|branding|kit de marca|brand kit|palette'), 'brandkit'],
  [pide('animaciones|animations?'), 'improve-animations'],
  [pide('landing|p[aá]gina web|web nueva|una web|website|web page'), 'design-taste-frontend'],
  [pide('email|mail'), 'cold-email'],
  [pide('oferta|garant[ií]a|offer|guarantee'), 'offers'],
  [pide('precios?|cotizaci[oó]n|pricing'), 'pricing'],
  [pide('seo'), 'seo-audit'],
  [pide('anuncios?|ads?\\b'), 'ad-creative'],
  [pide('textos?|copy|hero|titular|headline'), 'copywriting'],
  [/\b(esto|eso|la web|el script|el bot|this|it) (falla|no anda|tira error|se rompe|is broken|fails|crashes)|\bbug\b/i, 'superpowers:systematic-debugging'],
  [/revis[aá] (el |los )?(c[oó]digo|cambios)|review (my |the )?(code|changes)/i, 'code-review'],
  [/qu[eé] se dice|[uú]ltimos 30 d[ií]as|last 30 days/i, 'last30days'],
  [/investig[aá] a fondo|investigaci[oó]n (larga|profunda)|deep research/i, 'deep-research'],
  [pide('contrato|contract'), 'contract-review'],
  [/\b(en|a|un|to|into) word\b|\.docx/i, 'docx'],
  [/powerpoint|\.pptx|diapositivas|slide deck/i, 'pptx'],
  [/\bexcel\b|planilla|spreadsheet|\.xlsx/i, 'xlsx'],
  [pide('pdf'), 'pdf'],
  [pide('presentaci[oó]n|presentation'), 'frontend-slides'],
  [/sesi[oó]n nueva|new session/i, 'handoff'],
  [/skill para|hay (una )?skill|is there a skill/i, 'find-skills'],
  [/quiero (hacer|armar|crear)|idea nueva|i want to build/i, 'superpowers:brainstorming'],
]

// Skills instaladas en esta sesión (null = no se pudo averiguar: se muestra todo).
let instaladas: Set<string> | null = null
// Skills que la persona rechazó o silenció en esta sesión: no se vuelve a preguntar.
const silenciadas = new Set<string>()

const tiene = (fila: string): boolean => {
  if (!instaladas) return true
  return fila.split(/\s[·/]\s/).some(n => {
    const nombre = n.trim()
    const corto = nombre.split(':').pop()!
    return instaladas!.has(nombre) || instaladas!.has(corto) || [...instaladas!].some(i => i.endsWith(':' + corto))
  })
}

const leerInstaladas = async ($: any) => {
  try {
    const u = await $.session.usage({ breakdown: 'summary' })
    const lista = u?.context?.breakdown?.skills?.skillFrontmatter
    instaladas = Array.isArray(lista) && lista.length ? new Set<string>(lista.map((s: { name: string }) => s.name)) : null
  } catch {
    instaladas = null
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'guia', description: 'Abre la guía de qué skill usar para cada tarea' })
    await leerInstaladas($)
    return next(e)
  })

  on('prompt.submit', async ($, e, next) => {
    if (e.command || e.isMeta) return next(e)
    const hit = REGLAS.find(([re]) => re.test(e.text))
    if (!hit) return next(e)
    const skill = hit[1]
    if (silenciadas.has(skill) || !tiene(skill)) return next(e)
    $.ui.status(`skill sugerida: ${skill}`)
    const si = 'Sí, usala'
    const no = 'No'
    const nunca = 'No sugerir más en esta sesión'
    const answer = await $.ui
      .ask(`¿Uso la skill ${skill} para esto?`, { header: 'Skill', options: [si, no, nunca] })
      .catch(() => no)
    if (answer === nunca) silenciadas.add(skill)
    return next(answer === si ? { ...e, text: `Usá la skill ${skill}. ${e.text}` } : e)
  })

  on('turn.complete', ($, e, next) => {
    $.ui.status(undefined)
    return next(e)
  })

  on('command.run', { command: 'guia' }, async $ => {
    await leerInstaladas($)
    await $.ui.open({ id: PANE, title: TITLE })
    return { text: 'Guía de skills abierta.' }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    return (
      <Box flexDirection="column">
        <Text dimColor>No hace falta nombrar la skill: pídelo así y la uso yo. Las que no tienes instaladas salen en gris.</Text>
        {GUIA.map(([area, filas]) => (
          <Box flexDirection="column" marginTop={1}>
            <Text bold>{area}</Text>
            {filas.map(([tarea, skill, ej]) =>
              tiene(skill) ? (
                <Text wrap="wrap">
                  {tarea} → <Text color="cyan">{skill}</Text> <Text dimColor>{ej}</Text>
                </Text>
              ) : (
                <Text wrap="wrap" dimColor>
                  {tarea} → {skill} (no instalada; búscala con find-skills)
                </Text>
              ),
            )}
          </Box>
        ))}
      </Box>
    )
  })
}
