#!/usr/bin/env python3
"""
"Ishga tushish tokini (I_kr) topish" - ilmiy tushuntirish DOCX.
Faqat standart kutubxonalar.
"""
import zipfile
import os
from xml.sax.saxutils import escape

OUT_FILE = "Ishga_tushish_tokini_topish.docx"

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>
<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>
</Types>'''

RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>
</Relationships>'''

DOC_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>
</Relationships>'''

STYLES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:docDefaults>
<w:rPrDefault><w:rPr><w:rFonts w:ascii="Times New Roman" w:hAnsi="Times New Roman" w:cs="Times New Roman"/><w:sz w:val="24"/><w:szCs w:val="24"/><w:lang w:val="uz-Latn-UZ"/></w:rPr></w:rPrDefault>
<w:pPrDefault><w:pPr><w:spacing w:line="360" w:lineRule="auto" w:after="120"/></w:pPr></w:pPrDefault>
</w:docDefaults>
<w:style w:type="paragraph" w:default="1" w:styleId="Normal"><w:name w:val="Normal"/></w:style>
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="30"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Formula"><w:name w:val="Formula"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="120"/></w:pPr><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:i/><w:sz w:val="28"/></w:rPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:basedOn w:val="TableNormal"/></w:style>
<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/></w:style>
</w:styles>'''


def p(text, bold=False, italic=False, align=None):
    align_xml = f'<w:jc w:val="{align}"/>' if align else ''
    rpr = ''
    if bold or italic:
        rpr = '<w:rPr>'
        if bold: rpr += '<w:b/>'
        if italic: rpr += '<w:i/>'
        rpr += '</w:rPr>'
    return f'<w:p><w:pPr>{align_xml}</w:pPr><w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def h1(text):
    return f'<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def h2(text):
    return f'<w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr><w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def formula(text):
    return f'<w:p><w:pPr><w:pStyle w:val="Formula"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:i/><w:sz w:val="28"/></w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def fraction(numerator, denominator, prefix='', suffix=''):
    """Word OMML matematik kasr (chiroyli ko'rinish)."""
    def run(t):
        return f'<m:r><m:rPr><m:sty m:val="i"/></m:rPr><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:sz w:val="28"/></w:rPr><m:t xml:space="preserve">{escape(t)}</m:t></m:r>'
    pre = run(prefix) if prefix else ''
    suf = run(suffix) if suffix else ''
    frac = (
        '<m:f><m:fPr><m:ctrlPr><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:i/></w:rPr></m:ctrlPr></m:fPr>'
        f'<m:num>{run(numerator)}</m:num>'
        f'<m:den>{run(denominator)}</m:den></m:f>'
    )
    return (
        '<w:p><w:pPr><w:jc w:val="center"/></w:pPr>'
        '<m:oMathPara><m:oMath>'
        f'{pre}{frac}{suf}'
        '</m:oMath></m:oMathPara></w:p>'
    )


def bullet(text):
    return f'<w:p><w:pPr><w:ind w:left="360"/></w:pPr><w:r><w:t xml:space="preserve">- {escape(text)}</w:t></w:r></w:p>'


def table(headers, rows, col_widths=None):
    n = len(headers)
    if not col_widths:
        col_widths = [9000 // n] * n
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in col_widths)
    hc = ''
    for i, hd in enumerate(headers):
        hc += f'<w:tc><w:tcPr><w:tcW w:w="{col_widths[i]}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{escape(hd)}</w:t></w:r></w:p></w:tc>'
    hr = f'<w:tr><w:trPr><w:tblHeader/></w:trPr>{hc}</w:tr>'
    dr = ''
    for row in rows:
        cs = ''
        for i, v in enumerate(row):
            cs += f'<w:tc><w:tcPr><w:tcW w:w="{col_widths[i]}" w:type="dxa"/></w:tcPr><w:p><w:r><w:t xml:space="preserve">{escape(str(v))}</w:t></w:r></w:p></w:tc>'
        dr += f'<w:tr>{cs}</w:tr>'
    borders = '<w:tblBorders><w:top w:val="single" w:sz="4" w:color="000000"/><w:left w:val="single" w:sz="4" w:color="000000"/><w:bottom w:val="single" w:sz="4" w:color="000000"/><w:right w:val="single" w:sz="4" w:color="000000"/><w:insideH w:val="single" w:sz="4" w:color="000000"/><w:insideV w:val="single" w:sz="4" w:color="000000"/></w:tblBorders>'
    return f'<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/>{borders}</w:tblPr><w:tblGrid>{grid}</w:tblGrid>{hr}{dr}</w:tbl><w:p/>'


