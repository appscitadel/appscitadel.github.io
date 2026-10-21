'use strict';
const {apps, en, screenshots} = OFQ;
const isProduct = document.body.dataset.page === 'product';
const params = new URLSearchParams(location.search);
const arText = Object.fromEntries([...document.querySelectorAll('[data-t]')].map(e => [e.dataset.t, e.innerHTML]));
const categories = [['all','الكل','All'],['جماعية','جماعية','Social'],['كلمات','كلمات','Words'],['صور','صور','Pictures'],['ألغاز','ألغاز','Puzzles'],['ذكاء','ذكاء','Brain games'],['كرة قدم','كرة قدم','Football'],['تطبيقات','تطبيقات','Apps']];
const icon = {
  arrow:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M6 18 18 6M6 6h12v12"/></svg>',
  android:'<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="m8 5-1.3-2 .8-.5L9 4.6a9 9 0 0 1 6 0l1.5-2.1.8.5L16 5a7 7 0 0 1 3 5H5a7 7 0 0 1 3-5ZM5 11h14v7a1 1 0 0 1-1 1h-1v3h-2v-3H9v3H7v-3H6a1 1 0 0 1-1-1v-7ZM2 11h2v7H2v-7Zm18 0h2v7h-2v-7Z"/><circle cx="9" cy="7" r=".7" fill="white"/><circle cx="15" cy="7" r=".7" fill="white"/></svg>',
  web:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5" aria-hidden="true"><rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 22h8M12 18v4M3 8h18"/></svg>',
  share:'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><path d="M8 12H5a2 2 0 0 0-2 2v5a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-5a2 2 0 0 0-2-2h-3M12 15V3m-4 4 4-4 4 4"/></svg>'
};
let savedLang;try {savedLang=localStorage.getItem('ofq-language');} catch {}
let lang = ['ar','en'].includes(params.get('lang')) ? params.get('lang') : savedLang === 'en' ? 'en' : 'ar';
let category = categories.some(c=>c[0]===params.get('category')) ? params.get('category') : 'all';
const tx=(ar,english)=>lang==='ar'?ar:english;
const nameOf=a=>a[lang==='ar'?1:2];
const escapeHTML=s=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const normalize=s=>s.toLocaleLowerCase().normalize('NFKD').replace(/[\u064B-\u065F\u0670\u0640]/g,'').replace(/[أإآٱ]/g,'ا').replace(/ى/g,'ي').replace(/ة/g,'ه');
const grid=document.querySelector('#game-grid');
const search=document.querySelector('#search');
const menu=document.querySelector('.menu-toggle');
const nav=document.querySelector('#main-nav');
const lightbox=document.querySelector('#screenshot-dialog');
let currentShots=[],shotIndex=0,toastTimer;

