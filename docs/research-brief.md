# Karpathy Understanding Ladder — From Tweet to Agent Skills

Date: 2026-10-08 | Method: Reach-first (agent-reach OpenCLI + webfetch mirror + context7)

## Researcher haul summary (what the subagent brought back)

The researcher task returned 5 raw drops in `inbox/`, 2 immutable source extracts in `sources/`, and a working note in `notes/`, no brief per constraints. Primary tweet text was retrieved via `opencli twitter thread 2105819303471976479` [verified-primary] and cross-checked against `nitter.cf` mirror [verified-primary]. Thread replies (~30 recent, plus 15 high-engagement quote-tweets via search) and secondary coverage (SEJ, SERP Journal, RuntimeWire, Nardit, explainx, BestHub) were preserved. Toolchain docs for ASD home/FAQ [verified-primary], Manim CLI flags [verified-primary], Remotion renderMedia [verified-primary], and Mermaid parse API [verified-primary] were fetched. Key unresolved flags carried forward: 34GB/13.8MB video figure conflict [uncertain], Karpathy likes/reposts unconfirmed [uncertain], ASD Issue 9 PDF numeric limits still [secondary], cheat-sheet image OCR pending [uncertain]. This report synthesizes that haul into testable skill specs.

## 1. Tweet digest (max 200 words) and verification status

Karpathy posted 2026-10-02 00:37 UTC [verified-primary] that we will spend more time understanding LLM outputs, then gave a 4-rung ladder each introduced as better than the last [verified-primary]. Rung 1: explain in ASD-STE100 aerospace controlled English, with softening to quote: "80% of the way to ASD-STE100" [verified-primary]. Rung 2: diagrams/images easier to process and parse [verified-primary]. Rung 3: HTML interactive pages, models good at frontend [verified-primary]. Rung 4, most bullish: bespoke 3Blue1Brown-style videos on any topic, e.g. prompt with ElevenLabs key or free local alternative [verified-primary]. Thesis: models do legwork, human work rises to oversight, cheap intelligence/code enables large discardable artifacts like web apps and videos [verified-primary].

Verification: full text confirmed via OpenCLI thread dump plus live `nitter.cf` mirror fetch 2026-10-08 showing 54,502 likes / 6,405 reposts / 7.59M views [verified-primary]. Attached cheat-sheet image `HTlaHqgbwAAS1lv.png` exists but content not OCR'd here [uncertain]. User summary matches primary; secondary ladders are paraphrases only [inference]. Karpathy likes/reposts of examples could not be confirmed because likes endpoint needs login context and returned empty [uncertain]. State plainly: endorsement of any specific video is unverified [uncertain].

## 2. Technique findings

### 2.1 ASD-STE100 constrained writing

What the standard contains [verified-primary for FAQ/home webfetch]: ASD-STE100 Simplified Technical English is a controlled natural language and international standard owned by ASD Brussels, trademark 017966390 [verified-primary]. It started 1979 after European airlines asked manufacturers for unambiguous maintenance English, AECMA Guide 1986, spec 2005, standard Issue 9 on 2025-01-15 [verified-primary]. It has two parts: writing rules (grammar/style) plus controlled dictionary of general approved words [verified-primary]. Each approved word has one meaning and one part of speech in general, e.g. fall means move down by gravity not decrease, use start not begin/commence/initiate/originate, spelling follows American English Merriam-Webster [verified-primary]. Writers can also use company/field technical nouns/verbs under rules [verified-primary].

Key enforceable rules from FAQ [verified-primary]: avoid -ing forms except as technical nouns or listed nouns/adjectives/pronouns/prepositions like opening/remaining/something/during; put condition first if reader must know it before step; procedural writing uses imperative, descriptive uses active with passive only if agent unknown; one topic per sentence and short sentences carry over to general writing even though STE quote: "is not intended for general-purpose writing" [verified-primary]. Maintenance by STEMG working group, Issue 10 scheduled Jan 2028, distribution as free PDF only via DOWNLOADS request [verified-primary].

Numeric limits often quoted (procedural max 20 words, descriptive max 25, paragraph max 6 sentences, noun cluster max 3 words, 53 rules in nine sections, ~900 approved words plus ~1200 unapproved with alternatives) appear in Nardit and explainx secondaries [secondary]. PDF not fetched here, so treat numbers as [secondary] until PDF check.

