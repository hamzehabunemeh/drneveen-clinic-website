#!/usr/bin/env python3
"""Static site generator for Clinica Neveen. Run: python3 build.py <out_dir>"""
import html, sys, os

OUT = sys.argv[1] if len(sys.argv) > 1 else '../site'

def A(s):
    return html.escape(s, quote=True)

def T(en, ar, tag='span', cls='', attrs=''):
    c = f' class="{cls}"' if cls else ''
    a = f' {attrs}' if attrs else ''
    return f'<{tag}{c}{a} data-ar="{A(ar)}">{en}</{tag}>'

# ---------------------------------------------------------------- data
WA = '962798253922'
EMAIL = 'emadnivo@gmail.com'
MAPS = 'https://maps.app.goo.gl/aVE4g5ssPNjE4Hw29?g_st=ic'
MAP_EMBED = 'https://www.google.com/maps?q=' + 'Dr.+Neveen+Dababneh+Clinic,+7th+Circle,+Amman,+Jordan' + '&output=embed'
PHONES = [
    ('0798253922', '+962798253922', 'Mobile · WhatsApp', 'موبايل · واتساب'),
    ('0790163122', '+962790163122', 'Mobile', 'موبايل'),
    ('0776656767', '+962776656767', 'Mobile', 'موبايل'),
    ('06 582 6665', '+96265826665', 'Landline', 'أرضي'),
]
ADDR_EN = 'Behind Royal Jordanian Airlines building, next to Greater Amman restaurants, opposite Al Sarawat Restaurant — 7th Circle, Amman, Jordan'
ADDR_AR = 'خلف مبنى الملكية الأردنية للطيران، بجانب مطاعم عمّان الكبرى، مقابل مطعم السروات — الدوار السابع، عمّان، الأردن'
SOCIALS = [
    ('instagram', 'Instagram', '@clinicaneveen', 'https://www.instagram.com/clinicaneveen/'),
    ('tiktok', 'TikTok', '@clinicaneveen', 'https://www.tiktok.com/@clinicaneveen'),
    ('snapchat', 'Snapchat', '@clinicaneveen', 'https://www.snapchat.com/@clinicaneveen'),
    ('facebook', 'Facebook', '/clinicaneveen', 'https://www.facebook.com/clinicaneveen/'),
    ('threads', 'Threads', '@clinicaneveen', 'https://www.threads.com/@clinicaneveen'),
]

ICONS = {
 'syringe': '<path d="M18 2l4 4M17 3l4 4M19.5 4.5L14 10M6 18l-4 4M14.5 3.5l6 6M8.5 9.5l6 6M12 6l6 6-8 8H6v-4z"/><path d="M9 13l2 2M11 11l2 2"/>',
 'face': '<path d="M12 3c-4.2 0-7 3.2-7 7.5 0 3.3 1.6 6.4 3.6 8.4 1 1 2.2 2.1 3.4 2.1s2.4-1.1 3.4-2.1c2-2 3.6-5.1 3.6-8.4C19 6.2 16.2 3 12 3z"/><path d="M9 10.5h.01M15 10.5h.01M9.5 15.5c1.4 1 3.6 1 5 0"/>',
 'jaw': '<path d="M5 6c0 6 2.5 11 7 14 4.5-3 7-8 7-14"/><path d="M5 6c2-2 4.5-3 7-3s5 1 7 3"/><path d="M8 13l4 3 4-3"/>',
 'lift': '<path d="M12 21V8M7 12l5-5 5 5"/><path d="M5 3h14"/>',
 'eye': '<path d="M2 12s3.6-6 10-6 10 6 10 6-3.6 6-10 6S2 12 2 12z"/><circle cx="12" cy="12" r="2.6"/><path d="M6 19c2 1.2 4 1.6 6 1.6s4-.4 6-1.6"/>',
 'balance': '<path d="M12 3v18M5 7h14M5 7l-3 7a3.5 3.5 0 006 0zM19 7l-3 7a3.5 3.5 0 006 0z"/>',
 'smile': '<circle cx="12" cy="12" r="9"/><path d="M7.5 13.5c1 2 2.7 3 4.5 3s3.5-1 4.5-3"/><path d="M8.5 13.8h7"/>',
 'laser': '<path d="M3 21l7-7"/><path d="M10 14l3-3 4 4-3 3z"/><path d="M17 3v3M21 7h-3M19.6 4.4l-2 2"/>',
 'vein': '<path d="M7 21c0-5 2-6 2-10s-2-5-2-8M13 21c0-4-3-6-3-9M17 21c0-6-2-7-2-11s1-5 2-7"/>',
 'sparkle': '<path d="M12 3l1.8 4.6L18.5 9l-4.7 1.6L12 15l-1.8-4.4L5.5 9l4.7-1.4z"/><path d="M19 15l.8 2 2 .8-2 .8-.8 2-.8-2-2-.8 2-.8zM5 15l.6 1.4 1.4.6-1.4.6L5 19l-.6-1.4L3 17l1.4-.6z"/>',
 'drop': '<path d="M12 3s6 6.4 6 10.5A6 6 0 016 13.5C6 9.4 12 3 12 3z"/><path d="M9.5 14a2.5 2.5 0 002.5 2.5"/>',
 'dot': '<circle cx="12" cy="12" r="9"/><circle cx="9" cy="10" r="1.6"/><circle cx="15" cy="14" r="1.1"/><circle cx="14" cy="8.5" r=".7"/>',
 'scissors': '<circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4L8.1 15.9M14.5 14.5L20 20M8.1 8.1L12 12"/>',
 'stethoscope': '<path d="M5 3v5a5 5 0 0010 0V3"/><path d="M10 13v2a5 5 0 0010 0v-2"/><circle cx="20" cy="11" r="2"/>',
 'hair': '<path d="M4 20c0-9 3.5-16 8-16s8 7 8 16"/><path d="M9 20c0-6 1-11 3-11s3 5 3 11"/>',
 'leaf': '<path d="M5 19c8 0 14-6 14-15-9 0-15 6-15 14 0 .4 0 .7.1 1z"/><path d="M5 19C9 15 12 12 15 8"/>',
 'hand': '<path d="M8 13V5.5a1.5 1.5 0 013 0V12M11 11V4a1.5 1.5 0 013 0v7M14 11V5.5a1.5 1.5 0 013 0V13M17 9.5a1.5 1.5 0 013 0V15a7 7 0 01-7 7h-1a7 7 0 01-5.9-3.2L3.5 14a1.6 1.6 0 012.6-1.8L8 14"/>',
 'shield': '<path d="M12 3l8 3v6c0 5-3.4 8.4-8 9-4.6-.6-8-4-8-9V6z"/><path d="M8.5 12l2.5 2.5 4.5-5"/>',
 'clock': '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
 'pin': '<path d="M12 21s-7-6.2-7-11.5A7 7 0 0119 9.5C19 14.8 12 21 12 21z"/><circle cx="12" cy="9.5" r="2.5"/>',
 'phone': '<path d="M5 3h3.5l2 5-2.5 1.5a11 11 0 006 6L15.5 13l5 2V18.5A2.5 2.5 0 0118 21 15 15 0 013 6a2.5 2.5 0 012-3z"/>',
 'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/>',
 'calendar': '<rect x="3" y="5" width="18" height="16" rx="2"/><path d="M3 10h18M8 3v4M16 3v4"/>',
 'moon': '<path d="M20 14.5A8 8 0 019.5 4a8 8 0 1010.5 10.5z"/>',
 'star': '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
 'arrow': '<path d="M4 12h16M14 6l6 6-6 6"/>',
 'up': '<path d="M12 20V4M6 10l6-6 6 6"/>',
 'image': '<rect x="3" y="4" width="18" height="16" rx="2"/><circle cx="9" cy="10" r="2"/><path d="M21 16l-5-5-9 9"/>',
 'chat': '<path d="M21 12a8 8 0 01-11.8 7L4 20l1.1-4.6A8 8 0 1121 12z"/>',
 'heart': '<path d="M12 20s-7.5-4.5-7.5-10A4.3 4.3 0 0112 7.3 4.3 4.3 0 0119.5 10c0 5.5-7.5 10-7.5 10z"/>',
}
def icon(name, sw='1.4'):
    return f'<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

BRAND = {
 'whatsapp': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M17.5 14.4c-.3-.1-1.7-.8-2-.9-.3-.1-.5-.1-.7.1-.2.3-.8.9-.9 1.1-.2.2-.3.2-.6.1-.3-.1-1.2-.5-2.3-1.4-.9-.8-1.4-1.7-1.6-2-.2-.3 0-.5.1-.6l.4-.5c.2-.2.2-.3.3-.5.1-.2 0-.4 0-.5l-.9-2.2c-.2-.6-.5-.5-.7-.5h-.6c-.2 0-.5.1-.8.4-.3.3-1 1-1 2.4s1 2.8 1.2 3c.1.2 2 3.1 4.9 4.3.7.3 1.2.5 1.7.6.7.2 1.3.2 1.8.1.6-.1 1.7-.7 1.9-1.4.2-.7.2-1.2.2-1.4-.1-.1-.3-.2-.6-.3zM12 21.8c-1.8 0-3.5-.5-5-1.4l-.4-.2-3.7 1 1-3.6-.2-.4C2.7 15.6 2.2 13.8 2.2 12 2.2 6.6 6.6 2.2 12 2.2c2.6 0 5.1 1 6.9 2.9 1.8 1.8 2.9 4.3 2.9 6.9 0 5.4-4.4 9.8-9.8 9.8zm8.4-18.2C18.2 1.3 15.2 0 12 0 5.4 0 0 5.4 0 12c0 2.1.6 4.2 1.6 6L0 24l6.2-1.6c1.8 1 3.8 1.5 5.8 1.5 6.6 0 12-5.4 12-12 0-3.2-1.2-6.2-3.6-8.3z"/></svg>',
 'instagram': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5"/><circle cx="12" cy="12" r="4.2"/><circle cx="17.4" cy="6.6" r=".9" fill="currentColor" stroke="none"/></svg>',
 'tiktok': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M16.6 2h-3.3v13.4a2.9 2.9 0 11-2.9-2.9c.3 0 .6 0 .9.1V9.2a6.3 6.3 0 106.3 6.3V8.7a8 8 0 004.4 1.4V6.8a4.6 4.6 0 01-4.4-4.8z"/></svg>',
 'snapchat': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round" aria-hidden="true"><path d="M12 2.8c3.3 0 5.3 2.5 5.3 5.6v2.4c.5.3 1.3.2 1.9-.1.5.4.3 1.1-.3 1.4-.7.4-1.7.6-1.8 1.2.3 1.6 1.9 3.3 3.7 3.9-.2.7-1.5 1-2.6 1.2-.2.5-.2 1.2-.5 1.4-.9.1-1.9-.3-3 .1-1 .4-1.6 1.4-2.7 1.4s-1.7-1-2.7-1.4c-1.1-.4-2.1 0-3-.1-.3-.2-.3-.9-.5-1.4-1.1-.2-2.4-.5-2.6-1.2 1.8-.6 3.4-2.3 3.7-3.9-.1-.6-1.1-.8-1.8-1.2-.6-.3-.8-1-.3-1.4.6.3 1.4.4 1.9.1V8.4c0-3.1 2-5.6 5.3-5.6z"/></svg>',
 'facebook': '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M13.5 22v-8.2h2.8l.4-3.2h-3.2V8.5c0-.9.3-1.6 1.6-1.6h1.7V4.1c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2.4H7.3v3.2h2.8V22z"/></svg>',
 'threads': '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" aria-hidden="true"><path d="M17.5 7.5C16.4 4.9 14.4 3.5 12 3.5c-4.4 0-7.5 3.4-7.5 8.5s3.1 8.5 7.5 8.5c3.7 0 6.5-2.3 6.5-5.4 0-2.9-2.4-4.6-5.6-4.6-2.4 0-4 1.2-4 2.9 0 1.6 1.3 2.6 3 2.6 2.5 0 3.8-1.9 3.8-5.3"/></svg>',
}

