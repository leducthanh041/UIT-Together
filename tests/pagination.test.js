const fs = require('fs'), vm = require('vm'), assert = require('assert');
const source = fs.readFileSync('src/assets/js/site.js', 'utf8');
const helper = source.slice(source.indexOf('    function createPager('), source.indexOf('    function normalize('));
function element() {
  return {children:[], insertBefore(child){this.children.unshift(child);}, attrs:{}, handlers:{}, hidden:false, appendChild(child){this.children.push(child);},setAttribute(k,v){this.attrs[k]=v;},addEventListener(k,v){this.handlers[k]=v;},focus(){this.focused=true;},set textContent(value){this.text=value;this.children=[];},get textContent(){return this.text;}};
}
for (const vietnamese of [false, true]) {
  const create = vm.runInNewContext(helper + '\ncreatePager', {document:{createElement:element},vietnamese,Math,Number,String});
  const scope=element();scope.scrollIntoView=options=>{scope.scrolled=true;assert.equal(options.behavior,'instant');assert.equal(options.block,'start');};
  const items=Array.from({length:23},()=>element());let renders=0;
  const pager=create(scope,items,10,()=>renders++);pager.setItems(items);
  const nav=scope.children[0], info=nav.children[0], buttons=nav.children[1];
  assert.equal(items.filter(i=>!i.hidden).length,10);
  assert.equal(buttons.children[0].disabled,true);
  buttons.children[buttons.children.length-1].handlers.click();
  assert(scope.scrolled, 'Changing pages must scroll to the beginning of the updated list');
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
  const datasetScope=element();datasetScope.scrollIntoView=()=>{};
  const datasets=Array.from({length:13},()=>element());
  create(datasetScope,datasets,3).setItems(datasets);
  const datasetButtons=datasetScope.children[0].children[1];
  for(const count of [3,3,3,3,1]) {
    assert.equal(datasets.filter(item=>!item.hidden).length,count);
    const next=datasetButtons.children[datasetButtons.children.length-1];
    if(count===1) assert(next.disabled,'No extra empty dataset page');
    else next.handlers.click();
  }
  const cohorts=JSON.parse(fs.readFileSync('src/data/cohorts.json','utf8'));
  const cohortScope=element();cohortScope.scrollIntoView=()=>{};
  const students=cohorts.reduce((list,cohort)=>list.concat(cohort.names.map(name=>{
    const item=element();item.name=name;item.getAttribute=()=>cohort.cohort;return item;
  })),[]);
  const staff=Array.from({length:9},()=>{const item=element();item.getAttribute=()=>null;return item;});
  const all=staff.concat(students);
  const cohortPager=create(cohortScope,all,1,null,'data-year');cohortPager.setItems(all);
  const cohortNav=cohortScope.children[0], cohortButtons=cohortNav.children[1];
  assert.deepEqual(all.filter(item=>!item.hidden),staff);
  for(const cohort of cohorts){
    cohortButtons.children[cohortButtons.children.length-1].handlers.click();
    assert.deepEqual(students.filter(item=>!item.hidden).map(item=>item.name),cohort.names);
    assert(staff.every(item=>item.hidden));
    assert(cohortNav.children[0].textContent.endsWith(cohort.cohort));
  }
  assert(cohortButtons.children[cohortButtons.children.length-1].disabled);
  cohortButtons.children[0].handlers.click();
  assert.deepEqual(students.filter(item=>!item.hidden).map(item=>item.name),cohorts[6].names);
  const filtered=students.filter(item=>item.getAttribute()==='K2021');
  cohortPager.setItems(filtered);assert.deepEqual(all.filter(item=>!item.hidden),filtered);
  assert(cohortNav.hidden);assert(cohortNav.children[0].textContent.endsWith('K2021'));
  cohortPager.setItems([]);assert(all.every(item=>item.hidden));
  pager.setItems([]);assert(items.every(i=>i.hidden));assert.equal(nav.hidden,true);assert.equal(renders,5);
}
{
 const create=vm.runInNewContext(helper+'\ncreatePager',{document:{createElement:element},vietnamese:false,Math,Number,String});
 const scope=element(), content=element();scope.appendChild(content);
 create(scope,[element(),element()],1);
 assert.equal(scope.children[0],content,'Keep list content before the pager');
 assert.equal(scope.children[scope.children.length-1].className,'list-pagination','Pager must be the final child');
}
console.log('PASS: pagination boundaries, filtering reset, empty results, EN/VI labels.');
