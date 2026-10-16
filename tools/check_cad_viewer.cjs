// Exercise the exact WebAssembly STEP importer shipped with installed CAD Viewer.
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const ext = 'C:/Users/thoma/.vscode/extensions/thingraph.cad-viewer-1.5.7/dist/libs/occt';
async function main() {
  const engine = await require(path.join(ext, 'occt-import-js.js'))();
  if (process.argv.length < 3) {console.log(Object.keys(engine).filter(k => /read|step/i.test(k))); return;}
  const file = path.resolve(process.argv[2]);
  const bytes = fs.readFileSync(file);
  const start = Date.now();
  console.log('READ',path.basename(file),bytes.length);
  const result = engine.ReadStepFile(bytes, null);
  const summary = {
    file, sha256: crypto.createHash('sha256').update(bytes).digest('hex'),
    engine: 'CAD Viewer 1.5.7 bundled occt-import-js 0.0.23',
    success: result.success, keys: Object.keys(result),
    meshes: result.meshes?.length, triangles: result.meshes?.reduce((n,m) => n+(m.index?.array?.length||0)/3,0),
    milliseconds:Date.now()-start,
    meshExample:result.meshes?.[0] ? Object.keys(result.meshes[0]):[],
  };
  console.log(JSON.stringify(summary));
  if(process.argv[3])fs.writeFileSync(process.argv[3],JSON.stringify(summary,null,2));
  if(!result.success || !summary.meshes)process.exitCode=1;
}
main().catch(e=>{console.error(e.stack);process.exitCode=1;});
