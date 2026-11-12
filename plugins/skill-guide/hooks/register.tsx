import type { Register } from 'claude-code'

const PANE = 'skill-guide'
const TITLE = 'Skills by task'

// [task, skill(s), example request]. Several skills in one row: separate them with " · ".
// ponytail: fixed list; edit by hand to add or remove rows.
const GUIDE: [string, [string, string, string][]][] = [
  ['Code', [
    ['New idea or feature', 'superpowers:brainstorming', '"I want to build X"'],
    ['Big project (written plan)', 'egm:egm-draft', '"/egm:egm-draft"'],
    ['A bug', 'superpowers:systematic-debugging', '"this is broken: ..."'],
    ['Review changes', 'code-review', '"/code-review"'],
    ['Understand a project', 'graphify', '"/graphify"'],
  ]],
  ['Web and design', [
    ['New site or landing page', 'design-taste-frontend', '"landing page for a coffee shop"'],
    ['Screenshot to code', 'image-to-code', '"turn this screenshot into code"'],
    ['Brand, logo, palette', 'brandkit', '"brand kit for ..."'],
    ['Animations', 'improve-animations', '"improve the animations"'],
    ['UI that looks "amateur"', 'ux-design:refactoring-ui', '"my UI looks off, fix it"'],
  ]],
  ['Content and social', [
    ['Post calendar', 'ig-content-planner', '"plan this week\'s posts"'],
    ['Caption', 'ig-caption-writer', '"caption for this reel"'],
    ['Carousel', 'ig-carousel-planner', '"carousel about 3 mistakes in ..."'],
    ['Hooks', 'ig-hook-extractor', '"hooks for this topic"'],
    ['Make it not sound like AI', 'humanizer', '"humanize this text"'],
  ]],
  ['Video', [
    ['Reel or video', 'hyperframes', '"make a 15 s video about ..."'],
    ['Music, voice, images', 'media-use', '"add background music"'],
    ['Subtitles', 'embedded-captions', '"add subtitles to this video"'],
    ['Explainer video', 'faceless-explainer', '"explainer video about ..."'],
    ['YouTube script', 'youtube-scriptwriting', '"8 min script about ..."'],
  ]],
  ['Sales and marketing', [
    ['Cold email', 'cold-email', '"outreach email for ..."'],
    ['Build the offer', 'offers', '"improve my offer"'],
    ['Website copy', 'copywriting', '"rewrite the hero"'],
    ['SEO', 'seo-audit', '"audit the site\'s SEO"'],
    ['Ads', 'ad-creative', '"10 ad variations"'],
  ]],
  ['Research', [
    ['What people say today', 'last30days', '"what is being said about X in the last 30 days"'],
    ['Long research', 'deep-research', '"research this in depth ..."'],
    ['Find more skills', 'find-skills', '"is there a skill for ...?"'],
  ]],
  ['Documents', [
    ['Word, PowerPoint, Excel, PDF', 'docx · pptx · xlsx · pdf', '"turn it into a Word doc"'],
    ['Presentation', 'frontend-slides', '"presentation about ..."'],
    ['Review a contract', 'contract-review', '"review this contract"'],
    ['Business case', 'business-case', '"is it worth investing in ...?"'],
  ]],
  ['Session', [
    ['Move to a new session', 'handoff', '"/handoff topic"'],
    ['Switch skill profile', 'skill-profiles', '"today is video day"'],
  ]],
]

// Keyword in the request → suggested skill. The first rule that matches wins.
// Request verb + nearby object: "make a reel" yes, "did you add anything about the videos?" no.
// English and Spanish triggers on purpose.
// ponytail: regex, not a model; if it suggests wrong, tweak the rule here.
const V = String.raw`(?<!\p{L})(make|create|build|write|generate|edit|design|improve|rewrite|convert|need|want|add|plan|audit|review|find|hac[eé]|hacer|haceme|arm[aá]|armar|armame|cre[aá]|crear|gener[aá]|generar|edit[aá]|editar|escrib[ií]|escribir|dise[ñn][aá]|dise[ñn]ar|mejor[aá]|mejorar|reescrib[ií]|pas[aá]|pasar|quiero|necesito|sac[aá]|pon[eé]|agreg[aá]|planific[aá]|audit[aá]|revis[aá]|busc[aá])(?!\p{L})`
const asks = (object: string) => new RegExp(`${V}.{0,40}(${object})`, 'iu')

