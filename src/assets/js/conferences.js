(function(){
  'use strict';
  const scopes=Array.from(document.querySelectorAll('[data-conference-app]'));
  if(!scopes.length||!window.ConferenceClock)return;
  const clock=window.ConferenceClock,lang=document.documentElement.lang==='vi'?'vi':'en';
  const t=(en,vi)=>lang==='vi'?vi:en;
  const baseMeta=document.querySelector&&document.querySelector('meta[name="site-base-path"]');
  const basePath=baseMeta?baseMeta.content:'';
  const esc=value=>String(value==null?'':value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const url=value=>{try{const u=new URL(value);return ['https:','http:'].includes(u.protocol)&&!u.username&&!u.password?u.href:'';}catch(_){return '';}};
  const topicNames={'vision':'Computer Vision','machine-learning':'Machine Learning','medical':'Medical Imaging','multimedia':'Multimedia','retrieval':'Information Retrieval'};
  const states=scopes.map(scope=>{let seed;try{seed=JSON.parse(scope.querySelector('[data-conference-seed]').textContent);}catch(_){seed={conferences:[]};}return {scope,data:seed,page:1,query:'',topic:'',status:'',signature:'',renderedMinute:-1};});
  function validSchedule(data){
    const validDate=value=>value==null||(/^\d{4}-\d{2}-\d{2}$/.test(value)&&Number.isFinite(Date.parse(value+'T00:00:00Z')));
    return data&&Number.isFinite(Date.parse(data.updated_at))&&Array.isArray(data.conferences)&&data.conferences.length<=100&&data.conferences.every(c=>c&&typeof c.id==='string'&&typeof c.acronym==='string'&&typeof c.name==='string'&&Number.isInteger(c.year)&&c.year>=2000&&c.year<=2200&&Array.isArray(c.topics)&&c.topics.every(t=>typeof t==='string')&&Array.isArray(c.source_urls)&&c.source_urls.every(u=>typeof u==='string')&&validDate(c.starts_on)&&validDate(c.ends_on)&&Array.isArray(c.deadlines)&&c.deadlines.every(d=>d&&typeof d.label==='string'&&validDate(d.date)&&(!d.at||typeof d.at==='string'&&Number.isFinite(Date.parse(d.at)))));
  }
  function date(value){if(!value)return t('To Be Announced','Chưa công bố');return new Intl.DateTimeFormat(lang==='vi'?'vi-VN':'en-GB',{timeZone:'Asia/Ho_Chi_Minh',day:'2-digit',month:'short',year:'numeric'}).format(new Date(value+'T12:00:00+07:00'));}
  function statusLabel(status){return ({confirmed:t('Official Dates','Lịch chính thức'),tentative:t('Tentative','Dự kiến'),unannounced:t('To Be Announced','Chưa công bố'),conflicting:t('Dates Being Confirmed','Lịch đang xác nhận')})[status]||t('Awaiting Update','Đợi cập nhật');}
  function deadlineLabel(d){return ({'Main Paper':t('Main Paper','Bài chính'),'Full Paper':t('Full Paper','Bài dài'),'Short Paper':t('Short Paper','Bài ngắn'),'Round 1 Paper':t('Round 1 Paper','Bài vòng 1'),'Round 2 Paper':t('Round 2 Paper','Bài vòng 2'),'Regular Papers (Full & Short)':t('Regular Papers (Full & Short)','Bài thường (dài và ngắn)')})[d.label]||d.label;}
  function deadlineText(d){const c=clock.deadlineTime(d);if(!c)return t('To Be Announced','Chưa công bố');if(c.precision==='calendar')return date(d.date)+' · '+t('Time / Zone Not Announced','Chưa công bố giờ / múi giờ');return clock.vietnamTime(c.time,lang)+' · UTC+07:00';}
  function timingNote(c){if(c.precision==='calendar')return t('Calendar countdown to 00:00 Vietnam on the deadline date. The actual submission time is not announced.','Đếm lịch đến 00:00 Việt Nam của ngày deadline. Chưa công bố giờ nộp chính xác.');if(c.precision==='aoe-day')return t('Counts to the end of the published AoE date (UTC−12), converted to Vietnam time.','Đếm đến cuối ngày AoE đã công bố (UTC−12), quy đổi sang giờ Việt Nam.');return t('Official submission time, shown in Vietnam time.','Giờ nộp chính thức, hiển thị theo giờ Việt Nam.');}
  function countdown(target,mode='deadline'){
    const parts=clock.parts(target,Date.now()),labels=[t('Days','Ngày'),t('Hours','Giờ'),t('Minutes','Phút'),t('Seconds','Giây')];
    return `<div class="flip-clock" role="timer" aria-live="off" aria-label="${t('Time Remaining','Thời gian còn lại')}" data-countdown-target="${target}" data-countdown-mode="${mode}">${parts.map((value,i)=>`<div class="flip-unit"><span class="flip-tile"><span class="flip-face flip-value">${value}</span><span class="flip-face flip-upper" aria-hidden="true">${value}</span><span class="flip-face flip-lower" aria-hidden="true">${value}</span><span class="flip-seam" aria-hidden="true"></span></span><span class="flip-label">${labels[i]}</span></div>`).join('')}</div><p class="countdown-state" data-countdown-state></p>`;
  }
  function feature(state,now){
    const records=state.data.conferences||[],next=clock.nextDeadline(records,now),event=clock.nextEvent(records,now);
    const signature=JSON.stringify([next&&[next.conference.id,next.conference.year,next.deadline.at,next.deadline.date,next.deadline.label],event&&[event.conference.id,event.conference.year,event.time]]);
    if(state.signature===signature)return;state.signature=signature;
    let html='';
    if(next){const c=next.conference,d=next.deadline,target=next.clock;
      html=`<article class="conference-spotlight"><div class="spotlight-heading"><span class="conference-kicker">${t('Next Paper Deadline','Hạn nộp bài gần nhất')}</span><span class="conference-badge ${d.status==='tentative'?'tentative':''}">${d.status==='tentative'?statusLabel('tentative'):t('Upcoming','Sắp tới')}</span></div><div class="spotlight-body"><div class="spotlight-copy"><h2 translate="no">${esc(c.acronym)} <span>${c.year}</span></h2><p class="spotlight-fullname" translate="no">${esc(c.name)}</p><p class="conference-location"><i class="fas fa-map-marker-alt" aria-hidden="true"></i> ${esc(c.location||t('Location to Be Announced','Chưa công bố địa điểm'))}</p><p class="spotlight-date"><strong>${esc(deadlineLabel(d))}</strong><br>${esc(deadlineText(d))}</p><p class="spotlight-event-date">${t('Conference','Hội nghị')}: ${date(c.starts_on)}${c.ends_on?' – '+date(c.ends_on):''}</p><div class="conference-actions"><a class="conference-button" href="${esc(url(c.website))}" target="_blank" rel="noopener">${t('Official Conference','Website hội nghị')} ↗</a>${state.scope.hasAttribute('data-conference-home')?`<a href="${basePath}${lang==='vi'?'/vi':''}/conferences/">${t('Explore Deadlines','Xem các hạn nộp')} →</a>`:''}</div></div><div class="spotlight-counter"><p class="counter-heading">${target.precision==='calendar'?t('Until the Deadline Date','Đến ngày deadline'):t('Time to Submit','Thời gian còn để nộp')}</p>${countdown(target.time,target.precision==='calendar'?'calendar':'deadline')}<p class="counter-note">${timingNote(target)}</p></div></div></article>`;
    }else html=`<article class="conference-spotlight"><span class="conference-kicker">${t('Next Paper Deadline','Hạn nộp bài gần nhất')}</span><h2>${t('New Dates Are on the Way','Đang chờ lịch mới')}</h2><p>${t('No upcoming paper deadline has been published in the tracked schedule.','Chưa có hạn nộp bài sắp tới được công bố trong danh sách theo dõi.')}</p></article>`;
    if(event){const c=event.conference;html+=`<article class="conference-next-event"><p class="conference-kicker">${t('Next Conference','Hội nghị tổ chức gần nhất')}</p><h3 translate="no">${esc(c.acronym)} ${c.year}</h3><p class="conference-location">${esc(c.location)}</p><p class="event-date">${date(c.starts_on)} – ${date(c.ends_on)}</p>${countdown(event.time,'event')}<p class="counter-note">${t('Calendar countdown to the opening date at 00:00 Vietnam. Exact session times follow the official program.','Đếm lịch đến ngày khai mạc lúc 00:00 Việt Nam. Giờ các phiên theo chương trình chính thức.')}</p><a href="${esc(url(c.website))}" target="_blank" rel="noopener">${t('Visit Conference Website','Xem website hội nghị')} ↗</a></article>`;}
    state.scope.querySelector('[data-conference-feature]').innerHTML=html;
  }
  function card(c,now,featured){
    const upcoming=clock.candidates([c],now)[0];
    return `<article class="conference-card${featured&&featured.conference.id===c.id?' is-nearest':''}" data-conference-id="${esc(c.id)}"><div class="conference-card-top"><span class="conference-badge">${statusLabel(c.date_status)}</span>${featured&&featured.conference.id===c.id?`<span class="nearest-label">${t('Nearest Deadline','Deadline gần nhất')}</span>`:''}</div><h3 translate="no">${esc(c.acronym)} <span>${c.year}</span></h3><p class="conference-name" translate="no">${esc(c.name)}</p><p class="conference-location"><i class="fas fa-map-marker-alt" aria-hidden="true"></i> ${esc(c.location||t('Location to Be Announced','Chưa công bố địa điểm'))}</p><dl><div><dt>${t('Conference Dates','Ngày tổ chức')}</dt><dd>${date(c.starts_on)}${c.ends_on?' – '+date(c.ends_on):''}</dd></div>${(c.deadlines||[]).map(d=>{const time=clock.deadlineTime(d);const closed=time&&time.comparison<=now;return `<div><dt>${esc(deadlineLabel(d))} ${d.status==='tentative'?`<span class="conference-badge tentative">${statusLabel('tentative')}</span>`:''}</dt><dd>${esc(deadlineText(d))}${closed?`<span class="deadline-closed">${t('Closed','Đã hết hạn')}</span>`:''}</dd></div>`;}).join('')||`<div><dt>${t('Paper Deadline','Hạn nộp bài')}</dt><dd>${t('To Be Announced','Chưa công bố')}</dd></div>`}</dl>${upcoming?`<div class="card-countdown">${countdown(upcoming.clock.time,upcoming.clock.precision==='calendar'?'calendar':'deadline')}<p class="counter-note">${timingNote(upcoming.clock)}</p></div>`:''}<div class="conference-tags">${(c.topics||[]).map(topic=>`<span>${esc(topicNames[topic]||topic)}</span>`).join('')}</div>${c.rolled_over?`<p class="conference-note">${t('The previous edition has ended. Next-edition details will appear when announced.','Kỳ trước đã kết thúc. Thông tin kỳ mới sẽ hiện khi được công bố.')}</p>`:''}${(lang==='vi'?c.notes_vi:c.notes_en)?`<p class="conference-note">${esc(lang==='vi'?c.notes_vi:c.notes_en)}</p>`:''}<footer>${url(c.website)?`<a href="${esc(url(c.website))}" target="_blank" rel="noopener">${t('Official Website','Website chính thức')} ↗</a>`:`<span>${t('Official Website to Be Announced','Chưa công bố website kỳ mới')}</span>`}${c.source_urls&&c.source_urls[0]?`<a href="${esc(url(c.source_urls[0]))}" target="_blank" rel="noopener">${t('Dates Source','Nguồn lịch')}</a>`:''}</footer></article>`;
  }
  function directory(state,now){
    const container=state.scope.querySelector('[data-conference-list]');if(!container)return;
    let records=(state.data.conferences||[]).map(r=>clock.edition(r,now));
    const normalize=value=>String(value).normalize('NFD').replace(/[\u0300-\u036f]/g,'').toLowerCase();
    records=records.filter(c=>(!state.query||normalize([c.acronym,c.name,c.location,c.year].join(' ')).includes(normalize(state.query)))&&(!state.topic||(c.topics||[]).includes(state.topic))&&(!state.status||(state.status==='open'?clock.candidates([c],now).length:state.status==='pending'?!c.starts_on:!c.ends_on||Date.parse(c.ends_on+'T23:59:59-12:00')>now)));
    records.sort((a,b)=>{const da=clock.candidates([a],now)[0],db=clock.candidates([b],now)[0];return (da?da.clock.comparison:Infinity)-(db?db.clock.comparison:Infinity)||String(a.starts_on||'9999').localeCompare(String(b.starts_on||'9999'));});
    const pages=Math.max(1,Math.ceil(records.length/6));state.page=Math.min(state.page,pages);const nearest=clock.nextDeadline(state.data.conferences,now);
    container.innerHTML=records.slice((state.page-1)*6,state.page*6).map(c=>card(c,now,nearest)).join('')||`<p class="conference-empty" role="status">${t('No Conferences Match These Filters','Không có hội nghị phù hợp bộ lọc')}</p>`;
    const pager=state.scope.querySelector('[data-conference-pagination]');pager.hidden=pages<=1;
    const indexes=Array.from(new Set([1,state.page-1,state.page,state.page+1,pages])).filter(n=>n>=1&&n<=pages).sort((a,b)=>a-b);
    const button=(label,n,disabled,active)=>`<button type="button" data-conference-page="${n}" ${disabled?'disabled':''} ${active?'aria-current="page"':''}>${label}</button>`;
    pager.innerHTML=`<p class="pagination-status">${t('Page','Trang')} ${state.page} / ${pages} · ${records.length} ${t('Conferences','hội nghị')}</p><div class="pagination-buttons">${button(t('Previous','Trước'),state.page-1,state.page===1)}${indexes.map((n,i)=>`${i&&n-indexes[i-1]>1?'<span class="pagination-gap">…</span>':''}${button(n,n,false,n===state.page)}`).join('')}${button(t('Next','Sau'),state.page+1,state.page===pages)}</div>`;
  }
  function counters(state,now){
    const reduced=window.matchMedia&&window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    state.scope.querySelectorAll('[data-countdown-target]').forEach(element=>{
      const target=Number(element.dataset.countdownTarget),values=clock.parts(target,now);
      const text=element.nextElementSibling;
      if(target<=now&&text){text.textContent=element.dataset.countdownMode==='calendar'?t('Deadline Day — Check the Official Submission Time','Đến ngày deadline — kiểm tra giờ nộp chính thức'):element.dataset.countdownMode==='event'?t('Opening Date Reached — See the Official Program','Đã đến ngày khai mạc — xem chương trình chính thức'):t('Deadline Closed','Đã hết hạn nộp');}
      element.querySelectorAll('.flip-tile').forEach((tile,i)=>{const value=tile.querySelector('.flip-value');if(value.textContent===values[i])return;tile.querySelector('.flip-upper').textContent=value.textContent;tile.querySelector('.flip-lower').textContent=values[i];value.textContent=values[i];if(!reduced){tile.classList.remove('is-flipping');void tile.offsetWidth;tile.classList.add('is-flipping');}});
    });
    const live=state.scope.querySelector('[data-vietnam-clock]');if(live)live.textContent=clock.vietnamTime(now,lang)+' · UTC+07:00';
  }
  function syncText(state){
    const verified=state.data.conferences.map(r=>Date.parse(r.last_success_at)).filter(Number.isFinite);
    const last=verified.length?Math.min(...verified):null;
    const stale=state.data.conferences.some(r=>['stale','pending','partial','conflicting'].includes(r.sync_status))||!last||Date.now()-last>48*3600000;
    state.scope.querySelector('[data-conference-sync]').textContent=(stale?t('Some Sources Await Verification','Một số nguồn đang chờ xác minh'):t('Automatic Source Updates','Tự động cập nhật nguồn'))+' · '+t('Oldest Verified Update','Lần xác minh cũ nhất')+': '+(last?clock.vietnamTime(last,lang):t('Not Yet Verified','Chưa xác minh'));
  }
  function render(state){const now=Date.now();state.signature='';feature(state,now);directory(state,now);counters(state,now);syncText(state);}
  states.forEach(state=>{
    render(state);
    const form=state.scope.querySelector('[data-conference-filters]');if(form){form.addEventListener('submit',e=>e.preventDefault());const filter=()=>{state.query=form.elements.search.value;state.topic=form.elements.topic.value;state.status=form.elements.status.value;state.page=1;directory(state,Date.now());counters(state,Date.now());};form.addEventListener('input',filter);form.addEventListener('change',filter);}
    state.scope.addEventListener('click',e=>{const button=e.target.closest('[data-conference-page]');if(!button)return;state.page=Number(button.dataset.conferencePage);directory(state,Date.now());counters(state,Date.now());const active=state.scope.querySelector('[data-conference-pagination] [aria-current="page"]');if(active)active.focus({preventScroll:true});const list=state.scope.querySelector('.conference-directory');if(list)list.scrollIntoView({behavior:'instant',block:'start'});});
  });
  function tick(){if(document.hidden)return;const now=Date.now();states.forEach(state=>{const previous=state.signature;feature(state,now);if(previous!==state.signature||state.renderedMinute!==Math.floor(now/60000)){state.renderedMinute=Math.floor(now/60000);directory(state,now);}counters(state,now);});}
  setInterval(tick,1000);document.addEventListener('visibilitychange',tick);
  async function refresh(){
    const initial=states[0].data;const urls=[basePath+'/assets/data/conferences.json'];
    if(initial.live_url==='https://raw.githubusercontent.com/leducthanh041/UIT-Together/refs/heads/main/src/data/conferences.json')urls.push(initial.live_url);
    for(const endpoint of urls){const controller=typeof AbortController!=='undefined'?new AbortController():null;const timeout=controller?setTimeout(()=>controller.abort(),5000):null;
      try{const response=await fetch(endpoint,{cache:'no-store',signal:controller?controller.signal:undefined});if(!response.ok)continue;const fresh=await response.json();if(!validSchedule(fresh))continue;
        if(Date.parse(fresh.updated_at)>Date.parse(states[0].data.updated_at)){states.forEach(state=>{state.data=fresh;render(state);});}
      }catch(_){/* Keep the embedded last-known schedule when offline or source unavailable. */}finally{if(timeout)clearTimeout(timeout);}
    }
  }
  refresh();setInterval(refresh,5*60*1000);
})();
