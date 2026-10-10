const fs = require('fs'); const vm = require('vm'); const assert = require('assert');
function control(value='') {return {value,options:[{value:''}],handlers:{},addEventListener(event,fn){this.handlers[event]=fn;},closest(){return scope;},focus(){this.focused=true;},appendChild(option){this.options.push(option);},remove(i){this.options.splice(i,1);}};}
const input=control(), year=control(), type=control(), venue=control(), reset=control();
const status={setAttribute(){},textContent:''}, empty={hidden:true};
function record(text,year,type,venue,name){ const attrs={'data-search-text':text,'data-year':year,'data-publication-type':type,'data-venue':venue,'data-venue-name':name};return {hidden:false,textContent:text,getAttribute(k){return attrs[k]||null;},closest(){return this;}}; }
const papers=[record('Nguyễn Khang Aerial image','2023','journal','access','IEEE Access'),record('Khang Detection','2022','conference','kse','KSE'),record('Other caption','2023','journal','prl','Pattern Recognition Letters')];
const groups=papers.map(p=>({hidden:false,contains(element){return element===p;}}));
const elements={'[data-filter-input]':input,'[data-year-filter]':year,'[data-type-filter]':type,'[data-venue-filter]':venue,'[data-filter-status]':status,'[data-filter-empty]':empty};
const scope={querySelector(s){return elements[s]||null;},querySelectorAll(s){return s==='[data-filter-item]'?papers:s==='[data-filter-reset]'?[reset]:s==='[data-venue-group]'?groups:[];}};
const document={readyState:'complete',documentElement:{classList:{add(){}}},querySelectorAll(s){return s.startsWith('[data-filter-input]')?[input,year,type,venue]:[];},createElement(){return {};},addEventListener(){}};
vm.runInNewContext(fs.readFileSync('src/assets/js/site.js','utf8'),{document,window:{matchMedia(){return {matches:false};}},Map,Set,Array});
assert(papers.every(p=>!p.hidden));
type.value='journal';type.handlers.change();assert.equal(papers[1].hidden,true);assert.equal(venue.options.length,3);
venue.value='access';venue.handlers.change();assert.deepEqual(papers.map(p=>p.hidden),[false,true,true]);
year.value='2022';year.handlers.change();assert(papers.every(p=>p.hidden));assert.equal(empty.hidden,false);assert(groups.every(g=>g.hidden));
reset.handlers.click();assert(papers.every(p=>!p.hidden));assert.equal(venue.options.length,4);assert(input.focused);
input.value='nguyen khang';input.handlers.input();assert.deepEqual(papers.map(p=>p.hidden),[false,true,true]);
console.log('PASS: combined type/venue/year/search, empty groups, reset and Vietnamese accent search.');
