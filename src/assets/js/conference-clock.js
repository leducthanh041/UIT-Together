/* All comparisons use instants; Vietnam formatting never depends on visitor timezone. */
(function(root){
  'use strict';
  const DAY=86400000;
  function deadlineTime(d){
    if(!d||d.status==='unannounced')return null;
    if(d.at&&/(Z|[+-]\d\d:\d\d)$/.test(d.at)){const time=Date.parse(d.at);if(Number.isFinite(time))return {time,comparison:time,precision:'exact'};}
    if(!/^\d{4}-\d{2}-\d{2}$/.test(d.date||''))return null;
    if(!Number.isFinite(Date.parse(d.date+'T00:00:00Z')))return null;
    if(d.zone==='AoE'){const time=Date.parse(d.date+'T23:59:59-12:00');return {time,comparison:time,precision:'aoe-day'};}
    const time=Date.parse(d.date+'T00:00:00+07:00');
    return {time,comparison:time+DAY-1,precision:'calendar'};
  }
  function edition(record,now){
    const end=record.ends_on&&Date.parse(record.ends_on+'T23:59:59-12:00');
    if(!Number.isFinite(end)||end>=now)return record;
    // Never recycle last edition's location/deadlines into an unpublished edition.
    const result=Object.assign({},record,{year:record.year+(record.cadence||1),starts_on:null,ends_on:null,location:'',deadlines:[],date_status:'unannounced',sync_status:'next-edition-pending',source_urls:[],rolled_over:true});
    result.notes_en='Next edition: official dates and location have not been announced';
    result.notes_vi='Kỳ tiếp theo: chưa công bố ngày và địa điểm chính thức';
    result.website=record.series_url||'';return result;
  }
  function candidates(records,now){
    const items=[];records.map(r=>edition(r,now)).forEach(conference=>(conference.deadlines||[]).forEach(deadline=>{const clock=deadlineTime(deadline);if(clock&&clock.comparison>now)items.push({conference,deadline,clock});}));
    return items.sort((a,b)=>a.clock.comparison-b.clock.comparison);
  }
  function nextDeadline(records,now){return candidates(records,now)[0]||null;}
  function nextEvent(records,now){
    return records.map(r=>edition(r,now)).filter(r=>r.starts_on&&r.date_status!=='conflicting').map(conference=>({conference,time:Date.parse(conference.starts_on+'T00:00:00+07:00')})).filter(r=>r.time>now).sort((a,b)=>a.time-b.time)[0]||null;
  }
  function parts(target,now){let value=Math.max(0,Math.ceil((target-now)/1000));const days=Math.floor(value/86400);value%=86400;const hours=Math.floor(value/3600);value%=3600;return [String(days).padStart(2,'0'),String(hours).padStart(2,'0'),String(Math.floor(value/60)).padStart(2,'0'),String(value%60).padStart(2,'0')];}
  function vietnamTime(value,lang){return new Intl.DateTimeFormat(lang==='vi'?'vi-VN':'en-GB',{timeZone:'Asia/Ho_Chi_Minh',day:'2-digit',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit',second:'2-digit',hourCycle:'h23'}).format(new Date(value));}
  const api={deadlineTime,edition,candidates,nextDeadline,nextEvent,parts,vietnamTime};
  if(typeof module!=='undefined'&&module.exports)module.exports=api;else root.ConferenceClock=api;
})(typeof window!=='undefined'?window:{});