function productURL(a) {return `product.html?app=${a[0]}&lang=${lang}`;}
function catalogURL() {try {const url=new URL(sessionStorage.getItem('ofq-catalog-url')||'index.html',location.href);url.searchParams.set('lang',lang);return 'index.html'+url.search+'#games';} catch {return `index.html?lang=${lang}#games`;}}
function card(a) {
  const name=escapeHTML(nameOf(a));
  return `<article class="game-card"><div class="card-visual" style="--card-bg:${a[8]}"><img src="assets/apps/${a[0]}.webp" alt="" loading="lazy" width="112" height="112"></div><div class="card-body"><span class="card-category">${a[lang==='ar'?3:4]}</span><h3><a href="${productURL(a)}" class="card-link">${name}</a></h3><p class="card-desc">${a[lang==='ar'?5:6]}</p><div class="card-bottom"><span>${a[0]==='timoz'?'Web':'Android'}</span><span class="card-action">${tx('تفاصيل المنتج','View details')} ${icon.arrow}</span></div></div></article>`;
}
function renderFilters() {
  document.querySelector('#filters').innerHTML=categories.map(c=>`<button class="filter ${category===c[0]?'active':''}" data-category="${c[0]}" type="button" aria-pressed="${category===c[0]}">${c[lang==='ar'?1:2]}</button>`).join('');
}
function rememberCatalog() {
  const url=new URL(location.href);url.searchParams.set('lang',lang);
  if(category==='all')url.searchParams.delete('category');else url.searchParams.set('category',category);
  if(search.value.trim())url.searchParams.set('q',search.value.trim());else url.searchParams.delete('q');
  history.replaceState(null,'',url.pathname+url.search+url.hash);
  try {sessionStorage.setItem('ofq-catalog-url','index.html'+url.search+'#games');} catch {}
}
function renderCatalog(updateURL=true) {
  const words=normalize(search.value.trim()).split(/\s+/).filter(Boolean);
  const filtered=apps.filter(a=>(category==='all'||a[3]===category)&&words.every(q=>normalize([a[0],a[1],a[2],a[3],a[4],a[5],a[6]].join(' ')).includes(q)));
  grid.innerHTML=filtered.map(card).join('');
  document.querySelector('#result-count').textContent=tx(`${filtered.length} من ${apps.length} منتجًا`,`${filtered.length} of ${apps.length} products`);
  document.querySelector('#empty').hidden=filtered.length>0;
  document.querySelector('.clear-search').hidden=!search.value;
  if(updateURL)rememberCatalog();
}
function closeMenu(restore=false) {nav.classList.remove('is-open');menu.setAttribute('aria-expanded','false');menu.setAttribute('aria-label',tx('فتح القائمة','Open menu'));if(restore)menu.focus();}
menu.addEventListener('click',()=>{
  const open=menu.getAttribute('aria-expanded')!=='true';nav.classList.toggle('is-open',open);menu.setAttribute('aria-expanded',String(open));menu.setAttribute('aria-label',open?tx('إغلاق القائمة','Close menu'):tx('فتح القائمة','Open menu'));
});
nav.addEventListener('click',e=>{if(e.target.closest('a'))closeMenu();});
document.addEventListener('click',e=>{if(!e.target.closest('header'))closeMenu();});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&menu.getAttribute('aria-expanded')==='true')closeMenu(true);});
matchMedia('(min-width: 861px)').addEventListener('change',()=>closeMenu());

