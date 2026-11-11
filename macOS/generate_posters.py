#!/usr/bin/env python3
"""
Generate App Store promotional posters (2560x1600) for every App Store locale.

Striking design language:
  - Deep space background with a cinematic black hole BELOW the app icon:
      · Central event horizon (pure black sphere)
      · Soft orange accretion disk (layered radial-gradient donut, tilted edge-on)
      · Doppler-boosted hot arc (conic-gradient, screen blend)
      · Luminous photon ring hugging the event horizon
      · Star field + colorful nebula dust + vignette
      · Subtle aurora band along the disk equator
  - Bright white app name with warm glow (easily readable)
  - Solar-system icon floating ABOVE the black hole:
      the 7 classic planets on orbit rings + Pluto as the 8th, outermost
  - The 4 translated slogan chips (广告词) stacked on the LEFT of the black hole
  - The 4 feature cards stacked on the RIGHT of the black hole
  - Top badge: brand name "Ayiyahei" (啊咿呀嘿 for Chinese) left of "ayiyahei.com",
      rendered in an artistic script font
  - No text / marquee at the bottom

Output: preview/<language-folder>/promo.png
"""
import json, os, glob, subprocess, sys, html

ROOT = '/Users/zhangsaidong/Desktop/macProject/project/work/AISnapshotSource/Flutter/AISnapshot/aisnapshot/aisnapshot'
PREVIEW = os.path.join(ROOT, 'docs/AppReview/macOS/preview')
LOCALES = os.path.join(ROOT, 'docs/AppReview/macOS/promoLocales/all_locales.json')
LOCALE_DIR = os.path.join(ROOT, 'assets/locales')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
OUT_W, OUT_H = 2560, 1600

FOLDER_MAP = {
    '阿拉伯文': '阿拉伯语', '孟加拉语': '孟加拉语', '加泰罗尼亚语': '加泰罗尼亚语',
    '简体中文': '简体中文', '繁体中文': '繁体中文', '克罗地亚语': '克罗地亚语',
    '捷克语': '捷克语', '丹麦语': '丹麦语', '荷兰文': '荷兰语',
    '英文（澳大利亚）': '英语', '英文（加拿大）': '英语', '英文（英国）': '英语', '英文（美国）': '英语',
    '芬兰语': '芬兰语', '法文': '法语', '法文（加拿大）': '法语', '德文': '德语',
    '希腊语': '希腊语', '古吉拉特语': '古吉拉特语', '希伯来语': '希伯来语',
    '北印度语': '北印度语', '匈牙利语': '匈牙利语', '印度尼西亚语': '印度尼西亚语',
    '意大利语': '意大利语', '日语': '日语', '坎纳达语': '坎纳达语',
    '韩语': '韩语', '马来语': '马来语', '马拉雅拉姆语': '马拉雅拉姆语',
    '马拉地语': '马拉地语', '挪威语': '挪威语', '奥里亚语': '奥里亚语',
    '波兰语': '波兰语', '葡萄牙文（巴西）': '葡萄牙语', '葡萄牙文（葡萄牙）': '葡萄牙语',
    '旁遮普文': '旁遮普语', '罗马尼亚语': '罗马尼亚语', '俄语': '俄语',
    '斯洛伐克语': '斯洛伐克语', '斯洛文尼亚文': '斯洛文尼亚语',
    '西班牙语（墨西哥）': '西班牙语', '西班牙文（西班牙）': '西班牙语',
    '瑞典语': '瑞典语', '泰米尔文': '泰米尔语', '泰卢固文': '泰卢固语',
    '泰语': '泰语', '土耳其语': '土耳其语', '乌克兰语': '乌克兰语',
    '乌尔都文': '乌尔都语', '越南语': '越南语',
}

LOCALE_JSON = {
    'ar':'ar','bn':'bn','ca':'ca','zh-Hans':'zh_CN','zh-Hant':'zh_TW',
    'hr':'hr','cs':'cs','da':'da','nl':'nl',
    'en-AU':'en','en-CA':'en','en-GB':'en','en-US':'en',
    'fi':'fi','fr':'fr','fr-CA':'fr','de':'de',
    'el':'el','gu':'gu','he':'he','hi':'hi',
    'hu':'hu','id':'id','it':'it','ja':'ja',
    'kn':'kn','ko':'ko','ms':'ms','ml':'ml',
    'mr':'mr','nb':'no','or':'or','pl':'pl',
    'pt-BR':'pt','pt-PT':'pt','pa':'pa','ro':'ro',
    'ru':'ru','sk':'sk','sl':'sl',
    'es-MX':'es','es-ES':'es',
    'sv':'sv','ta':'ta','te':'te','th':'th',
    'tr':'tr','uk':'uk','ur':'ur','vi':'vi',
}

RTL = {'ar','ur','he'}
def is_rtl(locale):
    base = locale.split('-')[0].lower()
    return base in RTL

