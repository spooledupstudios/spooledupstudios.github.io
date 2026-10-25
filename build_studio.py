# Builds the studio pages (home, apps, about, contact, beta, terms, 404). Support and privacy pages come from build.py and are not touched here.
import os, html
SITE = 'https://spooledupstudios.com'
BETA_ENDPOINT = ''  # set to the Cloudflare Worker URL (see cloudflare/README.md); empty = form falls back to email

CSS = """
:root{--navy:#0E1726;--mid:#141F33;--deep:#070D18;--orange:#FF5A1F;--amber:#FFB03B;--steel:#C7D0DE;--muted:#8B98B0;--line:#24324B;--white:#fff;
--font:Inter,-apple-system,"Segoe UI",system-ui,sans-serif;color-scheme:dark}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;background:var(--navy);color:var(--steel);font:17px/1.65 var(--font);-webkit-font-smoothing:antialiased}
a{color:var(--orange)}
a:focus-visible,button:focus-visible,input:focus-visible,select:focus-visible,textarea:focus-visible{outline:3px solid var(--amber);outline-offset:2px}
.wrap{max-width:1080px;margin:0 auto;padding-inline:20px}
h1,h2,h3{color:var(--white);font-weight:800;letter-spacing:-.02em;line-height:1.1;margin:0;text-wrap:balance}
h1{font-size:clamp(40px,8vw,76px);font-weight:900;letter-spacing:-.035em}
h2{font-size:clamp(28px,4.5vw,40px)}
h3{font-size:21px;letter-spacing:-.01em}
p{margin:12px 0}
.eyebrow{color:var(--orange);font-weight:700;font-size:13px;letter-spacing:.16em;text-transform:uppercase;margin:0 0 14px}
.skip{position:absolute;left:-999px;top:8px;background:var(--orange);color:var(--navy);padding:8px 14px;border-radius:8px;z-index:20}
.skip:focus{left:8px}
header.top{position:sticky;top:0;z-index:10;background:rgba(14,23,38,.92);backdrop-filter:blur(10px);border-bottom:1px solid var(--line)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:16px;height:68px}
.logo img{height:30px;width:auto;display:block}
nav.main{display:flex;align-items:center;gap:6px 22px;flex-wrap:wrap}
nav.main a{color:var(--steel);text-decoration:none;font-weight:600;font-size:15px}
nav.main a:hover,nav.main a[aria-current=page]{color:var(--white)}
.btn{display:inline-block;background:var(--orange);color:var(--navy)!important;font:700 16px var(--font);padding:13px 22px;border-radius:10px;text-decoration:none;border:0;cursor:pointer}
.btn:hover{background:#ff7340}
.btn.ghost{background:transparent;color:var(--white)!important;border:1.5px solid #3A4B69}
.btn.ghost:hover{border-color:var(--steel);background:transparent}
.btn.small{padding:9px 16px;font-size:14px}
nav.main .btn{color:var(--navy)}
.hero{padding:96px 0 84px;background:radial-gradient(900px 420px at 85% -10%,rgba(255,90,31,.20),transparent 60%),var(--navy)}
.hero p.lead{font-size:clamp(18px,2.4vw,22px);max-width:620px;color:var(--steel);margin:22px 0 32px}
.cta{display:flex;flex-wrap:wrap;gap:12px}
section.block{padding:84px 0;border-top:1px solid var(--line)}
section.block.alt{background:var(--mid)}
.grid{display:grid;gap:18px;margin-top:34px}
.g3{grid-template-columns:repeat(auto-fit,minmax(250px,1fr))}
.g2{grid-template-columns:repeat(auto-fit,minmax(300px,1fr))}
.card{background:var(--mid);border:1px solid var(--line);border-radius:16px;padding:26px}
section.alt .card{background:var(--navy)}
.card p{margin:10px 0 0;color:var(--steel)}
.card .tag{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);border:1px solid #4a3a1e;border-radius:999px;padding:4px 10px;margin-bottom:14px}
.num{color:var(--orange);font-weight:900;font-size:15px;letter-spacing:.1em;margin-bottom:10px}
.band{background:linear-gradient(120deg,#1a2740,#2a1a14);border:1px solid var(--line);border-radius:20px;padding:44px 32px;display:flex;flex-wrap:wrap;gap:24px;align-items:center;justify-content:space-between}
.band h2{font-size:clamp(26px,4vw,34px)}
.band p{margin:8px 0 0;max-width:540px}
.page-head{padding:72px 0 40px}
.page-head p.lead{font-size:20px;max-width:680px;margin-top:18px}
.prose{max-width:720px}
.prose h2{font-size:26px;margin-top:44px}
.prose h3{margin-top:28px}
.prose ul{padding-left:22px}.prose li{margin:6px 0}
dl.facts{display:grid;grid-template-columns:max-content 1fr;gap:10px 28px;margin:26px 0}
dl.facts dt{color:var(--muted);font-weight:600}dl.facts dd{margin:0;color:var(--white)}
form.beta{display:grid;gap:18px;max-width:560px;margin-top:28px}
label{display:grid;gap:7px;color:var(--white);font-weight:600;font-size:15px}
label small{color:var(--muted);font-weight:400}
input,select,textarea{font:16px var(--font);background:var(--mid);color:var(--white);border:1.5px solid #34466a;border-radius:10px;padding:13px 14px;width:100%}
input::placeholder{color:#6f7d96}
.hp{position:absolute;left:-9999px;height:0;overflow:hidden}
.note{color:var(--muted);font-size:14px}
.ok{background:#12301f;border:1px solid #2F7A46;color:#cfeedd;border-radius:12px;padding:16px 18px}
.err{background:#3a1a14;border:1px solid #a33a22;color:#ffd9cf;border-radius:12px;padding:16px 18px}
footer.foot{border-top:1px solid var(--line);background:var(--deep);padding:48px 0 36px;margin-top:0;font-size:15px}
.fgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:28px}
.fgrid h4{color:var(--white);font-size:14px;letter-spacing:.08em;text-transform:uppercase;margin:0 0 12px}
.fgrid a{display:block;color:var(--steel);text-decoration:none;margin:7px 0}.fgrid a:hover{color:var(--white)}
.legal{margin-top:34px;padding-top:20px;border-top:1px solid var(--line);color:var(--muted);font-size:14px;display:flex;flex-wrap:wrap;gap:8px 24px;justify-content:space-between}
@media(max-width:720px){.hero{padding:64px 0 56px}section.block{padding:60px 0}nav.main{gap:4px 16px}.bar{height:auto;padding:12px 0;flex-wrap:wrap}}
@media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
"""

