(function(){
var d=document,H=d.documentElement,q=new URLSearchParams(location.search);
var from=(q.get('from')||'').replace(/[^\w.\-]/g,'').slice(0,60),en=H.lang==='en';
var pk=from.replace(/^com\.appscitadel\./,'');
var all=[].slice.call(d.querySelectorAll('[data-id]'));
var cards=all.filter(function(c){return c.classList.contains('card')});
var gone=all.filter(function(c){return from&&(c.dataset.id===pk||c.dataset.pkg===from)});
// ?from=<pkg>: hide the app the visitor is already playing, tag outgoing links
if(from){
  gone.forEach(function(c){c.hidden=true;c.dataset.gone='1'});
  var note=d.getElementById('now');
  if(gone[0]&&note){note.textContent=(en?'You are playing ':'أنت تلعب ')+gone[0].dataset.name+(en?' right now. Here are our other games.':' الآن. وهذه ألعابنا الأخرى.');note.hidden=false}
  [].forEach.call(d.querySelectorAll('a.sb'),function(a){
    var u=a.getAttribute('href');
    if(a.classList.contains('gp'))a.href=u+'&referrer='+encodeURIComponent('utm_source=ofq_hub&utm_medium='+from);
    else if(a.classList.contains('as'))a.href=u+'?ct='+encodeURIComponent(from.slice(0,40));
    else if(a.classList.contains('wb'))a.href=u+'?utm_source=ofq_hub&utm_medium='+encodeURIComponent(from);
  });
}
var qs=location.search.replace(/([?&])lang=\w+&?/,'$1').replace(/[?&]$/,'');
[].forEach.call(d.querySelectorAll('a[data-lang]'),function(a){a.href=a.getAttribute('href').split('?')[0]+qs});
// hide category groups (and their jump links) that have nothing left to show
[].forEach.call(d.querySelectorAll('.grp'),function(g){
  if(!g.querySelector('.card:not([hidden])')){g.hidden=true;var l=d.querySelector('a[data-grp="'+g.id+'"]');if(l)l.hidden=true}
});
// bottom sheet
var dlg=d.getElementById('sheet'),body=d.getElementById('sheet-body'),lastFocus;
function open(c){
  lastFocus=d.activeElement;
  var st=c.querySelector('.stores').cloneNode(true);
  body.textContent='';
  var w=d.createElement('div');w.className='sh';w.style.setProperty('--a',c.style.getPropertyValue('--a'));
  var x=d.createElement('button');x.className='x';x.type='button';x.setAttribute('aria-label',en?'Close':'إغلاق');x.textContent='×';x.addEventListener('click',function(){dlg.close()});
  var im=c.querySelector('.ic').cloneNode();im.removeAttribute('loading');im.className='ic';
  var h=d.createElement('h3');h.id='sheet-t';h.textContent=c.dataset.name;
  var tg=d.createElement('p');tg.className='tg';tg.textContent=c.dataset.tag;
  var ds=d.createElement('p');ds.className='ds';ds.textContent=c.dataset.desc;
  w.append(x,im,h,tg,ds,st);body.appendChild(w);
  dlg.showModal();
  x.focus();
}
d.addEventListener('click',function(e){
  var h=e.target.closest&&e.target.closest('a.hit');
  if(h&&dlg&&dlg.showModal){e.preventDefault();open(h.closest('[data-id]'));return}
  if(e.target===dlg)dlg.close();
});
if(dlg)dlg.addEventListener('close',function(){if(lastFocus&&lastFocus.focus)lastFocus.focus()});
// reveal on scroll (content stays visible if this never runs)
var rv=[].slice.call(d.querySelectorAll('.rv'));
if('IntersectionObserver' in window&&H.classList.contains('js')){
  var io=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}})},{rootMargin:'0px 0px -6% 0px'});
  rv.forEach(function(el){io.observe(el)});
}else{rv.forEach(function(el){el.classList.add('in')})}
})();
