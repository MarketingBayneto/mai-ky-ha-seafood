const fs=require('node:fs'),vm=require('node:vm'),assert=require('node:assert/strict');
const source=fs.readFileSync('dist/assets/app.js','utf8');
const code=source.slice(source.indexOf('// Keep the current inquiry'),source.indexOf('const form='));
for(const [from,to] of [['/lien-he/','/en/contact/'],['/en/contact/','/lien-he/']]){
 const a={getAttribute:()=>to};
 vm.runInNewContext(code,{URL,document:{querySelectorAll:()=>[a]},location:{href:'https://example.com'+from,search:'?san-pham=ca-bac-ma&nhu-cau=mua',hash:'#main'}});
 const u=new URL(a.href);assert.equal(u.pathname,to);assert.equal(u.searchParams.get('san-pham'),'ca-bac-ma');assert.equal(u.hash,'#main');
}
console.log('PASS: language switching preserves inquiry parameters and anchors in both directions.');