NAV = [('/apps/','Apps'),('/about/','About'),('/contact/','Contact')]

def page(path, title, desc, body, current='', og_title=None):
    url = SITE + path
    nav = ''.join(f'<a href="{h}"' + (' aria-current="page"' if h==current else '') + f'>{t}</a>' for h,t in NAV)
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title>
<meta name="description" content="{html.escape(desc)}">
<link rel="canonical" href="{url}">
<meta name="theme-color" content="#0E1726">
<meta property="og:type" content="website"><meta property="og:site_name" content="Spooled Up Studios">
<meta property="og:title" content="{html.escape(og_title or title)}"><meta property="og:description" content="{html.escape(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{SITE}/assets/og.png">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/svg+xml" href="/assets/favicon-512.svg"><link rel="icon" type="image/png" sizes="32x32" href="/assets/favicon-32.png">
<link rel="apple-touch-icon" href="/assets/favicon-192.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap">
<style>{CSS}</style>
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"Organization","name":"Spooled Up Studios","url":"{SITE}","logo":"{SITE}/assets/favicon-512.png","email":"info@spooledupstudios.com","address":{{"@type":"PostalAddress","addressRegion":"NY","addressCountry":"US"}}}}</script>
</head><body>
<a class="skip" href="#main">Skip to content</a>
<header class="top"><div class="wrap bar">
<a class="logo" href="/" aria-label="Spooled Up Studios home"><img src="/assets/spooled-up-lockup-horizontal-for-dark-bg.svg" alt="Spooled Up Studios" width="190" height="30"></a>
<nav class="main" aria-label="Main">{nav}<a class="btn small" href="/beta/">Join the beta</a></nav>
</div></header>
<main id="main">
{body}
</main>
<footer class="foot"><div class="wrap">
<div class="fgrid">
<div><a href="/" aria-label="Spooled Up Studios"><img src="/assets/spooled-up-lockup-horizontal-for-dark-bg.svg" alt="Spooled Up Studios" width="170" height="27"></a><p class="note" style="margin-top:14px">Independent app studio.<br>Built in New York. Made for everywhere.</p></div>
<div><h4>Studio</h4><a href="/apps/">Apps</a><a href="/about/">About</a><a href="/contact/">Contact</a><a href="/beta/">Join the beta</a></div>
<div><h4>What's for Dinner?</h4><a href="/support/">Support</a><a href="/privacy/">Privacy policy</a></div>
<div><h4>Legal</h4><a href="/terms/">Terms of use</a><a href="/privacy/">Privacy policy</a><a href="mailto:info@spooledupstudios.com">info@spooledupstudios.com</a></div>
</div>
<div class="legal"><span>&copy; 2026 Spooled Up Studios LLC. All rights reserved.</span><span>New York, USA</span></div>
</div></footer>
</body></html>
"""

def w(path, content):
    d = path.strip('/')
    if d: os.makedirs(d, exist_ok=True)
    open((d + '/' if d else '') + 'index.html', 'w', encoding='utf-8').write(content)

# ---------- Home ----------
home = """
<section class="hero"><div class="wrap">
<p class="eyebrow">Independent app studio &middot; New York</p>
<h1>Built to move.</h1>
<p class="lead">Spooled Up Studios designs and ships fast, useful apps, then keeps improving them long after launch. Full power from day one.</p>
<div class="cta"><a class="btn" href="/beta/">Join the beta</a><a class="btn ghost" href="/apps/">See our apps</a></div>
</div></section>

