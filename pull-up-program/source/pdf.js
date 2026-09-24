const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const [,, input, pdfOut, pngPrefix] = process.argv;
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 816, height: 1056 }, deviceScaleFactor: 1.5 });
  await p.goto('file://' + path.resolve(input));
  await p.evaluate(() => document.fonts.ready);
  await p.pdf({ path: pdfOut, format: 'Letter', printBackground: true, margin: {top:0,right:0,bottom:0,left:0}, preferCSSPageSize: true });
  if (pngPrefix) {
    await p.emulateMedia({ media: 'print' });
    const pages = await p.$$('.page');
    for (let i = 0; i < pages.length; i++) await pages[i].screenshot({ path: `${pngPrefix}${i+1}.png` });
  }
  // overflow check
  const over = await p.evaluate(() => [...document.querySelectorAll('.page')].map((pg, i) => {
    const foot = pg.querySelector('.pf').getBoundingClientRect().top;
    let max = 0; pg.querySelectorAll(':scope > *:not(.pf)').forEach(el => { max = Math.max(max, el.getBoundingClientRect().bottom); });
    return [i + 1, Math.round(foot - max)];
  }));
  console.log('space above footer (px):', JSON.stringify(over));
  await b.close();
})();