const RULES: [RegExp, string][] = [
  [asks('content calendar|calendario'), 'ig-content-planner'],
  [asks('captions?|epígrafe'), 'ig-caption-writer'],
  [asks('carousel|carrusel'), 'ig-carousel-planner'],
  [asks('hooks?|ganchos?'), 'ig-hook-extractor'],
  [/sounds? (like )?ai|humaniz|suene (a )?ia/i, 'humanizer'],
  [asks('subtitles?|subt[ií]tul'), 'embedded-captions'],
  [asks('explainer|faceless|stickman'), 'faceless-explainer'],
  [asks('script|gui[oó]n'), 'youtube-scriptwriting'],
  [asks('music|voiceover|m[uú]sica|voz|sonido'), 'media-use'],
  [asks('reel|video'), 'hyperframes'],
  [/screenshot.{0,30}code|captura.{0,30}c[oó]digo/i, 'image-to-code'],
  [asks('logo|palette|brand kit|branding|paleta|kit de marca'), 'brandkit'],
  [asks('animations?|animaciones'), 'improve-animations'],
  [asks('landing|website|web page|p[aá]gina web|web nueva|una web'), 'design-taste-frontend'],
  [asks('email|mail'), 'cold-email'],
  [asks('offer|guarantee|oferta|garant[ií]a'), 'offers'],
  [asks('pricing|precios?|cotizaci[oó]n'), 'pricing'],
  [asks('seo'), 'seo-audit'],
  [asks('ads?\\b|anuncios?'), 'ad-creative'],
  [asks('copy|headline|hero|textos?|titular'), 'copywriting'],
  [/\b(this|it|esto|eso|la web|el script|el bot) (is broken|fails|crashes|falla|no anda|tira error|se rompe)|\bbug\b/i, 'superpowers:systematic-debugging'],
  [/review (my |the )?(code|changes)|revis[aá] (el |los )?(c[oó]digo|cambios)/i, 'code-review'],
  [/last 30 days|qu[eé] se dice|[uú]ltimos 30 d[ií]as/i, 'last30days'],
  [/deep research|investig[aá] a fondo|investigaci[oó]n (larga|profunda)/i, 'deep-research'],
  [asks('contract|contrato'), 'contract-review'],
  [/\b(to|into|en|a|un) word\b|\.docx/i, 'docx'],
  [/powerpoint|\.pptx|slide deck|diapositivas/i, 'pptx'],
  [/\bexcel\b|spreadsheet|planilla|\.xlsx/i, 'xlsx'],
  [asks('pdf'), 'pdf'],
  [asks('presentation|presentaci[oó]n'), 'frontend-slides'],
  [/new session|sesi[oó]n nueva/i, 'handoff'],
  [/is there a skill|skill para|hay (una )?skill/i, 'find-skills'],
  [/i want to build|quiero (hacer|armar|crear)|idea nueva/i, 'superpowers:brainstorming'],
]

// Skills installed in this session (null = couldn't find out: show everything).
let installed: Set<string> | null = null
// Skills the person declined or muted this session: don't ask again.
const muted = new Set<string>()

const has = (row: string): boolean => {
  if (!installed) return true
  return row.split(/\s[·/]\s/).some(n => {
    const name = n.trim()
    const short = name.split(':').pop()!
    return installed!.has(name) || installed!.has(short) || [...installed!].some(i => i.endsWith(':' + short))
  })
}

const readInstalled = async ($: any) => {
  try {
    const u = await $.session.usage({ breakdown: 'summary' })
    const list = u?.context?.breakdown?.skills?.skillFrontmatter
    installed = Array.isArray(list) && list.length ? new Set<string>(list.map((s: { name: string }) => s.name)) : null
  } catch {
    installed = null
  }
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({ name: 'guide', description: 'Open the guide to which skill to use for each task' })
    await readInstalled($)
    return next(e)
  })

  on('prompt.submit', async ($, e, next) => {
    if (e.command || e.isMeta) return next(e)
    const hit = RULES.find(([re]) => re.test(e.text))
    if (!hit) return next(e)
    const skill = hit[1]
    if (muted.has(skill) || !has(skill)) return next(e)
    $.ui.status(`suggested skill: ${skill}`)
    const yes = 'Yes, use it'
    const no = 'No'
    const never = "Don't suggest again this session"
    const answer = await $.ui
      .ask(`Use the ${skill} skill for this?`, { header: 'Skill', options: [yes, no, never] })
      .catch(() => no)
    if (answer === never) muted.add(skill)
    return next(answer === yes ? { ...e, text: `Use the ${skill} skill. ${e.text}` } : e)
  })

  on('turn.complete', ($, e, next) => {
    $.ui.status(undefined)
    return next(e)
  })

  on('command.run', { command: 'guide' }, async $ => {
    await readInstalled($)
    await $.ui.open({ id: PANE, title: TITLE })
    return { text: 'Skill guide opened.' }
  })

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    return (
      <Box flexDirection="column">
        <Text dimColor>No need to name the skill: just ask like this and I'll use it. Skills you don't have installed are greyed out.</Text>
        {GUIDE.map(([area, rows]) => (
          <Box flexDirection="column" marginTop={1}>
            <Text bold>{area}</Text>
            {rows.map(([task, skill, example]) =>
              has(skill) ? (
                <Text wrap="wrap">
                  {task} → <Text color="cyan">{skill}</Text> <Text dimColor>{example}</Text>
                </Text>
              ) : (
                <Text wrap="wrap" dimColor>
                  {task} → {skill} (not installed; find it with find-skills)
                </Text>
              ),
            )}
          </Box>
        ))}
      </Box>
    )
  })
}