# ============================================================
body = []

body.append(p("ISHGA TUSHISH TOKINI (I_kr) TOPISH METODIKASI", bold=True, align="center"))
body.append(p("Yuklanishdan himoya bosqichi uchun ishga tushish tokini asoslash", italic=True, align="center"))
body.append(p("AVM-MP mikroprotsessorli himoya qurilmasi", italic=True, align="center"))
body.append(p(""))

# 1
body.append(h1("1. To'liq formula"))
body.append(p(
    "Yuklanishdan himoya bosqichida ishga tushish toki I_kr maksimal tok himoyasining "
    "(МТЗ - максимальная токовая защита) klassik formulasi bo'yicha aniqlanadi. "
    "Bu formula ishga tushish tokini nominal (ishchi) tokdan ishonchli zaxira bilan "
    "ajratish (otstroyka) tamoyiliga asoslanadi:"
))
body.append(fraction("k_nad . k_szp", "k_v", suffix=" . I_nom"))
body.append(p("Chiziqli ko'rinishda:"))
body.append(formula("I_kr = (k_nad x k_szp / k_v) x I_nom"))

# 2
body.append(h1("2. Formula belgilarining ma'nosi"))
body.append(table(
    ["Belgi", "Ma'nosi", "Qiymat", "Tanlash asosi"],
    [
        ["I_kr",   "Ishga tushish (kritik) toki",         "topiladi", "Hisoblanadi"],
        ["I_nom",  "Nominal (ishchi) tok",                "5 A",      "Loyiha qiymati"],
        ["k_nad",  "Ishonchlilik koeffitsiyenti",         "1,2",      "Yolg'on ishlamaslik zaxirasi"],
        ["k_szp",  "O'z-o'zidan ishga tushish koeff.",    "1,0",      "Motor yuki yo'q -> 1,0"],
        ["k_v",    "Qaytish koeffitsiyenti",              "0,96",     "Raqamli rele (ESP32)"],
    ],
    [1400, 3200, 1400, 3000]
))

# 2.1 koeffitsiyentlar izohi
body.append(h2("2.1. k_nad - ishonchlilik koeffitsiyenti"))
body.append(p(
    "Himoya normal ishchi tokda ishlamasligi, lekin undan biroz yuqorida ishonchli "
    "ishga tushishi uchun zaxira. Manbalarga ko'ra k_nad = 1,1...1,2 oralig'ida olinadi. "
    "AVM-MP uchun yuqori chegara (1,2) tanlandi - bu ko'proq ishonchlilik beradi."
))

body.append(h2("2.2. k_szp - o'z-o'zidan ishga tushish koeffitsiyenti"))
body.append(p(
    "Bu koeffitsiyent zanjirda elektr dvigatellar bo'lganda, ular birvarakayiga "
    "ishga tushganda yuzaga keladigan tok sakrashini hisobga oladi. Yo'l transformatori "
    "zanjirida bunday dvigatel yuki bo'lmagani uchun k_szp = 1,0 qabul qilinadi."
))

body.append(h2("2.3. k_v - qaytish koeffitsiyenti (nega kerak?)"))
body.append(p(
    "Himoyada ikkita chegara mavjud: ishga tushish toki (himoya yoqiladi) va qaytish "
    "toki (himoya o'chadi, normal holatga qaytadi). Bu ikki tok bir xil emas - qaytish "
    "toki har doim biroz pastroq. Ularning nisbati qaytish koeffitsiyenti deyiladi:"
))
body.append(fraction("I_qaytish", "I_ishga_tushish", prefix="k_v = "))
body.append(p(
    "Agar tok vaqtincha ko'tarilib, keyin yana normalga qaytsa, himoya ishonchli o'chishi "
    "kerak. Buni kafolatlash uchun ishga tushish toki biroz balandroq olinadi - shuning "
    "uchun k_v formulada maxrajda turadi. Eski elektromexanik releda k_v = 0,85, "
    "zamonaviy raqamli releda esa k_v = 0,96...0,98 (deyarli ideal). Bu raqamli qurilmaning "
    "afzalligi - himoyani sezgirroq sozlash imkonini beradi."
))

