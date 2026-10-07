// The form sends straight to the company Google Sheet when an endpoint is set, and falls back to email if sending fails.
const assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm');
const field=value=>({value,disabled:true,selectedOptions:[{textContent:value}],options:[{value}]});
async function run(fail){
 const elements={name:field('Đối tác'),company:field('Công ty A'),contact:field('a@b.vn'),message:field('Cần cá bạc má'),product:field('ca-bac-ma'),need:field('mua'),quantity:field('1 tấn'),destination:field('Đà Nẵng'),website:field('')};
 const required=['name','company','contact','message'].map(k=>elements[k]);const handlers={},copy={addEventListener(){}},submit={disabled:true},status={};let reset=false,sent=null;
 const form={elements,dataset:{endpoint:'https://script.google.com/macros/s/TEST/exec'},querySelector:()=>submit,querySelectorAll:s=>s==='button[disabled]'?[submit]:required,reportValidity:()=>true,addEventListener:(k,f)=>handlers[k]=f,reset(){reset=true}};
 const document={documentElement:{lang:'vi'},querySelector:s=>({'#inquiry':form,'#form-status':status,'#copy-request':copy,'#manual-copy':{}}[s])};
 const window={location:{href:''}};
 const full=fs.readFileSync('dist/assets/app.js','utf8'),code=full.slice(full.indexOf('const form='),full.indexOf('// Reveal below-the-fold'));
 const fetch=async(url,opt)=>{if(fail)throw new Error('offline');sent={url,body:opt.body.toString(),mode:opt.mode};};
 vm.runInNewContext(code,{document,window,location:{search:'',href:'https://maikyha.com/lien-he/'},URLSearchParams,encodeURIComponent,navigator:{},fetch,FormData:class{get(k){return elements[k].value}}});
 await handlers.submit({preventDefault(){}});
 return {sent,reset,status:status.textContent,href:window.location.href,disabled:submit.disabled};
}
(async()=>{
 const ok=await run(false);
 assert.equal(ok.sent.mode,'no-cors');assert(ok.sent.body.includes('message=C%E1%BA%A7n+c%C3%A1+b%E1%BA%A1c+m%C3%A1'));assert(ok.sent.body.includes('lang=vi'));
 assert(ok.reset);assert(ok.status.startsWith('Cảm ơn'));assert.equal(ok.href,'');assert.equal(ok.disabled,false);
 const bad=await run(true);
 assert(bad.href.startsWith('mailto:maikyhaseafood01@gmail.com?'),'falls back to email when sending fails');
 console.log('PASS: direct sending to the company sheet, form reset, and email fallback when offline.');
})();
