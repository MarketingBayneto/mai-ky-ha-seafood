document.documentElement.classList.add('js');
// Shadow on the pinned header once the page scrolls.
(()=>{const h=document.querySelector('header');if(!h)return;const f=()=>h.classList.toggle('is-scrolled',scrollY>8);addEventListener('scroll',f,{passive:true});f();})();
const toggle=document.querySelector('.menu-toggle'),nav=document.querySelector('#navigation');toggle?.addEventListener('click',()=>{const open=toggle.getAttribute('aria-expanded')!=='true';toggle.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open)});document.addEventListener('keydown',e=>{if(e.key==='Escape'){if(toggle?.getAttribute('aria-expanded')==='true'){toggle.setAttribute('aria-expanded','false');nav?.classList.remove('open');toggle.focus();}}});
document.querySelectorAll('[data-filter]').forEach(button=>button.addEventListener('click',()=>{document.querySelectorAll('[data-filter]').forEach(b=>b.setAttribute('aria-pressed',String(b===button)));document.querySelectorAll('[data-group]').forEach(card=>card.hidden=button.dataset.filter!=='all'&&card.dataset.group!==button.dataset.filter)}));
const dialog=document.querySelector('.lightbox');
const photos=[...document.querySelectorAll('[data-photo]')];let galleryIndex=0;
function displayPhoto(index){if(!photos.length||!dialog)return;galleryIndex=(index+photos.length)%photos.length;const b=photos[galleryIndex];dialog.querySelector('img').src=b.dataset.photo;dialog.querySelector('img').alt=b.dataset.caption;dialog.querySelector('p').textContent=b.dataset.caption;dialog.querySelector('.gallery-position').textContent=`${galleryIndex+1} / ${photos.length}`;dialog.querySelector('.gallery-controls').hidden=photos.length<2;}
photos.forEach((b,i)=>b.addEventListener('click',()=>{displayPhoto(i);dialog.showModal();}));
dialog?.querySelector('.close').addEventListener('click',()=>dialog.close());
dialog?.querySelector('[data-gallery-prev]').addEventListener('click',()=>displayPhoto(galleryIndex-1));
dialog?.querySelector('[data-gallery-next]').addEventListener('click',()=>displayPhoto(galleryIndex+1));
dialog?.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'||e.key==='ArrowRight'){e.preventDefault();displayPhoto(galleryIndex+(e.key==='ArrowLeft'?-1:1));}});
dialog?.addEventListener('click',e=>{if(e.target===dialog){const r=dialog.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)dialog.close();}});
// Keep the current inquiry and article anchor when switching languages.
document.querySelectorAll('[data-language-switch]').forEach(link=>{
 const destination=new URL(link.getAttribute('href'),location.href);
 destination.search=location.search;destination.hash=location.hash;link.href=destination.href;
});
const form=document.querySelector('#inquiry');
if(form){
 const isEnglish=document.documentElement.lang==='en';
 const message=isEnglish?{
  pending:'To be discussed',subject:'Seafood inquiry — ',
  prepared:'Your email draft is ready. Review it and press Send in your email application. If the application does not open, copy the inquiry and email it to maikyhaseafood01@gmail.com.',
  copied:'Copied. Paste your inquiry into an email to maikyhaseafood01@gmail.com.',
  manual:'Select and copy the text below, then email it to maikyhaseafood01@gmail.com.'
 }:{
  pending:'Trao đổi thêm',subject:'Yêu cầu thủy sản — ',
  prepared:'Email đã được chuẩn bị. Vui lòng kiểm tra và nhấn Gửi trong ứng dụng email. Nếu ứng dụng không mở, hãy sao chép nội dung và gửi đến maikyhaseafood01@gmail.com.',
  copied:'Đã sao chép. Bạn có thể dán nội dung vào email gửi đến maikyhaseafood01@gmail.com.',
  manual:'Chọn và sao chép nội dung bên dưới để gửi qua email.'
 };
 const q=new URLSearchParams(location.search);
 for(const [param,name] of [['san-pham','product'],['nhu-cau','need']]){
  const val=q.get(param);
  if(val&&[...form.elements[name].options].some(o=>o.value===val))form.elements[name].value=val;
 }
 const status=document.querySelector('#form-status');
 function validateInquiry(){
  for(const field of form.querySelectorAll('input[required],textarea[required]'))field.value=field.value.trim();
  return form.reportValidity();
 }
 function content(){
  const f=new FormData(form),selected=n=>form.elements[n].selectedOptions[0].textContent;
  if(isEnglish)return `Dear MAI KỲ HÀ SEAFOOD,\n\nInquiry type: ${selected('need')}\nContact name: ${f.get('name')}\nCompany: ${f.get('company')}\nEmail / phone: ${f.get('contact')}\nProduct: ${selected('product')}\nQuantity: ${f.get('quantity')||message.pending}\nDestination: ${f.get('destination')||message.pending}\n\nRequirements:\n${f.get('message')}\n\nKind regards.`;
  return `Kính gửi MAI KỲ HÀ SEAFOOD,\n\nNhu cầu: ${selected('need')}\nNgười liên hệ: ${f.get('name')}\nDoanh nghiệp: ${f.get('company')}\nEmail/Điện thoại: ${f.get('contact')}\nSản phẩm: ${selected('product')}\nKhối lượng: ${f.get('quantity')||message.pending}\nĐiểm giao: ${f.get('destination')||message.pending}\n\nNội dung yêu cầu:\n${f.get('message')}\n\nTrân trọng.`;
 }
 form.addEventListener('submit',e=>{
  e.preventDefault();if(!validateInquiry())return;
  window.location.href='mailto:maikyhaseafood01@gmail.com?subject='+encodeURIComponent(message.subject+form.elements.company.value)+'&body='+encodeURIComponent(content());
  status.textContent=message.prepared;
 });
 document.querySelector('#copy-request').addEventListener('click',async()=>{
  if(!validateInquiry())return;const text=content();
  try{await navigator.clipboard.writeText(text);status.textContent=message.copied;}
  catch{const box=document.querySelector('#manual-copy');box.hidden=false;const textarea=box.querySelector('textarea');textarea.value=text;textarea.focus();textarea.select();status.textContent=message.manual;}
 });
 form.querySelectorAll('button[disabled]').forEach(button=>button.disabled=false);
}