BUTTERFLY = ('<svg viewBox="0 0 100 100" aria-hidden="true"><defs><linearGradient id="bg{i}" x1="0" y1="0" x2="1" y2="1">'
  '<stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/></linearGradient></defs>'
  '<g class="wing"><path d="M50 52 C 38 20, 10 14, 14 40 C 17 56, 38 60, 50 52 Z" fill="url(#bg{i})"/>'
  '<path d="M50 54 C 40 62, 22 78, 32 84 C 42 88, 50 72, 50 54 Z" fill="url(#bg{i})" opacity=".85"/></g>'
  '<g class="wing r" transform="translate(100 0) scale(-1 1)"><path d="M50 52 C 38 20, 10 14, 14 40 C 17 56, 38 60, 50 52 Z" fill="url(#bg{i})"/>'
  '<path d="M50 54 C 40 62, 22 78, 32 84 C 42 88, 50 72, 50 54 Z" fill="url(#bg{i})" opacity=".85"/></g>'
  '<path d="M50 50 C 50 40, 54 30, 60 24 M50 50 C 50 40, 46 30, 40 24" stroke="{c2}" stroke-width="1.2" fill="none"/>'
  '<circle cx="60" cy="24" r="2" fill="{c2}"/><circle cx="40" cy="24" r="2" fill="{c2}"/></svg>')
def butterflies(specs):
    out = ['<div class="butterflies" aria-hidden="true">']
    for i, (top, left, size, dur, delay, flap, kind) in enumerate(specs):
        c1, c2 = ('#F6D77A', '#B88A17') if kind == 'g' else ('#C21C80', '#6B0F3A')
        out.append(f'<div class="bfly" style="top:{top};left:{left};--s:{size}px;--d:{dur}s;--delay:{delay}s;--f:{flap}s">{BUTTERFLY.format(i=f"{kind}{i}{size}", c1=c1, c2=c2)}</div>')
    out.append('</div>')
    return ''.join(out)

# Services --------------------------------------------------------
CATS = [
 ('injectables', 'Aesthetic Injectables', 'الحقن التجميلية',
  'Refined, natural-looking results through precise injection techniques — designed around your features, never against them.',
  'نتائج طبيعية وراقية بتقنيات حقن دقيقة، مصمّمة لتُبرز ملامحك لا لتغيّرها.', [
   ('botox', 'syringe', 'Anti-Wrinkle Injections', 'حقن التجاعيد (البوتوكس)',
    'Softens expression lines on the forehead, between the brows and around the eyes for a rested, refreshed look.',
    'تنعيم خطوط التعبير في الجبهة وبين الحاجبين وحول العينين لمظهر مرتاح ومنتعش.', ['Quick session', 'No downtime'], ['جلسة سريعة', 'بدون فترة نقاهة']),
   ('fillers', 'drop', 'Dermal Fillers', 'الفيلر',
    'Restores lost volume and refines the lips, cheeks and chin with balanced, natural proportions.',
    'استعادة الحجم المفقود وتحسين الشفاه والخدود والذقن بتناسق طبيعي.', ['Instant results'], ['نتائج فورية']),
   ('jawline', 'jaw', 'Jawline Contouring', 'تحديد الفك',
    'Subtle, carefully planned definition that frames the face — elegant and never overdone.',
    'تحديد مدروس وناعم يبرز إطار الوجه بأناقة ودون مبالغة.', ['Tailored plan'], ['خطة مخصّصة']),
   ('midface', 'lift', 'Cheek & Mid-Face Lifting', 'شد الخدود ومنتصف الوجه',
    'Lifting options for sagging cheeks — including techniques that lift without adding volume to the face.',
    'خيارات لشد الخدود المترهلة، منها تقنيات ترفع دون أن تزيد حجم الوجه.', ['Non-filler options'], ['خيارات بدون فيلر']),
   ('undereye', 'eye', 'Under-Eye Rejuvenation', 'علاج منطقة تحت العين',
    'Treats hollows and dark circles to bring back a brighter, well-rested look.',
    'علاج التجويف والهالات الداكنة لاستعادة إشراقة العين ومظهر مرتاح.', ['Delicate area'], ['منطقة حساسة']),
   ('harmony', 'balance', 'Facial Harmony & Symmetry', 'تناسق وتوازن ملامح الوجه',
    'Balances natural asymmetries between both sides of the face — cheeks, brows and lips.',
    'موازنة الفروقات الطبيعية بين جانبي الوجه في الخدود والحواجب والشفاه.', ['Full-face assessment'], ['تقييم شامل للوجه']),
   ('gummy', 'smile', 'Gummy Smile Treatment', 'علاج الابتسامة اللثوية',
    'A gentle, non-surgical treatment that reduces excessive gum show for a more confident smile.',
    'علاج لطيف وغير جراحي يقلّل ظهور اللثة لابتسامة أكثر ثقة.', ['Non-surgical'], ['غير جراحي']),
 ]),
 ('laser', 'Laser Therapy', 'العلاج بالليزر',
  'Advanced laser technology, calibrated to your skin type, for smoother, clearer and more even skin.',
  'تقنيات ليزر متطورة تُضبط حسب نوع بشرتك، لبشرة أنعم وأنقى وأكثر توحّداً.', [
   ('laser-hair', 'laser', 'Laser Hair Removal', 'إزالة الشعر بالليزر',
    'Long-lasting hair reduction for face and body, with settings adjusted to your skin and hair type.',
    'تقليل الشعر لفترات طويلة للوجه والجسم، بإعدادات تناسب نوع بشرتك وشعرك.', ['Face & body'], ['الوجه والجسم']),
   ('veins', 'vein', 'Hand Vein Treatment', 'إزالة عروق اليدين',
    'Reduces the appearance of prominent hand veins as part of a complete hand rejuvenation.',
    'التخفيف من ظهور العروق البارزة في اليدين ضمن علاج متكامل لتجديد شبابهما.', ['Hand rejuvenation'], ['تجديد اليدين']),
   ('resurfacing', 'sparkle', 'Laser Skin Resurfacing', 'تجديد البشرة بالليزر',
    'Improves texture, pores and fine lines while stimulating natural collagen renewal.',
    'تحسين ملمس البشرة والمسام والخطوط الدقيقة مع تحفيز تجدد الكولاجين الطبيعي.', ['Texture & tone'], ['الملمس واللون']),
   ('pigmentation', 'dot', 'Pigmentation & Melasma', 'التصبغات والكلف',
    'Targets dark spots, sun damage and uneven tone for a clearer, more luminous complexion.',
    'علاج البقع الداكنة وآثار الشمس وعدم توحّد اللون لبشرة أنقى وأكثر إشراقاً.', ['Even tone'], ['توحيد اللون']),
 ]),
 ('dermatology', 'Medical Dermatology', 'الأمراض الجلدية',
  'Expert diagnosis and treatment for skin concerns — from acne to moles — with a medical approach you can trust.',
  'تشخيص وعلاج متخصص لمشاكل الجلد، من حب الشباب إلى الشامات، بنهج طبي موثوق.', [
   ('acne', 'face', 'Acne & Acne Scars', 'حب الشباب وآثاره',
    'Personalised treatment plans to calm active acne and visibly improve scars and marks.',
    'خطط علاج مخصّصة لتهدئة حب الشباب النشط وتحسين الآثار والندبات بشكل واضح.', ['Active acne', 'Scars'], ['حب شباب نشط', 'ندبات']),
   ('moles', 'scissors', 'Mole & Skin Tag Removal', 'إزالة الشامات والزوائد الجلدية',
    'Safe, precise removal of moles and skin tags with careful attention to healing.',
    'إزالة آمنة ودقيقة للشامات والزوائد الجلدية مع عناية خاصة بالتئام البشرة.', ['Precise', 'Minimal marks'], ['دقة عالية', 'أثر بسيط']),
   ('consultation', 'stethoscope', 'Skin Consultation & Diagnosis', 'استشارة وتشخيص جلدي',
    'Assessment and treatment of eczema, rashes, infections and other skin conditions.',
    'تقييم وعلاج الإكزيما والطفح الجلدي والالتهابات وغيرها من الأمراض الجلدية.', ['Medical care'], ['رعاية طبية']),
 ]),
 ('hair', 'Hair & Rejuvenation', 'الشعر وتجديد الشباب',
  'Treatments that restore strength, density and vitality — to your hair, your skin and your hands.',
  'علاجات تعيد القوة والكثافة والحيوية لشعرك وبشرتك ويديك.', [
   ('hairloss', 'hair', 'Hair Loss Diagnosis & Treatment', 'تشخيص وعلاج تساقط الشعر',
    'Finds the real cause behind hair loss — hormonal, nutritional or seasonal — and treats it at the root.',
    'معرفة السبب الحقيقي وراء التساقط، سواء كان هرمونياً أو غذائياً أو موسمياً، وعلاجه من الجذور.', ['Root-cause care'], ['علاج السبب']),
   ('scalp', 'leaf', 'Scalp Revitalisation', 'تنشيط فروة الرأس',
    'In-clinic therapies that nourish the scalp and support thicker, healthier growth.',
    'جلسات داخل العيادة تغذّي فروة الرأس وتدعم نمو شعر أكثف وأكثر صحة.', ['Thicker hair'], ['شعر أكثف']),
   ('glow', 'star', 'Skin Boosters & Glow', 'معززات البشرة والنضارة',
    'Deep hydration and renewal treatments for a radiant, healthy-looking complexion.',
    'علاجات ترطيب عميق وتجديد لبشرة مشرقة وصحية المظهر.', ['Hydration', 'Radiance'], ['ترطيب', 'إشراقة']),
   ('hands', 'hand', 'Hand Rejuvenation', 'تجديد شباب اليدين',
    'Restores smoothness and youthfulness to the hands — often the first place age shows.',
    'استعادة نعومة اليدين وشبابهما، فهما غالباً أول ما يظهر عليه العمر.', ['Complete care'], ['عناية متكاملة']),
 ]),
]