How people prompt LLMs [verified-primary for tweet + primary reply cards]: Karpathy softens because spec is stringent; richardcsuwandi prompt (1061 likes) operationalizes 80% STE as short sentences, active voice, consistent terminology, relax vocab when awkward, preserve precision and uncertainty [verified-primary for prompt text via card]. hqmank (6510 likes) distills to 4 rules: short sentences, one action per step, say who does what, one name per thing, noting models break naming consistency [verified-primary for card]. Turkish reply notes verbatim STE makes agent instructions longer, prefers principles over verbatim [secondary]. Skill repos surfaced: danyuchn/asd-ste100-skill (disclaims dictionary omission per SEJ) [secondary], 0xpili/simplified-technical-english with rules + word list + check tool [secondary], ryanjmichie-git/ste-explain [secondary], hazrid93/pi-simplified-technical-english with /ste command [secondary], AsherHou/asd-ste100-for-coding plan-first [secondary].

Published experiments/evaluations: no controlled eval of STE-prompted LLM output found in haul [inference]. Closest evidence: 1996 study of 175 technicians found comprehension improved with Simplified English, most for hardest cards and non-native readers [secondary via Nardit]. July 2026 wave of STE skills with 3000+ stars each noted by Nardit [secondary]. ASD FAQ itself warns no tool replaces the standard [secondary via SEJ].

Implications for a skill: implement 80% STE as default, full STE as strict mode. Ship a checker (ste_check) for sentence length, -ing, passive in procedures, condition-first, naming consistency, plus approved-word advisory not hard block unless dictionary bundled. Must disclaim dictionary omission if not bundling PDF-derived list. Require uncertainty preservation to avoid false simplification.

### 2.2 Diagrams instead of paragraphs

Which formats LLMs generate most reliably [verified-primary for docs + secondary for practice]: Mermaid text definitions validate via `mermaid.parse(text)` without rendering [verified-primary]. That enables a generate-then-parse repair loop [inference]. Nardit advises diagram in text format such as Mermaid/Graphviz/SVG plus listing every relationship as a sentence [secondary]. Thread replies favor Excalidraw code output that Opus-class models know well, UML sequence for features, and inline Claude diagrams [secondary]. AYi_AInotes quote-tweet mentions Mermaid/SVG path [secondary].

Common failure modes [secondary unless noted]: invalid edge/arrow syntax (e.g. `--<` or `--|label|` missing dash causes parse error) [verified-primary for error examples]. Other modes from secondaries: hallucinated nodes/edges not in source, label drift (worker/agent/executor for same entity), layout unreadable at scale, UML lifeline errors, Excalidraw JSON schema drift [secondary]. No error corpus fetched [uncertain].

When a diagram beats prose [secondary]: evidence cited is Larkin & Simon 1987 on location indexing reducing search, and Cromley & Chen 2025 meta of 181 studies effect ~0.37 [secondary via Nardit]. Practical rule from replies: structure/flows/architecture, algorithm steps, and diff explanation benefit most; Summer_ikiki reports time-to-understand dropped with HTML/diagram vs text [secondary]. Violet8434 argues constrained formats fail visibly while fluent prose hides error [secondary].

Implications for a skill: require triple output — diffable source (Mermaid first, Graphviz/SVG fallback, Excalidraw JSON optional), rendered PNG/SVG, and edge-sentence list for audit. Gate on `mermaid.parse` or equivalent validator before showing render. Cap nodes/edges and enforce one name per thing via STE naming check.

### 2.3 Interactive single-file HTML pages

Patterns [verified-primary for reply concepts + secondary for lineage]: kimseong and alnooraniii replies propose predict-then-reveal: change assumption/variable, commit to answer, then run [verified-primary for concept via thread dump]. Shihipar May post plus Claude Blog lineage for HTML-over-Markdown noted by SEJ [secondary]. Claude artifacts and ChatGPT canvas (2024) are the delivery precedent [secondary]. Bret Victor 2011 Explorable Explanations for reactive documents cited by Nardit [secondary].

What makes them trustworthy [secondary]: Nardit mitigations — list assumptions visibly, test against real system, keep file self-contained [secondary]. explainx notes HTML is harder to diff than Markdown and needs harness [secondary]. Thread best suggestion per Nardit is a page where learner changes an assumption [secondary].

