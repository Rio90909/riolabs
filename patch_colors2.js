const fs = require('fs');
let content = fs.readFileSync('index.html', 'utf8');

const search = `.color-preview { width: 30px; height: 30px; border-radius: 50%; margin: 0 auto 5px auto; box-shadow: 0 0 10px rgba(0,0,0,0.5); }`;

const replace = `.color-preview { width: 40px; height: 10px; border-radius: 5px; margin: 0 auto 5px auto; box-shadow: 0 0 10px rgba(0,0,0,0.5); }`;

content = content.replace(search, replace);
fs.writeFileSync('index.html', content);