# 3
body.append(h1("3. Hisoblash (5 A nominal tok misolida)"))
body.append(p("3.1-qadam. Qiymatlarni formulaga qo'yamiz:"))
body.append(fraction("1,2 . 1,0", "0,96", suffix=" . 5 A"))
body.append(p("3.2-qadam. Avval koeffitsiyentlarni hisoblaymiz:"))
body.append(formula("1,2 x 1,0 = 1,2"))
body.append(formula("1,2 / 0,96 = 1,25"))
body.append(p("3.3-qadam. Natijani nominal tokka ko'paytiramiz:"))
body.append(formula("I_kr = 1,25 x 5 A = 6,25 A"))

# 4
body.append(h1("4. Natija"))
body.append(p("Yuklanishdan himoya bosqichining ishga tushish toki:", bold=True))
body.append(formula("I_kr = 1,25 x I_nom = 6,25 A"))
body.append(p(
    "Ya'ni, zanjir toki 6,25 A dan oshganda yuklanishdan himoya bosqichi ishga tushadi "
    "(va inversion vaqt tavsifi bo'yicha hisob boshlanadi).", bold=True
))

# 5
body.append(h1("5. Barcha nominal toklar uchun I_kr qiymatlari"))
body.append(table(
    ["Nominal tok I_nom", "Koeffitsiyent", "Ishga tushish toki I_kr"],
    [
        ["3 A",   "1,25", "3,75 A"],
        ["5 A",   "1,25", "6,25 A"],
        ["7,5 A", "1,25", "9,4 A"],
        ["10 A",  "1,25", "12,5 A"],
        ["15 A",  "1,25", "18,75 A"],
    ]
))

# 6
body.append(h1("6. 1,25 koeffitsiyentining qo'shimcha asoslari"))
body.append(p(
    "1,25 qiymati ikki tomonlama asoslangan. Birinchidan, yuqoridagi МТЗ formulasidan "
    "(k_nad/k_v = 1,2/0,96 = 1,25) kelib chiqadi. Ikkinchidan, klassik AVM-2 qurilmasining "
    "ma'lumotnomasi (Сороко, 2.4-band) qurilma quyidagi yuklarda uzilmasligini ko'rsatadi: "
    "3 A da 1,3.Iн, 5-10 A da 1,4.Iн, 15 A da 1,2.Iн. Eng kichik chegara 1,2.Iн bo'lib, "
    "1,25.Iн qiymati AVM-2 bilan moslikni saqlaydi va barcha nominal toklar uchun universal "
    "ishonchli qiymat hisoblanadi."
))

# Manba
body.append(h1("Foydalanilgan manbalar"))
body.append(p("1. Чернобровов Н.В. Релейная защита: Учебное пособие для техникумов. - 5-е изд. - М.: Энергия, 1974. - «Максимальная токовая защита» bobi."))
body.append(p("2. Шабад М.А. Расчёты релейной защиты и автоматики распределительных сетей. - Л.: Энергоатомиздат."))
body.append(p("3. Федосеев А.М. Релейная защита электроэнергетических систем. - М.: Энергоатомиздат."))
body.append(p("4. Сороко В.И., Фотькина Ж.В. Аппаратура железнодорожной автоматики и телемеханики: Справочник. Кн.3. - М.: НПФ «ПЛАНЕТА», 2013. - 2.4-band."))
body.append(p("5. Правила устройства электроустановок (ПУЭ). - Релейная защита bo'limi."))


DOCUMENT_XML = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
    'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
    '<w:body>'
    + ''.join(body) +
    '<w:sectPr><w:pgSz w:w="11906" w:h="16838"/>'
    '<w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1701" w:header="708" w:footer="708" w:gutter="0"/>'
    '</w:sectPr></w:body></w:document>'
)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUT_FILE)
with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', CONTENT_TYPES)
    z.writestr('_rels/.rels', RELS)
    z.writestr('word/_rels/document.xml.rels', DOC_RELS)
    z.writestr('word/styles.xml', STYLES)
    z.writestr('word/document.xml', DOCUMENT_XML)

print(f"OK: {out_path}")
print(f"Size: {os.path.getsize(out_path)} bytes")