Notable examples from replies [secondary]: aikamma pattern of UML plus interactive step-through HTML for algorithms [secondary]; neural_avb HTML explanation of STE itself with image [secondary]; Summer_ikiki Opus 5.5 HTML vs text comparison [secondary]. No code sample fetched for archival [uncertain].

Cost/constraints [secondary/inference]: single-file HTML with sliders/step-through is cheapest ladder rung above diagrams; no render farm needed, runs locally, but interactivity logic can hide wrong model [inference]. explainx table rates HTML strongest ROI, model-agnostic prompts, frontier coding models strongest [secondary].

Implications for a skill: template single-file HTML with assumption panel, controls (sliders/step-through), predict-then-reveal widget, and source-links footer. No external CDN dependency by default for auditability. Output must include assumption list and 3 spot-checks.

### 2.4 3Blue1Brown-style explainer videos

Toolchains [verified-primary for core CLIs]: Manim Community Edition `manim -pql main.py CreateCircle` for low-quality preview (854x480 15FPS) and `manim -pqh` for 1080p60 high which takes considerably longer [verified-primary]. Remotion `bundle()` once then `selectComposition` + `renderMedia({codec:'h264'})` with reusable inputProps parametrization [verified-primary]. Showtime 0.4.0 reads storyboard.md (Shot|Length|Visual|Narration, any column order, Chinese headers too) and renders locally [secondary]. HyperFrames HTML/canvas to MP4 deterministic render per explainx [secondary]. TTS split: ElevenLabs keyed (named in Karpathy prompt) vs free local Kokoro or Voicebox open alt [secondary for logging/alt details]. ElevenLabs logs text by default with enterprise opt-out per Nardit, keep key in credential settings not prompt [secondary].

Realistic cost and render constraints [secondary/uncertain]: Manim high quality is slow; Remotion needs Node/bundle + ffmpeg; local medium-small models questioned by dinolupo re rendiv route [secondary, needs repo fetch]. No timing trials run here [uncertain].

Examples cited [secondary/uncertain]: NikolozChichua GNN video via Opus 5.5 + ElevenLabs + Manim [verified-primary for reply existence]. GKev1n Opus 5.5 3b1b video in Chinese, doppia_x Japanese video, meseven_journey YouTube via GPT-Sol-6.1 & GLM-5.3 [secondary]. FavioVaz free route Kokoro + Manim + showtime with STE narration [secondary]. Perez Oct 1 pre-tweet film claimed as 34-minute, 34GB from 13.8MB HTML, Cloudflare 512MB cache note [secondary via highlight]. BestHub retells as 4-minute plus Karpathy endorsement [secondary, conflicts]. Verification: duration conflict (34 vs 4 min) likely typo [inference], size plausibility without bitrate/codec/log cannot be judged [uncertain], endorsement unverified because likes empty and Perez predates Karpathy [uncertain]. Do not cite figures or endorsement [uncertain].

Implications for a skill: storyboard-first workflow. Agent writes storyboard.md + narration script + captions/project files, then routes to renderer (Showtime local default, Manim for math, Remotion for React). Never paste API key in prompt. Require script read-before-watch and 3-claim spot-check.

## 3. Risks and mitigations

Comprehension-vs-verification tradeoff is the thread's own warning [secondary]. Polished formats can make errors harder to spot, and summarizing can hide mistakes [secondary]. Specific exhibits: cheat-sheet image in Karpathy post inverts one dictionary rule, approves a rejected verb, presents recommendation as entry while looking authoritative [secondary via Nardit]. Perez-size confusion shows how a striking number propagates with duration/endorsement drift [uncertain]. Nardit paraphrase: narrated wrong claim over animation is harder to catch than wrong sentence [secondary].

Mitigations proposed in thread or elsewhere:

