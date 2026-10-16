// Compile and render the actual embedded calendars with synthetic layout data.
// This checks Vega rendering and viewport bounds, not Power BI filter events.
const fs=require('node:fs'), path=require('node:path'), vm=require('node:vm');
const runtime=process.argv[2], destination=process.argv[3];
const root=process.argv[4] || path.resolve(__dirname,'../reports/WIP/SM WMPP Mission Control v16');
const activityManifest=path.join(root,'Change and discovery calendar revision.json');
const manifest=JSON.parse(fs.readFileSync(fs.existsSync(activityManifest)?activityManifest:path.join(root,'Discovery monitoring pages.json'),'utf8'));
const actualRows=process.argv[5]?JSON.parse(fs.readFileSync(process.argv[5],'utf8').replace(/^\uFEFF/,'')):null;
const context={console,setTimeout,clearTimeout,performance,URL,TextDecoder,TextEncoder,structuredClone};
vm.createContext(context);
vm.runInContext(fs.readFileSync(path.join(runtime,'vega.min.js'),'utf8'),context);
vm.runInContext(fs.readFileSync(path.join(runtime,'vega-lite.min.js'),'utf8'),context);
const end=new Date('2026-10-13T00:00:00Z');
const values=Array.from({length:365},(_,i)=>{
  const d=new Date(end);d.setUTCDate(d.getUTCDate()-364+i);
  return {Date:d.toISOString(),Weekday:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][d.getUTCDay()],
    'Calendar Day Runs':i%12,'Calendar Day Failures':i%73===0?1:0,
    'Calendar Day Other':i%71===0?1:0,
    'Changes / findings':i%12,'Captured discoveries':i%4===0?1:0,
    'Critical / error findings':i%73===0?1:0,__selected__:'neutral'};
});
(async()=>{
 const results=[];
 for(const page of manifest.pages){
   const filename=path.join(root,'SM WMPP Mission Control.Report/definition/pages',page.pageId,'visuals',page.calendarId,'visual.json');
   const visual=JSON.parse(fs.readFileSync(filename,'utf8'));
   const raw=visual.visual.objects.vega[0].properties.jsonSpec.expr.Literal.Value;
   const spec=JSON.parse(raw.slice(1,-1).replaceAll("''","'"));
   const pageRows=actualRows?actualRows.filter(r=>r['[Page]']===page.pageId).map(r=>({
     Date:r['[Date]'],Weekday:r['[Weekday]'],'Changes / findings':r['[Changes / findings]'],
     'Captured discoveries':r['[Captured discoveries]'],'Critical / error findings':r['[Critical / error findings]'],__selected__:'neutral'})):values;
   if(pageRows.length!==365)throw Error(page.displayName+' calendar does not contain exactly 365 days');
   spec.data={values:pageRows};
   const view=new context.vega.View(context.vega.parse(context.vegaLite.compile(spec).spec),{renderer:'none'});
   const svg=await view.toSVG();
   const width=+svg.match(/\bwidth="([\d.]+)"/)[1],height=+svg.match(/\bheight="([\d.]+)"/)[1];
   if(width>visual.position.width||height>visual.position.height)throw Error(page.displayName+' calendar exceeds its viewport: '+width+'x'+height);
   fs.writeFileSync(path.join(destination,'discovery-calendar-'+page.pageId+'.svg'),svg);
   results.push({page:page.displayName,width,height,viewport:visual.position.width+'x'+visual.position.height,
     activeDays:pageRows.filter(r=>r['Changes / findings']>0||r['Captured discoveries']>0).length,status:'PASS'});
   view.finalize();
 }
 fs.writeFileSync(path.join(root,'Discovery calendar rendering validation.json'),JSON.stringify({data:actualRows?'Actual imported cache, proposed measure definitions':'Synthetic layout fixture',results},null,2)+'\n');
 console.log(JSON.stringify(results));
})().catch(error=>{console.error(error);process.exitCode=1;});
