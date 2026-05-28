# СТРУКТУРА_AVM_MP.md

## Yo‘nalish: Temir yo‘l avtomatika va telemexanikasi

## Mavzu: AVM-MP asosidagi himoya qurilmasini takomillashtirish

> Mikroprotsessorli himoya algoritmlarini ilmiy asoslash + AI yordamida dissertatsiya yozishda strukturaviy nazorat
> Fayl hajmi optimallashtirilgan — katta matnlarda mantiqiy uzilishlarni kamaytirish

---

# 0. ILMIY ISHDA AI ZAIFLIKLARI VA KOMPENSATSIYA

| Zaiflik                                    | Holat | Kompensatsiya                |
| ------------------------------------------ | ----- | ---------------------------- |
| Formula noto‘g‘ri yozilishi                | ✅     | Formulalar jadvali           |
| Parametrlar chalkashuvi                    | ✅     | Parametr pasporti            |
| Vaqt diagrammasi buzilishi                 | ✅     | Jarayon xronologiyasi        |
| Texnik terminlar almashishi                | ✅     | Terminologik jadval          |
| Hisob-kitob xatolari                       | ⚠️    | Verifikatsiya jadvali        |
| Eksperiment tavsifi uzilishi               | ⚠️    | Sinov protokoli              |
| Grafik va jadval mos kelmasligi            | ⚠️    | Natijalar tekshiruvi         |
| “Samarali”, “ishonchli” kabi noaniq gaplar | ✅     | Taqiqlangan iboralar jadvali |
| AI tomonidan “uydirilgan” parametrlar      | ✅     | Manba validatsiyasi          |

---

# 1. DISSERTATSIYA STRUKTURASI

## Struktura A — “Mavjud himoya tizimi kamchiliklarini aniqlash”

### Qo‘llash holati

Agar tadqiqot:

* AVM qurilmalarining kamchiliklarini,
* sekin ishlashini,
* noto‘g‘ri ishga tushishini,
* qisqa tutashuvni aniqlashdagi muammolarni
  ko‘rsatsa.

### Shablon

```text
[1-blok] Muammo tavsifi
[2-blok] Amaldagi AVM qurilma analizi
[3-blok] Kamchiliklarni matematik asoslash
[4-blok] Yangi AVM-MP yechimi
[5-blok] Eksperimental tasdiqlash
```

---

## Struktura B — “di/dt asosidagi himoya algoritmi”

### Qo‘llash holati

Agar asosiy e’tibor:

* tok o‘zgarish tezligi,
* kritik di/dt,
* o‘tkinchi jarayonlar,
* selektiv himoya
  masalalariga qaratilgan bo‘lsa.

### Shablon

```text
[1-blok] Nazariy asos
[2-blok] di/dt matematik modeli
[3-blok] Kritik chegara aniqlanishi
[4-blok] AVM-MP algoritmi
[5-blok] Real sinov natijalari
```

---

## Struktura C — “Rels zanjiri xavfsizligini oshirish”

### Qo‘llash holati

Agar ish:

* rels zanjiri,
* signalizatsiya xavfsizligi,
* noto‘g‘ri bandlik,
* himoya selektivligi
  bilan bog‘liq bo‘lsa.

### Shablon

```text
[1-blok] Rels zanjiri parametrlari
[2-blok] Qisqa tutashuv modellari
[3-blok] Himoya ishlash algoritmi
[4-blok] AVM-MP integratsiyasi
[5-blok] Xavfsizlik ko‘rsatkichlari
```

---

# 2. DISSERTATSIYA BOBLARI

## 1-BOB. MUAMMO HOLATI TAHLILI

### Kiritiladi:

* Temir yo‘l rels zanjiri turlari
* Himoya tizimlari klassifikatsiyasi
* AVM qurilmalarining ishlash prinsipi
* Mavjud kamchiliklar
* Tadqiqot maqsadi va vazifalari

### Bob yakuni:

```text
Mavjud himoya vositalari yuqori sezgirlik va tezkorlik talablarini to‘liq qanoatlantirmaydi.
Shu sababli mikroprotsessorli AVM-MP qurilmasini ishlab chiqish dolzarb hisoblanadi.
```

---

## 2-BOB. MATEMATIK MODEL

### Kiritiladi:

* Elektrik ekvivalent sxema
* Tok tenglamalari
* di/dt modeli
* O‘tkinchi jarayonlar
* Kritik parametrlar

### Asosiy formula

\frac{di}{dt}=\frac{U-Ri}{L}

### Qisqa tutashuv toki

---

## 3-BOB. AVM-MP ALGORITMI

### Kiritiladi:

* Mikroprotsessor strukturasi
* Signal filtrlash
* ADC ishlashi
* di/dt monitoring
* Qaror qabul qilish algoritmi

### Algoritm ketma-ketligi

```text
1. Tok signalini olish
2. ADC orqali raqamlashtirish
3. di/dt hisoblash
4. Kritik qiymat bilan solishtirish
5. Himoya signalini shakllantirish
6. Rele ishga tushishi
```

---

## 4-BOB. EKSPERIMENTAL SINOV

### Kiritiladi:

* Laboratoriya sxemasi
* Q.t rejimi
* Normal rejim
* O‘lchov asboblari
* Grafiklar
* Oscillogrammalar

### Tavsiya etilgan parametrlar jadvali

| Parametr     | Belgilanishi | Qiymat  |
| ------------ | ------------ | ------- |
| Nominal tok  | Inom         | 5 A     |
| Q.t toki     | Iqt          | 75 A    |
| Himoya vaqti | t_h          | 25 ms   |
| Kritik di/dt | (di/dt)kr    | 18 A/ms |
| Kuchlanish   | U            | 24 V    |