# ---------------------------------------------------------------- layout
NAV = [
 ('index.html', 'Home', 'الرئيسية'),
 ('services.html', 'Services', 'الخدمات'),
 ('before-after.html', 'Before & After', 'قبل وبعد'),
 ('booking.html', 'Book', 'الحجز'),
 ('working-hours.html', 'Hours', 'ساعات العمل'),
 ('faq.html', 'FAQ', 'الأسئلة الشائعة'),
 ('contact.html', 'Contact', 'تواصل معنا'),
]
MENU_FULL = {'booking.html': ('Book Appointment', 'حجز موعد'), 'working-hours.html': ('Working Hours', 'ساعات العمل'), 'contact.html': ('Contact Us', 'تواصل معنا')}

HEAD_SCRIPT = """<script>(function(){var d=document.documentElement,l=null;try{l=new URLSearchParams(location.search).get('lang')||localStorage.getItem('cn-lang');}catch(e){}if(l==='ar'){d.lang='ar';d.dir='rtl';d.classList.add('ar-pending');}try{if(sessionStorage.getItem('cn-seen'))d.classList.add('no-preload');}catch(e){}})();</script>"""

def head(title_en, title_ar, desc):
    return f"""<!DOCTYPE html>
<html lang="en" dir="ltr">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title data-ar="{A(title_ar)}">{title_en}</title>
<meta name="description" content="{A(desc)}">
<meta name="theme-color" content="#3A0820">
<meta property="og:title" content="{A(title_en)}">
<meta property="og:description" content="{A(desc)}">
<meta property="og:image" content="assets/img/office.jpg">
<meta property="og:type" content="website">
<link rel="icon" href="assets/img/favicon.svg" type="image/svg+xml">
<link rel="icon" href="assets/img/favicon-32.png" sizes="32x32">
<link rel="apple-touch-icon" href="assets/img/apple-touch-icon.png">
{HEAD_SCRIPT}
<style>html.ar-pending body{{opacity:0}}</style>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,400;0,500;0,600;1,400;1,500&family=Jost:wght@300;400;500&family=El+Messiri:wght@400;500;600&family=Tajawal:wght@300;400;500;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
<script type="application/ld+json">{{"@context":"https://schema.org","@type":"MedicalClinic","name":"Clinica Neveen — Dr. Neveen Dababneh","medicalSpecialty":["Dermatology","PlasticSurgery"],"telephone":"+962798253922","email":"{EMAIL}","address":{{"@type":"PostalAddress","streetAddress":"7th Circle, behind Royal Jordanian building","addressLocality":"Amman","addressCountry":"JO"}},"openingHoursSpecification":[{{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"10:00","closes":"19:00"}}],"sameAs":["https://www.instagram.com/clinicaneveen/","https://www.facebook.com/clinicaneveen/","https://www.tiktok.com/@clinicaneveen"]}}</script>
</head>
"""

def header(active):
    links = ''.join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""} data-ar="{A(ar)}">{en}</a></li>'
        for h, en, ar in NAV)
    mlinks = ''.join(
        f'<li><a href="{h}"{" aria-current=\"page\"" if h == active else ""} data-ar="{A(MENU_FULL.get(h, (en, ar))[1])}">{MENU_FULL.get(h, (en, ar))[0]}</a></li>'
        for h, en, ar in NAV)
    return f"""<body>
<a href="#main" class="skip" data-ar="تخطَّ إلى المحتوى">Skip to content</a>
<div class="preloader" aria-hidden="true"><img src="assets/img/logo-light-520.png" alt=""><div class="bar"></div></div>
<div class="page-curtain" aria-hidden="true"></div>
<header class="site-header">
  <div class="nav-wrap">
    <a href="index.html" class="brand" aria-label="Clinica Neveen — Home"><img src="assets/img/logo-520.png" alt="Clinica Neveen Dermatology" width="520" height="246"></a>
    <nav class="main-nav" aria-label="Main"><ul>{links}</ul></nav>
    <div class="nav-actions">
      <button class="lang-toggle" type="button" aria-label="التحويل إلى العربية">عربي</button>
      <a href="booking.html" class="btn btn-gold btn-sm" data-ar="احجز موعدك">Book Now</a>
      <button class="burger" type="button" aria-label="Menu" data-ar-aria="القائمة" aria-expanded="false" aria-controls="menu"><span></span><span></span></button>
    </div>
  </div>
</header>
<div class="menu-overlay" id="menu">
  <ol>{mlinks}</ol>
  <div class="menu-meta">
    <a class="wa-link" href="https://wa.me/{WA}" target="_blank" rel="noopener"><span data-ar="واتساب">WhatsApp</span> · <span class="ltr">+962 79 825 3922</span></a>
    <a href="mailto:{EMAIL}">{EMAIL}</a>
    <span data-ar="يومياً · 10 صباحاً – 7 مساءً">Daily · 10 AM – 7 PM</span>
  </div>
</div>
<main id="main">
"""

def footer():
    quick = ''.join(f'<li><a href="{h}" data-ar="{A(MENU_FULL.get(h,(en,ar))[1])}">{MENU_FULL.get(h,(en,ar))[0]}</a></li>' for h, en, ar in NAV)
    soc = ''.join(f'<a href="{u}" target="_blank" rel="noopener" aria-label="{n}">{BRAND[k]}</a>' for k, n, _, u in SOCIALS)
    phones = ''.join(f'<li><a href="tel:{t}" class="ltr">{d}</a></li>' for d, t, _, _ in PHONES)
    return f"""</main>
<footer class="site-footer">
  <div class="container">
    <div class="foot-grid">
      <div class="foot-brand">
        <img src="assets/img/logo-light-520.png" alt="Clinica Neveen" width="520" height="246" loading="lazy">
        <p data-ar="عيادة الدكتورة نيفين دبابنة للأمراض الجلدية والتجميل والعلاج بالليزر — حيث يلتقي العلم بالجمال في قلب عمّان.">Dr. Neveen Dababneh's clinic for dermatology, aesthetics and laser therapy — where medical science meets refined beauty, in the heart of Amman.</p>
        <div class="foot-social">{soc}</div>
      </div>
      <div>
        <h4 data-ar="روابط">Explore</h4>
        <ul>{quick}<li><a href="privacy.html" data-ar="سياسة الخصوصية">Privacy Policy</a></li></ul>
      </div>
      <div>
        <h4 data-ar="اتصل بنا">Call Us</h4>
        <ul>{phones}<li><a href="mailto:{EMAIL}">{EMAIL}</a></li></ul>
      </div>
      <div>
        <h4 data-ar="زورونا">Visit</h4>
        <ul>
          <li data-ar="{A(ADDR_AR)}">{ADDR_EN}</li>
          <li><a href="{MAPS}" target="_blank" rel="noopener" data-ar="عرض على الخريطة ←">Get directions →</a></li>
          <li style="margin-top:10px;color:var(--gold-300)" data-ar="يومياً · 10 صباحاً – 7 مساءً">Open daily · 10 AM – 7 PM</li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>© <span data-year>2026</span> <span data-ar="عيادة الدكتورة نيفين دبابنة. جميع الحقوق محفوظة.">Clinica Neveen — Dr. Neveen Dababneh. All rights reserved.</span></span>
      <a href="privacy.html" data-ar="سياسة الخصوصية">Privacy Policy</a>
    </div>
  </div>
  <div class="foot-word" aria-hidden="true">Clinica Neveen</div>
</footer>
<a class="wa-float wa-link" href="https://wa.me/{WA}" target="_blank" rel="noopener" aria-label="WhatsApp" data-ar-aria="تواصل عبر واتساب">{BRAND['whatsapp']}</a>
<button class="to-top" type="button" aria-label="Back to top" data-ar-aria="العودة للأعلى">{icon('up','1.6')}</button>
<script src="https://cdn.jsdelivr.net/npm/lenis@1.1.13/dist/lenis.min.js" defer></script>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""

def page_hero(crumb_en, crumb_ar, eyebrow_en, eyebrow_ar, title_en, title_ar, lead_en, lead_ar, letter):
    return f"""<section class="page-hero grain">
  <div class="container">
    <div class="breadcrumb reveal-fade"><a href="index.html" data-ar="الرئيسية">Home</a><span>/</span>{T(crumb_en, crumb_ar)}</div>
    {T(eyebrow_en, eyebrow_ar, 'div', 'eyebrow reveal')}
    <h1 class="split-words" data-ar="{A(title_ar)}">{title_en}</h1>
    {T(lead_en, lead_ar, 'p', 'lead reveal', 'style="--rd:.25s"')}
  </div>
  <div class="big-letter" aria-hidden="true">{letter}</div>
  {butterflies([('22%','78%',48,18,0,.8,'g'),('60%','88%',35,15,-4,.7,'p')])}
</section>
"""

def picture(name, alt_en, cls='', extra='', pos=None):
    style = f' style="object-position:{pos}"' if pos else ''
    return (f'<picture><source srcset="assets/img/{name}.webp" type="image/webp">'
            f'<img src="assets/img/{name}.jpg" alt="{A(alt_en)}" loading="lazy"{style} {extra}></picture>')

def cta_band():
    return f"""<section class="cta bg-plum grain">
  <div class="container">
    <div class="divider-orn reveal">{icon('sparkle','1.2')}</div>
    <h2 class="split-words" data-ar="بشرتك تستحق <em>أفضل رعاية</em>">Your skin deserves <em>expert care</em></h2>
    {T('Book a private consultation with Dr. Neveen and receive a treatment plan designed only for you.', 'احجز استشارة خاصة مع الدكتورة نيفين واحصل على خطة علاج مصمّمة لك وحدك.', 'p', 'lead center reveal')}
    <div class="btns reveal" style="--rd:.2s">
      <a href="booking.html" class="btn btn-gold"><span data-ar="احجز موعدك">Book Appointment</span>{icon('arrow','1.6').replace('<svg','<svg class="arrow"')}</a>
      <a href="https://wa.me/{WA}" class="btn btn-ghost-light wa-link" target="_blank" rel="noopener">{BRAND['whatsapp']}<span data-ar="واتساب">WhatsApp</span></a>
    </div>
  </div>
  {butterflies([('18%','10%',54,20,0,.9,'g'),('70%','86%',41,17,-6,.8,'g'),('40%','92%',32,14,-3,.7,'p')])}