PALETTES = {
    'en':   ['#06B6D4', '#6366F1', '#8B5CF6', '#22D3EE'],
    'ar':   ['#F59E0B', '#EF4444', '#8B5CF6', '#FCD34D'],
    'bn':   ['#EC4899', '#8B5CF6', '#06B6D4', '#F472B6'],
    'ca':   ['#10B981', '#06B6D4', '#F59E0B', '#34D399'],
    'zh-Hans': ['#EF4444', '#F59E0B', '#EC4899', '#FB923C'],
    'zh-Hant': ['#F472B6', '#A855F7', '#3B82F6', '#FB7185'],
    'hr':   ['#3B82F6', '#8B5CF6', '#EC4899', '#60A5FA'],
    'cs':   ['#0EA5E9', '#6366F1', '#10B981', '#38BDF8'],
    'da':   ['#EF4444', '#F59E0B', '#06B6D4', '#FB923C'],
    'nl':   ['#F97316', '#EF4444', '#8B5CF6', '#FB923C'],
    'fi':   ['#0EA5E9', '#06B6D4', '#6366F1', '#22D3EE'],
    'fr':   ['#3B82F6', '#8B5CF6', '#EC4899', '#60A5FA'],
    'de':   ['#FACC15', '#EF4444', '#1F2937', '#FDE047'],
    'el':   ['#06B6D4', '#3B82F6', '#10B981', '#22D3EE'],
    'gu':   ['#F59E0B', '#EF4444', '#8B5CF6', '#FBBF24'],
    'he':   ['#8B5CF6', '#EC4899', '#3B82F6', '#A78BFA'],
    'hi':   ['#F97316', '#EF4444', '#A855F7', '#FB923C'],
    'hu':   ['#10B981', '#06B6D4', '#3B82F6', '#34D399'],
    'id':   ['#EF4444', '#F59E0B', '#06B6D4', '#FB923C'],
    'it':   ['#10B981', '#84CC16', '#F59E0B', '#34D399'],
    'ja':   ['#EC4899', '#8B5CF6', '#3B82F6', '#F472B6'],
    'kn':   ['#F59E0B', '#EF4444', '#A855F7', '#FBBF24'],
    'ko':   ['#A855F7', '#EC4899', '#3B82F6', '#C084FC'],
    'ms':   ['#0EA5E9', '#F59E0B', '#10B981', '#38BDF8'],
    'ml':   ['#10B981', '#84CC16', '#F59E0B', '#34D399'],
    'mr':   ['#F97316', '#EC4899', '#6366F1', '#FB923C'],
    'nb':   ['#EF4444', '#3B82F6', '#8B5CF6', '#FB923C'],
    'or':   ['#A855F7', '#EC4899', '#06B6D4', '#C084FC'],
    'pl':   ['#DC2626', '#F59E0B', '#10B981', '#FB923C'],
    'pt':   ['#10B981', '#F59E0B', '#3B82F6', '#34D399'],
    'pa':   ['#F97316', '#EF4444', '#A855F7', '#FB923C'],
    'ro':   ['#3B82F6', '#F59E0B', '#EF4444', '#60A5FA'],
    'ru':   ['#DC2626', '#1E40AF', '#F59E0B', '#FCA5A5'],
    'sk':   ['#0EA5E9', '#6366F1', '#10B981', '#38BDF8'],
    'sl':   ['#8B5CF6', '#EC4899', '#06B6D4', '#A78BFA'],
    'es':   ['#FACC15', '#EF4444', '#F97316', '#FDE047'],
    'sv':   ['#3B82F6', '#FACC15', '#06B6D4', '#60A5FA'],
    'ta':   ['#F59E0B', '#EF4444', '#8B5CF6', '#FBBF24'],
    'te':   ['#10B981', '#F59E0B', '#A855F7', '#34D399'],
    'th':   ['#A855F7', '#EC4899', '#3B82F6', '#C084FC'],
    'tr':   ['#EF4444', '#F59E0B', '#06B6D4', '#FB923C'],
    'uk':   ['#3B82F6', '#FACC15', '#06B6D4', '#60A5FA'],
    'ur':   ['#10B981', '#F59E0B', '#EC4899', '#34D399'],
    'vi':   ['#EF4444', '#FACC15', '#06B6D4', '#FB923C'],
}

def is_zh(locale):
    base = locale.split('-')[0].lower()
    return base == 'zh'

def palette_for(locale):
    jp = LOCALE_JSON.get(locale, 'en')
    return PALETTES.get(jp, PALETTES['en'])

# Vivid per-locale gradient overrides for the hero text (app name + subtitle).
# When a locale is listed here, the app name and subtitle use these 5 stops
# instead of the palette c1..c4. Designed to be more striking than the default.
#
# Chinese locales use a soft pastel 莫兰迪 (Morandi) neon rainbow — light,
# dreamy mid-saturation stops (powder pink → peach → butter yellow → lavender
# → sky blue) that pair with thin 圆体 rounded fonts for an airy 手帐/治愈系
# vibe. Each stop is ~30% lighter than the previous saturated rainbow.
GRADIENT = {
    'zh-Hans': ['#FFB3C8', '#FFCFA8', '#FFEAA8', '#C9B8F0', '#A8D8F0'],
    'zh-Hant': ['#FFB1D1', '#FFC9A5', '#FFE89C', '#C5B0F2', '#A2D5F2'],
    'zh_CN':   ['#FFB3C8', '#FFCFA8', '#FFEAA8', '#C9B8F0', '#A8D8F0'],
    'zh_TW':   ['#FFB1D1', '#FFC9A5', '#FFE89C', '#C5B0F2', '#A2D5F2'],
}

def gradient_for(locale):
    base = locale.split('-')[0].lower()
    if base == 'zh':
        region = locale.split('-')[1] if '-' in locale else 'Hans'
        jp = 'zh-Hans' if region in ('Hans', 'CN') else 'zh-Hant'
        return GRADIENT.get(jp, GRADIENT['zh-Hans'])
    jp = LOCALE_JSON.get(locale, base)
    return GRADIENT.get(jp)  # None -> caller falls back to c1..c4