function pageDescription(a) {
  if(a[0]==='timoz')return tx('تيموز منصة ألعاب عربية تجمع الألغاز والكلمات ومسابقات المعلومات والتحديات الجماعية. العب بمفردك أو مع أصحابك مباشرة من المتصفح على الموبايل أو الكمبيوتر، واستكشف أدلة الألعاب قبل بدء التحدي.','Timoz is an Arabic games platform with puzzles, word games, trivia and social challenges. Play on your own or with friends in your mobile or desktop browser, and explore the game guides before your next challenge.');
  if(a[0]==='sabakalemat')return tx('لعبة كلمات وتفكير تجمع فيها مقاطع الحروف لتكوين الإجابات. كل لغز يضم سبعة أسئلة، فتكتشف الرابط وتكوّن الكلمات المطلوبة خطوة بخطوة.','A word and thinking game where you assemble letter segments into answers. Each puzzle presents seven questions: find the connection and build the words, one step at a time.');
  return a[lang==='ar'?5:6];
}
function relatedApps(a) {return [...apps.filter(b=>b[0]!==a[0]&&b[3]===a[3]),...apps.filter(b=>b[0]!==a[0]&&b[3]!==a[3])].slice(0,3);}
function renderProduct() {
  const a=apps.find(a=>a[0]===params.get('app'));
  const content=document.querySelector('#product-content');
  if(!a) {
    content.innerHTML=`<section class="container not-found"><span class="eyebrow">OFQ PRODUCTS</span><h1>${tx('المنتج غير موجود','Product not found')}</h1><p>${tx('قد يكون الرابط غير مكتمل. تصفّح منتجات أفق للعثور على تجربتك التالية.','This link may be incomplete. Explore the OFQ collection to find your next experience.')}</p><a class="button primary" href="index.html?lang=${lang}#games">${tx('تصفّح المنتجات','Explore products')} ${icon.arrow}</a></section>`;
    document.title=tx('المنتج غير موجود | أفق','Product not found | OFQ Ventures');return;
  }
  const isWeb=a[0]==='timoz';
  const shots=screenshots[a[0]]||[];
  const privacy=`https://apps.ofqventures.com/privacy/${a[0]}${lang==='en'?'-en':''}.html`;
  const store=isWeb?'https://timoz.app':`https://play.google.com/store/apps/details?id=${a[7]}`;
  const title=nameOf(a);
  const storeText=isWeb?tx('العب من المتصفح','Play in your browser'):tx('متوفر على Google Play','Get it on Google Play');
  const meta=tx('الفئة','Category'),platform=tx('المنصة','Platform');
  content.innerHTML=`<section class="product-hero" style="--product-bg:${a[8]}"><div class="container"><nav class="breadcrumbs" aria-label="${tx('مسار التنقل','Breadcrumb')}"><a href="index.html?lang=${lang}">${tx('الرئيسية','Home')}</a><span aria-hidden="true">/</span><a href="${catalogURL()}">${tx('منتجاتنا','Products')}</a><span aria-hidden="true">/</span><span aria-current="page">${escapeHTML(title)}</span></nav><div class="product-hero-grid"><div class="product-summary"><span class="eyebrow">${tx('من تطوير أفق','A PRODUCT BY OFQ')}</span><h1>${escapeHTML(title)}</h1><p>${a[lang==='ar'?5:6]}</p><div class="product-tags"><span>${a[lang==='ar'?3:4]}</span><span>${isWeb?'Web · Mobile · Desktop':'Android'}</span><span>${tx('من منتجات أفق','Built by OFQ')}</span></div><div class="product-hero-actions"><a class="button primary" href="${store}" target="_blank" rel="noopener">${isWeb?icon.web:icon.android}<span>${storeText}</span>${icon.arrow}</a><button class="share-button icon-button" type="button" aria-label="${tx('نسخ رابط المنتج','Copy product link')}">${icon.share}</button></div></div><div class="product-brand-art" aria-hidden="true"><div class="product-orbit"></div><span class="product-spark">✳</span><img src="assets/apps/${a[0]}.webp" alt="" width="220" height="220"><span class="product-art-label">OFQ / ${isWeb?'PLATFORM':'APPS'}</span></div></div></div></section><div class="container product-layout"><div class="product-main"><section class="product-section"><div class="section-kicker">${tx('عن المنتج','ABOUT THE PRODUCT')}</div><h2>${tx('تعرّف على','Meet')} ${escapeHTML(title)}</h2><p>${pageDescription(a)}</p>${isWeb?`<a class="text-link" href="https://timoz.app/guides" target="_blank" rel="noopener">${tx('استكشف أدلة الألعاب','Explore the game guides')} ${icon.arrow}</a>`:''}</section>${shots.length?`<section class="product-section"><div class="section-kicker">${tx('من داخل التطبيق','INSIDE THE APP')}</div><div class="screens-heading"><h2>${tx('شاهد التجربة','Take a closer look')}</h2><span>${tx('اضغط على الصورة لتكبيرها','Select an image to enlarge')}</span></div><div class="screenshot-gallery">${shots.map((src,i)=>`<button class="screenshot-thumb" type="button" data-shot="${i}" aria-label="${tx('تكبير لقطة شاشة','Enlarge screenshot')} ${i+1}"><img src="${src}" alt="${escapeHTML(title)} — ${tx('لقطة شاشة','screenshot')} ${i+1}" loading="lazy" width="210" height="400"><span>${String(i+1).padStart(2,'0')} <span aria-hidden="true">⤢</span></span></button>`).join('')}</div><p class="screenshot-source">${tx('صور من صفحة التطبيق الرسمية على Google Play. قد تختلف الواجهة حسب الإصدار.','Images from the app’s official Google Play listing. The interface may vary by version.')}</p></section>`:''}<section class="product-section product-support"><div><h2>${tx('نحن هنا للمساعدة','Here to help')}</h2><p>${tx('لديك سؤال أو ملاحظة عن المنتج؟ تواصل مع فريق أفق.','Have a question or feedback about this product? Talk to the OFQ team.')}</p></div><a class="text-link" href="mailto:contact@ofqventures.com?subject=${encodeURIComponent('Support — '+a[2])}">${tx('تواصل مع الدعم','Contact support')} ${icon.arrow}</a></section></div><aside class="product-sidebar" aria-label="${tx('معلومات المنتج','Product information')}"><div class="product-info"><h2>${tx('ابدأ التجربة','Make it your next experience')}</h2><dl><div><dt>${meta}</dt><dd>${a[lang==='ar'?3:4]}</dd></div><div><dt>${platform}</dt><dd>${isWeb?tx('المتصفح','Web browser'):'Android'}</dd></div><div><dt>${tx('من منتجات','A product of')}</dt><dd>OFQ Ventures</dd></div></dl><a class="button primary" href="${store}" target="_blank" rel="noopener">${isWeb?icon.web:icon.android}<span>${isWeb?tx('ابدأ اللعب','Start playing'):'Google Play'}</span>${icon.arrow}</a><p class="store-note">${isWeb?tx('العب على الموبايل أو الكمبيوتر مباشرة من المتصفح.','Play directly in your mobile or desktop browser.'):tx('رابط إلى المتجر الرسمي. التوافق والتوفر حسب جهازك ومنطقتك.','Opens the official store. Compatibility and availability depend on your device and region.')}</p><a class="privacy-link" href="${privacy}" target="_blank" rel="noopener">${tx('سياسة خصوصية المنتج','Product privacy policy')} ${icon.arrow}</a></div></aside></div><section class="container related-products"><div class="related-heading"><div><span class="eyebrow">${tx('المزيد من أفق','MORE FROM OFQ')}</span><h2>${tx('قد يعجبك أيضًا','You might also like')}</h2></div><a class="text-link" href="${catalogURL()}">${tx('كل المنتجات','All products')} ${icon.arrow}</a></div><div class="game-grid related-grid">${relatedApps(a).map(card).join('')}</div></section>`;
  currentShots=shots;
  document.querySelector('.share-button').addEventListener('click',shareProduct);
  document.querySelectorAll('[data-shot]').forEach(b=>b.addEventListener('click',()=>openShot(Number(b.dataset.shot))));
  document.title=`${title} | OFQ Ventures`;
  document.querySelector('meta[name="description"]').content=pageDescription(a);
  document.querySelector('meta[property="og:title"]').content=document.title;
  document.querySelector('meta[property="og:description"]').content=pageDescription(a);
}
function showToast(message) {clearTimeout(toastTimer);const t=document.querySelector('#toast');t.textContent=message;t.classList.add('is-visible');toastTimer=setTimeout(()=>t.classList.remove('is-visible'),3500);}
async function shareProduct() {
  const url=new URL(location.href);url.searchParams.set('lang',lang);
  try {await navigator.clipboard.writeText(url.href);showToast(tx('تم نسخ رابط المنتج','Product link copied'));} catch {showToast(tx('يمكنك نسخ الرابط من شريط عنوان المتصفح','You can copy the link from your browser’s address bar'));}
}
function paintShot() {
  const a=apps.find(a=>a[0]===params.get('app'));
  const img=document.querySelector('#large-screenshot');img.src=currentShots[shotIndex];img.alt=`${nameOf(a)} — ${tx('لقطة شاشة','screenshot')} ${shotIndex+1}`;
  document.querySelector('#screenshot-title').textContent=nameOf(a);
  document.querySelector('.lightbox-count').textContent=`${shotIndex+1} / ${currentShots.length}`;
  document.querySelector('.previous-shot').disabled=shotIndex===0;
  document.querySelector('.next-shot').disabled=shotIndex===currentShots.length-1;
}
function openShot(i) {shotIndex=i;paintShot();lightbox.showModal();document.documentElement.classList.add('lightbox-open');}
function nextShot(delta) {shotIndex=Math.max(0,Math.min(currentShots.length-1,shotIndex+delta));paintShot();}
document.querySelector('.close-lightbox').addEventListener('click',()=>lightbox.close());
document.querySelector('.previous-shot').addEventListener('click',()=>nextShot(-1));
document.querySelector('.next-shot').addEventListener('click',()=>nextShot(1));
lightbox.addEventListener('close',()=>document.documentElement.classList.remove('lightbox-open'));
lightbox.addEventListener('click',e=>{if(e.target===lightbox){const r=lightbox.getBoundingClientRect();if(e.clientX<r.left||e.clientX>r.right||e.clientY<r.top||e.clientY>r.bottom)lightbox.close();}});
lightbox.addEventListener('keydown',e=>{if(e.key==='ArrowRight'){e.preventDefault();nextShot(1);}if(e.key==='ArrowLeft'){e.preventDefault();nextShot(-1);}});