<section class="block" id="apps"><div class="wrap">
<p class="eyebrow">Our apps</p>
<h2>Made to be used, not admired.</h2>
<div class="grid g2">
<article class="card">
<span class="tag">In beta</span>
<h3>What's for Dinner?</h3>
<p>Can't decide where to eat? Spin for a restaurant near you, a recipe to cook at home, or something to do. Pick together with friends and plan the week.</p>
<div class="cta" style="margin-top:22px"><a class="btn small" href="/apps/#whats-for-dinner">Learn more</a></div>
</article>
<article class="card">
<span class="tag">Coming</span>
<h3>More on the way</h3>
<p>Tools for shops and small businesses, and products with roots in aviation: places where things have to work the first time. Join the beta list to hear first.</p>
<div class="cta" style="margin-top:22px"><a class="btn small ghost" href="/beta/">Get early access</a></div>
</article>
</div></div></section>

<section class="block alt"><div class="wrap">
<p class="eyebrow">How we build</p>
<h2>Three rules for everything we ship.</h2>
<div class="grid g3">
<div class="card"><div class="num">01</div><h3>Full power, every time</h3><p>We don't ship half-done. If it isn't ready, it waits.</p></div>
<div class="card"><div class="num">02</div><h3>Built to move</h3><p>Fast to load, fast to use, fast to improve. Updates keep coming after launch.</p></div>
<div class="card"><div class="num">03</div><h3>Made for everywhere</h3><p>Global from the first release, on the phone in your pocket or the browser on your desk.</p></div>
</div></div></section>

<section class="block"><div class="wrap">
<div class="band">
<div><h2>Try our apps before anyone else.</h2><p>Join the beta list for early builds of What's for Dinner? No spam, just invites.</p></div>
<a class="btn" href="/beta/">Join the beta</a>
</div></div></section>
"""
w('/', page('/', 'Spooled Up Studios | Independent app studio, New York',
 'Spooled Up Studios is an independent app development studio in New York. We build fast, useful apps, including What\'s for Dinner?. Join the beta.', home))

# ---------- Apps ----------
apps = """
<section class="page-head"><div class="wrap">
<p class="eyebrow">Apps</p><h1 style="font-size:clamp(36px,6vw,56px)">Our apps</h1>
<p class="lead">Everything we make, in one place.</p>
</div></section>

