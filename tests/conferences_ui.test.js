'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('assert');
const ConferenceClock=require('../src/assets/js/conference-clock.js');
const seed=JSON.parse(fs.readFileSync('src/data/conferences.json','utf8'));
let now=Date.parse('2026-10-10T08:00:00Z');
class ClockDate extends Date {static now(){return now;}}
function run(lang,home,base=""){
 const fetched=[];
 const handlers={},timers=[];
 const nodes={};
 ['feature','list','pagination','sync'].forEach(name=>nodes[name]={innerHTML:'',textContent:'',hidden:false});
 const live={textContent:''};
 const form={elements:{search:{value:''},topic:{value:''},status:{value:''}},addEventListener(name,fn){handlers[name]=fn;}};
 const scope={hasAttribute(){return home;},querySelector(selector){
   if(selector==='[data-conference-seed]')return {textContent:JSON.stringify(seed)};
   if(selector==='[data-vietnam-clock]')return live;
   if(selector==='[data-conference-filters]')return home?null:form;
   const match=selector.match(/^\[data-conference-(feature|list|pagination|sync)\]$/);
   if(match)return home&&['list','pagination'].includes(match[1])?null:nodes[match[1]];
   return null;
 },querySelectorAll(){return [];},addEventListener(name,fn){handlers[name]=fn;}};
 const context={window:{ConferenceClock,matchMedia(){return {matches:true};}},document:{hidden:false,documentElement:{lang},querySelector(){return {content:base};},querySelectorAll(){return [scope];},addEventListener(){}},Date:ClockDate,Intl,URL,console,setInterval(fn,ms){timers.push({fn,ms});},fetch(endpoint){fetched.push(endpoint);return Promise.reject(new Error('offline'));},setTimeout(){},clearTimeout(){}};
 vm.runInNewContext(fs.readFileSync('src/assets/js/conferences.js','utf8'),context);
 assert(nodes.feature.innerHTML.includes('ECIR'));
 assert(nodes.feature.innerHTML.includes('ACM MM'));
 assert(nodes.feature.innerHTML.includes('data-countdown-target'));
 assert(nodes.sync.textContent.includes(lang==='vi'?'xác minh':'Verified'));
 assert.equal(fetched[0],base+'/assets/data/conferences.json');
 if(home)assert(nodes.feature.innerHTML.includes('href="'+base+(lang==='vi'?'/vi':'')+'/conferences/"'));
 assert(timers.some(t=>t.ms===1000));assert(timers.some(t=>t.ms===300000));
 if(!home){
  assert(live.textContent.includes('15:00:00'));assert(live.textContent.includes('UTC+07:00'));
  assert(nodes.list.innerHTML.includes('data-conference-id="ecir"'));
  assert.equal((nodes.list.innerHTML.match(/data-conference-id=/g)||[]).length,6);
  handlers.click({target:{closest(){return {dataset:{conferencePage:'3'}};}}});
  assert.equal((nodes.list.innerHTML.match(/data-conference-id=/g)||[]).length,2);
  form.elements.search.value='MICCAI';handlers.input();
  assert(nodes.list.innerHTML.includes('MICCAI'));assert(nodes.pagination.hidden);
  form.elements.search.value='does-not-exist';handlers.input();
  assert(nodes.list.innerHTML.includes(lang==='vi'?'Không có hội nghị':'No Conferences'));
 }
 now=Date.parse('2026-10-13T08:00:00Z');timers.find(t=>t.ms===1000).fn();
 assert(nodes.feature.innerHTML.includes('CVPR'));
 assert(!nodes.feature.innerHTML.includes('spotlight-fullname" translate="no">European'));
 now=Date.parse('2026-10-10T08:00:00Z');
}
run('en',false);run('vi',false);run('en',true);run('vi',true);run('en',false,'/UIT-Together');run('vi',true,'/UIT-Together');
console.log('Conference UI: EN/VI, Home, live Vietnam time, filter, bottom pager, automatic featured-deadline switching and offline fallback passed');