</section>
"""

def ba_slider(label_en='', label_ar=''):
    return f"""<div class="ba">
  <div class="ba-pane ba-before">{icon('image','1.2')}<span data-ar="صورة قبل">Before photo</span></div>
  <div class="ba-pane ba-after">{icon('image','1.2')}<span data-ar="صورة بعد">After photo</span></div>
  <span class="ba-label l" data-ar="قبل">Before</span><span class="ba-label r" data-ar="بعد">After</span>
  <div class="ba-handle"></div>
  <input type="range" min="0" max="100" value="50" aria-label="Compare before and after" data-ar-aria="قارن بين قبل وبعد">
</div>"""

ARROW = icon('arrow', '1.6')

# ================================================================ PAGES
def page_home():
    svc_cards = [
        ('services.html#injectables', 'syringe', 'Anti-Wrinkle Injections', 'حقن التجاعيد', 'Smooth expression lines for a refreshed look that still looks like you.', 'تنعيم خطوط التعبير لمظهر منتعش يبقى طبيعياً ويشبهك.'),
        ('services.html#injectables', 'jaw', 'Fillers & Contouring', 'الفيلر ونحت الملامح', 'Jawline, cheeks and lips — refined with balance and restraint.', 'الفك والخدود والشفاه، بتوازن ودون مبالغة.'),
        ('services.html#laser', 'laser', 'Laser Therapy', 'العلاج بالليزر', 'Hair removal, resurfacing and pigmentation with advanced technology.', 'إزالة الشعر وتجديد البشرة وعلاج التصبغات بأحدث التقنيات.'),
        ('services.html#dermatology', 'face', 'Acne & Scars', 'حب الشباب وآثاره', 'Medical treatment plans that clear skin and restore confidence.', 'خطط علاج طبية تنقّي البشرة وتعيد الثقة.'),
        ('services.html#hair', 'hair', 'Hair Loss Treatment', 'علاج تساقط الشعر', 'We find the true cause of hair loss and treat it at the root.', 'نبحث عن السبب الحقيقي للتساقط ونعالجه من الجذور.'),
        ('services.html#injectables', 'eye', 'Under-Eye Rejuvenation', 'علاج تحت العين', 'Brighten dark circles and soften hollows for well-rested eyes.', 'تفتيح الهالات وتعبئة التجويف لعيون تبدو مرتاحة.'),
    ]
    cards = ''.join(f"""<a href="{h}" class="card">
      <span class="idx">0{i+1}</span>
      <div class="icon">{icon(ic)}</div>
      {T(en, ar, 'h3')}
      {T(de, da, 'p')}
      <span class="link-arrow"><span data-ar="اكتشف المزيد">Discover</span>{ARROW}</span>
    </a>""" for i, (h, ic, en, ar, de, da) in enumerate(svc_cards))
    marquee_items = [('Laser Therapy','العلاج بالليزر'),('Jawline Contouring','تحديد الفك'),('Skin Rejuvenation','تجديد البشرة'),('Hair Loss Treatment','علاج تساقط الشعر'),('Anti-Wrinkle','حقن التجاعيد'),('Acne & Scars','حب الشباب وآثاره'),('Under-Eye Care','علاج تحت العين'),('Medical Dermatology','الأمراض الجلدية')]
    mq = ''.join(T(e, a) for e, a in marquee_items)
    return head('Clinica Neveen | Dermatology, Aesthetics & Laser — Amman', 'عيادة الدكتورة نيفين دبابنة | جلدية وتجميل وليزر — عمّان',
                'Dr. Neveen Dababneh — dermatology, aesthetic medicine and laser therapy clinic at the 7th Circle, Amman. Book your consultation online or via WhatsApp.') + header('index.html') + f"""
<!-- HERO -->
<section class="hero grain">
  <div class="container hero-grid">
    <div class="hero-copy">
      {T('Dermatology · Aesthetics · Laser', 'جلدية · تجميل · ليزر', 'div', 'eyebrow reveal')}
      <h1 class="split-words" data-ar="فنّ البشرة <em>المشرقة</em> بلمسة طبية">The art of <em>radiant</em> skin, guided by medicine</h1>
      {T("Dr. Neveen Dababneh's clinic blends medical dermatology with refined aesthetics — so every treatment looks natural, feels safe and is designed only for you.",
         'تجمع عيادة الدكتورة نيفين دبابنة بين طب الجلد والتجميل الراقي، لتكون كل جلسة طبيعية النتيجة وآمنة ومصمّمة لك وحدك.', 'p', 'lead reveal', 'style="--rd:.3s"')}
      <div class="hero-ctas reveal" style="--rd:.45s">
        <a href="booking.html" class="btn"><span data-ar="احجز استشارتك">Book Consultation</span>{ARROW.replace('<svg','<svg class="arrow"')}</a>
        <a href="services.html" class="btn btn-ghost" data-ar="استكشف الخدمات">Explore Services</a>
      </div>
      <div class="hero-meta reveal" style="--rd:.6s">
        <div><strong>230K+</strong><span data-ar="متابع على إنستغرام">Instagram community</span></div>
        <div><strong>7/7</strong><span data-ar="أيام في الأسبوع">Days a week</span></div>
        <div><strong>4</strong><span data-ar="تخصصات">Specialties</span></div>
      </div>
    </div>
    <div class="hero-visual reveal" style="--rd:.2s">
      <div class="arch-outline" aria-hidden="true"></div>
      <div class="arch reveal-mask" style="--rd:.35s">{picture('hero-doctor', 'Dr. Neveen Dababneh with a patient during an advanced skin treatment', extra='fetchpriority="high" width="860" height="1024"').replace(' loading="lazy"','')}</div>
      <div class="float-card">
        <span class="name" data-ar="د. نيفين دبابنة">Dr. Neveen Dababneh</span>
        <small data-ar="الجلدية والتجميل والليزر">Dermatology & Aesthetics</small>
      </div>
      <div class="seal" aria-hidden="true">
        <svg viewBox="0 0 120 120"><defs><path id="circ" d="M60,60 m-46,0 a46,46 0 1,1 92,0 a46,46 0 1,1 -92,0"/></defs><text><textPath href="#circ">Clinica Neveen ✦ Dermatology ✦ Amman ✦</textPath></text></svg>
        <svg class="core" viewBox="0 0 24 24" fill="none" stroke="#F6D77A" stroke-width="1.2" style="position:static;animation:none">{ICONS['sparkle']}</svg>
      </div>
    </div>
  </div>
  {butterflies([('16%','46%',48,19,0,.85,'g'),('72%','6%',38,16,-5,.75,'p'),('30%','92%',35,14,-2,.7,'g')])}
  <div class="scroll-cue" aria-hidden="true"><span>Scroll</span><i></i></div>
</section>

<div class="marquee" aria-hidden="true"><div class="marquee-track"><span>{mq}</span><span>{mq}</span></div></div>

<!-- OVERVIEW -->
<section class="section" id="overview">
  <div class="container overview-grid">
    <div>
      {T('Overview', 'نظرة عامة', 'div', 'eyebrow reveal')}
      <h2 class="split-words" data-ar="حيث يلتقي <em>العلم</em> بالجمال">Where <em>science</em> meets beauty</h2>
      {T('Clinica Neveen is a specialised dermatology, beauty and laser therapy clinic at the 7th Circle in Amman. Every visit begins with a medical assessment, because beautiful results start with healthy skin.',
         'عيادة الدكتورة نيفين عيادة متخصصة في الأمراض الجلدية والتجميل والعلاج بالليزر في الدوار السابع بعمّان. تبدأ كل زيارة بتقييم طبي، لأن النتائج الجميلة تبدأ ببشرة صحية.', 'p', 'lead reveal')}
      <a href="services.html" class="link-arrow reveal"><span data-ar="جميع الخدمات">All treatments</span>{ARROW}</a>
    </div>
    <div class="stats">
      <div class="stat reveal"><div class="num"><span data-count="230">0</span><sup>K+</sup></div>{T('Followers trust our work', 'متابع يثقون بعملنا', 'p')}</div>
      <div class="stat reveal" style="--rd:.1s"><div class="num"><span data-count="20">0</span><sup>+</sup></div>{T('Treatments offered', 'علاج ومعالجة', 'p')}</div>
      <div class="stat reveal" style="--rd:.2s"><div class="num"><span data-count="7">0</span><sup>/7</sup></div>{T('Open every day', 'مفتوحون كل يوم', 'p')}</div>
      <div class="stat reveal" style="--rd:.3s"><div class="num"><span data-count="100">0</span><sup>%</sup></div>{T('Doctor-led care', 'رعاية بإشراف الطبيبة', 'p')}</div>
    </div>
  </div>
</section>

<!-- ABOUT -->
<section class="about section-sm" id="about" style="padding-top:0">
  <div class="container">
    <div class="about-media reveal-mask">{picture('office', 'Dr. Neveen Dababneh in her clinic office in Amman', extra='data-parallax="0.08" width="1600" height="900"')}</div>
    <div class="about-card reveal">
      {T('About the Doctor', 'عن الطبيبة', 'div', 'eyebrow')}
      <h2 class="split-words" data-ar="د. نيفين <em>دبابنة</em>">Dr. Neveen <em>Dababneh</em></h2>
      {T('Dr. Neveen Dababneh is a dermatologist dedicated to medical and aesthetic skin care. Her approach is simple: listen first, diagnose precisely, and treat with restraint — enhancing each patient\'s natural features rather than changing them.',
         'الدكتورة نيفين دبابنة طبيبة متخصصة في الأمراض الجلدية، تكرّس عملها للعناية الطبية والتجميلية بالبشرة. نهجها بسيط: أن تستمع أولاً، وتشخّص بدقة، وتعالج باعتدال، لتُبرز جمال كل مريض الطبيعي لا لتغيّره.', 'p')}
      {T('From acne and hair loss to laser therapy and facial contouring, every plan she creates is built on medical knowledge, honest advice and a genuine care for how you feel in your own skin.',
         'من حب الشباب وتساقط الشعر إلى العلاج بالليزر ونحت ملامح الوجه، تُبنى كل خطة علاج على المعرفة الطبية والنصيحة الصادقة واهتمام حقيقي بشعورك تجاه بشرتك.', 'p', 'muted')}
      <div class="signature"><span data-ar="د. نيفين دبابنة">Dr. Neveen Dababneh</span><small data-ar="أخصائية الجلدية والتجميل والليزر">Dermatology · Aesthetics · Laser</small></div>
    </div>
  </div>
