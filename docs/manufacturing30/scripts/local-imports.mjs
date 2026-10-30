import {readFile,writeFile,access} from 'node:fs/promises';
await access('vendor/three.module.js');await access('vendor/controls/OrbitControls.js');
const path='index.html';let html=await readFile(path,'utf8');html=html.replace('https://cdn.jsdelivr.net/npm/three@0.164.1/build/three.module.js','./vendor/three.module.js').replace('https://cdn.jsdelivr.net/npm/three@0.164.1/examples/jsm/','./vendor/');await writeFile(path,html);