// Reveal below-the-fold content once as it enters the viewport.
(()=>{
  const motion=window.matchMedia('(prefers-reduced-motion: reduce)');
  if(motion.matches || !('IntersectionObserver' in window)) return;
  const selector='main h2, main .eyebrow, main .sub, main .mosaic-item, main .product-card, main figure, main .panel, main .story, main .steps li, main .prose > p, main .section-heading, main .detail-info, main form, main aside, main .event-grid > div, main .detail-tile, main .editorial-photo, main details';
  const targets=[...document.querySelectorAll(selector)].filter(el=>!el.closest('.hero')&&!el.parentElement.closest(selector));
  const pending=new Set();
  const reveal=el=>{el.classList.remove('scroll-pending');pending.delete(el);observer.unobserve(el);};
  const observer=new IntersectionObserver(entries=>{
    const entering=entries.filter(e=>e.isIntersecting);
    entering.forEach((entry,index)=>{
      entry.target.style.setProperty('--reveal-delay',`${Math.min(index,3)*70}ms`);
      reveal(entry.target);
    });
  },{threshold:0,rootMargin:'0px 0px -28px 0px'});
  targets.forEach(el=>{
    if(el.getBoundingClientRect().top<window.innerHeight) return;
    el.classList.add('scroll-reveal','scroll-pending');pending.add(el);observer.observe(el);
  });
  document.addEventListener('focusin',event=>{
    const el=event.target.closest('.scroll-pending');
    if(el){el.style.setProperty('--reveal-delay','0ms');reveal(el);}
  });
  motion.addEventListener('change',event=>{
    if(event.matches){pending.forEach(reveal);observer.disconnect();}
  });
})();

// Exhibition photo slideshow on the homepage.
(()=>{
 const box=document.querySelector('[data-slides]');if(!box)return;
 const slides=[...box.querySelectorAll('.event-slide')],dots=[...box.querySelectorAll('[data-slide-to]')];
 const preference=matchMedia('(prefers-reduced-motion: reduce)');let current=0,visible=true,timer;
 const show=i=>{current=i;slides.forEach((s,k)=>{s.classList.toggle('is-active',k===i);s.setAttribute('aria-hidden',String(k!==i));});dots.forEach((d,k)=>d.setAttribute('aria-pressed',String(k===i)));};
 const sync=()=>{clearInterval(timer);if(!preference.matches&&visible&&!document.hidden)timer=setInterval(()=>show((current+1)%slides.length),5000);};
 dots.forEach((d,i)=>d.addEventListener('click',()=>{show(i);sync();}));
 document.addEventListener('visibilitychange',sync);preference.addEventListener('change',sync);
 if('IntersectionObserver' in window)new IntersectionObserver(e=>{visible=e[0].isIntersecting;sync();},{threshold:.1}).observe(box);
 sync();
})();

// Metallic light sweep on red buttons as they first appear.
(()=>{
 const buttons=[...document.querySelectorAll('.button:not(.secondary):not(.outline)')];
 if(!buttons.length)return;
 if(!('IntersectionObserver' in window)){buttons.forEach(b=>b.classList.add('shine'));return;}
 const io=new IntersectionObserver(entries=>entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('shine');io.unobserve(e.target);}}),{threshold:.6});
 buttons.forEach(b=>io.observe(b));
})();

// Hero plays automatically while visible, respecting reduced-motion preferences.
(()=>{
 const hero=document.querySelector('.hero');if(!hero)return;
 const slides=[...hero.querySelectorAll('.hero-slide')],dots=[...hero.querySelectorAll('[data-slide]')];
 const preference=matchMedia('(prefers-reduced-motion: reduce)');
 let current=0,visible=true,timer;
 const show=index=>{current=index;slides.forEach((slide,i)=>{slide.classList.toggle('is-active',i===index);slide.setAttribute('aria-hidden',String(i!==index));dots[i].setAttribute('aria-pressed',String(i===index));});};
 const sync=()=>{clearInterval(timer);const stopped=preference.matches||!visible||document.hidden;hero.classList.toggle('motion-paused',stopped);if(!stopped)timer=setInterval(()=>show((current+1)%slides.length),6500);};
 dots.forEach((dot,i)=>dot.addEventListener('click',()=>{show(i);sync();}));
 document.addEventListener('visibilitychange',sync);preference.addEventListener('change',sync);
 if('IntersectionObserver' in window)new IntersectionObserver(entries=>{visible=entries[0].isIntersecting;sync();},{threshold:0.05}).observe(hero);
 hero.querySelector('.hero-controls').hidden=false;hero.classList.add('motion-ready');sync();
})();