</section>

<!-- SERVICES PREVIEW -->
<section class="section bg-ivory grain" id="services">
  <div class="container">
    <div class="section-head center">
      {T('Signature Treatments', 'علاجاتنا المميزة', 'div', 'eyebrow both reveal')}
      <h2 class="split-words" data-ar="علاجات مصمّمة <em>لك وحدك</em>">Treatments designed <em>around you</em></h2>
      {T('A complete range of medical and aesthetic treatments, each performed with precision and care.', 'مجموعة متكاملة من العلاجات الطبية والتجميلية، كلٌّ منها يُجرى بدقة وعناية.', 'p', 'lead reveal')}
    </div>
    <div class="cards stagger">{cards}</div>
    <div class="center reveal" style="margin-top:56px;text-align:center"><a href="services.html" class="btn btn-ghost" data-ar="عرض جميع الخدمات">View all services</a></div>
  </div>
</section>

<!-- PRECISION / WHY -->
<section class="section" id="why">
  <div class="container split">
    <div class="framed reveal">
      <div class="inner reveal-mask" style="--rd:.15s">{picture('precision', 'Dr. Neveen carefully marking a treatment area before an aesthetic procedure', extra='data-parallax="0.06" width="1000" height="1000"')}</div>
      <span class="tag" data-ar="الدقة في كل تفصيل">Precision in every detail</span>
    </div>
    <div>
      {T('Why Clinica Neveen', 'لماذا عيادة الدكتورة نيفين', 'div', 'eyebrow reveal')}
      <h2 class="split-words" data-ar="جمال <em>مدروس</em>، لا مبالغ فيه">Beauty that is <em>considered</em>, never overdone</h2>
      <ul class="why-list stagger">
        <li><span class="n">01</span><div>{T('Medical assessment first', 'التقييم الطبي أولاً', 'h4')}{T('Every treatment starts with understanding your skin, your history and your goals.', 'يبدأ كل علاج بفهم بشرتك وتاريخك الصحي وأهدافك.', 'p')}</div></li>
        <li><span class="n">02</span><div>{T('Natural, balanced results', 'نتائج طبيعية ومتوازنة', 'h4')}{T('Subtle enhancements that respect your features and facial harmony.', 'لمسات ناعمة تحترم ملامحك وتناسق وجهك.', 'p')}</div></li>
        <li><span class="n">03</span><div>{T('Advanced technology', 'تقنيات متطورة', 'h4')}{T('Modern laser and skin-imaging devices for precise, comfortable sessions.', 'أجهزة ليزر وتصوير بشرة حديثة لجلسات دقيقة ومريحة.', 'p')}</div></li>
        <li><span class="n">04</span><div>{T('Honest, personal advice', 'نصيحة صادقة وشخصية', 'h4')}{T('We recommend only what you truly need — nothing more.', 'ننصحك فقط بما تحتاجه فعلاً، لا أكثر.', 'p')}</div></li>
      </ul>
      <a href="booking.html" class="btn reveal"><span data-ar="احجز استشارتك">Book Consultation</span>{ARROW.replace('<svg','<svg class="arrow"')}</a>
    </div>
  </div>
</section>

<!-- IMAGE BAND -->
<section class="band">
  <div class="band-media" data-parallax="0.12">{picture('treatment-device', 'Advanced skin treatment at Clinica Neveen', extra='width="1400" height="869"')}</div>
  <div class="container">
    <span class="quote-mark reveal" aria-hidden="true">“</span>
    <h2 class="split-words" data-ar="تقنية متقدمة، <em>ويدٌ لطيفة</em>">Advanced technology, <em>gentle hands</em></h2>
    {T('We pair the latest aesthetic devices with a calm, attentive approach — so you feel cared for at every step.', 'نجمع بين أحدث الأجهزة التجميلية وأسلوب هادئ ومنتبه، لتشعر بالاهتمام في كل خطوة.', 'p', 'reveal', 'style="--rd:.2s"')}
    <a href="services.html#laser" class="btn btn-gold reveal" style="--rd:.3s"><span data-ar="اكتشف العلاج بالليزر">Discover laser therapy</span>{ARROW.replace('<svg','<svg class="arrow"')}</a>
  </div>
</section>

<!-- BEFORE / AFTER TEASER -->
<section class="section bg-ivory">
  <div class="container ba-feature">
    <div class="reveal">{ba_slider()}</div>
    <div>
      {T('Real Results', 'نتائج حقيقية', 'div', 'eyebrow reveal')}
      <h2 class="split-words" data-ar="النتائج <em>تتحدث</em> عن نفسها">Results that <em>speak</em> for themselves</h2>
      {T('Drag the slider to compare. Explore our gallery of before & after cases across every specialty.', 'اسحب المؤشر للمقارنة، واستكشف معرض حالات قبل وبعد في جميع التخصصات.', 'p', 'lead reveal')}
      <a href="before-after.html" class="btn reveal"><span data-ar="معرض قبل وبعد">View gallery</span>{ARROW.replace('<svg','<svg class="arrow"')}</a>
    </div>
  </div>
</section>
""" + cta_band() + footer()

def page_services():
    navs = ''.join(f'<li><a href="#{k}" data-ar="{A(ar)}">{en}</a></li>' for k, en, ar, *_ in CATS)
    body = ''
    for ci, (k, en, ar, den, dar, items) in enumerate(CATS):
        svcs = ''
        for (key, ic, ten, tar, sen, sar, tags_en, tags_ar) in items:
            tags = ''.join(T(a, b) for a, b in zip(tags_en, tags_ar))
            svcs += f"""<article class="svc">
        <div class="icon">{icon(ic)}</div>
        <div>
          {T(ten, tar, 'h3')}
          {T(sen, sar, 'p')}
          <div class="meta">{tags}</div>
          <a href="booking.html?service={key}" class="link-arrow"><span data-ar="احجز هذا العلاج">Book this treatment</span>{ARROW}</a>
        </div>
      </article>"""
        body += f"""<section class="svc-cat" id="{k}">
  <div class="container">
    <div class="svc-head">
      <div><span class="num reveal">0{ci+1}</span><h2 class="split-words" data-ar="{A(ar)}">{en}</h2></div>
      {T(den, dar, 'p', 'lead reveal')}
    </div>
    <div class="svc-list stagger">{svcs}</div>
  </div>
</section>
"""
    return head('Services | Clinica Neveen — Dermatology, Aesthetics & Laser', 'الخدمات | عيادة الدكتورة نيفين دبابنة',
                'Aesthetic injectables, laser therapy, medical dermatology and hair treatments at Clinica Neveen, Amman.') + header('services.html') + \
        page_hero('Services', 'الخدمات', 'Our Treatments', 'علاجاتنا', 'Expert care for <em>every</em> skin story', 'رعاية متخصصة <em>لكل</em> بشرة',
                  'From medical dermatology to refined aesthetics and advanced laser therapy — explore treatments designed with precision and care.',
                  'من طب الجلد إلى التجميل الراقي والعلاج بالليزر المتطور، اكتشف علاجات مصمّمة بدقة وعناية.', 'S') + \
        f'<nav class="cat-nav" data-subnav aria-label="Service categories"><ul>{navs}</ul></nav>' + body + cta_band() + footer()

def page_before_after():
    cases = [
        ('injectables', 'Jawline Contouring', 'تحديد الفك', '1 session', 'جلسة واحدة'),
        ('injectables', 'Lip Enhancement', 'تحسين الشفاه', '1 session', 'جلسة واحدة'),
        ('injectables', 'Under-Eye Rejuvenation', 'علاج تحت العين', '1 session', 'جلسة واحدة'),
        ('injectables', 'Anti-Wrinkle Injections', 'حقن التجاعيد', '2 weeks after', 'بعد أسبوعين'),
        ('laser', 'Laser Hair Removal', 'إزالة الشعر بالليزر', '6 sessions', '6 جلسات'),
        ('laser', 'Pigmentation & Melasma', 'التصبغات والكلف', '4 sessions', '4 جلسات'),
        ('laser', 'Hand Vein Treatment', 'إزالة عروق اليدين', '2 sessions', 'جلستان'),
        ('dermatology', 'Acne & Acne Scars', 'حب الشباب وآثاره', '3 months', '3 أشهر'),
        ('dermatology', 'Mole Removal', 'إزالة الشامات', '1 session', 'جلسة واحدة'),
        ('hair', 'Hair Loss Treatment', 'علاج تساقط الشعر', '4 months', '4 أشهر'),
        ('hair', 'Scalp Revitalisation', 'تنشيط فروة الرأس', '6 sessions', '6 جلسات'),
        ('hair', 'Hand Rejuvenation', 'تجديد شباب اليدين', '2 sessions', 'جلستان'),
    ]
    chips = [('all', 'All', 'الكل')] + [(k, en, ar) for k, en, ar, *_ in CATS]
    chip_html = ''.join(f'<button type="button" class="chip{" active" if k=="all" else ""}" data-filter="{k}" aria-pressed="{"true" if k=="all" else "false"}" data-ar="{A(ar)}">{en}</button>' for k, en, ar in chips)
    grid = ''.join(f"""<figure class="ba-card" data-cat="{c}">{ba_slider()}<figcaption>{T(en, ar, 'strong')}{T(sen, sar)}</figcaption></figure>""" for c, en, ar, sen, sar in cases)
    return head('Before & After | Clinica Neveen', 'قبل وبعد | عيادة الدكتورة نيفين دبابنة',
                'Before and after results from Clinica Neveen — injectables, laser therapy, dermatology and hair treatments.') + header('before-after.html') + \
        page_hero('Before & After', 'قبل وبعد', 'Results Gallery', 'معرض النتائج', 'Real people, <em>real</em> results', 'أشخاص حقيقيون، نتائج <em>حقيقية</em>',
                  'Drag each slider to compare. All photos are shared with our patients\' consent and show results achieved at our clinic.',
                  'اسحب المؤشر للمقارنة. جميع الصور منشورة بموافقة المرضى وتعرض نتائج حققناها في عيادتنا.', 'B') + f"""
