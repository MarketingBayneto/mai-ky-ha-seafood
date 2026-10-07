/* Decides, before first paint, whether the homepage "wave opening" intro plays.
   Plays once per tab session, only on the homepage, never with reduced motion.
   Any failure leaves the page untouched; a timer clears the cover regardless. */
/* Mark scripts as available before first paint so the phone menu starts folded (no layout jump). */
document.documentElement.classList.add('js');
(function(){
 try{
  var d=document.documentElement;
  if(d.getAttribute('data-page')!=='home'){sessionStorage.setItem('mkh-intro','seen');return;}
  if(window.matchMedia&&matchMedia('(prefers-reduced-motion: reduce)').matches)return;
  if(sessionStorage.getItem('mkh-intro'))return;
  sessionStorage.setItem('mkh-intro','seen');
  if(sessionStorage.getItem('mkh-intro')!=='seen')return;
  d.classList.add('intro-on','intro-hold');
  setTimeout(function(){d.classList.remove('intro-on','intro-hold');},7000);
 }catch(e){}
})();