- Source-linking and assumption panel in HTML, keep script/captions/source for video and read script before watch [secondary].
- Show-me-where controls: diagram edge-sentence list, HTML assumption test against real system, video storyboard with timing [secondary].
- Predict-then-reveal: learner changes variable, commits to answer, then runs (kimseong/alnooraniii) [verified-primary for proposal].
- Independent checks: AnirudhVas35945 pairs video with new problem to solve without it; liukai1919 notes explaining own diff catches bugs but failure is when explanation sounds right and checking stops; Violet8434 prefers formats that fail visibly [verified-primary for reply existence, secondary for efficacy].
- TheoremExplainAgent ACL 2025 evidence: 240 theorems, videos exposed flaws hidden in text, supporting generation as audit not just polish [secondary].
- Operational hygiene: keep ElevenLabs key out of prompts, note logging default [secondary]; if publishing, needs publication review, keep artifacts discardable [secondary].

Each mitigation needs efficacy testing; none has controlled human-comprehension eval in haul beyond edX median engagement ~6 min over 6.9M sessions/862 videos and Cromley/Chen meta [secondary]. Flag as [uncertain] for causal claims.

## 4. Skill specs

### Summary table

| # | kebab-case name | Trigger (under 50 words) | Value | Effort | Depends |
|---|-----------------|--------------------------|-------|--------|---------|
| 1 | ste-explain | Rewrite/explain any technical text or diff in 80% STE for fast human check. Use when readability or ambiguity blocks review. | High | Low | — |
| 2 | diagram-first | Turn structure, flow, or architecture into validated Mermaid plus edge list. Use when prose hides relationships. | High | Low | ste-explain naming |
| 3 | explorable-html | Build single-file interactive explainer with predict-then-reveal. Use when parameters or assumptions drive understanding. | Highest | Medium | 1+2 |
| 4 | storyboard-video | Draft storyboard and narration then render local 3b1b-style video. Use only when motion adds value. | Medium | High | 1-3 |
| 5 | verify-ladder | Cross-check any ladder artifact for STE, edges, assumptions, script. Use after 1-4 before sharing. | High | Medium | 1-4 |

Router question answered in §5.

### 4.1 ste-explain — 80% STE rewriter + checker

Description (trigger-style, 43 words): Rewrite explanations, diffs, and plans in readable 80% STE. Use when LLM prose is bloated, ambiguous, or hard to verify.

Inputs: source text or diff or topic + audience + strictness flag (80% default, strict STE optional) + term glossary (optional) + max length.

Procedure the agent follows:
1. Extract terms, lock one name per thing, list synonyms to replace.
2. Split into one-topic sentences, ≤20 words procedural / ≤25 descriptive [secondary until PDF].
3. Convert procedural to imperative, descriptive to active; move condition first.
4. Remove -ing except approved technical nouns; replace unapproved vocab with start/fall-style approved picks where safe, else keep technical term and flag.
5. Preserve numbers, modals of uncertainty, safety warnings verbatim; never drop caveats.
6. Run ste_check and fix violations or explicitly waive with reason.
7. Output STE text + waivers + term map.

Output artifact and format: Markdown with `## STE text`, `## Term map`, `## Waivers`, plus machine-readable `ste-report.json` (sentence count, avg length, violations).

Tools and dependencies: prompt template + approved-word advisory list (embed small subset, link full PDF via DOWNLOADS); `ste_check.py` using regex for length/-ing/passive/condition-first/naming; no network needed.

Built-in verification step: checker must pass or waivers justified; second pass asks: does any sentence have >1 instruction? Is actor explicit? Are uncertainties preserved? Spot-check 3 surprising claims against source.

Test prompts with pass/fail:
1. Prompt: Explain Raft leader election in 80% STE for a junior. Pass if all sentences ≤25 words, active, one name per role (leader/follower/candidate consistent), uncertainty kept; Fail if any comma-chained >25 words or role synonym drift.
2. Prompt: Rewrite this 5-file diff summary in STE imperative. Pass if each step starts with verb, condition-first where needed, term map lists renamed symbols; Fail if passive procedural or missing actor.
3. Prompt: Convert this paragraph with begin/commence/utilize/approximately to STE. Pass if start/use/about-as-concerned-with applied or flagged as technical term, -ing removed; Fail if unapproved synonyms remain unflagged.

Known failure modes: over-simplification drops precision; false STE-compliance while violating vocab (Nardit Issue 9 warning) [secondary]; longer output when strict; cheat-sheet-style dictionary errors if copying secondary image.

### 4.2 diagram-first — text-source diagram + edge audit

Description (38 words): Generate validated diagrams from text or code. Use when flows, sequences, or architecture are hard to follow in prose.