<section class="section">
  <div class="container">
    <div class="chips reveal" role="group" aria-label="Filter results">{chip_html}</div>
    <div class="ba-grid stagger">{grid}</div>
    <p class="center muted reveal" style="max-width:640px;margin:70px auto 0;text-align:center;font-size:14.5px" data-ar="* تختلف النتائج من شخص لآخر. تُحدَّد خطة العلاج المناسبة لك خلال الاستشارة الطبية.">* Individual results vary from person to person. Your personal treatment plan is determined during your medical consultation.</p>
  </div>
</section>
""" + cta_band() + footer()

def page_booking():
    opts = '<option value="" data-ar="اختر العلاج">Select a treatment</option>'
    for k, en, ar, _, _, items in CATS:
        opts += f'<optgroup label="{A(en)}">'
        for key, _, ten, tar, *_ in items:
            opts += f'<option value="{A(ten)}" data-key="{key}" data-ar="{A(tar)}">{ten}</option>'
        opts += '</optgroup>'
    opts += '<option value="Consultation — not sure yet" data-key="consult" data-ar="استشارة — لست متأكداً بعد">Consultation — not sure yet</option>'
    times = ''.join(f'<option value="{h}" class="ltr">{h}</option>' for h in
                    ['10:00 AM', '10:30 AM', '11:00 AM', '11:30 AM', '12:00 PM', '12:30 PM', '1:00 PM', '1:30 PM', '2:00 PM', '2:30 PM', '3:00 PM', '3:30 PM', '4:00 PM', '4:30 PM', '5:00 PM', '5:30 PM', '6:00 PM', '6:30 PM'])
    faqs = [
        ('Is the appointment confirmed once I submit?', 'هل يتم تأكيد الموعد بمجرد إرسال الطلب؟',
         'Not yet — our team will contact you by phone or WhatsApp to confirm the exact date and time.', 'ليس بعد، سيتواصل معك فريقنا عبر الهاتف أو واتساب لتأكيد التاريخ والوقت بالضبط.'),
        ('Do I need a consultation before treatment?', 'هل أحتاج إلى استشارة قبل العلاج؟',
         'For most treatments, yes. The consultation helps the doctor understand your skin and recommend the right plan.', 'في معظم العلاجات نعم، فالاستشارة تساعد الطبيبة على فهم بشرتك واقتراح الخطة المناسبة.'),
        ('Can I reschedule or cancel?', 'هل يمكنني تغيير الموعد أو إلغاؤه؟',
         'Of course. Please let us know as early as possible by calling or messaging us on WhatsApp.', 'بالتأكيد. يرجى إبلاغنا في أقرب وقت ممكن عبر الاتصال أو رسالة واتساب.'),
    ]
    acc = ''.join(f'<details class="acc"><summary><span data-ar="{A(qa)}">{q}</span><span class="pm"></span></summary><div class="body">{T(a, aa, "p")}</div></details>' for q, qa, a, aa in faqs)
    E = lambda en, ar: f'<span class="err" role="alert"></span>'
    return head('Book an Appointment | Clinica Neveen', 'حجز موعد | عيادة الدكتورة نيفين دبابنة',
                'Request an appointment at Clinica Neveen, 7th Circle, Amman. Fill in the form or book instantly via WhatsApp.') + header('booking.html') + \
        page_hero('Book', 'الحجز', 'Appointments', 'المواعيد', 'Reserve your <em>moment</em>', 'احجز <em>موعدك</em>',
                  'Send us your request and our team will contact you shortly to confirm your appointment.',
                  'أرسل طلبك وسيتواصل معك فريقنا قريباً لتأكيد موعدك.', 'R') + f"""
<section class="section">
  <div class="container booking-grid">
    <div class="form-card reveal">
      <form id="booking-form" action="https://formsubmit.co/{EMAIL}" method="POST" novalidate>
        <input type="hidden" name="_subject" value="New Booking Request – Clinica Neveen">
        <input type="hidden" name="_template" value="table">
        <input type="hidden" name="_captcha" value="false">
        <input type="hidden" name="_next" value="">
        <input type="hidden" name="_replyto" value="">
        <input type="hidden" name="Language" value="English">
        <input type="text" name="_honey" class="hp" tabindex="-1" autocomplete="off" aria-hidden="true">
        <div class="form-grid">
          <div class="field"><label for="f-name"><span data-ar="الاسم الكامل">Full name</span> <span class="req">*</span></label><input id="f-name" name="Name" type="text" autocomplete="name" required placeholder="Your full name" data-ar-placeholder="اسمك الكامل">{E('','')}</div>
          <div class="field"><label for="f-phone"><span data-ar="رقم الهاتف">Phone number</span> <span class="req">*</span></label><input id="f-phone" name="Phone" type="tel" autocomplete="tel" inputmode="tel" required placeholder="07X XXX XXXX" dir="ltr">{E('','')}</div>
          <div class="field full"><label for="f-email"><span data-ar="البريد الإلكتروني">Email</span> <small class="muted" style="text-transform:none;letter-spacing:0" data-ar="(اختياري)">(optional)</small></label><input id="f-email" name="email" type="email" autocomplete="email" placeholder="name@example.com" dir="ltr">{E('','')}</div>
          <div class="field full"><label for="f-svc"><span data-ar="العلاج المطلوب">Treatment</span> <span class="req">*</span></label><select id="f-svc" name="Treatment" required>{opts}</select>{E('','')}</div>
          <div class="field"><label for="f-date"><span data-ar="التاريخ المفضّل">Preferred date</span> <span class="req">*</span></label><input id="f-date" name="Preferred Date" type="date" required>{E('','')}</div>
          <div class="field"><label for="f-time"><span data-ar="الوقت المفضّل">Preferred time</span> <span class="req">*</span></label><select id="f-time" name="Preferred Time" required><option value="" data-ar="اختر الوقت">Select a time</option>{times}</select>{E('','')}</div>
          <fieldset class="field full"><legend data-ar="هل هذه زيارتك الأولى؟">Is this your first visit?</legend>
            <div class="radios">
              <label><input type="radio" name="First Visit" value="Yes" checked><span data-ar="نعم">Yes</span></label>
              <label><input type="radio" name="First Visit" value="No"><span data-ar="لا، زرتكم من قبل">No, I've visited before</span></label>
            </div>
          </fieldset>
          <div class="field full"><label for="f-notes" data-ar="ملاحظات">Notes</label><textarea id="f-notes" name="Notes" placeholder="Tell us briefly about your concern (optional)" data-ar-placeholder="أخبرنا باختصار عن حالتك (اختياري)"></textarea></div>
          <div class="field full"><label class="consent"><input type="checkbox" name="Privacy Consent" value="Agreed" required><span data-ar="أوافق على &lt;a href=&quot;privacy.html&quot;&gt;سياسة الخصوصية&lt;/a&gt; وعلى تواصل العيادة معي بخصوص طلبي.">I agree to the <a href="privacy.html">Privacy Policy</a> and to being contacted by the clinic about my request.</span></label>{E('','')}</div>
        </div>
        <div class="form-foot">
          <small data-ar="سنتواصل معك لتأكيد الموعد.">We'll contact you to confirm your appointment.</small>
          <button type="submit" class="btn"><span class="lbl" data-ar="إرسال الطلب">Send Request</span>{ARROW.replace('<svg','<svg class="arrow"')}</button>
        </div>
      </form>
    </div>
    <aside class="side-card">
      <a class="wa-box wa-link reveal" href="https://wa.me/{WA}" target="_blank" rel="noopener">
        <span class="ic">{BRAND['whatsapp']}</span>
        <span><strong data-ar="تفضّل الحجز السريع؟">Prefer to book instantly?</strong><small data-ar="راسلنا على واتساب">Message us on WhatsApp</small></span>
      </a>
      <div class="side-img reveal-mask">{picture('office-portrait', 'Clinica Neveen reception and consultation office')}</div>
      <div class="info-box reveal">
        <h3 data-ar="معلومات الزيارة">Visit details</h3>
        <div class="row">{icon('clock')}<span data-ar="يومياً، 10 صباحاً – 7 مساءً">Every day, 10 AM – 7 PM</span></div>
        <div class="row">{icon('pin')}<a href="{MAPS}" target="_blank" rel="noopener" data-ar="الدوار السابع، خلف مبنى الملكية الأردنية — عمّان">7th Circle, behind Royal Jordanian building — Amman</a></div>
        <div class="row">{icon('phone')}<a href="tel:+962790163122" class="ltr">0790 163 122</a></div>
      </div>
    </aside>
  </div>
</section>
<section class="section-sm bg-ivory">
  <div class="container narrow">
    <div class="center" style="text-align:center;margin-bottom:40px">{T('Good to know', 'معلومات مهمة', 'div', 'eyebrow both reveal')}<h2 class="split-words" data-ar="قبل أن <em>تحجز</em>">Before you <em>book</em></h2></div>
    <div class="reveal">{acc}</div>
    <p class="center reveal" style="text-align:center;margin-top:36px"><a href="faq.html" class="link-arrow"><span data-ar="جميع الأسئلة الشائعة">All FAQs</span>{ARROW}</a></p>
  </div>
</section>
""" + footer()

def page_hours():
    days = [('Sat', 'Saturday', 'السبت'), ('Sun', 'Sunday', 'الأحد'), ('Mon', 'Monday', 'الاثنين'), ('Tue', 'Tuesday', 'الثلاثاء'),
            ('Wed', 'Wednesday', 'الأربعاء'), ('Thu', 'Thursday', 'الخميس'), ('Fri', 'Friday', 'الجمعة')]
    rows = ''.join(f'<div class="r" data-day="{k}"><span class="d" data-ar="{A(ar)}">{en}</span><span class="t">10:00 AM – 7:00 PM</span></div>' for k, en, ar in days)
    return head('Working Hours | Clinica Neveen', 'ساعات العمل | عيادة الدكتورة نيفين دبابنة',
                'Clinica Neveen is open every day from 10 AM to 7 PM at the 7th Circle, Amman.') + header('working-hours.html') + \
        page_hero('Working Hours', 'ساعات العمل', 'Opening Times', 'أوقات الدوام', 'Open <em>every</em> day for you', 'مفتوحون <em>كل</em> يوم لأجلك',
                  'Seven days a week, including Fridays — so you can find a time that fits your life.',
                  'سبعة أيام في الأسبوع بما فيها الجمعة، لتجد الوقت الذي يناسبك.', 'H') + f"""