# 4 slogans per locale. Order is fixed:
#   0: Capture Anything   (截图)
#   1: Record Everything  (录屏)
#   2: Annotate Instantly (标注)
#   3: Edit Like a Pro    (修图)
SLOGANS = {
    'ar':      ['التقط كل شيء', 'سجّل كل شيء', 'علّق فورًا', 'حرّر باحتراف'],
    'bn':      ['সবকিছু ক্যাপচার করুন', 'সবকিছু রেকর্ড করুন', 'তাৎক্ষণিক টীকা', 'প্রফের মতো সম্পাদনা'],
    'ca':      ['Captura-ho tot', 'Enregistra-ho tot', 'Anota a l’instant', 'Edita com un pro'],
    'zh-Hans': ['一切皆可截', '声画全能录', '标注零等待', '修图如行云'],
    'zh-Hant': ['一切皆可截', '聲畫全能錄', '標註零等待', '修圖如行雲'],
    'hr':      ['Uhvati sve', 'Snimi sve', 'Anotiraj odmah', 'Uredi kao profesionalac'],
    'cs':      ['Zachyť vše', 'Nahraj vše', 'Anotuj hned', 'Upravuj jako profík'],
    'da':      ['Fang alt', 'Optag alt', 'Annotér med det samme', 'Redigér som en professionel'],
    'nl':      ['Leg alles vast', 'Neem alles op', 'Annoteer direct', 'Bewerk als een pro'],
    'en':      ['Capture Anything', 'Record Everything', 'Annotate Instantly', 'Edit Like a Pro'],
    'fi':      ['Kaappaa kaikki', 'Tallenna kaikki', 'Merkitse heti', 'Muokkaa kuin ammattilainen'],
    'fr':      ['Tout capturer', 'Tout enregistrer', 'Annoter instantanément', 'Retoucher comme un pro'],
    'de':      ['Alles erfassen', 'Alles aufnehmen', 'Sofort kommentieren', 'Wie ein Profi bearbeiten'],
    'el':      ['Στιγμιότυπο για όλα', 'Εγγραφή για όλα', 'Σχολίασε αμέσως', 'Επεξεργασία σαν επαγγελματίας'],
    'gu':      ['બધું કેપ્ચર કરો', 'બધું રેકોર્ડ કરો', 'તરત ટીકા કરો', 'પ્રો જેવું એડિટ'],
    'he':      ['לכוד הכול', 'הקלט הכול', 'הוסף הערות מיד', 'ערוך כמו מקצוען'],
    'hi':      ['सब कुछ कैप्चर करें', 'सब कुछ रिकॉर्ड करें', 'तुरंत एनोटेट करें', 'प्रो की तरह एडिट करें'],
    'hu':      ['Rögzíts mindent', 'Vegyél fel mindent', 'Annotálj azonnal', 'Szerkessz profi módon'],
    'id':      ['Tangkap Segalanya', 'Rekam Segalanya', 'Anotasi Seketika', 'Edit Seperti Pro'],
    'it':      ['Cattura tutto', 'Registra tutto', 'Annota subito', 'Edita come un pro'],
    'ja':      ['すべてをキャプチャ', 'すべてを録画', 'すぐに注釈', 'プロのように編集'],
    'kn':      ['ಎಲ್ಲವನ್ನೂ ಕ್ಯಾಪ್ಚರ್ ಮಾಡಿ', 'ಎಲ್ಲವನ್ನೂ ರೆಕಾರ್ಡ್ ಮಾಡಿ', 'ತಕ್ಷಣ ಟಿಪ್ಪಣಿ', 'ಪ್ರೊ ನಂತೆ ಎಡಿಟ್'],
    'ko':      ['모든 것을 캡처', '모든 것을 녹화', '바로 주석', '프로처럼 편집'],
    'ms':      ['Tangkap Semua', 'Rakam Semua', 'Anotasi Segera', 'Edit Seperti Pro'],
    'ml':      ['എല്ലാം ക്യാപ്ചർ ചെയ്യൂ', 'എല്ലാം റെക്കോർഡ് ചെയ്യൂ', 'ഉടനെ അനോട്ടേറ്റ് ചെയ്യൂ', 'പ്രോ പോലെ എഡിറ്റ്'],
    'mr':      ['सगळे कॅप्चर करा', 'सगळे रेकॉर्ड करा', 'लगेच ॲनोटेशन', 'प्रो सारखे एडिट'],
    'nb':      ['Fang alt', 'Ta opp alt', 'Annoter med én gang', 'Rediger som en proff'],
    'or':      ['ସବୁ କ୍ୟାପ୍ଚର କରନ୍ତୁ', 'ସବୁ ରେକର୍ଡ କରନ୍ତୁ', 'ତୁରନ୍ତ ଆନୋଟେସନ', 'ପ୍ରୋ ଭଳି ଏଡିଟ'],
    'pl':      ['Uchwyć wszystko', 'Nagraj wszystko', 'Adnotuj od razu', 'Edytuj jak pro'],
    'pt':      ['Capture tudo', 'Grave tudo', 'Anote agora', 'Edite como um pro'],
    'pa':      ['ਸਭ ਕੁਝ ਕੈਪਚਰ ਕਰੋ', 'ਸਭ ਕੁਝ ਰਿਕਾਰਡ ਕਰੋ', 'ਤੁਰੰਤ ਟਿੱਪਣੀ', 'ਪ੍ਰੋ ਵਾਂਗ ਸੰਪਾਦਨ'],
    'ro':      ['Capturează tot', 'Înregistrează tot', 'Adnotează instant', 'Editează ca un profesionist'],
    'ru':      ['Снимай всё', 'Записывай всё', 'Помечай мгновенно', 'Редактируй как про'],
    'sk':      ['Zachyť všetko', 'Nahraj všetko', 'Anotuj hneď', 'Upravuj ako profík'],
    'sl':      ['Zajemi vse', 'Posnemi vse', 'Anotiraj takoj', 'Uredi kot profesionalec'],
    'es':      ['Captura todo', 'Graba todo', 'Anota al instante', 'Edita como un pro'],
    'sv':      ['Fånga allt', 'Spela in allt', 'Annotera direkt', 'Redigera som ett proffs'],
    'ta':      ['அனைத்தையும் கேப்சர்', 'அனைத்தையும் பதிவு', 'உடனே சிறுகுறிப்பு', 'ப்ரோ போல் எடிட்'],
    'te':      ['అన్నీ క్యాప్చర్ చేయండి', 'అన్నీ రికార్డ్ చేయండి', 'వెంటనే యానోటేషన్', 'ప్రోలా ఎడిట్'],
    'th':      ['จับภาพทุกอย่าง', 'บันทึกทุกอย่าง', 'ใส่คำอธิบายทันที', 'ตกแต่งอย่างมือโปร'],
    'tr':      ['Her şeyi yakala', 'Her şeyi kaydet', 'Anında not ekle', 'Profesyonel gibi düzenle'],
    'uk':      ['Захоплюй усе', 'Записуй усе', 'Анотуй миттєво', 'Редагуй як профі'],
    'ur':      ['سب کچھ کیپچر کریں', 'سب کچڈ ریکارڈ کریں', 'فوری طور پر تشریح', 'پرو کی طرح ترمیم'],
    'vi':      ['Chụp mọi thứ', 'Quay mọi thứ', 'Chú thích ngay', 'Chỉnh như dân chuyên'],
}

