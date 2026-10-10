'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('assert');
function classes(){const values=new Set();return {add(v){values.add(v);},remove(v){values.delete(v);},has(v){return values.has(v);}};}
function run(reduced,observers){
 const chapter=id=>({id,hidden:false,top:200,classList:classes(),focused:false,contains(){return this.focused;},getBoundingClientRect(){return {top:this.top};},closest(){return this;}});
 const chapters=['supervisors','current-members','former-members'].map(chapter);
 const cohort=chapter('cohort-K2022');cohort.closest=()=>chapters[2];
 const card=chapter('member-card');card.closest=()=>chapters[1];
 const panels=[card,cohort];panels.forEach(panel=>panel.style={setProperty(){}});
 const links=chapters.map(ch=>({hidden:false,attrs:{href:'#'+ch.id},getAttribute(k){return this.attrs[k];},setAttribute(k,v){this.attrs[k]=v;},removeAttribute(k){delete this.attrs[k];},closest(){return this;}}));
 const navHandlers={},mainHandlers={},docHandlers={},properties={};
 const nav={querySelectorAll(){return links;},getBoundingClientRect(){return {height:60};},addEventListener(n,fn){navHandlers[n]=fn;},contains(link){return links.includes(link);}};
 const main={addEventListener(n,fn){mainHandlers[n]=fn;}};
 const directory={querySelectorAll(selector){return selector==='[data-member-chapter]'?chapters:panels;},querySelector(){return nav;},closest(){return main;}};
 const motion={matches:reduced,addEventListener(name,fn){this.change=fn;}};
 const callbacks=[];
 function Observer(fn){callbacks.push(fn);this.observe=()=>{};}
 const window={matchMedia(){return motion;},addEventListener(){}};
 if(observers)window.IntersectionObserver=Observer;
 const document={activeElement:null,documentElement:{style:{setProperty(k,v){properties[k]=v;}}},querySelector(selector){return selector==='.member-directory'?directory:{getBoundingClientRect(){return {height:84};}};},addEventListener(name,fn){docHandlers[name]=fn;}};
 vm.runInNewContext(fs.readFileSync('src/assets/js/members.js','utf8'),{window,document,IntersectionObserver:Observer,Set,Array});
 assert.equal(properties['--member-anchor-offset'],'176px');
 if(observers){
  const callback=callbacks[0],reveal=callbacks[1];
  const scroller={scrollTop:200};
  docHandlers.scroll({target:scroller});assert(!card.classList.has('member-instant'));
  scroller.scrollTop=100;docHandlers.scroll({target:scroller});assert(card.classList.has('member-instant'));
  scroller.scrollTop=150;docHandlers.scroll({target:scroller});assert(!card.classList.has('member-instant'));

  callback([{target:chapters[0],isIntersecting:true}]);
  assert(!chapters[0].classList.has('has-member-motion'),'Whole sections must never be hidden');
  assert(!card.classList.has('is-member-visible'),'Below-fold cards wait for their own intersection');
  reveal([{target:card,isIntersecting:true}]);
  assert(card.classList.has('is-member-visible'));
  assert(!cohort.classList.has('is-member-visible'),'Another member does not reveal early');
  reveal([{target:card,isIntersecting:false}]);
  if(!reduced)assert(!card.classList.has('is-member-visible'));
  reveal([{target:card,isIntersecting:true}]);
  assert(card.classList.has('is-member-visible'),'Scrolling back repeats individual card animation');
  callback([{target:chapters[0],isIntersecting:false},{target:chapters[1],isIntersecting:true}]);
  assert.equal(links[1].attrs['aria-current'],'location');
  callback([{target:chapters[0],isIntersecting:true},{target:chapters[1],isIntersecting:false}]);
  docHandlers.focusin({target:{closest(){return cohort;}}});
  assert(cohort.classList.has('is-member-visible'));assert(chapters[2].classList.has('is-member-visible'));
  assert.equal(links[2].attrs['aria-current'],'location');
  motion.matches=true;motion.change({matches:true});
  assert(panels.every(ch=>ch.classList.has('is-member-visible')));
 }else assert(panels.every(ch=>ch.classList.has('is-member-visible')));
 chapters[0].hidden=true;mainHandlers.input();assert(links[0].hidden);assert.equal(links[1].attrs['aria-current'],'location');
 let prevented=false;navHandlers.click({target:links[2],preventDefault(){prevented=true;}});
 assert.equal(links[2].attrs['aria-current'],'location');assert(!prevented,'Native anchor behavior is preserved');
}
run(false,true);run(true,true);run(false,false);
console.log('PASS: Independent Member reveals, active groups, focus, reduced motion, filters, native anchors and unsupported-observer fallback');