---

## 5-BOB. TEXNIK-IQTISODIY SAMARADORLIK

### Kiritiladi:

* AVM va AVM-MP taqqoslash
* Ishonchlilik
* Nosozlik kamayishi
* Xizmat xarajati
* Energiya samaradorligi

---

# 3. TIZIM ELEMENTLARI JADVALI

| Element      | Vazifa          | Holat  | Izoh                 |
| ------------ | --------------- | ------ | -------------------- |
| AVM-MP       | Himoya          | Aktiv  | Asosiy qurilma       |
| Rele         | Uzish           | Aktiv  | Ijro elementi        |
| ADC          | Raqamlashtirish | Aktiv  | Signal qayta ishlash |
| PLC          | Monitoring      | Aktiv  | Diagnostika          |
| Rels zanjiri | Signal uzatish  | Normal | Nazorat obyekti      |

---

# 4. JARAYON XRONOLOGIYASI

| Vaqt | Hodisa             | Natija                 |
| ---- | ------------------ | ---------------------- |
| t0   | Normal rejim       | Tok barqaror           |
| t1   | Qisqa tutashuv     | Tok oshishi            |
| t2   | di/dt kritik nuqta | Algoritm ishga tushadi |
| t3   | Rele aktivlashuvi  | Himoya bajariladi      |
| t4   | Tizim tiklanishi   | Normal holat           |

---

# 5. PARAMETRLAR PASPORTI

| Parametr              | Belgisi | Birligi | Izoh                       |
| --------------------- | ------- | ------- | -------------------------- |
| Tok                   | I       | A       | Zanjir toki                |
| Kuchlanish            | U       | V       | Ta’minot kuchlanishi       |
| Qarshilik             | R       | Om      | Umumiy qarshilik           |
| Induktivlik           | L       | Gn      | Zanjir induktivligi        |
| Tok o‘zgarish tezligi | di/dt   | A/ms    | Asosiy diagnostik parametr |

---

# 6. TAQIQLANGAN ILMIY IBORALAR

| Noto‘g‘ri ibora         | To‘g‘ri variant                      |
| ----------------------- | ------------------------------------ |
| “Juda samarali qurilma” | “Himoya vaqti 18% kamaydi”           |
| “Ishonchli tizim”       | “Nosozlik ehtimoli kamaydi”          |
| “Zamonaviy texnologiya” | “Mikroprotsessorli himoya algoritmi” |
| “Tez ishlaydi”          | “25 ms ichida ishga tushdi”          |
| “Yaxshi natija”         | “Selektivlik oshdi”                  |

---

# 7. VERIFIKATSIYA JADVALLARI

## 7.1 Formula tekshiruvi

| Formula            | Tekshirildi | Holat   |
| ------------------ | ----------- | ------- |
| di/dt tenglamasi   | ✅           | To‘g‘ri |
| Q.t toki formulasi | ✅           | To‘g‘ri |
| Rele ish vaqti     | ✅           | To‘g‘ri |

---

## 7.2 Eksperiment validatsiyasi

| Sinov                         | Holat |
| ----------------------------- | ----- |
| Normal rejim                  | ✅     |
| Qisqa tutashuv                | ✅     |
| Ortiqcha yuklama              | ✅     |
| Noto‘g‘ri ishga tushish testi | ✅     |

---

## 7.3 Dissertatsiya chek-listi

| Kriteriy                    | Holat |
| --------------------------- | ----- |
| Matematik model mavjud      | ✅     |
| Algoritm keltirilgan        | ✅     |
| Grafiklar mavjud            | ✅     |
| Tajriba o‘tkazilgan         | ✅     |
| Formulalar izohlangan       | ✅     |
| Parametrlar jadvali mavjud  | ✅     |
| AVM bilan taqqoslash mavjud | ✅     |
| Xulosa aniq yozilgan        | ✅     |

---

# 8. XULOSA SHABLONI

```text
Tadqiqot natijasida AVM-MP asosidagi mikroprotsessorli himoya qurilmasi ishlab chiqildi.

Taklif etilgan algoritm qisqa tutashuv rejimlarini di/dt parametriga asosan aniqlaydi.

Eksperimental natijalar himoya ishlash vaqtining kamayganligini hamda rels zanjiri xavfsizligi oshganligini ko‘rsatdi.

Ishlab chiqilgan qurilmani temir yo‘l avtomatika va telemexanika tizimlarida qo‘llash maqsadga muvofiq hisoblanadi.
```

---

# 9. ILMIY YANGILIK SHABLONI

```text
1. di/dt parametriga asoslangan yangi himoya algoritmi ishlab chiqildi.

2. AVM-MP qurilmasining matematik modeli taklif qilindi.

3. Himoya qurilmasining kritik ishga tushish chegaralari aniqlandi.

4. Mikroprotsessorli boshqaruv asosida rels zanjiri xavfsizligi oshirildi.
```

---

# 10. AMALIY AHAMIYAT

```text
Taklif etilgan AVM-MP qurilmasi:
- himoya tezkorligini oshiradi;
- noto‘g‘ri ishga tushishlarni kamaytiradi;
- ekspluatatsion xarajatlarni pasaytiradi;
- rels zanjiri xavfsizligini oshiradi.
```

*Fayl: СТРУКТУРА_AVM_MP.md*
*Yo‘nalish: Temir yo‘l avtomatika va telemexanikasi*
*Mavzu: AVM-MP asosidagi himoya qurilmasi*