# Brand name localisation. The App Store brand is "Ayiyahei"; for Chinese
# locales we show the phonetic transliteration 啊咿呀嘿 (traditional for zh-Hant).
BRAND = {
    'zh-Hans': '啊咿呀嘿',
    'zh-Hant': '啊咿呀嘿',
    'zh_CN': '啊咿呀嘿',
    'zh_TW': '啊咿呀嘿',
}

def brand_for(locale):
    base = locale.split('-')[0].lower()
    if base == 'zh':
        region = locale.split('-')[1] if '-' in locale else 'Hans'
        jp = 'zh-Hans' if region in ('Hans', 'CN') else 'zh-Hant'
        return BRAND.get(jp, BRAND['zh-Hans'])
    jp = LOCALE_JSON.get(locale, base)
    return BRAND.get(jp, BRAND.get(base, 'Ayiyahei'))

def slogans_for(locale):
    # The SLOGANS keys are the JSON-keys used in PALETTES (zh-Hans / zh-Hant / en).
    # LOCALE_JSON maps Apple locale -> JSON-key, but Chinese locales there are
    # zh_CN / zh_TW, so resolve via the PALETTES-known short codes.
    base = locale.split('-')[0].lower()
    if base == 'zh':
        region = locale.split('-')[1] if '-' in locale else 'Hans'
        jp = 'zh-Hans' if region in ('Hans', 'CN') else 'zh-Hant'
    else:
        jp = LOCALE_JSON.get(locale, base)
    return SLOGANS.get(jp, SLOGANS.get(base, SLOGANS['en']))

def get_all_locales():
    return json.load(open(LOCALES, encoding='utf-8'))

def get_features(locale):
    jp = LOCALE_JSON.get(locale)
    if not jp:
        return None
    p = os.path.join(LOCALE_DIR, f'{jp}.json')
    if not os.path.exists(p):
        return None
    d = json.load(open(p, encoding='utf-8'))
    return [d.get(f'about_feature_{i}', '').lstrip('• ').strip() for i in range(1, 7)]

def hex_to_rgba(h, a):
    h = h.lstrip('#')
    if len(h) == 3:
        h = ''.join(c*2 for c in h)
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return f'rgba({r},{g},{b},{a})'

