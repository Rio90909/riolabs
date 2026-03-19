const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

const search = `                let previewHtml = \`<div class="color-preview" style="background: \${item.acc || item.color || item.value};"></div>\`;
                if(tab === 'badges') {`;

const replace = `                let previewHtml = \`<div class="color-preview" style="background: \${item.acc || item.color || item.value};"></div>\`;
                if(tab === 'bubbles') {
                    // Show a split gradient of bubble background and text color
                    const bg = item.color || 'var(--island)';
                    const text = item.text || '#fff';
                    previewHtml = \`<div class="color-preview" style="background: linear-gradient(135deg, \${bg} 50%, \${text} 50%); border: 1px solid var(--glass-border);"></div>\`;
                } else if(tab === 'themes') {
                    // Show a split gradient of theme background and accent color
                    const bg = item.bg || 'var(--bg-dark)';
                    const acc = item.acc || 'var(--accent-yellow)';
                    previewHtml = \`<div class="color-preview" style="background: linear-gradient(135deg, \${bg} 50%, \${acc} 50%); border: 1px solid var(--glass-border);"></div>\`;
                } else if(tab === 'badges') {`;

content = content.replace(search, replace);
fs.writeFileSync('index.html', content);
