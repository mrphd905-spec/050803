#!/usr/bin/env python3
"""
EMA filtrlash haqida ilmiy tushuntirish — Word hujjat (DOCX) yaratuvchi.
Faqat standart kutubxonalardan foydalanadi.
"""
import zipfile
import os
from xml.sax.saxutils import escape

OUT_FILE = "EMA_filtrlash_AVM_MP.docx"

# ============================================================
# DOCX uchun kerakli minimal XML fayllar
# ============================================================

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
<w:style w:type="paragraph" w:styleId="Heading1"><w:name w:val="heading 1"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:before="240" w:after="120"/><w:outlineLvl w:val="0"/></w:pPr><w:rPr><w:b/><w:sz w:val="32"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading2"><w:name w:val="heading 2"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:before="200" w:after="100"/><w:outlineLvl w:val="1"/></w:pPr><w:rPr><w:b/><w:sz w:val="28"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Heading3"><w:name w:val="heading 3"/><w:basedOn w:val="Normal"/><w:next w:val="Normal"/><w:pPr><w:spacing w:before="160" w:after="80"/><w:outlineLvl w:val="2"/></w:pPr><w:rPr><w:b/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Formula"><w:name w:val="Formula"/><w:basedOn w:val="Normal"/><w:pPr><w:jc w:val="center"/><w:spacing w:before="120" w:after="120"/></w:pPr><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:i/><w:sz w:val="26"/></w:rPr></w:style>
<w:style w:type="paragraph" w:styleId="Code"><w:name w:val="Code"/><w:basedOn w:val="Normal"/><w:pPr><w:spacing w:before="80" w:after="80"/><w:ind w:left="284"/></w:pPr><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/><w:sz w:val="22"/></w:rPr></w:style>
<w:style w:type="table" w:styleId="TableGrid"><w:name w:val="Table Grid"/><w:basedOn w:val="TableNormal"/><w:tblPr><w:tblBorders><w:top w:val="single" w:sz="4" w:color="000000"/><w:left w:val="single" w:sz="4" w:color="000000"/><w:bottom w:val="single" w:sz="4" w:color="000000"/><w:right w:val="single" w:sz="4" w:color="000000"/><w:insideH w:val="single" w:sz="4" w:color="000000"/><w:insideV w:val="single" w:sz="4" w:color="000000"/></w:tblBorders></w:tblPr></w:style>
<w:style w:type="table" w:default="1" w:styleId="TableNormal"><w:name w:val="Normal Table"/></w:style>
</w:styles>'''


# ============================================================
# Helper funksiyalar — paragraf, sarlavha, jadval va h.k. yaratish
# ============================================================

def p(text, style=None, bold=False, italic=False, align=None):
    """Oddiy paragraf yaratadi."""
    style_xml = f'<w:pStyle w:val="{style}"/>' if style else ''
    align_xml = f'<w:jc w:val="{align}"/>' if align else ''
    rpr = ''
    if bold or italic:
        rpr = '<w:rPr>'
        if bold: rpr += '<w:b/>'
        if italic: rpr += '<w:i/>'
        rpr += '</w:rPr>'
    return f'<w:p><w:pPr>{style_xml}{align_xml}</w:pPr><w:r>{rpr}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def h1(text):
    return f'<w:p><w:pPr><w:pStyle w:val="Heading1"/></w:pPr><w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def h2(text):
    return f'<w:p><w:pPr><w:pStyle w:val="Heading2"/></w:pPr><w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def h3(text):
    return f'<w:p><w:pPr><w:pStyle w:val="Heading3"/></w:pPr><w:r><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def formula(text):
    """Markazlashgan formula."""
    return f'<w:p><w:pPr><w:pStyle w:val="Formula"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Cambria Math" w:hAnsi="Cambria Math"/><w:i/><w:sz w:val="28"/></w:rPr><w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>'


def code(text):
    """Kod / monospace bloki."""
    lines = text.split('\n')
    out = []
    for line in lines:
        out.append(f'<w:p><w:pPr><w:pStyle w:val="Code"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Consolas" w:hAnsi="Consolas"/></w:rPr><w:t xml:space="preserve">{escape(line)}</w:t></w:r></w:p>')
    return ''.join(out)


def bullet(text):
    return f'<w:p><w:pPr><w:ind w:left="360"/></w:pPr><w:r><w:t xml:space="preserve">• {escape(text)}</w:t></w:r></w:p>'


def table(headers, rows, col_widths=None):
    """Jadval yaratadi."""
    n_cols = len(headers)
    if not col_widths:
        col_widths = [9000 // n_cols] * n_cols

    # tblGrid
    grid = ''.join(f'<w:gridCol w:w="{w}"/>' for w in col_widths)

    # Sarlavha qator
    header_cells = ''
    for i, hd in enumerate(headers):
        header_cells += f'''<w:tc><w:tcPr><w:tcW w:w="{col_widths[i]}" w:type="dxa"/><w:shd w:val="clear" w:color="auto" w:fill="D9E2F3"/></w:tcPr><w:p><w:pPr><w:jc w:val="center"/></w:pPr><w:r><w:rPr><w:b/></w:rPr><w:t xml:space="preserve">{escape(hd)}</w:t></w:r></w:p></w:tc>'''
    header_row = f'<w:tr><w:trPr><w:tblHeader/></w:trPr>{header_cells}</w:tr>'

    # Ma'lumot qatorlar
    data_rows = ''
    for row in rows:
        cells = ''
        for i, val in enumerate(row):
            cells += f'''<w:tc><w:tcPr><w:tcW w:w="{col_widths[i]}" w:type="dxa"/></w:tcPr><w:p><w:r><w:t xml:space="preserve">{escape(str(val))}</w:t></w:r></w:p></w:tc>'''
        data_rows += f'<w:tr>{cells}</w:tr>'

    return f'''<w:tbl><w:tblPr><w:tblStyle w:val="TableGrid"/><w:tblW w:w="0" w:type="auto"/><w:tblBorders><w:top w:val="single" w:sz="4" w:color="000000"/><w:left w:val="single" w:sz="4" w:color="000000"/><w:bottom w:val="single" w:sz="4" w:color="000000"/><w:right w:val="single" w:sz="4" w:color="000000"/><w:insideH w:val="single" w:sz="4" w:color="000000"/><w:insideV w:val="single" w:sz="4" w:color="000000"/></w:tblBorders></w:tblPr><w:tblGrid>{grid}</w:tblGrid>{header_row}{data_rows}</w:tbl><w:p/>'''


# ============================================================
# DOCX hujjat tarkibi
# ============================================================

body_parts = []

# === Sarlavha ===
body_parts.append(p("MUSTAQIL TADQIQOT ISHIDAN UCHUN ILMIY TUSHUNTIRISH", bold=True, align="center"))
body_parts.append(p("Mavzu: AVM-MP himoya qurilmasida EMA filtrlash usulining qadamlar soni va aniqligi o'rtasidagi bog'liqlik", bold=True, align="center"))
body_parts.append(p("Yo'nalish: Temir yo'l avtomatika va telemexanikasi", italic=True, align="center"))
body_parts.append(p("", ))

# === KIRISH ===
body_parts.append(h1("1. KIRISH"))
body_parts.append(p(
    "Mikroprotsessorli AVM-MP himoya qurilmasida ACS724-50A tok datchigidan kelgan signal "
    "ESP32 mikrokontrollerining 12-bitli analog-raqamli o'zgartkichi (ADC) orqali "
    "raqamlashtiriladi. Bu signalda har doim tashqi ta'sirlardan kelib chiqadigan shovqin "
    "(elektromagnit halaqitlar, tarmoq chastotasi gum, kvantlash xatoligi) mavjud bo'ladi."
))
body_parts.append(p(
    "Shovqinni kamaytirish va aniq di/dt qiymatini olish uchun raqamli filtrlash usuli — "
    "Eksponensial siljiydigan o'rtacha (EMA — Exponential Moving Average) qo'llanadi."
))

# === EMA FORMULASI ===
body_parts.append(h1("2. EMA FILTR FORMULASI"))
body_parts.append(p("EMA filtrining asosiy rekurrent tenglamasi:"))
body_parts.append(formula("If[k] = α · Iraw[k] + (1 − α) · If[k−1]"))

body_parts.append(p("Bu yerda:"))
body_parts.append(bullet("Iraw[k] — ACS724 dan kelgan k-namunadagi xom (filtrlanmagan) tok qiymati"))
body_parts.append(bullet("If[k] — k-namunadagi filtrlangan tok qiymati"))
body_parts.append(bullet("If[k−1] — oldingi (k−1) namunadagi filtrlangan qiymat (xotira)"))
body_parts.append(bullet("α — silliqlash koeffitsiyenti, 0 < α ≤ 1"))
body_parts.append(bullet("k — namuna nomeri (diskret vaqt indeksi)"))

body_parts.append(p("Filtrlangan signaldan di/dt parametrini hisoblash:"))
body_parts.append(formula("di/dt[k] = (If[k] − If[k−1]) / Δt"))
body_parts.append(p("bu yerda Δt — namunalar orasidagi vaqt oralig'i (sampling period). "
                    "AVM-MP uchun tipik qiymat: Δt = 50 µs (chastota 20 kHz)."))

# === QADAMLAR SONI ===
body_parts.append(h1("3. QADAMLAR SONI (N) — TUSHUNCHA"))
body_parts.append(p(
    "EMA filtrida \"qadamlar soni\" deganda filtrning ekvivalent o'rtachalash oynasi tushuniladi. "
    "Bu α koeffitsiyenti orqali quyidagicha aniqlanadi:"
))
body_parts.append(formula("N_eff = (2 / α) − 1"))
body_parts.append(p("yoki teskari ifodada:"))
body_parts.append(formula("α = 2 / (N_eff + 1)"))

body_parts.append(p("Qadamlar soni va silliqlash koeffitsiyenti orasidagi muvofiqlik jadvali:"))
body_parts.append(table(
    ["α (silliqlash)", "N_eff (qadamlar)", "Vaqt doimiysi τ, µs (Δt=50µs)"],
    [
        ["1.0", "1", "50 (filtrsiz)"],
        ["0.5", "3", "100"],
        ["0.3", "5–6", "170"],
        ["0.2", "9", "250"],
        ["0.1", "19", "500"],
        ["0.05", "39", "1 000"],
    ]
))

# === ANIQLIK ===
body_parts.append(h1("4. ANIQLIK NIMA SABABDAN OSHADI?"))
body_parts.append(p(
    "Qadamlar soni N oshgan sari aniqlik oshadi. Buning matematik asoslangan UCH ASOSIY SABABI mavjud."
))

# Sabab 1
body_parts.append(h2("4.1. Statistik o'rtachalash effekti (Markaziy chegara teoremasi)"))
body_parts.append(p(
    "Mustaqil shovqin namunalarining o'rtacha qiymatining standart og'ishi alohida bitta o'lchov "
    "standart og'ishidan √N marta kichik bo'ladi:"
))
body_parts.append(formula("σ_o'rtacha = σ_xom / √N"))
body_parts.append(p(
    "Demak, masalan N=9 qadam olinsa (α=0.2), shovqin amplitudasi √9 = 3 marta kamayadi. "
    "N=19 da esa √19 ≈ 4.4 marta kamayadi."
))
body_parts.append(p("EMA uchun aniq dispersiya kamayish koeffitsiyenti:"))
body_parts.append(formula("σ²_filtered / σ²_raw = α / (2 − α)"))

body_parts.append(table(
    ["α", "Shovqin dispersiyasi kamayishi", "Aniqlik oshishi (RMS)"],
    [
        ["0.5", "3.0×",  "1.7× baravar"],
        ["0.3", "5.7×",  "2.4× baravar"],
        ["0.2", "9.0×",  "3.0× baravar"],
        ["0.1", "19.0×", "4.4× baravar"],
        ["0.05","39.0×", "6.2× baravar"],
    ]
))

# Sabab 2
body_parts.append(h2("4.2. Past chastotali filtr effekti"))
body_parts.append(p(
    "EMA filtri o'z mohiyatiga ko'ra birinchi tartibli past chastotali filtr (Low-Pass Filter) hisoblanadi. "
    "Uning kesish chastotasi (–3 dB nuqtasi):"
))
body_parts.append(formula("f_kesish = α / (2π · Δt)"))

body_parts.append(p("Δt = 50 µs bo'lganda kesish chastotalari:"))
body_parts.append(table(
    ["α", "Kesish chastotasi f_kesish", "So'ndiriladigan shovqinlar"],
    [
        ["0.5",  "1 600 Hz", "Yuqori chastotali EMI"],
        ["0.3",  "950 Hz",   "EMI + impulsli shovqinlar"],
        ["0.2",  "640 Hz",   "Yuqori garmonikalar"],
        ["0.1",  "320 Hz",   "150 Hz va undan yuqori garmonikalar"],
        ["0.05", "160 Hz",   "Hatto 50 Hz tarmoq guming kuchsizlanadi"],
    ]
))

body_parts.append(p(
    "Demak, qadamlar soni N qancha katta bo'lsa (α qancha kichik bo'lsa), filtrning kesish chastotasi "
    "shuncha pastga tushadi va sanoat shovqinlari (50 Hz tarmoq, garmonikalar, EMI) shuncha kuchli "
    "so'ndiriladi."
))

# Sabab 3
body_parts.append(h2("4.3. Kvantlash xatoligini kompensatsiya qilish"))
body_parts.append(p(
    "ESP32 ning 12-bitli ADC si har bir o'lchovda ±0.5 LSB darajasida kvantlash xatoligini "
    "kiritadi. ACS724-50A datchigi uchun bitta LSB qiymati:"
))
body_parts.append(formula("LSB = (50 A × 2) / 4096 ≈ 0.024 A"))
body_parts.append(p(
    "N ta o'lchovni o'rtachalash bu kvantlash xatoligining tasodifiy tarqalishini "
    "1/√N ga kamaytiradi. Masalan, N=19 da xatolik ≈ 0.024 / 4.4 ≈ 0.005 A gacha kamayadi, "
    "ya'ni AVM-MP nominal toki I_nom = 5 A ning faqat 0.1% ni tashkil etadi."
))

# === KECHIKISH ===
body_parts.append(h1("5. KOMPROMIS — KECHIKISH ↔ ANIQLIK"))
body_parts.append(p(
    "Qadamlar sonini cheksiz oshirib bo'lmaydi, chunki har bir qo'shimcha qadam himoya "
    "qurilmasining javob vaqtini (T₃) oshiradi. Filtrning vaqt doimiysi:"
))
body_parts.append(formula("τ_EMA = Δt / α = Δt · (N_eff + 1) / 2"))

body_parts.append(p(
    "Ya'ni N qancha katta bo'lsa — qurilma signalga shuncha sekin javob beradi. "
    "Bu yerda asosiy muvozanat masalasi paydo bo'ladi:"
))
body_parts.append(bullet("ANIQLIK ko'p qadam (kichik α) talab qiladi"))
body_parts.append(bullet("TEZKORLIK kam qadam (katta α) talab qiladi"))
body_parts.append(p(""))
body_parts.append(p(
    "AVM-MP qurilmasi ikki bosqichli himoyaga ega bo'lgani uchun har bir bosqich uchun "
    "alohida α qiymati tanlanadi.", bold=True
))

# === TANLOV ===
body_parts.append(h1("6. AVM-MP UCHUN OPTIMAL QIYMATLAR"))

body_parts.append(h2("6.1. 1-bosqich — di/dt asosida tezkor himoya"))
body_parts.append(bullet("Maqsadi: qisqa tutashuvni eng tez aniqlash"))
body_parts.append(bullet("Asosiy talab: tezkorlik (T₃ ≤ 200 µs)"))
body_parts.append(bullet("Tavsiya etilgan: α = 0.3...0.5, N = 3–6 qadam"))
body_parts.append(bullet("Natija: shovqin 3–5× kamayadi, kechikish ≤ 170 µs"))

body_parts.append(h2("6.2. 2-bosqich — yuklanishdan kechikishli himoya"))
body_parts.append(bullet("Maqsadi: yo'l transformatorini overheating dan himoya qilish"))
body_parts.append(bullet("Asosiy talab: aniqlik (RMS qiymat aniq)"))
body_parts.append(bullet("Tavsiya etilgan: α = 0.05...0.1, N = 19–39 qadam"))
body_parts.append(bullet("Natija: shovqin 19–39× kamayadi, juda aniq RMS qiymat"))

body_parts.append(h2("6.3. Yakuniy tavsiyalar jadvali"))
body_parts.append(table(
    ["Bosqich", "α", "N qadam", "Aniqlik oshishi", "Kechikish T₃", "Asoslash"],
    [
        ["1-bosqich (di/dt)",  "0.3",  "5–6",  "×2.4",  "170 µs",  "Tezkorlik muhim"],
        ["2-bosqich (yuk)",    "0.1",  "19",   "×4.4",  "500 µs",  "Aniqlik muhim"],
    ]
))

# === XULOSA ===
body_parts.append(h1("7. ASOSIY XULOSALAR"))
body_parts.append(p(
    "EMA filtrlash usulida qadamlar soni N oshirilganda aniqlik oshadi. "
    "Buning uchta asosiy fizik-matematik sababi mavjud:", bold=True
))
body_parts.append(p(
    "1. Statistik effekt — Markaziy chegara teoremasi bo'yicha N ta mustaqil shovqinli "
    "o'lchovning o'rtachasi bitta o'lchovga qaraganda √N marta aniqroq bo'ladi."
))
body_parts.append(p(
    "2. Spektral effekt — EMA past chastotali filtr sifatida ishlab, kesish chastotasidan "
    "yuqori bo'lgan shovqinlarni (50 Hz tarmoq guming, EMI, garmonikalar) so'ndiradi."
))
body_parts.append(p(
    "3. Kvantlash effekti — ADC ning ±0.5 LSB diskret xatoliklari N ta o'lchov o'rtachalanganda "
    "1/√N koeffitsiyenti bo'yicha kompensatsiyalanadi."
))
body_parts.append(p(""))
body_parts.append(p(
    "Lekin qadamlar sonini oshirish kechikishni proporsional ravishda oshiradi, shuning uchun "
    "AVM-MP qurilmasida ikki bosqichli yondashuv qo'llanadi: 1-bosqichda tezkor reaksiya uchun "
    "kam qadam (N=5–6, α=0.3), 2-bosqichda yuklanish uchun ko'p qadam (N=19, α=0.1) tanlanadi.",
    bold=True
))

# === ADABIYOTLAR ===
body_parts.append(h1("ADABIYOTLAR / MANBALAR"))
body_parts.append(p("1. Allegro MicroSystems. ACS724 Datasheet. — 2023."))
body_parts.append(p("2. Espressif Systems. ESP32 Technical Reference Manual. — 2024."))
body_parts.append(p("3. Oppenheim A.V., Schafer R.W. Discrete-Time Signal Processing. — Prentice Hall, 2010."))
body_parts.append(p("4. Smith S.W. The Scientist and Engineer's Guide to Digital Signal Processing. — California Technical Publishing, 1999."))
body_parts.append(p("5. IEC 60255-151:2009. Functional requirements for over/under current protection."))


# ============================================================
# To'liq document.xml ni tuzish
# ============================================================
DOCUMENT_XML = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">
<w:body>
{''.join(body_parts)}
<w:sectPr>
<w:pgSz w:w="11906" w:h="16838"/>
<w:pgMar w:top="1134" w:right="850" w:bottom="1134" w:left="1701" w:header="708" w:footer="708" w:gutter="0"/>
</w:sectPr>
</w:body>
</w:document>'''


# ============================================================
# DOCX faylni yaratish
# ============================================================
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUT_FILE)
with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('[Content_Types].xml', CONTENT_TYPES)
    z.writestr('_rels/.rels', RELS)
    z.writestr('word/_rels/document.xml.rels', DOC_RELS)
    z.writestr('word/styles.xml', STYLES)
    z.writestr('word/document.xml', DOCUMENT_XML)

print(f"OK: {out_path}")
print(f"Size: {os.path.getsize(out_path)} bytes")