Inputs: source description/code/diff + diagram type (flowchart/sequence/architecture) + renderer preference (Mermaid default) + max nodes/edges.

Procedure:
1. Identify entities, lock names via ste-explain term map.
2. List every relationship as one sentence (Actor verb Target).
3. Emit Mermaid source (flowchart TD or sequenceDiagram) with short labels.
4. Validate with `mermaid.parse`; fix syntax (arrows, semicolons, reserved words) until parse passes [verified-primary for parse API].
5. Render SVG/PNG locally; check layout legibility, break up if >15 nodes.
6. Output source + render + edge sentences + STE caption.

Output artifact: `diagram.mmd`, `diagram.svg/png`, `edges.md` (numbered sentences), `README.md` snippet to embed.

Tools and dependencies: Mermaid CLI + `mermaid.parse` validator [verified-primary]; Graphviz fallback; Excalidraw JSON exporter optional; no API keys.

Built-in verification: parse must succeed; every edge in render must have matching sentence and vice versa; names must match term map; reviewer can click edge → sentence.

Test prompts:
1. Explain OAuth code flow as sequenceDiagram. Pass if parse succeeds, participants consistent, token exchange edges numbered; Fail if arrow syntax error or participant rename mid-diagram.
2. Map this microservice PR architecture. Pass if ≤15 nodes or split, all arrows labeled, edge list complete; Fail if unlabeled arrow or missing dependency.
3. Turn this stack trace into flowchart. Pass if condition-first diamonds, one action per node, error path explicit; Fail if two actions in one node or swallowed branch.

Known failure modes: Mermaid version drift (v10 vs v11) [secondary]; LLM invents edges; label overflow; UML lifeline misuse; Excalidraw schema drift [secondary].

### 4.3 explorable-html — single-file interactive with predict-reveal

Description (44 words): Build discardable single-file HTML explainers with sliders and guess-first checks. Use when understanding depends on parameters or assumptions.

Inputs: topic + target misconception + 2-5 adjustable variables with ranges/defaults + source links + audience level.

Procedure:
1. List assumptions visibly and unknowns.
2. Scaffold single `index.html` (inline CSS/JS, no CDN by default) with sections: What it is (STE), Try it (sliders/step-through), Guess first (input + reveal), Check (3 questions).
3. Implement predict-then-reveal: user sets variable, commits prediction, runs, sees result vs prediction [verified-primary for pattern].
4. Add source-links footer and assumption panel toggle.
5. Self-test in headless browser or `python -m http.server` + screenshot; fix JS errors.
6. Output file + test log.

Output artifact: `explainer.html` (<500KB aim, self-contained), `assumptions.md`, `checks.md`.

Tools and dependencies: HTML/CSS/JS template, no build step; optional canvas for animation; Playwright or manual open for verification.

Built-in verification: file opens offline with no console errors; all controls change output deterministically; 3 spot-checks of surprising behaviors reproduced; assumptions listed.

Test prompts:
1. Explain exponential backoff with retry slider. Pass if slider changes timing graph, guess-first asks to predict 3rd retry delay, answer reveals with math; Fail if control does nothing or math wrong.
2. Visualize Raft quorum with node failure toggles. Pass if toggling nodes flips availability correctly, assumptions list quorum rule; Fail if quorum logic inverted.
3. Compare two cache eviction policies step-through. Pass if step buttons advance identically for both, source links present; Fail if external CDN required or steps desync.

Known failure modes: JS hides wrong model behind polish; harder to diff than Markdown [secondary]; over-animation distracts; accessibility/keyboard neglect.

### 4.4 storyboard-video — storyboard.md to local 3b1b-style video

Description (46 words): Create storyboard, narration, and local render for bespoke explainer videos. Use when motion and narration beat static pages.

Inputs: topic + duration target (60-180s default) + voice route (local Kokoro default, ElevenLabs only if key in env) + style (Manim/Remotion/Showtime) + script sources.

Procedure:
1. Write `storyboard.md` table Shot|Length|Visual|Narration (any order) [secondary for Showtime spec].
2. Write narration in 80% STE, cap ~130 wpm, add captions file.
3. Generate visuals as code (Manim Scene or Remotion composition or Showtime storyboard), never diffusion-only.
4. Render preview low (`manim -pql` or Remotion preview) [verified-primary], review, then final `manim -pqh` 1080p60 or `renderMedia h264` [verified-primary].
5. TTS locally by default; if ElevenLabs, read key from env/credential store, never paste in prompt, note logging default [secondary].
6. Output video + script + project + render log; instruct read-script-before-watch.

