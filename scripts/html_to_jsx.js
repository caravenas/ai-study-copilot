const fs = require('fs');
const path = require('path');

const extractAndConvert = (inputFile, outputType) => {
  const html = fs.readFileSync(inputFile, 'utf8');
  const styleMatch = html.match(/<style[^>]*>([\s\S]*?)<\/style>/);
  const styles = styleMatch ? styleMatch[1] : '';

  let bodyHtml = html.match(/<body[^>]*>([\s\S]*?)<\/body>/i);
  if (!bodyHtml) bodyHtml = html; // fallback
  else bodyHtml = bodyHtml[1];

  // Remove <script> tags if any
  bodyHtml = bodyHtml.replace(/<script\b[^<]*(?:(?!<\/script>)<[^<]*)*<\/script>/gi, '');

  // JSX conversions
  bodyHtml = bodyHtml.replace(/class="/g, 'className="');
  bodyHtml = bodyHtml.replace(/for="/g, 'htmlFor="');
  
  // Self closing tags
  ['img', 'input', 'hr', 'br', 'path'].forEach(tag => {
    const regex = new RegExp(`<${tag}([^>]*?)>`, 'gi');
    bodyHtml = bodyHtml.replace(regex, (m, c) => {
      if (m.endsWith('/>')) return m;
      return `<${tag}${c} />`;
    });
  });

  // Convert inline styles to React style objects
  bodyHtml = bodyHtml.replace(/style="([^"]*)"/g, (match, styleString) => {
    const parts = styleString.split(';').filter(p => p.trim() !== '');
    const objVars = parts.map(p => {
      const idx = p.indexOf(':');
      if (idx === -1) return '';
      const k = p.substring(0, idx);
      const v = p.substring(idx + 1);
      // camelCase key, but keep custom CSS properties like --accent intact (React supports custom props in style as strings)
      let ccKey = k.trim();
      if (!ccKey.startsWith('--')) {
        ccKey = ccKey.replace(/-([a-z])/g, g => g[1].toUpperCase());
      }
      return `'${ccKey}': '${v.trim().replace(/'/g, "\\'")}'`;
    }).filter(Boolean);
    return `style={{ ${objVars.join(', ')} }}`;
  });

  // specific fixes for SVG
  bodyHtml = bodyHtml.replace(/fill-rule="/g, 'fillRule="');
  bodyHtml = bodyHtml.replace(/clip-rule="/g, 'clipRule="');
  bodyHtml = bodyHtml.replace(/stroke-width="/g, 'strokeWidth="');
  bodyHtml = bodyHtml.replace(/stroke-linecap="/g, 'strokeLinecap="');
  bodyHtml = bodyHtml.replace(/stroke-linejoin="/g, 'strokeLinejoin="');

  // Wrap in a simple React component
  const componentName = outputType.charAt(0).toUpperCase() + outputType.slice(1) + 'View';
  const outPath = path.join(__dirname, 'apps/web/app', outputType !== 'chat' ? outputType : '', 'page.tsx');
  
  // ensure dir exists
  fs.mkdirSync(path.dirname(outPath), { recursive: true });

  const tsxCode = `"use client";\n\nexport default function ${componentName}() {\n  return (\n    <>\n      ${bodyHtml}\n    </>\n  );\n}\n`;
  fs.writeFileSync(outPath, tsxCode);
  
  return styles;
};

const views = [
  { file: 'apps/web/stitch-exports/chat.html', type: 'chat' },
  { file: 'apps/web/stitch-exports/screen_173.html', type: 'explorer' },
  { file: 'apps/web/stitch-exports/screen_177.html', type: 'study' },
  { file: 'apps/web/stitch-exports/screen_181.html', type: 'admin' },
];

let allStyles = '';
views.forEach(v => {
  console.log(`Converting ${v.file} -> ${v.type}`);
  const s = extractAndConvert(path.join(__dirname, v.file), v.type);
  if (s) {
    allStyles += `\n/* --- ${v.type.toUpperCase()} STYLES --- */\n` + s;
  }
});

// Write global CSS
const globalsPath = path.join(__dirname, 'apps/web/app/globals.css');
if (fs.existsSync(globalsPath)) {
  fs.appendFileSync(globalsPath, allStyles);
} else {
  fs.writeFileSync(globalsPath, allStyles);
}
console.log('Conversion complete.');