def build_html(item, features, rtl, slogans):
    app_name = html.escape(item['应用名称'])
    subtitle = html.escape(item['副标题'])
    locale = item['locale']
    zh = is_zh(locale)
    p = palette_for(locale)
    c1, c2, c3, c4 = p[0], p[1], p[2], p[3]
    g = gradient_for(locale)
    if g:
        g1, g2, g3, g4, g5 = g
    else:
        g1, g2, g3, g4, g5 = c4, c1, c2, c3, '#ffffff'
    dir_attr = 'rtl' if rtl else 'ltr'

    # Thin / 细软 rounded 圆体 (round-style) font stack for Chinese locales.
    # Soft, light-weight geometric round fonts evoke 手帐 (journaling) and
    # 治愈系 (healing-style) cover art — light strokes, generous apertures,
    # and round terminals. macOS 11+: 站酷小薇LOGO体 rounded; iOS: Hiragino
    # Maru Gothic ProN round; web fallback to 思源柔黑 Source Han Sans HW +
    # 阿里巴巴普惠体 light + OPPO Sans Rounded + HarmonyOS Sans rounded for
    # the characteristic 圆角 terminals.
    if zh:
        body_font = ('-apple-system, BlinkMacSystemFont, '
                     '"Hiragino Maru Gothic ProN", "ヒラギノ丸ゴ ProN", '
                     '"Yuanti SC", "圆体", "站酷小薇LOGO体", '
                     '"ZCOOL XiaoWei", '
                     '"Source Han Sans HW", "思源柔黑", '
                     '"Noto Sans CJK SC Light", "Noto Sans SC Light", '
                     '"Source Han Sans CN Light", '
                     '"Alibaba PuHuiTi Light", "阿里巴巴普惠体 Light", '
                     '"HarmonyOS Sans SC Light", '
                     '"OPPO Sans Rounded", '
                     '"PingFang SC Light", "PingFang SC", '
                     '"Microsoft YaHei Light", "微软雅黑 Light", '
                     '"Microsoft YaHei", "微软雅黑", sans-serif')
        brush_font = ('"Hiragino Maru Gothic ProN","ヒラギノ丸ゴ ProN",'
                      '"Yuanti SC","圆体","ZCOOL XiaoWei","站酷小薇LOGO体",'
                      '"Source Han Sans HW","思源柔黑",'
                      '"Noto Sans CJK SC Light","Noto Sans SC Light",'
                      '"Alibaba PuHuiTi Light","HarmonyOS Sans SC Light",'
                      '"OPPO Sans Rounded","PingFang SC Light",'
                      '"PingFang SC",sans-serif')
        # Letter spacing & weight tuned for CJK glyph density at light weight.
        hero_letter_spacing = '0.18em'
        hero_font_weight = 300
        sub_letter_spacing = '0.32em'
        sub_font_weight = 300
        chip_letter_spacing = '0.18em'
        chip_font_weight = 300
        card_letter_spacing = '0.15em'
        card_font_weight = 300
        # Brand badge typography — 4-char 啊咿呀嘿 reads as 圆体 rounded sans,
        # not calligraphic. Use light weight at large size with wide tracking
        # so the rounded glyphs feel airy and dreamy.
        brand_font = ('"Hiragino Maru Gothic ProN","ヒラギノ丸ゴ ProN",'
                      '"Yuanti SC","圆体","ZCOOL XiaoWei","站酷小薇LOGO体",'
                      '"Source Han Sans HW","思源柔黑",'
                      '"Noto Sans CJK SC Light","Noto Sans SC Light",'
                      '"Alibaba PuHuiTi Light","HarmonyOS Sans SC Light",'
                      '"OPPO Sans Rounded","PingFang SC Light",'
                      '"PingFang SC",sans-serif')
        brand_size = 152
        brand_letter_spacing = '0.42em'
        brand_rotate = 0
    else:
        body_font = ('-apple-system, BlinkMacSystemFont, "SF Pro Display", '
                     '"Helvetica Neue", "Segoe UI", "Arial Unicode MS", '
                     '"PingFang SC", "Hiragino Sans GB", "Apple SD Gothic Neo", '
                     '"Microsoft YaHei", sans-serif')
        brush_font = ('"Snell Roundhand","Allura","Great Vibes","Pinyon Script",'
                      '"Apple Chancery","Savoye LET","Brush Script MT",'
                      '"Bradley Hand",cursive')
        hero_letter_spacing = '-0.02em'
        hero_font_weight = 900
        sub_letter_spacing = '0.025em'
        sub_font_weight = 600
        chip_letter_spacing = '0.02em'
        chip_font_weight = 400
        card_letter_spacing = '0.01em'
        card_font_weight = 400
        brand_font = ('"Snell Roundhand","Savoye LET","Allura","Great Vibes",'
                      '"Pinyon Script","Apple Chancery","Brush Script MT",'
                      '"Bradley Hand",cursive')
        brand_size = 112
        brand_letter_spacing = '0.01em'
        brand_rotate = -2.5

    feats = [f for f in (features or []) if f][:4]
    if not feats:
        feats = ['Full screen capture', 'Window capture', 'OCR text extraction', 'Annotation tools']

    brand = brand_for(locale)

    icons = ['◉', '✦', '◈', '✧']

    # All 4 feature cards on the RIGHT of the black hole (no icon, no box)
    def card(i, ftext):
        return (f'<div class="card">'
                f'<div class="card-text">{html.escape(ftext)}</div>'
                f'</div>')
    right_cards = '\n'.join(card(i, f) for i, f in enumerate(feats))

    # 4 slogan chips (广告词) stacked on the LEFT of the black hole
    def chip(i, text):
        return (f'<div class="chip">'
                f'<span class="chip-text">{html.escape(text)}</span>'
                f'</div>')
    chips = '\n'.join(chip(i, s) for i, s in enumerate(slogans))

    html_str = f'''<!doctype html><html dir="{dir_attr}" lang="{html.escape(locale)}">
<head><meta charset="utf-8"><style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html,body {{ width:{OUT_W}px; height:{OUT_H}px; overflow:hidden;
    font-family:{body_font}; }}

  .canvas {{ position:relative; width:{OUT_W}px; height:{OUT_H}px;
    background: radial-gradient(ellipse at 50% 58%, #1a0a1a 0%, #0a0510 34%, #02000a 70%, #000005 100%);
    overflow:hidden; }}

  /* === Star field === */
  .stars {{ position:absolute; inset:0; background-image:
      radial-gradient(circle at 1px 1px, rgba(255,255,255,0.95) 1.2px, transparent 0),
      radial-gradient(circle at 1px 1px, rgba(255,255,255,0.7) 0.9px, transparent 0),
      radial-gradient(circle at 1px 1px, rgba(255,255,255,0.5) 0.7px, transparent 0);
    background-size: 120px 120px, 80px 80px, 45px 45px;
    background-position: 0 0, 30px 50px, 10px 20px;
    opacity:0.85; mix-blend-mode:screen; }}
  .stars-big {{ position:absolute; inset:0; background-image:
      radial-gradient(circle at 2px 2px, rgba(255,240,220,1) 2px, transparent 0),
      radial-gradient(circle at 2px 2px, rgba(200,220,255,1) 1.6px, transparent 0),
      radial-gradient(circle at 2px 2px, rgba(255,200,180,1) 1.4px, transparent 0);
    background-size: 400px 400px, 320px 320px, 260px 260px;
    background-position: 60px 80px, 200px 40px, 130px 220px;
    opacity:0.6; mix-blend-mode:screen; }}

  /* === Distant nebula (palette tinted) === */
  .nebula {{ position:absolute; inset:0;
    background:
      radial-gradient(ellipse at 15% 20%, {hex_to_rgba(c1, 0.18)} 0%, transparent 35%),
      radial-gradient(ellipse at 85% 25%, {hex_to_rgba(c2, 0.16)} 0%, transparent 38%),
      radial-gradient(ellipse at 20% 82%, {hex_to_rgba(c3, 0.14)} 0%, transparent 40%),
      radial-gradient(ellipse at 80% 88%, {hex_to_rgba(c4, 0.18)} 0%, transparent 42%);
    mix-blend-mode:screen; filter:blur(40px); }}

  /* === Black hole (BELOW the icon) === */
  .hole {{ position:absolute; left:50%; top:72%; transform:translate(-50%,-50%);
    width:0; height:0; }}

  /* Smooth tilted accretion disk: layered donut, edge-on */
  .disk {{ position:absolute; left:50%; top:50%; width:1320px; height:1320px; border-radius:50%;
    transform: translate(-50%,-50%) rotateX(70deg);
    background: radial-gradient(circle at 50% 50%,
      transparent 24%,
      rgba(255,120,40,0.12) 31%,
      rgba(255,150,60,0.55) 36%,
      rgba(255,195,110,0.95) 41%,
      rgba(255,150,55,0.85) 46%,
      rgba(214,84,30,0.55) 50%,
      rgba(150,55,20,0.30) 55%,
      rgba(90,35,15,0.12) 60%,
      transparent 66%);
    filter: blur(7px); }}

  /* Doppler-boosted hot arc on one side of the disk */
  .disk-hot {{ position:absolute; left:50%; top:50%; width:1320px; height:1320px; border-radius:50%;
    transform: translate(-50%,-50%) rotateX(70deg);
    background: conic-gradient(from -50deg at 50% 50%,
      transparent 0deg, transparent 90deg,
      rgba(255,235,180,0.85) 140deg,
      rgba(255,175,75,0.90) 175deg,
      rgba(255,125,45,0.60) 210deg,
      rgba(205,75,28,0.28) 250deg,
      transparent 300deg, transparent 360deg);
    mix-blend-mode: screen;
    -webkit-mask: radial-gradient(circle, transparent 24%, #000 33%, #000 60%, transparent 66%);
    mask: radial-gradient(circle, transparent 24%, #000 33%, #000 60%, transparent 66%);
    filter: blur(12px); }}

  /* Photon ring hugging the event horizon */
  .photon-ring {{ position:absolute; left:50%; top:50%; width:540px; height:540px; border-radius:50%;
    transform: translate(-50%,-50%);
    background: radial-gradient(circle at 50% 50%,
      transparent 44%,
      rgba(255,215,150,0.95) 49%,
      rgba(255,155,60,0.85) 51%,
      transparent 56%);
    box-shadow: 0 0 40px 6px rgba(255,195,115,0.7), 0 0 110px 24px rgba(255,135,50,0.45);
    filter: blur(1.5px); }}

  /* Event horizon: pure black sphere with warm rim */
  .event-horizon {{ position:absolute; left:50%; top:50%; width:480px; height:480px; border-radius:50%;
    transform: translate(-50%,-50%);
    background: radial-gradient(circle at 40% 32%, #1c0d06 0%, #080303 30%, #000000 62%);
    box-shadow:
      0 0 0 2px #000,
      0 0 50px 4px rgba(0,0,0,0.95),
      0 0 110px 30px rgba(0,0,0,0.6); }}

  /* Horizontal lens flare across the bright side */
  .flare {{ position:absolute; left:50%; top:50%; width:1500px; height:180px;
    transform: translate(-50%,-50%);
    background: linear-gradient(90deg, transparent 32%, rgba(255,190,100,0.16) 48%, rgba(255,225,160,0.32) 52%, rgba(255,190,100,0.16) 56%, transparent 72%);
    filter: blur(22px); }}

  /* Aurora band along the disk equator (subtle) */
  .aurora {{ position:absolute; left:50%; top:50%; width:1700px; height:46px;
    transform: translate(-50%,-50%) rotateX(70deg);
    background: linear-gradient(90deg,
      transparent 0%,
      {hex_to_rgba(c2, 0.35)} 25%,
      {hex_to_rgba(c1, 0.55)} 50%,
      {hex_to_rgba(c4, 0.35)} 75%,
      transparent 100%);
    filter: blur(28px); mix-blend-mode: screen; opacity:0.85; }}

  /* Vignette */
  .vignette {{ position:absolute; inset:0; pointer-events:none;
    background: radial-gradient(ellipse at 50% 58%, transparent 34%, rgba(0,0,0,0.5) 74%, #000 100%); }}

  /* === UI layer === */
  .content {{ position:absolute; inset:0; display:flex; flex-direction:column; align-items:center;
    z-index:10; pointer-events:none; }}

  .hero-top {{ margin-top:84px; display:flex; flex-direction:column; align-items:center; text-align:center;
    max-width:2240px; pointer-events:auto; }}

  /* Badge: artistic brand name on the left, domain on the right */
  .badge {{ display:inline-flex; align-items:baseline; gap:30px; padding:0; background:transparent;
    border:0; box-shadow:none; margin-bottom:36px; }}
  .badge-dot {{ width:14px; height:14px; border-radius:50%; background:{c4};
    box-shadow:0 0 24px {hex_to_rgba(c4, 0.95)}; align-self:center; }}
  .badge-brand {{ font-family:{brand_font};
    font-size:{brand_size}px; font-weight:{hero_font_weight}; line-height:1;
    background:linear-gradient(100deg, #fff 15%, {hex_to_rgba(c2, 1.0)} 55%, #fff 90%);
    -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; color:{c2};
    filter:drop-shadow(0 2px 22px rgba(0,0,0,0.8));
    transform:rotate({brand_rotate}deg);
    /* Generous padding so the first/last glyph (y, i descenders/ascenders in
       "Ayiyahei") never get clipped by the badge container or adjacent text. */
    padding: 8px 36px;
    display:inline-block;
    /* Disable kerning-pulling on cursive fonts that visually swallow y/i. */
    text-rendering: geometricPrecision;
    letter-spacing:{brand_letter_spacing};
    /* Force a wider bounding box than the text so calligraphic descenders
       (the tail of y) and dots of i never bleed into neighbouring elements. */
    overflow:visible;
    white-space:nowrap;
    /* For Latin script: lift the baseline so descender of y has room. */
    {('padding-top: 28px; padding-bottom: 36px;' if not zh else '')} }}
  .badge-sep {{ display:none; }}
  .badge-domain {{ font-size:38px; font-weight:700; color:#fff; letter-spacing:0.10em;
    text-shadow:0 2px 18px rgba(0,0,0,0.85); }}

  /* Bright, readable app name with a vivid multi-stop neon gradient */
  .appname {{ font-size:128px; font-weight:{hero_font_weight}; letter-spacing:{hero_letter_spacing}; line-height:1.04;
    background: linear-gradient(95deg,
      #ffffff 0%, {g1} 18%, {g2} 38%, {g3} 58%, {g4} 78%, {g5} 100%);
    -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; color:transparent;
    filter:
      drop-shadow(0 0 22px {hex_to_rgba(g1, 0.90)})
      drop-shadow(0 0 40px {hex_to_rgba(g2, 0.60)})
      drop-shadow(0 6px 32px rgba(0,0,0,0.9)); }}

  .subtitle {{ margin-top:24px; font-size:48px; font-weight:{sub_font_weight}; letter-spacing:{sub_letter_spacing}; line-height:1.3;
    background: linear-gradient(95deg,
      #ffffff 0%, {g1} 25%, {g2} 50%, {g3} 75%, {g4} 100%);
    -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; color:transparent;
    filter:
      drop-shadow(0 0 16px {hex_to_rgba(g1, 0.75)})
      drop-shadow(0 0 32px {hex_to_rgba(g2, 0.50)})
      drop-shadow(0 2px 22px rgba(0,0,0,0.9)); }}

  /* === Solar system icon ABOVE the black hole === */
  .solarsys {{ position:absolute; left:50%; top:42%; transform:translate(-50%,-50%);
    width:420px; height:420px; z-index:11; pointer-events:none; }}
  .orbit {{ position:absolute; left:50%; top:50%; border-radius:50%; border:1px solid rgba(255,255,255,0.18);
    transform:translate(-50%,-50%); }}
  .o1  {{ width:80px;   height:80px;   }}
  .o2  {{ width:130px;  height:130px; }}
  .o3  {{ width:185px;  height:185px; }}
  .o4  {{ width:240px;  height:240px; }}
  .o5  {{ width:300px;  height:300px; }}
  .o6  {{ width:355px;  height:355px; }}
  .o7  {{ width:398px;  height:398px; }}
  .o8  {{ width:438px;  height:438px; }}
  .planet {{ position:absolute; border-radius:50%; }}
  /* Mercury – grey */
  .p1 {{ width:12px; height:12px; top:50%; left:50%;
    transform:translate(-50%,-50%) translateX(-40px);
    background:radial-gradient(circle at 35% 35%, #ccc, #888); box-shadow:0 0 8px rgba(180,180,180,0.5); }}
  /* Venus – pale yellow */
  .p2 {{ width:16px; height:16px; top:50%; left:50%;
    transform:translate(-50%,-50%) translateX(65px);
    background:radial-gradient(circle at 35% 35%, #f5e090, #d4b840); box-shadow:0 0 10px rgba(220,195,60,0.55); }}
  /* Earth – blue/green */
  .p3 {{ width:17px; height:17px; top:50%; left:50%;
    transform:translate(-50%,-50%) translateX(-92.5px);
    background:radial-gradient(circle at 38% 35%, #6ab4ff, #2a7bc8 45%, #1a9040);
    box-shadow:0 0 10px rgba(80,160,255,0.55); }}
  /* Mars – rust red */
  .p4 {{ width:13px; height:13px; top:50%; left:50%;
    transform:translate(-50%,-50%) translateX(120px);
    background:radial-gradient(circle at 35% 35%, #e07050, #a83820); box-shadow:0 0 8px rgba(210,80,40,0.5); }}
  /* Jupiter – orange banded */
  .p5 {{ width:28px; height:28px; top:50%; left:50%;
    transform:translate(-50%,-50%) translateX(-150px);
    background:repeating-linear-gradient(0deg, #d09030 0%, #b07020 20%, #c08030 40%, #a86020 60%, #d09030 80%);
    border-radius:50%; box-shadow:0 0 14px rgba(210,130,40,0.65); }}
  /* Saturn – gold + ring */
  .p6 {{ width:24px; height:24px; top:50%; left:50%;
    transform:translate(-50%,-50%) translateX(177.5px);
    background:radial-gradient(circle at 38% 35%, #f5d070, #c8a030);
    box-shadow:0 0 12px rgba(245,200,80,0.6); }}
  .satring {{ position:absolute; top:50%; left:50%;
    transform:translate(-50%,-50%) translateX(177.5px);
    width:46px; height:12px; border-radius:50%;
    background:transparent;
    border:2px solid rgba(230,195,100,0.55);
    box-shadow:0 0 0 1px rgba(200,165,70,0.25); }}
  /* Uranus – cyan */
  .p7 {{ width:20px; height:20px; top:50%; left:50%;
    transform:translate(-50%,-50%) translateX(-199px);
    background:radial-gradient(circle at 38% 35%, #a0f0ff, #38b8d8);
    box-shadow:0 0 12px rgba(100,220,255,0.55); }}
  /* Neptune – deep blue */
  .p8 {{ width:19px; height:19px; top:50%; left:50%;
    transform:translate(-50%,-50%) translateX(219px);
    background:radial-gradient(circle at 38% 35%, #5070ff, #1828c8);
    box-shadow:0 0 11px rgba(60,100,255,0.55); }}
  /* Sun – warm glow at centre */
  .sun {{ position:absolute; left:50%; top:50%; width:28px; height:28px;
    transform:translate(-50%,-50%);
    background:radial-gradient(circle at 40% 38%, #fff8d0, #ffcc30, #ff8800);
    border-radius:50%; box-shadow:0 0 28px 8px rgba(255,180,40,0.75), 0 0 60px 18px rgba(255,130,20,0.35); }}

  /* Slogan chips — VERTICAL stack on the LEFT of the black hole (opaque, bigger, no icon) */
  .chips {{ position:absolute; top:74%; left:90px; transform:translateY(-50%);
    display:flex; flex-direction:column; gap:22px; z-index:11; pointer-events:auto; }}
  .chip {{ display:flex; align-items:center; justify-content:center;
    padding:0; background:transparent; border:0; box-shadow:none;
    box-sizing:border-box; }}
  .chip-text {{
    font-family:{brush_font};
    font-size:60px; font-weight:{chip_font_weight}; line-height:1;
    background: linear-gradient(95deg, #fff 0%, {hex_to_rgba(c1, 1.0)} 45%, {hex_to_rgba(c2, 1.0)} 100%);
    -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; color:transparent;
    white-space:nowrap; letter-spacing:{chip_letter_spacing};
    filter: drop-shadow(0 2px 14px rgba(0,0,0,0.75))
            drop-shadow(0 0 18px {hex_to_rgba(c1, 0.45)}); }}

  /* Feature cards — VERTICAL stack on the RIGHT of the black hole (opaque, bigger text) */
  .cards {{ position:absolute; top:74%; right:90px; transform:translateY(-50%);
    display:flex; flex-direction:column; gap:20px; z-index:11; pointer-events:auto; }}
  .card {{ display:flex; align-items:center; gap:0; padding:0; width:540px;
    background:transparent; border:0; box-shadow:none;
    box-sizing:border-box; }}
  .card-icon {{ font-size:46px; font-weight:400; line-height:1; flex:0 0 auto;
    filter: drop-shadow(0 0 18px {hex_to_rgba(c4, 0.6)}); }}
  .card-text {{
    font-family:{brush_font};
    font-size:56px; font-weight:{card_font_weight}; line-height:1.2; text-align:start;
    background: linear-gradient(95deg, #fff 0%, {hex_to_rgba(c3, 1.0)} 55%, {hex_to_rgba(c1, 1.0)} 100%);
    -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent; color:transparent;
    letter-spacing:{card_letter_spacing};
    filter: drop-shadow(0 2px 16px rgba(0,0,0,0.8))
            drop-shadow(0 0 18px {hex_to_rgba(c3, 0.40)}); }}
</style></head><body>
  <div class="canvas">
    <div class="stars"></div>
    <div class="stars-big"></div>
    <div class="nebula"></div>

    <div class="hole">
      <div class="disk"></div>
      <div class="disk-hot"></div>
      <div class="aurora"></div>
      <div class="photon-ring"></div>
      <div class="event-horizon"></div>
      <div class="flare"></div>
    </div>

    <div class="vignette"></div>

    <div class="content">
      <div class="hero-top">
        <div class="badge">
          <span class="badge-brand">{brand}</span>
        </div>
        <div class="appname">{app_name}</div>
        <div class="subtitle">{subtitle}</div>
      </div>
    </div>

    <!-- Solar system above the black hole -->
    <div class="solarsys">
      <div class="sun"></div>
      <div class="orbit o1"><div class="planet p1"></div></div>
      <div class="orbit o2"><div class="planet p2"></div></div>
      <div class="orbit o3"><div class="planet p3"></div></div>
      <div class="orbit o4"><div class="planet p4"></div></div>
      <div class="orbit o5"><div class="planet p5"></div></div>
      <div class="orbit o6"><div class="planet p6"></div><div class="satring"></div></div>
      <div class="orbit o7"><div class="planet p7"></div></div>
      <div class="orbit o8"><div class="planet p8"></div></div>
    </div>

    <!-- Slogans on the LEFT of the black hole -->
    <div class="chips">
{chips}
    </div>

    <!-- Feature cards on the RIGHT of the black hole -->
    <div class="cards">
{right_cards}
    </div>
  </div>
</body></html>'''
    return html_str

