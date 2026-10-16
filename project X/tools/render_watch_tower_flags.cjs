const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const [runtime,root,dest]=process.argv.slice(2);
const ctx={console,setTimeout,clearTimeout,performance,URL,TextDecoder,TextEncoder,structuredClone};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(runtime,'vega.min.js'),'utf8'),ctx);
vm.runInContext(fs.readFileSync(path.join(runtime,'vega-lite.min.js'),'utf8'),ctx);
const manifest=JSON.parse(fs.readFileSync(path.join(root,'Watch Tower flags revision.json'),'utf8'));
const visual=JSON.parse(fs.readFileSync(path.join(root,'SM WMPP Mission Control.Report/definition/pages',manifest.pageId,'visuals',manifest.flagVisualIds[0],'visual.json'),'utf8'));
const raw=visual.visual.objects.vega[0].properties.jsonSpec.expr.Literal.Value;
const spec=JSON.parse(raw.slice(1,-1).replaceAll("''","'"));
(async()=>{
 const checks=[];
 for(const [code,label,color] of [[0,'No record','#F3F7EF'],[1,'History','#8E9991'],[2,'Prior 7 days','#FFC45C'],[3,'Latest day','#FF4D5E']]){
  const example=structuredClone(spec);example.data={values:[{'Flag code':code,'Flag label':label,'Flag explanation':'Example '+label}]};
  const view=new ctx.vega.View(ctx.vega.parse(ctx.vegaLite.compile(example).spec),{renderer:'none'});
  const svg=await view.toSVG();
  const width=+svg.match(/\bwidth="([\d.]+)"/)[1],height=+svg.match(/\bheight="([\d.]+)"/)[1];
  if(width>visual.position.width||height>visual.position.height||!svg.toLowerCase().includes(color.toLowerCase()))throw Error('Flag rendering mismatch '+label);
  fs.writeFileSync(path.join(dest,'watch-tower-flag-'+code+'.svg'),svg);
  checks.push({code,label,width,height,color,status:'PASS'});view.finalize();
 }
 fs.writeFileSync(path.join(root,'Watch Tower flags rendering validation.json'),JSON.stringify({status:'PASS',checks},null,2)+'\n');
 console.log(JSON.stringify(checks));
})().catch(e=>{console.error(e);process.exitCode=1});
