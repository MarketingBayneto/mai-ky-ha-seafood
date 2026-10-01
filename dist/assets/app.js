document.documentElement.classList.add('js');
// Homepage intro "Sóng mở màn": built only when intro-gate.js armed it.
(()=>{
 const root=document.documentElement;
 if(!root.classList.contains('intro-on'))return;
 const release=()=>root.classList.remove('intro-hold');
 const clear=()=>{root.classList.remove('intro-on','intro-hold','intro-built');};
 try{
  const en=root.lang==='en';
  const logo=document.querySelector('header .brand img');
  const wave=(fill,d,stroke)=>`<svg viewBox="0 0 1440 320" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path fill="${fill}" d="${d} V320 H0 Z"/>${stroke?`<path fill="none" stroke="${stroke}" stroke-width="2" stroke-opacity=".55" vector-effect="non-scaling-stroke" d="${d}"/>`:''}</svg>`;
  const el=document.createElement('div');
  el.className='intro';
  el.innerHTML=`<div class="intro-art" aria-hidden="true">
   <div class="intro-wave w1">${wave('#075579','M0 120 C 180 60, 330 40, 520 92 S 860 180, 1040 118 S 1310 40, 1440 86',  '#9fdcf0')}</div>
   <div class="intro-wave w2">${wave('#0a4468','M0 96 C 220 150, 400 170, 600 112 S 940 30, 1160 96 S 1380 150, 1440 132','#5fb3d3')}</div>
   <div class="intro-wave w3">${wave('#061F35','M0 70 C 160 30, 360 20, 560 64 S 900 140, 1120 82 S 1360 30, 1440 52',  '#2f86ad')}</div>
   ${logo?`<figure class="intro-logo"><img src="${logo.getAttribute('src')}" alt="" decoding="async"></figure>`:''}
   <div class="intro-edge"><svg viewBox="0 0 1440 260" preserveAspectRatio="none" aria-hidden="true" focusable="false"><path fill="#061F35" d="M0 0 H1440 V120 C 1250 210, 1060 250, 860 196 S 500 96, 300 152 S 70 228, 0 182 Z"/><path fill="none" stroke="#5fb3d3" stroke-opacity=".45" stroke-width="2" vector-effect="non-scaling-stroke" d="M1440 120 C 1250 210, 1060 250, 860 196 S 500 96, 300 152 S 70 228, 0 182"/></svg></div>
  </div><button type="button" class="intro-skip">${en?'Skip':'Bỏ qua'}</button>`;
  const others=[...document.body.children];
  others.forEach(n=>{n.inert=true;});
  document.body.prepend(el);
  root.classList.add('intro-built');
  let done=false;
  const t=parseFloat(getComputedStyle(el).getPropertyValue('--t'))||1;
  const finish=()=>{
   if(done)return;done=true;
   const hadFocus=el.contains(document.activeElement);
   others.forEach(n=>{n.inert=false;});
   el.remove();clear();release();
   document.removeEventListener('keydown',onKey);
   if(hadFocus){const b=document.querySelector('header .brand');b&&b.focus({preventScroll:true});}
  };
  const skip=()=>{if(done)return;release();el.classList.add('is-skipping');setTimeout(finish,300);};
  const onKey=e=>{if(e.key==='Escape')skip();};
  document.addEventListener('keydown',onKey);
  el.querySelector('.intro-skip').addEventListener('click',skip);
  // Reveal the hero copy as the overlay starts to lift, then clean up.
  setTimeout(release,950*t);
  el.addEventListener('animationend',e=>{if(e.target===el)finish();});
  setTimeout(finish,(1500+700)*t);
 }catch(err){clear();document.querySelectorAll('.intro').forEach(n=>n.remove());[...document.body.children].forEach(n=>{n.inert=false;});}
})();


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
 const buttons=[...document.querySelectorAll('.button:not(.secondary):not(.outline),.footer-contact .contact-icon')];
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
