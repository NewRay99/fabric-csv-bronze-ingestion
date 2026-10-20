// Render embedded phone Deneb specifications and check their real SVG bounds.
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const [runtime,root,destination,actualFile]=process.argv.slice(2);
const manifest=JSON.parse(fs.readFileSync(path.join(root,'Mission Control mobile layout revision.json'),'utf8'));
const actual=actualFile?JSON.parse(fs.readFileSync(actualFile,'utf8').replace(/^\uFEFF/,'')):null;
const ctx={console,setTimeout,clearTimeout,performance,URL,TextDecoder,TextEncoder,structuredClone};
vm.createContext(ctx);
vm.runInContext(fs.readFileSync(path.join(runtime,'vega.min.js'),'utf8'),ctx);
vm.runInContext(fs.readFileSync(path.join(runtime,'vega-lite.min.js'),'utf8'),ctx);
const end=new Date('2026-10-14T00:00:00Z');
const fixture=Array.from({length:365},(_,i)=>{
 const day=new Date(end);day.setUTCDate(day.getUTCDate()-364+i);
 return {Date:day.toISOString(),Weekday:['Sun','Mon','Tue','Wed','Thu','Fri','Sat'][day.getUTCDay()],
  'Calendar Day Runs':i%12,'Calendar Day Failures':i%83===0?1:0,'Calendar Day Other':i%91===0?1:0,
  'Changes / findings':i%15,'Captured discoveries':i%4===0?1:0,'Critical / error findings':i%37===0?1:0,
  __selected__:'neutral',__identity__:'day-'+i};
});
const jobs=Array.from({length:8},(_,i)=>({
 job_run_id:'job-'+i,started_at:`2026-10-13T06:${String(i*5).padStart(2,'0')}:00Z`,ended_at:`2026-10-13T06:${String(i*5+4).padStart(2,'0')}:00Z`,
 pipeline_name:'90_run_live_pipeline',Pipeline:'90_run_live_pipeline',notebook_name:'Notebook '+i,Outcome:'Successful',step_sequence:i+1,
 'Job actual min':4,'Job baseline n':8,'Job prior mean min':3,'Job prior median min':3,'Job prior p25 min':2,'Job prior p75 min':5,
 'Step actual min':4,'Step baseline n':8,'Step prior mean min':3,'Step prior median min':3,'Step prior p25 min':2,'Step prior p75 min':5,
 'Single calendar day':1,'Day Explorer Job Visible':1,'Timeline Job Visible':1,'Timeline Step Visible':1,
 __selected__:'neutral',__identity__:'job-'+i,
}));
function actualCalendar(pid){
 if(!actual)return fixture;
 return actual.filter(r=>r['[Page]']===pid).map(r=>({Date:r['[Date]'],Weekday:r['[Weekday]'],
  'Calendar Day Runs':r['[Jobs]'],'Calendar Day Failures':r['[Failures]'],'Calendar Day Other':r['[Other]'],
  'Changes / findings':r['[Changes]'],'Captured discoveries':r['[Discoveries]'],'Critical / error findings':r['[Critical]'],
  __selected__:'neutral',__identity__:'day-'+r['[Date]']}));
}
(async()=>{
 const results=[];
 for(const page of manifest.pages){
  for(const record of page.records.filter(r=>r.type.startsWith('deneb'))){
   const folder=path.join(root,'SM WMPP Mission Control.Report/definition/pages',page.id,'visuals',record.id);
   const phone=JSON.parse(fs.readFileSync(path.join(folder,'mobile.json'),'utf8'));
   const raw=phone.objects.vega[0].properties.jsonSpec.expr.Literal.Value;
   const spec=JSON.parse(raw.slice(1,-1).replaceAll("''","'"));
   const calendar=record.role==='four-band calendar',flag=record.role==='recency flag';
   const values=calendar?actualCalendar(page.id):flag?[{'Flag code':3,'Flag label':'Latest day','Flag explanation':'Layout fixture'}]:jobs;
   if(calendar&&values.length!==365)throw Error(page.name+' calendar must preserve all 365 records');
   spec.data={values};
   const view=new ctx.vega.View(ctx.vega.parse(ctx.vegaLite.compile(spec).spec),{renderer:'none'});
   const svg=await view.toSVG();
   let retainedCalendarTiles=0;
   if(calendar){
    const ids=new Set();
    function checkScene(node){
     if(node.datum?.__identity__ && node.mark?.marktype==='rect')ids.add(node.datum.__identity__);
     for(const item of node.items||[])checkScene(item);
    }
    checkScene(view.scenegraph().root);
    if(ids.size!==365)throw Error(page.name+' calendar did not retain 365 selectable day identities: '+ids.size);
    retainedCalendarTiles=ids.size;
   }
   const width=+svg.match(/\bwidth="([\d.]+)"/)[1],height=+svg.match(/\bheight="([\d.]+)"/)[1];
   if(width>phone.position.width+.1)throw Error(page.name+' '+record.role+' too wide: '+width+' > '+phone.position.width);
   if((calendar||flag)&&height>phone.position.height+.1)throw Error(page.name+' '+record.role+' too tall: '+height+' > '+phone.position.height);
   fs.writeFileSync(path.join(destination,'phone-'+page.id+'-'+record.id+'.svg'),svg);
   results.push({page:page.name,visual:record.id,role:record.role,width,height,viewport:phone.position.width+'x'+phone.position.height,
     data:calendar?(actual?'Actual retained calendar records':'365-day layout fixture'):'Layout fixture',
     retainedCalendarTiles,status:'PASS'});
   view.finalize();
  }
 }
 fs.writeFileSync(path.join(root,'Mission Control mobile chart validation.json'),JSON.stringify({status:'PASS',results},null,2)+'\n');
 console.log(JSON.stringify(results));
})().catch(e=>{console.error(e);process.exitCode=1});
