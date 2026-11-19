/* Clinica Neveen — interactions, language switching & motion */
(function () {
  'use strict';
  var doc = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var store = {
    get: function (k) { try { return localStorage.getItem(k); } catch (e) { return null; } },
    set: function (k, v) { try { localStorage.setItem(k, v); } catch (e) {} },
    sget: function (k) { try { return sessionStorage.getItem(k); } catch (e) { return null; } },
    sset: function (k, v) { try { sessionStorage.setItem(k, v); } catch (e) {} }
  };
  var WA = '962798253922';
  var WA_TEXT = {
    en: 'Hello Clinica Neveen, I would like to book an appointment.',
    ar: 'مرحباً عيادة الدكتورة نيفين، أرغب بحجز موعد.'
  };

  /* ---------------- i18n ---------------- */
  var lang = doc.getAttribute('lang') === 'ar' ? 'ar' : 'en';
  var i18nEls = [];
  function captureI18n() {
    i18nEls = Array.prototype.slice.call(document.querySelectorAll('[data-ar],[data-ar-placeholder],[data-ar-aria],[data-ar-value]'));
    i18nEls.forEach(function (el) {
      if (el.hasAttribute('data-ar') && !el.hasAttribute('data-en')) el.setAttribute('data-en', el.innerHTML);
      if (el.hasAttribute('data-ar-placeholder')) el.setAttribute('data-en-placeholder', el.getAttribute('placeholder') || '');
      if (el.hasAttribute('data-ar-aria')) el.setAttribute('data-en-aria', el.getAttribute('aria-label') || '');
      if (el.hasAttribute('data-ar-value')) el.setAttribute('data-en-value', el.getAttribute('value') || '');
    });
  }
  function applyLang(l) {
    lang = l;
    doc.setAttribute('lang', l);
    doc.setAttribute('dir', l === 'ar' ? 'rtl' : 'ltr');
    i18nEls.forEach(function (el) {
      if (el.hasAttribute('data-ar')) el.innerHTML = el.getAttribute('data-' + l);
      if (el.hasAttribute('data-ar-placeholder')) el.setAttribute('placeholder', el.getAttribute('data-' + l + '-placeholder'));
      if (el.hasAttribute('data-ar-aria')) el.setAttribute('aria-label', el.getAttribute('data-' + l + '-aria'));
      if (el.hasAttribute('data-ar-value')) el.setAttribute('value', el.getAttribute('data-' + l + '-value'));
    });
    document.querySelectorAll('.lang-toggle').forEach(function (b) {
      b.textContent = l === 'ar' ? 'EN' : 'عربي';
      b.setAttribute('aria-label', l === 'ar' ? 'Switch to English' : 'التحويل إلى العربية');
    });
    document.querySelectorAll('.wa-link').forEach(function (a) {
      a.href = 'https://wa.me/' + WA + '?text=' + encodeURIComponent(WA_TEXT[l]);
    });
    var langField = document.querySelector('input[name="Language"]');
    if (langField) langField.value = l === 'ar' ? 'Arabic' : 'English';
    splitAll();
    updateHours();
    store.set('cn-lang', l);
    doc.classList.remove('ar-pending');
  }

  /* ---------------- split words ---------------- */
  function splitNode(node, counter) {
    Array.prototype.slice.call(node.childNodes).forEach(function (n) {
      if (n.nodeType === 3) {
        var parts = n.textContent.split(/(\s+)/);
        var frag = document.createDocumentFragment();
        parts.forEach(function (p) {
          if (!p) return;
          if (/^\s+$/.test(p)) { frag.appendChild(document.createTextNode(' ')); return; }
          var w = document.createElement('span'); w.className = 'w';
          var i = document.createElement('span'); i.textContent = p; i.style.setProperty('--i', counter.n++);
          w.appendChild(i); frag.appendChild(w);
        });
        n.parentNode.replaceChild(frag, n);
      } else if (n.nodeType === 1 && n.tagName !== 'BR') {
        splitNode(n, counter);
      }
    });
  }
  function splitAll() {
    if (reduce) return;
    document.querySelectorAll('.split-words').forEach(function (el) {
      if (!el.hasAttribute('data-src')) el.setAttribute('data-src', el.innerHTML);
      if (el.hasAttribute('data-ar')) el.setAttribute('data-src', el.innerHTML);
      el.innerHTML = el.getAttribute('data-src');
      splitNode(el, { n: 0 });
    });
  }

  /* ---------------- reveal on scroll ---------------- */
  function initReveal() {
    var els = document.querySelectorAll('.reveal,.reveal-fade,.reveal-mask,.reveal-line,.split-words,.stagger,[data-count]');
    if (!('IntersectionObserver' in window) || reduce) {
      els.forEach(function (e) { e.classList.add('in'); if (e.hasAttribute('data-count')) countUp(e); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          en.target.classList.add('in');
          if (en.target.hasAttribute('data-count')) countUp(en.target);
          io.unobserve(en.target);
        }
      });
    }, { threshold: 0.14, rootMargin: '0px 0px -6% 0px' });
    els.forEach(function (e) { io.observe(e); });
  }
  function countUp(el) {
    if (el.dataset.done) return; el.dataset.done = 1;
    var end = parseFloat(el.getAttribute('data-count')), dur = 1900, t0 = null;
    if (reduce) { el.textContent = end; return; }
    function step(t) {
      if (!t0) t0 = t;
      var p = Math.min((t - t0) / dur, 1), e = 1 - Math.pow(1 - p, 4);
      el.textContent = Math.round(end * e);
      if (p < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  /* ---------------- smooth scroll + parallax ---------------- */
  var lenis = null;
  function initScroll() {
    if (!reduce && window.Lenis) {
      lenis = new window.Lenis({ duration: 1.25, easing: function (t) { return Math.min(1, 1.001 - Math.pow(2, -10 * t)); }, smoothWheel: true });
      function raf(t) { lenis.raf(t); requestAnimationFrame(raf); }
      requestAnimationFrame(raf);
      document.querySelectorAll('a[href^="#"]').forEach(function (a) {
        a.addEventListener('click', function (e) {
          var id = a.getAttribute('href'); if (id.length < 2) return;
          var t = document.querySelector(id); if (!t) return;
          e.preventDefault(); lenis.scrollTo(t, { offset: -110 });
        });
      });
    }
    var px = Array.prototype.slice.call(document.querySelectorAll('[data-parallax]'));
    var header = document.querySelector('.site-header');
    var toTop = document.querySelector('.to-top');
    var lastY = 0, ticking = false;
    function onScroll() {
      var y = window.scrollY || window.pageYOffset;
      if (header) {
        header.classList.toggle('scrolled', y > 30);
        header.classList.toggle('hide', y > 500 && y > lastY + 4 && !doc.classList.contains('menu-open'));
        if (y < lastY - 4) header.classList.remove('hide');
      }
      if (toTop) toTop.classList.toggle('show', y > 900);
      if (!reduce) {
        var vh = window.innerHeight;
        px.forEach(function (el) {
          var r = el.parentElement.getBoundingClientRect();
          if (r.bottom < -200 || r.top > vh + 200) return;
          var s = parseFloat(el.getAttribute('data-parallax')) || 0.15;
          var off = (r.top + r.height / 2 - vh / 2) * -s;
          el.style.transform = 'translate3d(0,' + off.toFixed(1) + 'px,0)';
        });
      }
      lastY = y; ticking = false;
    }
    window.addEventListener('scroll', function () { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
    window.addEventListener('resize', onScroll);
    onScroll();
    if (toTop) toTop.addEventListener('click', function () { lenis ? lenis.scrollTo(0) : window.scrollTo({ top: 0, behavior: 'smooth' }); });
  }

  /* ---------------- menu ---------------- */
  function initMenu() {
    var btn = document.querySelector('.burger');
    if (!btn) return;
    function close() { doc.classList.remove('menu-open'); btn.setAttribute('aria-expanded', 'false'); if (lenis) lenis.start(); }
    btn.addEventListener('click', function () {
      var open = doc.classList.toggle('menu-open');
      btn.setAttribute('aria-expanded', open ? 'true' : 'false');
      if (lenis) open ? lenis.stop() : lenis.start();
    });
    document.addEventListener('keydown', function (e) { if (e.key === 'Escape') close(); });
    document.querySelectorAll('.menu-overlay a').forEach(function (a) { a.addEventListener('click', close); });
  }

  /* ---------------- page transitions ---------------- */
  function initTransitions() {
    var curtain = document.querySelector('.page-curtain');
    if (!curtain || reduce) return;
    if (store.sget('cn-nav')) {
      curtain.style.transition = 'none'; curtain.classList.add('on');
      requestAnimationFrame(function () { requestAnimationFrame(function () {
        curtain.style.transition = ''; curtain.classList.remove('on');
      }); });
    }
    document.addEventListener('click', function (e) {
      var a = e.target.closest && e.target.closest('a');
      if (!a || a.target === '_blank' || e.metaKey || e.ctrlKey || e.shiftKey) return;
      var href = a.getAttribute('href') || '';
      if (!/\.html(\?|#|$)/.test(href) || /^https?:/.test(href)) return;
      e.preventDefault();
      store.sset('cn-nav', '1');
      curtain.classList.add('on');
      setTimeout(function () { window.location.href = href; }, 520);
    });
    window.addEventListener('pageshow', function (ev) { if (ev.persisted) curtain.classList.remove('on'); });
  }

  /* ---------------- preloader ---------------- */
  function initPreloader() {
    var pre = document.querySelector('.preloader');
    if (!pre || doc.classList.contains('no-preload')) return;
    store.sset('cn-seen', '1');
    var t = reduce ? 0 : 1500;
    setTimeout(function () { pre.classList.add('done'); setTimeout(function () { pre.remove(); }, 1200); }, t);
  }

  /* ---------------- before / after ---------------- */
  function initBA() {
    document.querySelectorAll('.ba').forEach(function (ba) {
      var r = ba.querySelector('input[type=range]');
      if (!r) return;
      function set() { ba.style.setProperty('--pos', r.value + '%'); }
      r.addEventListener('input', set); set();
    });
    var chips = document.querySelectorAll('.chip[data-filter]');
    chips.forEach(function (c) {
      c.addEventListener('click', function () {
        chips.forEach(function (x) { x.classList.remove('active'); x.setAttribute('aria-pressed', 'false'); });
        c.classList.add('active'); c.setAttribute('aria-pressed', 'true');
        var f = c.getAttribute('data-filter');
        document.querySelectorAll('.ba-card[data-cat]').forEach(function (card) {
          var show = f === 'all' || card.getAttribute('data-cat') === f;
          card.classList.toggle('is-hidden', !show);
        });
        if (lenis) lenis.resize();
      });
    });
  }

  /* ---------------- FAQ accordion ---------------- */
  function initFAQ() {
    document.querySelectorAll('details.acc').forEach(function (d) {
      var s = d.querySelector('summary'), b = d.querySelector('.body');
      s.addEventListener('click', function (e) {
        if (reduce || !b.animate) return;
        e.preventDefault();
        if (d.open) {
          var h = b.offsetHeight;
          b.animate([{ height: h + 'px', opacity: 1 }, { height: '0px', opacity: 0 }], { duration: 450, easing: 'cubic-bezier(.22,1,.36,1)' })
            .onfinish = function () { d.open = false; if (lenis) lenis.resize(); };
        } else {
          d.open = true;
          var h2 = b.offsetHeight;
          b.animate([{ height: '0px', opacity: 0 }, { height: h2 + 'px', opacity: 1 }], { duration: 550, easing: 'cubic-bezier(.22,1,.36,1)' })
            .onfinish = function () { if (lenis) lenis.resize(); };
        }
      });
    });
  }

  /* ---------------- sticky sub-nav active state ---------------- */
  function initSubNav() {
    var links = document.querySelectorAll('[data-subnav] a[href^="#"]');
    if (!links.length || !('IntersectionObserver' in window)) return;
    var map = {};
    links.forEach(function (a) { map[a.getAttribute('href').slice(1)] = a; });
    var io = new IntersectionObserver(function (en) {
      en.forEach(function (x) {
        if (x.isIntersecting) {
          links.forEach(function (a) { a.classList.remove('active'); });
          var a = map[x.target.id]; if (a) a.classList.add('active');
        }
      });
    }, { rootMargin: '-40% 0px -55% 0px' });
    Object.keys(map).forEach(function (id) { var s = document.getElementById(id); if (s) io.observe(s); });
  }

  /* ---------------- working hours ---------------- */
  var DAYS = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  function ammanNow() {
    try {
      var parts = new Intl.DateTimeFormat('en-US', { timeZone: 'Asia/Amman', weekday: 'short', hour: 'numeric', minute: 'numeric', hour12: false }).formatToParts(new Date());
      var o = {}; parts.forEach(function (p) { o[p.type] = p.value; });
      return { day: o.weekday, mins: (parseInt(o.hour, 10) % 24) * 60 + parseInt(o.minute, 10) };
    } catch (e) { var d = new Date(); return { day: DAYS[d.getDay()], mins: d.getHours() * 60 + d.getMinutes() }; }
  }
  function updateHours() {
    var now = ammanNow();
    var open = now.mins >= 600 && now.mins < 1140; // 10:00 – 19:00 daily
    document.querySelectorAll('.hours-table .r').forEach(function (r) {
      r.classList.toggle('today', r.getAttribute('data-day') === now.day);
      var d = r.querySelector('.d'); if (d) d.setAttribute('data-today', lang === 'ar' ? 'اليوم' : 'Today');
    });
    document.querySelectorAll('[data-status]').forEach(function (p) {
      p.classList.toggle('open', open); p.classList.toggle('closed', !open);
      var txt = p.querySelector('span');
      if (!txt) return;
      if (open) txt.textContent = lang === 'ar' ? 'مفتوح الآن · يغلق الساعة 7 مساءً' : 'Open now · Closes at 7 PM';
      else txt.textContent = lang === 'ar' ? 'مغلق الآن · نفتح الساعة 10 صباحاً' : 'Closed now · Opens at 10 AM';
    });
  }

  /* ---------------- booking form ---------------- */
  function initForm() {
    var form = document.querySelector('#booking-form');
    if (!form) return;
    var params = new URLSearchParams(location.search);
    var svc = params.get('service'), sel = form.querySelector('select[name="Treatment"]');
    if (svc && sel) {
      Array.prototype.forEach.call(sel.options, function (o) { if (o.getAttribute('data-key') === svc) o.selected = true; });
    }
    var date = form.querySelector('input[type=date]');
    if (date) {
      var t = new Date(); var iso = new Date(t.getTime() - t.getTimezoneOffset() * 60000).toISOString().slice(0, 10);
      date.min = iso;
    }
    var next = form.querySelector('input[name="_next"]');
    if (next) next.value = new URL('thank-you.html', location.href).href;

    var MSG = {
      en: { req: 'This field is required.', phone: 'Please enter a valid phone number.', email: 'Please enter a valid email address.', consent: 'Please agree to the privacy policy to continue.', sending: 'Sending…' },
      ar: { req: 'هذا الحقل مطلوب.', phone: 'يرجى إدخال رقم هاتف صحيح.', email: 'يرجى إدخال بريد إلكتروني صحيح.', consent: 'يرجى الموافقة على سياسة الخصوصية للمتابعة.', sending: 'جارٍ الإرسال…' }
    };
    function check(field) {
      var input = field.querySelector('input,select,textarea'); if (!input) return true;
      var err = field.querySelector('.err'), m = MSG[lang], msg = '';
      var v = (input.type === 'checkbox') ? input.checked : (input.value || '').trim();
      if (input.required && !v) msg = input.type === 'checkbox' ? m.consent : m.req;
      else if (input.type === 'tel' && v && !/^[+\d][\d\s\-()]{7,}$/.test(v)) msg = m.phone;
      else if (input.type === 'email' && v && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v)) msg = m.email;
      field.classList.toggle('invalid', !!msg);
      if (err) err.textContent = msg;
      return !msg;
    }
    var fields = form.querySelectorAll('.field');
    fields.forEach(function (f) {
      var i = f.querySelector('input,select,textarea'); if (!i) return;
      i.addEventListener('blur', function () { if (f.classList.contains('invalid')) check(f); });
      i.addEventListener('change', function () { if (f.classList.contains('invalid')) check(f); });
    });
    form.addEventListener('submit', function (e) {
      var ok = true, first = null;
      fields.forEach(function (f) { if (!check(f)) { ok = false; if (!first) first = f; } });
      if (!ok) {
        e.preventDefault();
        if (lenis) lenis.scrollTo(first, { offset: -140 }); else first.scrollIntoView({ behavior: 'smooth', block: 'center' });
        var fi = first.querySelector('input,select,textarea'); if (fi) setTimeout(function () { fi.focus({ preventScroll: true }); }, 600);
        return;
      }
      var reply = form.querySelector('input[name="_replyto"]'), em = form.querySelector('input[name="email"]');
      if (reply && em) reply.value = em.value;
      var subj = form.querySelector('input[name="_subject"]'), nm = form.querySelector('input[name="Name"]');
      if (subj && nm) subj.value = 'New Booking Request – ' + nm.value.trim() + ' – Clinica Neveen';
      var btn = form.querySelector('button[type=submit]');
      if (btn) { btn.disabled = true; var l = btn.querySelector('.lbl'); if (l) l.textContent = MSG[lang].sending; }
    });
  }

  /* ---------------- year ---------------- */
  function initYear() { document.querySelectorAll('[data-year]').forEach(function (y) { y.textContent = new Date().getFullYear(); }); }

  /* ---------------- boot ---------------- */
  function boot() {
    doc.classList.add('js');
    captureI18n();
    var params = new URLSearchParams(location.search);
    var start = params.get('lang') || store.get('cn-lang') || 'en';
    applyLang(start === 'ar' ? 'ar' : 'en');
    document.querySelectorAll('.lang-toggle').forEach(function (b) {
      b.addEventListener('click', function () {
        doc.classList.add('lang-switching');
        applyLang(lang === 'ar' ? 'en' : 'ar');
        document.querySelectorAll('.split-words').forEach(function (el) {
          var r = el.getBoundingClientRect();
          if (r.top < window.innerHeight) el.classList.add('in');
        });
        if (lenis) lenis.resize();
      });
    });
    initYear();
    initPreloader();
    initTransitions();
    initScroll();
    initMenu();
    initReveal();
    initBA();
    initFAQ();
    initSubNav();
    initForm();
    setInterval(updateHours, 60000);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot); else boot();
})();