<section class="block" id="whats-for-dinner" style="border-top:0"><div class="wrap">
<span class="tag" style="display:inline-block;font-size:12px;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--amber);border:1px solid #4a3a1e;border-radius:999px;padding:4px 10px;margin-bottom:14px">In beta</span>
<h2>What's for Dinner?</h2>
<p class="prose" style="font-size:20px;margin-top:16px">Stop scrolling and just pick. Tap Spin and get one answer, in three modes.</p>
<div class="grid g3">
<div class="card"><div class="num">OUT</div><h3>A restaurant near you</h3><p>Choose walking or driving distance, pick the kinds of food you're in the mood for, hide the ones you aren't, and skip chains or places you've been.</p></div>
<div class="card"><div class="num">HOME</div><h3>A recipe to cook tonight</h3><p>A built-in library of 200+ original recipes. Scale servings, check off steps, run timers, and filter by pantry, budget and time.</p></div>
<div class="card"><div class="num">DO</div><h3>Something to do nearby</h3><p>Parks, trails, museums and, when you want them, events.</p></div>
</div>
<div class="grid g2" style="margin-top:34px">
<div class="card"><h3>Also in the app</h3>
<ul class="prose" style="margin:12px 0 0">
<li>Dietary and allergy filters</li><li>Pick together: 2 to 12 people vote</li><li>Shared dinners with invites and ratings</li><li>Weekly meal planner and shopping list</li><li>Directions in Apple Maps, Google Maps or Waze</li><li>Home screen widget on iPhone</li></ul></div>
<div class="card"><h3>Privacy first</h3>
<p>No account, no ads, no tracking, and nothing is sold. Your location is used only while the app is open, and your history and favorites stay on your phone.</p>
<p><a href="/privacy/">Read the privacy policy</a></p></div>
</div>

