const fs=require('fs'),vm=require('vm'),assert=require('assert');
const source=fs.readFileSync('src/assets/js/site.js','utf8');
function classes(){const set=new Set();return {add:v=>set.add(v),remove:v=>set.delete(v),toggle(v,on){if(on)set.add(v);else set.delete(v);},has:v=>set.has(v)};}
const slide=()=>({classList:classes(),attrs:{},setAttribute(k,v){this.attrs[k]=v;}});
const slides=Array.from({length:3},slide);slides[0].classList.add('is-active');
function control(){return {hidden:true,handlers:{},attrs:{},addEventListener(k,fn){this.handlers[k]=fn;},setAttribute(k,v){this.attrs[k]=v;}};}
const controls={'.slideshow-controls':control(),'[data-slide-pause]':control(),'[data-slide-prev]':control(),'[data-slide-next]':control(),'[data-slide-status]':control()};
const carousel={querySelectorAll:()=>slides,querySelector:s=>controls[s],addEventListener(){},getBoundingClientRect:()=>({top:100,bottom:400}),contains:()=>false};
let tick;const motion={matches:false};const document={hidden:false,querySelectorAll:()=>[carousel]};
const code=source.slice(source.indexOf("    document.querySelectorAll('[data-slideshow]')"),source.indexOf('    // Viewport intersections'));
vm.runInNewContext(code,{document,vietnamese:false,window:{innerHeight:800,matchMedia:()=>motion,setInterval(fn){tick=fn;}},Array,String});
tick();assert(slides[1].classList.has('is-active'));assert.equal(slides[0].attrs['aria-hidden'],'true');
controls['[data-slide-pause]'].handlers.click();tick();assert(slides[1].classList.has('is-active'));
controls['[data-slide-next]'].handlers.click();assert(slides[2].classList.has('is-active'));
controls['[data-slide-pause]'].handlers.click();motion.matches=true;tick();assert(slides[2].classList.has('is-active'));
motion.matches=false;document.hidden=true;tick();assert(slides[2].classList.has('is-active'));
const revealHandlers = {};
let callback;const target={classList:classes(),closest:()=>null,parentElement:{closest:()=>null},contains:()=>false};
const reveal=source.slice(source.indexOf('    // Viewport intersections'),source.lastIndexOf('\n  }\n'));
function IntersectionObserver(fn){callback=fn;this.observe=()=>{};this.disconnect=()=>{};}
vm.runInNewContext(reveal,{document:{querySelectorAll:()=>[target],addEventListener(name, fn){revealHandlers[name]=fn;},activeElement:null},window:{IntersectionObserver,matchMedia:()=>({matches:false})},IntersectionObserver,Array});
callback([{target,isIntersecting:true}]);assert(target.classList.has('is-revealed'));
callback([{target,isIntersecting:false}]);assert(!target.classList.has('is-revealed'));
callback([{target,isIntersecting:true}]);assert(target.classList.has('is-revealed'));
console.log('PASS: slideshow rotation/pause/reduced motion and repeat scroll reveal.');

const scroller={scrollTop:200};
revealHandlers.scroll({target:scroller});assert(!target.classList.has('reveal-instant'));
scroller.scrollTop=100;revealHandlers.scroll({target:scroller});assert(target.classList.has('reveal-instant'));
callback([{target,isIntersecting:true}]);assert(target.classList.has('is-revealed'));
scroller.scrollTop=150;revealHandlers.scroll({target:scroller});assert(!target.classList.has('reveal-instant'));