function setLanguage(next,updateURL=true) {
  lang=next;document.documentElement.lang=lang;document.documentElement.dir=lang==='ar'?'rtl':'ltr';
  document.querySelectorAll('[data-t]').forEach(e=>{const copy=lang==='ar'?arText[e.dataset.t]:en[e.dataset.t];if(copy!==undefined)e.innerHTML=copy;});
  document.querySelector('.language-label').textContent=tx('English','العربية');
  document.querySelector('#language').setAttribute('aria-label',tx('Switch to English','التبديل إلى العربية'));
  nav.setAttribute('aria-label',tx('التنقل الرئيسي','Main navigation'));closeMenu();
  document.querySelector('.close-lightbox').setAttribute('aria-label',tx('إغلاق الصورة','Close image'));
  document.querySelector('.previous-shot').setAttribute('aria-label',tx('الصورة السابقة','Previous screenshot'));
  document.querySelector('.next-shot').setAttribute('aria-label',tx('الصورة التالية','Next screenshot'));
  const footerPrivacy=document.querySelector('footer [data-t="privacy"]');footerPrivacy.href=`https://apps.ofqventures.com/privacy/${lang==='en'?'en.html':''}`;
  if(isProduct) {
    if(updateURL){const url=new URL(location.href);url.searchParams.set('lang',lang);history.replaceState(null,'',url.pathname+url.search);}
    document.querySelectorAll('header nav a[href^="index.html"],a.brand').forEach(a=>{const url=new URL(a.getAttribute('href'),location.href);url.searchParams.set('lang',lang);a.href=url.pathname+url.search+url.hash;});
    renderProduct();
  } else {
    search.placeholder=tx('ابحث عن لعبة أو تطبيق…','Search games & apps…');
    document.querySelector('.clear-search').setAttribute('aria-label',tx('مسح البحث','Clear search'));
    document.querySelector('#filters').setAttribute('aria-label',tx('تصنيف المنتجات','Product categories'));
    document.querySelector('.hero-bottom a').setAttribute('aria-label',tx('استكشف خدمات أفق','Explore OFQ services'));
    document.querySelector('.c1').textContent=tx('مين أسرع واحد فيكم؟ 👀','Who’s the quickest? 👀');
    document.querySelector('.c2').textContent=tx('دورك تبهرهم ✨','Your moment to shine ✨');
    document.querySelector('.board-title').textContent=tx('التحدي يبدأ من هنا','The challenge starts here');
    document.querySelector('.board-bottom span').textContent=tx('أنت + أصحابك','You + your friends');
    document.querySelector('.store-links .outline').href=`product.html?app=timoz&lang=${lang}`;
    document.title=tx('أفق | نبني البرمجيات ونفتح آفاقًا جديدة — OFQ Ventures','OFQ Ventures | Software. Products. Possibilities.');
    document.querySelector('meta[name="description"]').content=tx('أفق فينتشرز: نطوّر منتجاتنا الرقمية ونبني حلولًا برمجية للشركات وأصحاب الأفكار. اكتشف خدماتنا ومنتجاتنا.','OFQ Ventures builds digital products and custom software for businesses and founders. Explore our services and own products.');
    renderFilters();renderCatalog(true);
  }
  try {localStorage.setItem('ofq-language',lang);} catch {}
}
document.querySelector('#language').addEventListener('click',()=>setLanguage(lang==='ar'?'en':'ar'));
document.querySelector('#year').textContent=new Date().getFullYear();
if(!isProduct) {
  search.value=params.get('q')||'';
  document.querySelector('#filters').addEventListener('click',e=>{const b=e.target.closest('[data-category]');if(!b)return;category=b.dataset.category;document.querySelectorAll('.filter').forEach(f=>{const selected=f===b;f.classList.toggle('active',selected);f.setAttribute('aria-pressed',String(selected));});renderCatalog();});
  search.addEventListener('input',()=>renderCatalog());
  document.querySelector('.clear-search').addEventListener('click',()=>{search.value='';renderCatalog();search.focus();});
  document.querySelector('#reset').addEventListener('click',()=>{category='all';search.value='';renderFilters();renderCatalog();search.focus();});
}
setLanguage(lang,false);