<section class="section">
  <div class="container hours-wrap">
    <div>
      <div class="status-pill" data-status><i></i><span>Open daily · 10 AM – 7 PM</span></div>
      <h2 class="split-words" data-ar="يومياً من <em>العاشرة صباحاً</em> حتى السابعة مساءً">10 AM <em>to 7 PM</em>, daily</h2>
      {T('Walk-ins are welcome when the schedule allows, but we recommend booking ahead to secure your preferred time with Dr. Neveen.', 'نرحب بالزيارات المباشرة حسب توفر المواعيد، لكننا ننصح بالحجز المسبق لضمان الوقت المناسب لك مع الدكتورة نيفين.', 'p', 'lead reveal')}
      <div class="hero-ctas reveal" style="margin-top:34px">
        <a href="booking.html" class="btn"><span data-ar="احجز موعدك">Book Appointment</span>{ARROW.replace('<svg','<svg class="arrow"')}</a>
        <a href="https://wa.me/{WA}" class="btn btn-ghost wa-link" target="_blank" rel="noopener">{BRAND['whatsapp']}<span data-ar="واتساب">WhatsApp</span></a>
      </div>
    </div>
    <div class="hours-table reveal" style="--rd:.15s">{rows}</div>
  </div>
</section>
<section class="section-sm bg-ivory">
  <div class="container">
    <div class="note-cards stagger">
      <div class="note"><div class="icon">{icon('moon')}</div>{T('Ramadan hours', 'دوام رمضان', 'h4')}{T('Special opening hours during the holy month will be announced here and on our Instagram.', 'سيتم الإعلان عن ساعات الدوام الخاصة بالشهر الفضيل هنا وعلى حسابنا في إنستغرام.', 'p')}</div>
      <div class="note"><div class="icon">{icon('star')}</div>{T('Public holidays & Eid', 'العطل الرسمية والأعياد', 'h4')}{T('Hours may change on official holidays. Please call or message us to confirm before your visit.', 'قد تتغير ساعات الدوام في العطل الرسمية، يرجى الاتصال أو مراسلتنا للتأكد قبل زيارتك.', 'p')}</div>
      <div class="note"><div class="icon">{icon('calendar')}</div>{T('Best time to visit', 'أفضل وقت للزيارة', 'h4')}{T('Morning appointments are usually calmer. Book ahead for evenings and weekends.', 'المواعيد الصباحية عادةً أهدأ، وننصح بالحجز المسبق للمساء وعطلة نهاية الأسبوع.', 'p')}</div>
    </div>
  </div>
</section>
""" + cta_band() + footer()

FAQ = [
 ('general', 'General', 'أسئلة عامة', [
   ('Do I need a consultation before any treatment?', 'هل أحتاج إلى استشارة قبل أي علاج؟',
    'Yes, for most treatments. A consultation lets Dr. Neveen assess your skin, understand your goals and recommend a safe, personalised plan.',
    'نعم في معظم العلاجات. تتيح الاستشارة للدكتورة نيفين تقييم بشرتك وفهم أهدافك واقتراح خطة آمنة ومخصّصة لك.'),
   ('Who performs the treatments?', 'من يُجري العلاجات؟',
    'Treatments are performed or directly supervised by Dr. Neveen Dababneh, with a medical approach to every procedure.',
    'تُجرى العلاجات من قِبل الدكتورة نيفين دبابنة أو تحت إشرافها المباشر، وبنهج طبي في كل إجراء.'),
   ('How do I know which treatment is right for me?', 'كيف أعرف العلاج المناسب لي؟',
    "You don't need to decide alone. Book a consultation and the doctor will explain your options honestly — including when no treatment is needed.",
    'لا داعي لأن تقرر وحدك. احجز استشارة وستشرح لك الطبيبة الخيارات بكل صدق، حتى لو لم تكن بحاجة لأي علاج.'),
 ]),
 ('injectables', 'Injectables', 'الحقن التجميلية', [
   ('Are injections painful?', 'هل الحقن مؤلمة؟',
    'Most patients describe a mild, brief discomfort. Numbing options and fine needles are used to keep you comfortable.',
    'يصف معظم المرضى شعوراً خفيفاً وقصيراً بعدم الارتياح، ونستخدم خيارات التخدير الموضعي وإبراً دقيقة لراحتك.'),
   ('How long do results last?', 'كم تدوم النتائج؟',
    'It depends on the treatment and on your skin. Anti-wrinkle injections typically last a few months, while fillers usually last longer. The doctor will give you a realistic estimate.',
    'يعتمد ذلك على نوع العلاج وطبيعة بشرتك. عادةً تدوم حقن التجاعيد بضعة أشهر، بينما يدوم الفيلر لفترة أطول، وستعطيك الطبيبة تقديراً واقعياً.'),
   ('Will I look natural?', 'هل سأبدو طبيعياً؟',
    'That is our priority. Our philosophy is subtle enhancement that respects your features and facial balance.',
    'هذه أولويتنا. فلسفتنا هي التحسين الناعم الذي يحترم ملامحك وتوازن وجهك.'),
 ]),
 ('laser', 'Laser', 'الليزر', [
   ('Is laser treatment safe for my skin type?', 'هل الليزر آمن لنوع بشرتي؟',
    'Laser settings are adjusted to your skin and hair type after an assessment, to keep treatment both effective and safe.',
    'تُضبط إعدادات الليزر حسب نوع بشرتك وشعرك بعد التقييم، ليكون العلاج فعّالاً وآمناً.'),
   ('How many sessions will I need?', 'كم جلسة سأحتاج؟',
    'Most laser treatments need a series of sessions. The exact number depends on the area, your skin and your goals.',
    'تحتاج معظم علاجات الليزر إلى عدة جلسات، ويعتمد العدد على المنطقة وطبيعة بشرتك وأهدافك.'),
   ('What should I avoid after a laser session?', 'ما الذي يجب تجنبه بعد جلسة الليزر؟',
    'Avoid direct sun exposure and use sunscreen daily. You will receive clear aftercare instructions after every session.',
    'تجنّب التعرض المباشر للشمس واستخدم واقي الشمس يومياً، وستحصل على تعليمات عناية واضحة بعد كل جلسة.'),
 ]),
 ('visits', 'Booking & Visits', 'الحجز والزيارة', [
   ('Are you open on Fridays?', 'هل تفتحون يوم الجمعة؟',
    'Yes. We are open every day of the week, including Fridays, from 10 AM to 7 PM.',
    'نعم، نحن مفتوحون كل أيام الأسبوع بما فيها الجمعة، من الساعة 10 صباحاً حتى 7 مساءً.'),
   ('How do I book an appointment?', 'كيف أحجز موعداً؟',
    'Use our online booking form, message us on WhatsApp at +962 79 825 3922, or call any of our numbers.',
    'من خلال نموذج الحجز على الموقع، أو مراسلتنا على واتساب ‎+962 79 825 3922، أو الاتصال على أي من أرقامنا.'),
   ('Where exactly is the clinic?', 'أين تقع العيادة بالضبط؟',
    'At the 7th Circle in Amman, behind the Royal Jordanian Airlines building, next to Greater Amman restaurants and opposite Al Sarawat Restaurant.',
    'في الدوار السابع بعمّان، خلف مبنى الملكية الأردنية للطيران، بجانب مطاعم عمّان الكبرى ومقابل مطعم السروات.'),
 ]),
]

def page_faq():
    aside = ''.join(f'<a href="#faq-{k}" data-ar="{A(ar)}">{en}</a>' for k, en, ar, _ in FAQ)
    groups = ''
    for k, en, ar, qs in FAQ:
        acc = ''.join(f'<details class="acc"><summary><span data-ar="{A(qa)}">{q}</span><span class="pm"></span></summary><div class="body">{T(a, aa, "p")}</div></details>' for q, qa, a, aa in qs)
        groups += f'<div class="faq-group reveal" id="faq-{k}">{T(en, ar, "h3")}{acc}</div>'
    return head('FAQ | Clinica Neveen', 'الأسئلة الشائعة | عيادة الدكتورة نيفين دبابنة',
                'Answers to common questions about treatments, laser, injectables and booking at Clinica Neveen, Amman.') + header('faq.html') + \
        page_hero('FAQ', 'الأسئلة الشائعة', 'Questions & Answers', 'أسئلة وأجوبة', 'Everything you <em>wish</em> to know', 'كل ما <em>تودّ</em> معرفته',
                  'Clear, honest answers to the questions we hear most. Can\'t find yours? We\'re one message away.',
                  'إجابات واضحة وصادقة على أكثر الأسئلة شيوعاً. لم تجد سؤالك؟ نحن على بُعد رسالة.', '?') + f"""
<section class="section">
  <div class="container faq-layout">
    <aside class="faq-aside"><nav data-subnav aria-label="FAQ topics">{aside}</nav>
      <a class="wa-box wa-link" style="margin-top:30px" href="https://wa.me/{WA}" target="_blank" rel="noopener"><span class="ic">{BRAND['whatsapp']}</span><span><strong data-ar="لديك سؤال آخر؟">Still have a question?</strong><small data-ar="اسألنا على واتساب">Ask us on WhatsApp</small></span></a>
      <div class="side-img" style="margin-top:18px;aspect-ratio:1/1">{picture('precision', 'Dr. Neveen during a consultation')}</div>
    </aside>
    <div>{groups}</div>
  </div>
</section>
""" + cta_band() + footer()

def page_contact():
    phones = ''.join(f'<li><a href="tel:{t}"><span>{d}</span><small data-ar="{A(lar)}">{len_}</small></a></li>' for d, t, len_, lar in PHONES)
    socials = ''.join(f'<a class="social" href="{u}" target="_blank" rel="noopener"><span class="ic">{BRAND[k]}</span><strong>{n}</strong><small>{h}</small></a>' for k, n, h, u in SOCIALS)
    return head('Contact Us | Clinica Neveen', 'تواصل معنا | عيادة الدكتورة نيفين دبابنة',
                'Contact Clinica Neveen — WhatsApp +962 79 825 3922, phone numbers, location at the 7th Circle Amman and social media.') + header('contact.html') + \
        page_hero('Contact', 'تواصل معنا', 'Get in Touch', 'تواصل معنا', "We'd love to <em>hear</em> from you", 'يسعدنا <em>تواصلك</em> معنا',
                  'Reach us on WhatsApp, call us, or visit the clinic at the 7th Circle — we are open every day.',
                  'راسلنا على واتساب أو اتصل بنا أو زُرنا في الدوار السابع، نحن مفتوحون كل يوم.', 'C') + f"""
