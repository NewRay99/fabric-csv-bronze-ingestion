// Compile and render the actual embedded calendars with synthetic layout data.
// This checks Vega rendering and viewport bounds, not Power BI filter events.
const fs=require('node:fs'), path=require('node:path'), vm=require('node:vm');
const runtime=process.argv[2], destination=process.argv[3];
const root=path.resolve(__dirname,'../reports/WIP/SM WMPP Mission Control v16');
const manifest=JSON.parse(fs.readFileSync(path.join(root,'Discovery monitoring pages.json'),'utf8'));
const context={console,setTimeout,clearTimeout,performance,URL,TextDecoder,TextEncoder,structuredClone};
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(runtime,'vega.min.js'),'utf8'),context);
vm.runInContext(fs.readFileSync(path.join(runtime,'vega-lite.min.js'),'utf8'),context);
const end=new Date('2026-10-12T00:00:00Z');
const values=Array.from({length:365},(_,i)=>{
  const d=new Date(end);d.setUTCDate(d.getUTCDate()-364+i);
  return {Date:d.toISOString(),Weekday:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][d.getUTCDay()],
    'Calendar Day Runs':i%12,'Calendar Day Failures':i%73===0?1:0,
    'Calendar Day Other':i%71===0?1:0,__selected__:'neutral'};
});
(async()=>{
 const results=[];
 for(const page of manifest.pages){
   const filename=path.join(root,'SM WMPP Mission Control.Report/definition/pages',page.pageId,'visuals',page.calendarId,'visual.json');
   const visual=JSON.parse(fs.readFileSync(filename,'utf8'));
   const raw=visual.visual.objects.vega[0].properties.jsonSpec.expr.Literal.Value;
   const spec=JSON.parse(raw.slice(1,-1).replaceAll("''","'"));spec.data={values};
   const view=new context.vega.View(context.vega.parse(context.vegaLite.compile(spec).spec),{renderer:'none'});
   const svg=await view.toSVG();
   const width=+svg.match(/\bwidth="([\d.]+)"/)[1],height=+svg.match(/\bheight="([\d.]+)"/)[1];
   if(width>visual.position.width||height>visual.position.height)throw Error(page.displayName+' calendar exceeds its viewport: '+width+'x'+height);
   fs.writeFileSync(path.join(destination,'discovery-calendar-'+page.pageId+'.svg'),svg);
   results.push({page:page.displayName,width,height,viewport:visual.position.width+'x'+visual.position.height,status:'PASS'});
   view.finalize();
 }
 fs.writeFileSync(path.join(root,'Discovery calendar rendering validation.json'),JSON.stringify({data:'Synthetic layout fixture',results},null,2)+'\n');
 console.log(JSON.stringify(results));
})().catch(error=>{console.error(error);process.exitCode=1;});