def render(html_str, out_path):
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    tmp_html = '/tmp/promo_render.html'
    with open(tmp_html, 'w', encoding='utf-8') as f:
        f.write(html_str)
    cmd = [
        CHROME, '--headless=new', '--disable-gpu', '--hide-scrollbars',
        '--force-device-scale-factor=1', '--window-size=%d,%d' % (OUT_W, OUT_H),
        '--screenshot=%s' % out_path,
        'file://' + tmp_html,
    ]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if not os.path.exists(out_path):
        print('  RENDER FAILED:', r.stderr[-400:])
        return False
    from PIL import Image
    im = Image.open(out_path)
    if im.size != (OUT_W, OUT_H):
        print('  BAD SIZE:', im.size, r.stderr[-200:])
        return False
    return True

def main():
    all_locs = get_all_locales()
    ok, fail = 0, 0
    for item in all_locs:
        locale = item['locale']
        folder = FOLDER_MAP.get(item['语言'])
        features = get_features(locale)
        if not features:
            features = get_features('en-US')
        slogans = slogans_for(locale)
        rtl = is_rtl(locale)
        html_str = build_html(item, features or [], rtl, slogans)
        out_dir = os.path.join(PREVIEW, folder) if folder else os.path.join(PREVIEW, locale)
        out_path = os.path.join(out_dir, 'promo.png')
        if render(html_str, out_path):
            ok += 1
            print('  OK   %-10s -> %s' % (locale, os.path.relpath(out_path)))
        else:
            fail += 1
            print('  FAIL %-10s' % locale)
    print(f'\nDone. OK={ok} FAIL={fail}')

if __name__ == '__main__':
    main()