Output artifact: `storyboard.md`, `narration.txt`, `captions.srt`, `main.py` or Remotion `src/`, `out.mp4` + `render.log`.

Tools and dependencies: Python + ManimCE, Node + Remotion + ffmpeg, or Showtime 0.4.0; Kokoro local TTS; ffmpeg for concat; disk for renders.

Built-in verification: script fact-check (3 claims), TTS text matches captions, preview watched at 2x for timing/overlap, final render log records resolution/fps/codec/duration/size; do not claim 34GB-scale figures without log [uncertain].

Test prompts:
1. 90s 3b1b-style video on binary search. Pass if storyboard has ≤12 shots, narration STE, `manim -pql` preview succeeds, captions align; Fail if missing storyboard or key in prompt.
2. Remotion video comparing two sorts with inputProps. Pass if `bundle`+`selectComposition`+`renderMedia h264` succeeds, props change output; Fail if hardcoded data or render error.
3. Local-only video with Kokoro, no API keys. Pass if no network upload, render log present, script read checklist included; Fail if external TTS call or no log.

Known failure modes: render time blowup on `-pqh`/4k [verified-primary for slower]; TTS mispronunciation; ManimGL vs ManimCE API mismatch [secondary]; large uncompressed intermediates mistaken for delivery size (Perez confusion) [uncertain]; narrated error harder to catch [secondary].

### 4.5 verify-ladder — cross-format checker

Description (42 words): Audit any STE, diagram, HTML, or video artifact for hidden errors. Use after generation and before sharing.

Inputs: artifact(s) + original sources + risk level (internal share vs publish).

Procedure:
1. STE parse: length, -ing, passive, condition-first, naming vs term map.
2. Edge audit: every diagram edge ↔ sentence, every HTML control ↔ assumption.
3. Assumption test: flip one variable, predict, run; reproduce bug with real code where applicable.
4. Script read: read narration/script without watching, list 3 surprising claims, verify each to source.
5. Verdict: APPROVE / APPROVE-WITH-NITS / BLOCK with fix list.

Output artifact: `verify.md` with checklist, failures, required fixes, plus updated `ste-report.json` if applicable.

Tools and dependencies: reuses ste_check, mermaid.parse, HTML console log, video script diff; no extra deps.

Built-in verification (self): verifier must find planted error in test; must not pass fluent-but-wrong prose.

Test prompts:
1. Audit this STE + diagram for auth flow. Pass if catches worker/agent/executor drift and unlabeled edge; Fail if approves despite drift.
2. Audit this HTML explainer. Pass if finds hidden assumption (e.g. fixed timeout) and missing source link; Fail if passes on polish alone.
3. Audit this video script. Pass if flags narrated claim contradicting code and missing captions; Fail if video passes without script read.

Known failure modes: checker fatigue (liukai1919 stop-checking) [secondary]; false confidence from green checks; needs human for domain truth.

## 5. Recommended build order

Value vs effort (high value, low effort first):

1. ste-explain first. Cheapest, underpins all others via naming/clarity, directly implements Karpathy rung 1 and 80% compromise. Effort: prompt + regex checker. Risk: dictionary errors — mitigate by advisory mode + PDF link.
2. diagram-first second. High comprehension ROI per meta effect ~0.37 [secondary], validator exists (`mermaid.parse`) [verified-primary]. Pairs with STE term map to fix naming drift.
3. verify-ladder third (thin version: STE + edge checks only). Needed before scaling HTML/video to avoid polishing errors. Add HTML/script checks when 3-4 land.
4. explorable-html fourth. Highest learning ROI per predict-then-reveal thread consensus but medium effort (template + JS testing). Build after checker so assumptions are audited.
5. storyboard-video last. Most bullish but slowest/heaviest (Manim/Remotion/ffmpeg/TTS). Start with storyboard + preview only; gate full render behind verify-ladder.

Router: ship thin `understanding-ladder` router that picks rung by task (explain→STE, structure→diagram, parameters→HTML, motion→video, any share→verify), cf ChangWenC understanding-ladder skill [secondary]. Keep skills separate, router only routes; do not merge implementations. Reason: separate testing, separate deps, discardable artifacts stay discardable.

