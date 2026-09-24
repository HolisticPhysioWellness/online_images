// Auto-crop every exercise panel to its drawing, then export SVG + PNG.
const { chromium } = require('playwright');
const fs = require('fs'), path = require('path');
(async () => {
  const dir = path.resolve(process.argv[2] || 'svg');
  const outSvg = path.resolve(process.argv[3] || 'svg_cropped');
  const outPng = path.resolve(process.argv[4] || 'png');
  fs.mkdirSync(outSvg, { recursive: true }); fs.mkdirSync(outPng, { recursive: true });
  const files = fs.readdirSync(dir).filter(f => f.endsWith('.svg')).sort();
  const fonts = fs.readFileSync('fonts.css', 'utf8').split('url(fonts/').join('url(file://' + path.resolve('fonts') + '/');
  const b = await chromium.launch();
  const p = await b.newPage({ deviceScaleFactor: 2 });
  for (const f of files) {
    const src = fs.readFileSync(path.join(dir, f), 'utf8');
    await p.setContent(`<html><head><meta charset="utf-8"><style>${fonts} body{margin:0;background:#fff}</style></head><body>${src}</body></html>`);
    await p.evaluate(() => document.fonts.ready);
    const svg = await p.evaluate(() => {
      const s = document.querySelector('svg');
      const c = s.querySelector('g.content'), t = s.querySelector('g.tag');
      const bb = c.getBBox();
      const pad = 10, top = t ? 38 : pad;
      const x = bb.x - pad, y = bb.y - top, w = bb.width + 2 * pad, h = bb.height + pad + top;
      s.setAttribute('viewBox', `${x.toFixed(1)} ${y.toFixed(1)} ${w.toFixed(1)} ${h.toFixed(1)}`);
      s.setAttribute('width', Math.round(w)); s.setAttribute('height', Math.round(h));
      if (t) t.setAttribute('transform', `translate(${(x + 6).toFixed(1)},${(y + 6).toFixed(1)})`);
      return s.outerHTML;
    });
    fs.writeFileSync(path.join(outSvg, f), svg);
    const el = await p.$('svg');
    await el.screenshot({ path: path.join(outPng, f.replace('.svg', '.png')) });
  }
  await b.close();
  console.log('cropped', files.length);
})();