<section class="section">
  <div class="container contact-grid stagger">
    <a class="c-card wa wa-link" href="https://wa.me/{WA}" target="_blank" rel="noopener">
      <div><div class="icon">{BRAND['whatsapp']}</div>
      <h3 data-ar="الحجز عبر واتساب">Book on WhatsApp</h3>
      <span class="num">+962 79 825 3922</span>
      <p data-ar="الطريقة الأسرع للحجز والاستفسار، نرد على رسائلك خلال ساعات الدوام.">The fastest way to book and ask questions — we reply during working hours.</p></div>
      <span class="btn btn-gold" style="align-self:flex-start"><span data-ar="ابدأ المحادثة">Start chat</span>{ARROW.replace('<svg','<svg class="arrow"')}</span>
    </a>
    <div class="c-card">
      <div class="icon">{icon('phone')}</div>
      <h3 data-ar="اتصل بنا">Call us</h3>
      <ul class="phones">{phones}</ul>
    </div>
    <a class="c-card" href="mailto:{EMAIL}">
      <div class="icon">{icon('mail')}</div>
      <h3 data-ar="البريد الإلكتروني">Email</h3>
      <p class="ltr" style="color:var(--plum-700);font-size:18px">{EMAIL}</p>
      <span class="link-arrow" style="margin-top:auto"><span data-ar="أرسل رسالة">Send an email</span>{ARROW}</span>
    </a>
    <a class="c-card" href="working-hours.html">
      <div class="icon">{icon('clock')}</div>
      <h3 data-ar="ساعات العمل">Working hours</h3>
      <div class="status-pill" data-status style="margin-bottom:14px"><i></i><span>Open daily</span></div>
      <p data-ar="يومياً بما فيها الجمعة، من 10 صباحاً حتى 7 مساءً.">Every day including Friday, from 10 AM to 7 PM.</p>
      <span class="link-arrow" style="margin-top:auto"><span data-ar="جدول الدوام">Full schedule</span>{ARROW}</span>
    </a>
    <a class="c-card" href="booking.html">
      <div class="icon">{icon('calendar')}</div>
      <h3 data-ar="احجز أونلاين">Book online</h3>
      <p data-ar="املأ نموذج الحجز وسنتواصل معك لتأكيد موعدك.">Fill in the booking form and we'll contact you to confirm.</p>
      <span class="link-arrow" style="margin-top:auto"><span data-ar="نموذج الحجز">Booking form</span>{ARROW}</span>
    </a>
    <div class="map-wrap">
      <div class="addr">
        <div class="icon" style="width:56px;height:56px;border-radius:50%;background:var(--ivory);color:var(--plum-600);display:grid;place-items:center;margin-bottom:22px">{icon('pin')}</div>
        <h3 data-ar="موقع العيادة">Find the clinic</h3>
        <p class="muted" data-ar="{A(ADDR_AR)}">{ADDR_EN}</p>
        <a href="{MAPS}" class="btn" target="_blank" rel="noopener" style="margin-top:12px"><span data-ar="احصل على الاتجاهات">Get Directions</span>{ARROW.replace('<svg','<svg class="arrow"')}</a>
      </div>
      <iframe src="{MAP_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Clinica Neveen location map" allowfullscreen></iframe>
    </div>
  </div>
</section>
<section class="section-sm bg-ivory">
  <div class="container">
    <div class="section-head center" style="text-align:center">
      {T('Follow Us', 'تابعنا', 'div', 'eyebrow both reveal')}
      <h2 class="split-words" data-ar="انضم إلى <em>مجتمعنا</em>">Join our <em>community</em></h2>
      {T('Tips, real cases and offers — shared daily with more than 230,000 followers.', 'نصائح وحالات حقيقية وعروض، نشاركها يومياً مع أكثر من 230 ألف متابع.', 'p', 'lead reveal')}
    </div>
    <div class="socials stagger">{socials}</div>
  </div>
</section>
""" + footer()

def page_privacy():
    secs = [
      ('Who we are', 'من نحن',
       '<p>This website belongs to Clinica Neveen — the clinic of Dr. Neveen Dababneh for dermatology, aesthetics and laser therapy, located at the 7th Circle, Amman, Jordan. For any privacy question, contact us at <a href="mailto:emadnivo@gmail.com">emadnivo@gmail.com</a>.</p>',
       '<p>هذا الموقع تابع لعيادة الدكتورة نيفين دبابنة للأمراض الجلدية والتجميل والعلاج بالليزر، الواقعة في الدوار السابع، عمّان، الأردن. لأي استفسار يتعلق بالخصوصية، تواصل معنا على <a href="mailto:emadnivo@gmail.com">emadnivo@gmail.com</a>.</p>'),
      ('Information we collect', 'المعلومات التي نجمعها',
       '<p>When you submit the booking form, we collect the details you provide: your name, phone number, email (optional), the treatment you are interested in, your preferred date and time, and any notes you choose to share.</p><p>We do not ask for sensitive medical records through this website. Please do not send detailed medical information through the form — we will discuss it with you privately during your consultation.</p>',
       '<p>عند إرسال نموذج الحجز، نجمع البيانات التي تقدّمها: اسمك ورقم هاتفك وبريدك الإلكتروني (اختياري) والعلاج الذي تهتم به والتاريخ والوقت المفضّلين وأي ملاحظات تختار مشاركتها.</p><p>لا نطلب سجلات طبية حساسة عبر هذا الموقع. يرجى عدم إرسال معلومات طبية مفصّلة من خلال النموذج، وسنناقشها معك بخصوصية خلال الاستشارة.</p>'),
      ('How we use it', 'كيف نستخدمها',
       '<ul><li>To contact you and confirm your appointment.</li><li>To prepare for your visit and answer your questions.</li><li>To send a reminder about your appointment, where needed.</li></ul><p>We never sell or rent your personal information.</p>',
       '<ul><li>للتواصل معك وتأكيد موعدك.</li><li>للتحضير لزيارتك والإجابة عن أسئلتك.</li><li>لإرسال تذكير بموعدك عند الحاجة.</li></ul><p>لا نبيع بياناتك الشخصية ولا نؤجّرها لأي جهة.</p>'),
      ('Third-party services', 'خدمات الأطراف الخارجية',
       '<p>Booking requests are delivered to the clinic by email through FormSubmit. The site also uses Google Maps to show our location and Google Fonts for typography; these services may process technical data such as your IP address according to their own policies.</p>',
       '<p>تُرسل طلبات الحجز إلى بريد العيادة عبر خدمة FormSubmit. كما يستخدم الموقع خرائط جوجل لعرض موقعنا وخطوط جوجل للتصميم، وقد تعالج هذه الخدمات بيانات تقنية مثل عنوان IP وفقاً لسياساتها الخاصة.</p>'),
      ('Photos & patient consent', 'الصور وموافقة المرضى',
       '<p>Before & after photos are published only with the written consent of our patients. Patients may withdraw their consent at any time and the photos will be removed.</p>',
       '<p>تُنشر صور قبل وبعد فقط بموافقة خطية من المرضى، ويحق للمريض سحب موافقته في أي وقت وسيتم حذف الصور.</p>'),
      ('Your rights', 'حقوقك',
       '<p>You may ask us at any time to access, correct or delete the information you have sent us. Contact us by email or WhatsApp and we will respond promptly.</p>',
       '<p>يحق لك في أي وقت أن تطلب الاطلاع على بياناتك أو تصحيحها أو حذفها. تواصل معنا عبر البريد الإلكتروني أو واتساب وسنرد عليك سريعاً.</p>'),
      ('Updates', 'التحديثات',
       '<p>We may update this policy from time to time. The latest version will always be available on this page.</p>',
       '<p>قد نقوم بتحديث هذه السياسة من وقت لآخر، وستكون أحدث نسخة متاحة دائماً على هذه الصفحة.</p>'),
    ]
    body = ''.join(f'{T(en, ar, "h2")}<div data-ar="{A(bar)}">{ben}</div>' for en, ar, ben, bar in secs)
    return head('Privacy Policy | Clinica Neveen', 'سياسة الخصوصية | عيادة الدكتورة نيفين دبابنة',
                'Privacy policy of Clinica Neveen — how booking information is collected and used.') + header('privacy.html') + \
        page_hero('Privacy Policy', 'سياسة الخصوصية', 'Your Privacy', 'خصوصيتك', 'Your trust, <em>protected</em>', 'ثقتك <em>محميّة</em>',
                  'How we collect, use and protect the information you share with us.', 'كيف نجمع المعلومات التي تشاركها معنا ونستخدمها ونحميها.', 'P') + f"""
<section class="section">
  <div class="container narrow prose reveal">{body}
    <p class="muted" style="margin-top:50px;font-size:14px" data-ar="آخر تحديث: نوفمبر 2026">Last updated: November 2026</p>
  </div>
</section>
""" + footer()

def page_thanks():
    return head('Request Received | Clinica Neveen', 'تم استلام طلبك | عيادة الدكتورة نيفين دبابنة', 'Thank you — your booking request has been received.') + header('') + f"""
<section class="hero grain" style="min-height:92svh">
  <div class="container narrow center" style="text-align:center">
    <div class="divider-orn reveal">{icon('heart','1.2')}</div>
    {T('Request Received', 'تم استلام طلبك', 'div', 'eyebrow both reveal')}
    <h1 class="split-words" data-ar="شكراً <em>لك</em>">Thank <em>you</em></h1>
    {T('Your booking request has reached us. Our team will contact you shortly by phone or WhatsApp to confirm your appointment.',
       'وصلنا طلب الحجز الخاص بك، وسيتواصل معك فريقنا قريباً عبر الهاتف أو واتساب لتأكيد موعدك.', 'p', 'lead reveal', 'style="--rd:.25s;margin-inline:auto"')}
    <div class="hero-ctas reveal" style="justify-content:center;margin-top:30px;--rd:.4s">
      <a href="index.html" class="btn" data-ar="العودة للرئيسية">Back to Home</a>
      <a href="https://wa.me/{WA}" class="btn btn-ghost wa-link" target="_blank" rel="noopener">{BRAND['whatsapp']}<span data-ar="واتساب">WhatsApp</span></a>
    </div>
  </div>
  {butterflies([('20%','15%',51,18,0,.85,'g'),('65%','80%',41,16,-4,.75,'p'),('35%','88%',35,14,-2,.7,'g')])}
</section>
""" + footer()

PAGES = {
  'index.html': page_home, 'services.html': page_services, 'before-after.html': page_before_after,
  'booking.html': page_booking, 'working-hours.html': page_hours, 'faq.html': page_faq,
  'contact.html': page_contact, 'privacy.html': page_privacy, 'thank-you.html': page_thanks,
}
for name, fn in PAGES.items():
    with open(os.path.join(OUT, name), 'w', encoding='utf-8') as f:
        f.write(fn())
    print('built', name)