## 6. Source list tagged primary or secondary

Primary (direct fetch or thread dump):
- https://x.com/karpathy/status/2105819303471976479 | Fetched 2026-10-08 — tweet text, ladder, 80% STE, ElevenLabs prompt, discardable-artifacts thesis [verified-primary].
- https://nitter.cf/karpathy/status/2105819303471976479 | Fetched 2026-10-08 — mirror proving X-block bypass, counts 54502/6405/7.59M [verified-primary].
- https://www.asd-ste100.org/ | Fetched 2026-10-08 — owner ASD Brussels, history 1979/AECMA/AIA/AEA, Guide 1986/spec 2005/standard 2025 Issue 9, trademark [verified-primary].
- https://www.asd-ste100.org/STE_faq.html | Fetched 2026-10-08 — two parts, one meaning/POS, start/fall examples, Merriam-Webster, technical nouns/verbs, -ing rule, condition-first, imperative/active, not for general writing [verified-primary].
- Thread reply IDs via OpenCLI (NikolozChichua GNN video, kimseong/alnooraniii predict-reveal, liukai1919/Violet8434/AnirudhVas35945 verification warnings, Hems_910/aikamma diagram patterns) [verified-primary for existence/text].
- Quote-tweet cards (hqmank 4 rules + danyuchn skill, richardcsuwandi prompt + 0xpili skill) [verified-primary for prompt/card text].
- Context7 docs: /manimcommunity/manim CLI `-pql` low vs `-pqh` 1080p60 longer [verified-primary]; /remotion-dev/remotion `bundle`+`selectComposition`+`renderMedia h264` [verified-primary]; /mermaid-js/mermaid `mermaid.parse` + arrow error examples [verified-primary].

Secondary (needs primary follow-up before citing as fact):
- https://max.nardit.com/articles/karpathy-understanding-llm-outputs — cheat-sheet error analysis, Larkin&Simon 1987, Cromley&Chen 2025 meta ~0.37, Victor 2011, TheoremExplainAgent ACL 2025 240 theorems, edX 6.9M/862/~6min, ElevenLabs logging, mitigations [secondary].
- https://www.searchenginejournal.com/karpathy-llm-aircraft-manual-writing/591813/ — Shihipar/Claude Blog lineage, FAQ scope limiter, dictionary omission [secondary].
- https://serpjournal.com/articles/karpathy-ask-llms-to-write-like-aircraft-maintenance-manuals-05d6785d5 — ~900 words, Karpathy-Anthropic note [secondary].
- https://runtimewire.com/article/karpathy-ai-explanations-custom-videos — Issue 9 AI-consistency warning [secondary].
- https://explainx.ai/blog/karpathy-understand-llm-outputs-ste100-diagrams-html-video-2026 — cost/catch table, code-not-diffusion, HyperFrames/Voicebox, spot-check 3 [secondary].
- https://www.besthub.dev/articles/karpathy-replace-raw-ai-text-with-diagrams-interactive-pages-videos-ee5341dd3359 — 4-min/34GB/endorsement claim, conflicts with Perez 34-min pre-tweet [secondary, do not cite].
- https://nitter.cf/IntuitMachine/status/2105809378825982387 — Perez 34-min/34GB/13.8MB HTML source of figure [secondary highlight, unverified size/endorsement].
- ASD spec PDF https://www.asd-ste100.org/assets/files/ASD-STE100_ISSUE9.pdf — numeric limits, 53 rules, dictionary counts [secondary until fetched].
- Skill repos (danyuchn, 0xpili, ryanjmichie-git/ste-explain, hazrid93/pi, AsherHou, ChangWenC/understanding-ladder, FavioVazquez/showtime), rendiv, MulmoCast mentions [secondary, READMEs not cloned].

Gaps flagged [uncertain]: cheat-sheet OCR, Karpathy likes/reposts, ASD PDF numbers, Mermaid/Graphviz/Excalidraw/draw.io reliability corpus, HTML code samples, TTS logging docs, TheoremExplainAgent/edX/Larkin PDFs, Perez render logs.

Word count note: target 2500-3500; this draft prioritizes spec completeness over brevity.
