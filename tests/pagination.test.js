const fs = require('fs'), vm = require('vm'), assert = require('assert');
const source = fs.readFileSync('src/assets/js/site.js', 'utf8');
const helper = source.slice(source.indexOf('    function createPager('), source.indexOf('    function normalize('));
function element() {
  return {children:[], insertBefore(child){this.children.unshift(child);}, attrs:{}, handlers:{}, hidden:false, appendChild(child){this.children.push(child);},setAttribute(k,v){this.attrs[k]=v;},addEventListener(k,v){this.handlers[k]=v;},focus(){this.focused=true;},set textContent(value){this.text=value;this.children=[];},get textContent(){return this.text;}};
}
for (const vietnamese of [false, true]) {
  const create = vm.runInNewContext(helper + '\ncreatePager', {document:{createElement:element},vietnamese,Math,Number,String});
  const scope=element();scope.scrollIntoView=()=>{scope.scrolled=true;};
  const items=Array.from({length:23},()=>element());let renders=0;
  const pager=create(scope,items,10,()=>renders++);pager.setItems(items);
  const nav=scope.children[0], info=nav.children[0], buttons=nav.children[1];
  assert.equal(items.filter(i=>!i.hidden).length,10);
  assert.equal(buttons.children[0].disabled,true);
  buttons.children[buttons.children.length-1].handlers.click();
  assert(!scope.scrolled, 'Changing pages must not scroll the viewport');
  assert(items.slice(0,10).every(i=>i.hidden));assert.equal(items.filter(i=>!i.hidden).length,10);
  buttons.children[buttons.children.length-1].handlers.click();
  assert.equal(items.filter(i=>!i.hidden).length,3);assert.equal(buttons.children[buttons.children.length-1].disabled,true);
  pager.setItems([items[0]]);assert.equal(items.filter(i=>!i.hidden).length,1);assert.equal(nav.hidden,true);
  assert(info.textContent.startsWith(vietnamese?'Trang 1':'Page 1'));
  const many=Array.from({length:123},()=>element());
  const largeScope=element();largeScope.scrollIntoView=()=>{};
  const largePager=create(largeScope,many,10);largePager.setItems(many);
  const largeButtons=largeScope.children[0].children[1];
  assert(largeButtons.children.some(b=>b.textContent==='…'));
  largeButtons.children.find(b=>b.textContent==='13').handlers.click();
  assert.equal(many.filter(i=>!i.hidden).length,3);
  assert(largeButtons.children.some(b=>b.textContent==='12'));
  assert(largeButtons.children.some(b=>b.textContent==='1'));
  assert(largeButtons.children.some(b=>b.textContent==='…'));
  pager.setItems([]);assert(items.every(i=>i.hidden));assert.equal(nav.hidden,true);assert.equal(renders,5);
}
console.log('PASS: pagination boundaries, filtering reset, empty results, EN/VI labels.');
