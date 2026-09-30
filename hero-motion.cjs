const assert=require('node:assert/strict');
const fs=require('node:fs');
const vm=require('node:vm');
function target(){return {handlers:{},attrs:{},hidden:false,textContent:'',classList:{values:new Set(),toggle(k,v){v?this.values.add(k):this.values.delete(k)},add(k){this.values.add(k)}},addEventListener(k,f){this.handlers[k]=f},setAttribute(k,v){this.attrs[k]=v}}}
const hero=target(),control=target(),controls=target(),slides=Array.from({length:3},target),dots=Array.from({length:3},target),pref=target(),doc=target();
pref.matches=false;doc.hidden=false;let tick=null,observe;
hero.querySelectorAll=s=>s==='.hero-slide'?slides:dots;
hero.querySelector=s=>s==='.motion-toggle'?control:controls;
hero.contains=x=>x===control;doc.querySelector=()=>hero;
const source=fs.readFileSync('dist/assets/app.js','utf8').split('// Hero plays automatically')[1];
vm.runInNewContext('// Hero plays automatically'+source,{document:doc,window:{IntersectionObserver:true},matchMedia:()=>pref,IntersectionObserver:class{constructor(fn){observe=fn}observe(){}},clearInterval:()=>{tick=null},setInterval:fn=>{tick=fn;return 1}});
assert.equal(typeof tick,'function');tick();assert.equal(dots[1].attrs['aria-pressed'],'true');
doc.hidden=true;doc.handlers.visibilitychange();assert.equal(tick,null);
doc.hidden=false;doc.handlers.visibilitychange();assert.equal(typeof tick,'function');
observe([{isIntersecting:false}]);assert.equal(tick,null);observe([{isIntersecting:true}]);assert.equal(typeof tick,'function');
pref.matches=true;pref.handlers.change();assert.equal(tick,null);
dots[2].handlers.click();assert.equal(slides[2].attrs['aria-hidden'],'false');assert.equal(tick,null);
const css=fs.readFileSync('dist/assets/style.css','utf8');assert(css.includes('.hero.motion-ready.motion-paused .hero-slide.is-active img'));
console.log('PASS: autoplay, slide selection, visibility, offscreen pause and reduced motion.');