<h2 style="margin-top:64px">Get it</h2>
<div class="grid g3">
<div class="card"><h3>iPhone</h3><p>Now in beta on TestFlight. Join the list and we'll send your invite.</p><div class="cta" style="margin-top:18px"><a class="btn small" href="/beta/">Join the iPhone beta</a></div></div>
<div class="card"><h3>Android, Windows, Mac</h3><p>A web version that runs in any browser is coming. Join the list and we'll tell you the day it opens.</p><div class="cta" style="margin-top:18px"><a class="btn small" href="/beta/">Get notified</a></div></div>
<div class="card"><h3>Need help?</h3><p>Questions, bugs or ideas: we reply within two days.</p><div class="cta" style="margin-top:18px"><a class="btn small ghost" href="/support/">Support</a></div></div>
</div>
</div></section>
"""
w('/apps/', page('/apps/', "Apps | Spooled Up Studios", "What's for Dinner? by Spooled Up Studios: spin for a restaurant, a recipe or something to do. In beta on iPhone.", apps, '/apps/'))

# ---------- About ----------
about = """
<section class="page-head"><div class="wrap">
<p class="eyebrow">About</p><h1 style="font-size:clamp(36px,6vw,56px)">Spooled up: ready to go.</h1>
<p class="lead">Spooled Up Studios is an independent app development studio based in New York.</p>
</div></section>
<section class="block" style="border-top:0"><div class="wrap"><div class="prose">
<p>We design and build apps that are fast, useful, and ready the moment you need them, then keep improving them long after launch. Our work spans consumer apps, tools for shops and small businesses, and products with roots in aviation: industries where things have to work the first time.</p>
<h2>The name</h2>
<p>When a jet engine spools up, the turbine comes up to full power and the aircraft is ready to go. It also means exactly what it sounds like: fired up and ready. That's the standard for everything we ship.</p>
<h2>At a glance</h2>
<dl class="facts">
<dt>Company</dt><dd>Spooled Up Studios LLC</dd>
<dt>Based in</dt><dd>New York, USA</dd>
<dt>Founded</dt><dd>2026</dd>
<dt>Focus</dt><dd>Consumer apps, tools for small businesses, aviation</dd>
<dt>Contact</dt><dd><a href="mailto:info@spooledupstudios.com">info@spooledupstudios.com</a></dd>
</dl>
<h2>What we stand for</h2>
<ul><li><strong>Full power, every time.</strong> We don't ship half-done.</li><li><strong>Built to move.</strong> Fast to load, fast to use, fast to improve.</li><li><strong>Made for everywhere.</strong> Global from the first release.</li></ul>
<div class="cta" style="margin-top:34px"><a class="btn" href="/apps/">See our apps</a><a class="btn ghost" href="/contact/">Get in touch</a></div>
</div></div></section>
"""
w('/about/', page('/about/', 'About | Spooled Up Studios', 'Spooled Up Studios is an independent app studio in New York, building fast, useful apps for consumers, small businesses and aviation.', about, '/about/'))

# ---------- Contact ----------
contact = """
<section class="page-head"><div class="wrap">
<p class="eyebrow">Contact</p><h1 style="font-size:clamp(36px,6vw,56px)">Get in touch</h1>
<p class="lead">We read everything. Email is the fastest way to reach us.</p>
</div></section>
<section class="block" style="border-top:0"><div class="wrap">
<div class="grid g3" style="margin-top:0">
<div class="card"><h3>General</h3><p>Partnerships, press and custom app work.</p><p><a href="mailto:info@spooledupstudios.com">info@spooledupstudios.com</a></p></div>
<div class="card"><h3>Support</h3><p>Help with What's for Dinner?. We reply within two days.</p><p><a href="mailto:support@spooledupstudios.com">support@spooledupstudios.com</a></p><p><a href="/support/">Support page</a></p></div>
<div class="card"><h3>Feedback</h3><p>Ideas, bugs and things you'd change.</p><p><a href="mailto:feedback@spooledupstudios.com">feedback@spooledupstudios.com</a></p></div>
</div>
<div class="prose">
<h2>Press</h2>
<p><strong>About Spooled Up Studios.</strong> Spooled Up Studios LLC is an independent app development studio based in New York. Founded in 2026, the studio designs and builds apps for consumers, small businesses, and aviation, with a focus on speed, reliability, and products that are ready from day one. Learn more at spooledupstudios.com.</p>
<p>Logos and brand files are available on request.</p>
</div>
</div></section>
"""
w('/contact/', page('/contact/', 'Contact | Spooled Up Studios', 'Contact Spooled Up Studios: general, support and feedback email addresses, plus press information.', contact, '/contact/'))

# ---------- Beta ----------
beta = """
<section class="page-head"><div class="wrap">
<p class="eyebrow">Beta</p><h1 style="font-size:clamp(36px,6vw,56px)">Join the beta</h1>
<p class="lead">Get early builds of What's for Dinner? and tell us what to fix. iPhone testers get a TestFlight invite. On Android or a computer? Join too, and we'll tell you when the web version opens.</p>
</div></section>
<section class="block" style="border-top:0"><div class="wrap">
<div id="done" class="ok" role="status" hidden><strong>You're on the list.</strong> We'll email your invite soon.</div>
<div id="fail" class="err" role="alert" hidden>Something went wrong. Please email <a href="mailto:info@spooledupstudios.com">info@spooledupstudios.com</a> and we'll add you by hand.</div>
<form class="beta" id="betaForm" novalidate>
<label>Name<input name="name" type="text" autocomplete="name" required maxlength="80"></label>
<label>Email<input name="email" type="email" autocomplete="email" required maxlength="120" inputmode="email"></label>
<label>Your device<select name="device" required>
<option value="">Choose one</option><option>iPhone</option><option>Android phone</option><option>Windows or Mac computer</option><option>Other</option></select></label>
<label>Anything you'd like us to know? <small>Optional</small><textarea name="note" rows="3" maxlength="400"></textarea></label>
<div class="hp" aria-hidden="true"><label>Leave empty<input name="website" tabindex="-1" autocomplete="off"></label></div>
<div><button class="btn" type="submit" id="send">Join the beta</button></div>
<p class="note">We use your name and email only to send beta invites and updates about our apps. Reply to any email to be removed. See the <a href="/privacy/">privacy policy</a>.</p>
</form>
</div></section>
<script>
(function(){
var ENDPOINT = "__ENDPOINT__";
var f=document.getElementById('betaForm'),ok=document.getElementById('done'),bad=document.getElementById('fail'),b=document.getElementById('send');
f.addEventListener('submit',function(e){
  e.preventDefault(); bad.hidden=true;
  var d=Object.fromEntries(new FormData(f).entries());
  if(d.website) return;
  if(!d.name.trim()||!/^\\S+@\\S+\\.\\S+$/.test(d.email)||!d.device){bad.textContent='Please fill in your name, a valid email and your device.';bad.hidden=false;return;}
  b.disabled=true;
  if(!ENDPOINT){
    var body='Name: '+d.name+'\\nEmail: '+d.email+'\\nDevice: '+d.device+'\\nNote: '+(d.note||'');
    location.href='mailto:info@spooledupstudios.com?subject='+encodeURIComponent('Beta sign-up')+'&body='+encodeURIComponent(body);
    f.hidden=true; ok.hidden=false; return;
  }
  fetch(ENDPOINT,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:d.name,email:d.email,device:d.device,note:d.note||''})})
   .then(function(r){if(!r.ok)throw 0;f.hidden=true;ok.hidden=false;})
   .catch(function(){b.disabled=false;bad.hidden=false;});
});
})();
</script>
""".replace('__ENDPOINT__', BETA_ENDPOINT)
w('/beta/', page('/beta/', 'Join the beta | Spooled Up Studios', "Join the What's for Dinner? beta. Get a TestFlight invite for iPhone, or be first to know when the web version opens.", beta))

# ---------- Terms ----------
terms = """
<section class="page-head"><div class="wrap">
<p class="eyebrow">Legal</p><h1 style="font-size:clamp(36px,6vw,56px)">Terms of use</h1>
<p class="note">Last updated October 2026</p>
</div></section>
<section class="block" style="border-top:0"><div class="wrap"><div class="prose">
<p>These terms cover this website and Spooled Up Studios apps, including What's for Dinner? on iPhone and on the web. By using them you agree to these terms.</p>
<h2>Using our apps</h2>
<p>Use the apps lawfully and fairly. Don't misuse them, try to break them, or post content that is illegal, hateful or harassing. We may remove content or limit access to protect other people.</p>
<h2>Information may be wrong</h2>
<p>Restaurant, place and recipe information comes from third parties and may be out of date. Dietary and allergy filters are a best guess. Always check labels and ask the restaurant. Opening hours, prices and distances are estimates.</p>
<h2>Beta software</h2>
<p>Beta builds may have bugs and may change or stop at any time. Please report problems to <a href="mailto:feedback@spooledupstudios.com">feedback@spooledupstudios.com</a>.</p>
<h2>Our content</h2>
<p>The apps, name, logo and site are owned by Spooled Up Studios LLC. You may not copy or resell them without permission. Third-party names and data belong to their owners.</p>
<h2>No warranty and limits</h2>
<p>The apps and site are provided as is, without warranties. To the extent the law allows, Spooled Up Studios LLC is not liable for losses from using them, including decisions based on information shown.</p>
<h2>Privacy</h2>
<p>How we handle data is described in the <a href="/privacy/">privacy policy</a>.</p>
<h2>Changes and contact</h2>
<p>We may update these terms and will change the date above. Questions: <a href="mailto:info@spooledupstudios.com">info@spooledupstudios.com</a>.</p>
</div></div></section>
"""
w('/terms/', page('/terms/', 'Terms of use | Spooled Up Studios', 'Terms of use for the Spooled Up Studios website and apps.', terms))

# ---------- 404 ----------
nf = """<section class="hero"><div class="wrap"><p class="eyebrow">404</p><h1>Off course.</h1><p class="lead">That page doesn't exist. Head back to the start.</p><div class="cta"><a class="btn" href="/">Home</a><a class="btn ghost" href="/apps/">Apps</a></div></div></section>"""
open('404.html','w',encoding='utf-8').write(page('/404.html','Page not found | Spooled Up Studios','Page not found.',nf))

# ---------- robots + sitemap ----------
open('robots.txt','w').write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
urls = ['/','/apps/','/about/','/contact/','/beta/','/support/','/privacy/','/terms/']
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{SITE}{u}</loc></url>\n' for u in urls) + '</urlset>\n')
print('built')
