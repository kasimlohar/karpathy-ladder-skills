#!/usr/bin/env node
/* audit_html.js — headless HTML explainer audit (Node + puppeteer-core).
 * Checks: console errors, external (non-file/data) requests, controls present,
 * and that wiggling the first range/checkbox control changes page output.
 * Static checks always run; browser part reports browser:"ran"|"unavailable".
 * A static-only pass is NEVER a browser pass.
 * Env: CHROME_PATH (chrome binary), PUPPETEER_MOD (dir containing puppeteer-core).
 * Usage: node audit_html.js explainer.html [--json]
 */
const fs = require('fs');
const os = require('os');
const path = require('path');

const home = os.homedir();
// No personal paths: override with CHROME_PATH / PUPPETEER_MOD env vars.
const CHROME_CANDIDATES = [
  process.env.CHROME_PATH,
  path.join(home, '.cache', 'puppeteer', 'chrome'),
  process.env.LOCALAPPDATA ? path.join(process.env.LOCALAPPDATA, 'ms-playwright') : null,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/usr/bin/google-chrome',
  '/usr/bin/chromium',
].filter(Boolean);

function chromeExists(p) {
  try {
    if (fs.existsSync(p) && fs.statSync(p).isFile()) return p;
    // puppeteer cache layout: <dir>/chrome/<platform>/chrome-win64/chrome.exe (etc.)
    const LEAVES = ['chrome.exe', 'chrome', 'headless_shell', 'chrome-headless-shell'];
    const walk = (dir, depth) => {
      let out = [];
      try {
        for (const d of fs.readdirSync(dir, { withFileTypes: true })) {
          const full = path.join(dir, d.name);
          if (d.isFile() && LEAVES.includes(d.name)) out.push(full);
          else if (d.isDirectory() && depth > 0) out = out.concat(walk(full, depth - 1));
        }
      } catch { /* skip */ }
      return out;
    };
    const found = walk(p, 3).filter(f => /chrome|chromium|headless/i.test(f));
    if (found.length) return found[0];
  } catch { /* not usable */ }
  return null;
}

const PUPPETEER_CANDIDATES = [
  process.env.PUPPETEER_MOD,
  path.join(__dirname, 'node_modules'),
].filter(Boolean);

function loadPuppeteer() {
  for (const dir of PUPPETEER_CANDIDATES) {
    try { return require(path.join(dir, 'puppeteer-core')); } catch { /* next */ }
  }
  try { return require('puppeteer-core'); } catch { return null; }
}

function staticChecks(html) {
  const errs = [];
  if (/<script\s+src=/.test(html) && !/integrity=/.test(html)) errs.push('static: CDN script without integrity hash');
  if (!/[Gg]uess/.test(html)) errs.push('static: missing guess-first control');
  if (!/[Aa]ssumption/.test(html)) errs.push('static: missing assumptions panel');
  if (/https?:\/\//.test(html) && !/[Ss]ources/.test(html)) errs.push('static: external link without Sources footer');
  return errs;
}

(async () => {
  const args = process.argv.slice(2);
  if (args.includes('--help') || args.includes('-h') || !process.argv[2]) {
    console.log('usage: node audit_html.js explainer.html [--json]');
    console.log('Checks: console errors, external requests, controls present,');
    console.log('first range/checkbox control changes output. Static checks always');
    console.log('run; browser part needs puppeteer-core + Chrome (CHROME_PATH /');
    console.log('PUPPETEER_MOD envs). Reports browser:ran|unavailable.');
    process.exit(0);
  }
  const file = process.argv[2];
  const html = fs.readFileSync(file, 'utf8');
  const staticErrs = staticChecks(html);
  const puppeteer = loadPuppeteer();
  let chrome = null;
  for (const p of CHROME_CANDIDATES) {
    if (/\.exe$|\/chrome$|\/chromium$|Chrome$/.test(p) && fs.existsSync(p)) { chrome = p; break; }
    const resolved = chromeExists(p);
    if (resolved) { chrome = resolved; break; }
  }
  let browserPart = { browser: 'unavailable', reason: !puppeteer ? 'puppeteer-core not found' : 'chrome binary not found' };
  if (puppeteer && chrome) {
    try {
      const browser = await puppeteer.launch({ executablePath: chrome, args: ['--no-sandbox'] });
      const page = await browser.newPage();
      const errors = [], requests = [];
      page.on('console', m => { if (m.type() === 'error') errors.push('console.error: ' + m.text().slice(0, 200)); });
      page.on('pageerror', e => errors.push('pageerror: ' + String(e).slice(0, 200)));
      page.on('request', r => { const u = r.url(); if (!u.startsWith('file://') && !u.startsWith('data:')) requests.push(u.slice(0, 120)); });
      await page.goto('file:///' + path.resolve(file).replace(/\\/g, '/'), { waitUntil: 'load', timeout: 30000 });
      const controls = await page.evaluate(() => [...document.querySelectorAll('input,select,button')].map(e => e.id || e.type));
      const changed = await page.evaluate(() => {
        const r = document.querySelector('input[type=range],input[type=checkbox]');
        if (!r) return 'no-testable-control';
        const before = document.body.innerText;
        if (r.type === 'checkbox') { r.checked = !r.checked; }
        else { r.value = String(r.min || 0); }
        r.dispatchEvent(new Event('input', { bubbles: true }));
        r.dispatchEvent(new Event('change', { bubbles: true }));
        r.dispatchEvent(new Event('click', { bubbles: true }));
        return before === document.body.innerText ? 'unchanged' : 'changed';
      });
      await browser.close();
      browserPart = { browser: 'ran', consoleErrors: errors, externalRequests: requests, controls, controlTest: changed };
    } catch (e) {
      browserPart = { browser: 'unavailable', reason: 'launch failed: ' + String(e).slice(0, 200) };
    }
  }
  const rep = { file, staticErrors: staticErrs, ...browserPart };
  const asJson = process.argv.includes('--json');
  if (asJson) console.log(JSON.stringify(rep, null, 2));
  else {
    console.log(`browser=${rep.browser} staticErrors=${staticErrs.length} consoleErrors=${(rep.consoleErrors || []).length} external=${(rep.externalRequests || []).length} controlTest=${rep.controlTest || 'n/a'}`);
    staticErrs.forEach(e => console.log('- ' + e));
    (rep.consoleErrors || []).forEach(e => console.log('- ' + e));
    (rep.externalRequests || []).forEach(u => console.log('- external: ' + u));
    if (rep.reason) console.log('reason: ' + rep.reason);
  }
  const fail = staticErrs.length > 0 || (rep.consoleErrors || []).length > 0 || rep.controlTest === 'unchanged';
  process.exit(fail ? 1 : 0);
})().catch(e => { console.error('AUDIT_FAIL ' + String(e).slice(0, 300)); process.exit(2); });
