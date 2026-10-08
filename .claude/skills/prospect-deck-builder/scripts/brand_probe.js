#!/usr/bin/env node
/*
 * Read a prospect's brand from the rendered page, the way a browser paints it.
 * Optional companion to brand_extract.py, which reads stylesheets. Computed styles
 * beat stylesheet guessing, so brand_extract.py --probe gives these readings priority.
 *
 *   node brand_probe.js https://www.example.com brand/probe.json
 *   node brand_probe.js file:///path/to/saved/index.html brand/probe.json
 *
 * Needs Node 18+ and Playwright (npm i playwright). If Playwright's own browser is
 * not installed, set CHROME=/path/to/chrome and it is used instead.
 *
 * Writes probe.json with the computed colours and fonts of the body, headings, links,
 * the primary button, the header and the footer, the font families the page actually
 * loaded, and a PNG of the header mark beside probe.json (logo-rendered.png).
 * The page is loaded once, scripts run as they would for any visitor, nothing is
 * clicked and nothing is submitted.
 */
const path = require('path');
const fs = require('fs');

async function main() {
  const [url, out] = process.argv.slice(2);
  if (!url || !out) {
    console.error('usage: node brand_probe.js <url> <probe.json>');
    process.exit(2);
  }
  let chromium;
  try { ({ chromium } = require('playwright')); } catch (e) {
    console.error('Playwright not found. npm i playwright, or use brand_extract.py on its own.');
    process.exit(2);
  }
  const opts = process.env.CHROME ? { executablePath: process.env.CHROME } : {};
  const browser = await chromium.launch(opts);
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
  await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 }).catch(() => page.waitForTimeout(3000));
  await page.waitForTimeout(800);
  const data = await page.evaluate(() => {
    const cs = el => (el ? getComputedStyle(el) : null);
    const solid = c => (c && !/rgba\(.*,\s*0(\.0+)?\)$/.test(c) && c !== 'transparent' ? c : null);
    const bgOf = el => {
      for (let e = el; e; e = e.parentElement) { const b = solid(cs(e).backgroundColor); if (b) return b; }
      return 'rgb(255, 255, 255)';
    };
    const q = s => document.querySelector(s);
    const body = document.body;
    const h1 = q('h1') || q('h2');
    const link = q('main a[href]:not([class*="btn"]):not([class*="button"])') || q('a[href]');
    const btns = Array.from(document.querySelectorAll(
      'a[class*="btn"], button[class*="primary"], a[class*="button"], [class*="cta"], button, .btn-primary'));
    const btn = btns.find(b => {
      const s = cs(b); const bg = solid(s.backgroundColor);
      if (!bg) return false;
      const m = bg.match(/\d+/g).map(Number);
      const max = Math.max(...m.slice(0, 3)), min = Math.min(...m.slice(0, 3));
      return max - min > 40 && b.offsetWidth > 40;
    });
    const header = q('header') || q('[class*="header"]') || q('nav');
    const footer = q('footer');
    let logo = null;
    if (header) {
      logo = header.querySelector('[class*="logo"], [id*="logo"], a[href="/"] svg, a[href="/"] img, svg, img');
    }
    const box = logo ? logo.getBoundingClientRect() : null;
    const fonts = new Set();
    if (document.fonts) document.fonts.forEach(f => { if (f.status === 'loaded') fonts.add(f.family.replace(/["']/g, '')); });
    return {
      title: document.title,
      computed: {
        body_bg: bgOf(body), body_color: cs(body).color, body_font: cs(body).fontFamily,
        h1_color: h1 ? cs(h1).color : null, h1_font: h1 ? cs(h1).fontFamily : null, h1_weight: h1 ? cs(h1).fontWeight : null,
        link_color: link ? cs(link).color : null,
        button_bg: btn ? cs(btn).backgroundColor : null, button_color: btn ? cs(btn).color : null,
        button_radius: btn ? cs(btn).borderTopLeftRadius : null,
        header_bg: header ? bgOf(header) : null, footer_bg: footer ? bgOf(footer) : null,
        footer_color: footer ? cs(footer).color : null,
      },
      loaded_fonts: Array.from(fonts),
      // A header mark is small. A box wider than 640px or taller than 240px is a layout
      // accident or a hero image, so it is not captured.
      logo_box: box && box.width > 8 && box.height > 8 && box.width <= 640 && box.height <= 240
        ? { x: box.x, y: box.y, width: box.width, height: box.height } : null,
    };
  });
  const toHex = c => {
    if (!c) return c;
    const m = c.match(/\d+(\.\d+)?/g);
    if (!m || m.length < 3) return c;
    return '#' + m.slice(0, 3).map(n => Math.round(+n).toString(16).padStart(2, '0')).join('').toUpperCase();
  };
  for (const k of Object.keys(data.computed)) {
    if (/_bg$|_color$/.test(k)) data.computed[k] = toHex(data.computed[k]);
  }
  data.url = url;
  data.captured = new Date().toISOString().slice(0, 10);
  if (data.logo_box) {
    const png = path.join(path.dirname(out), 'logo-rendered.png');
    const b = data.logo_box, pad = 6;
    await page.screenshot({ path: png, clip: { x: Math.max(0, b.x - pad), y: Math.max(0, b.y - pad), width: b.width + pad * 2, height: b.height + pad * 2 } });
    data.logo_png = png;
  }
  fs.mkdirSync(path.dirname(path.resolve(out)), { recursive: true });
  fs.writeFileSync(out, JSON.stringify(data, null, 2));
  console.log(`Wrote ${out}. Accent candidate ${data.computed.button_bg || data.computed.link_color}, body font ${data.computed.body_font}.`);
  await browser.close();
}

main().catch(e => { console.error(e.message || e); process.exit(1); });
