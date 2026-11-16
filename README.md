# ENS202 — short solutions and exact course tables

## 7-Cal'e yapıştırılacak prompt

[online_prompt.txt — raw](https://raw.githubusercontent.com/bugra053/termodynamic/main/online_prompt.txt) dosyasını aç, metnin tamamını kopyala ve **Create Custom Prompt → Content** alanındaki eski metnin yerine yapıştır. Başlık `ENS202`; online tarama açık olmalı.

Çıktı talimatı: sayısal sorularda yazılı açıklama olmadan **denklem → sayısal yerleştirme → kutulu sonuç**. Genellikle alt soru başına iki kısa satır; zorunlu tablo/süreç adımları için ek satır. Grafik istenen soruda küçük, eksenleri/durumları/yönleri etiketli çizim eklenir; platform görsel çizimi desteklemiyorsa dar bir ASCII şema kullanılır. Hesaplar kısa kalır. TikZ ve uzun çizim kodu yok. Kaynak okuma işlemleri çıktıda anlatılmaz. Tablo değerinin ilk kullanıldığı satırın sonunda yalnızca `(A-13)` gibi küçük bir etiket yazılır; aynı satırda iki tablo varsa `(A-13, A-11)` kullanılır. Sonraki hesap satırlarında tekrarlanmaz. Platformun kendi eklediği alıntı veya bağlantı gösterimleri prompt dışında uygulanabilir.

## Hocanın gerçek tablosu

Kullanıcının hocaya ait olduğunu belirttiği `Property_tables (1).pdf`, değiştirilmeden [tables/Property_tables.pdf](tables/Property_tables.pdf) olarak eklendi. **50 sayfa**, basılı sayfalar **907–956**. Baskı numarası dosyada açıkça doğrulanmadığı için tahmin edilmedi. Özellik değerlerinde başka baskıya geçiş yok.

- [source.json](tables/source.json): kaynak kimliği, SHA256, tablo/sayfa dizini ve raw metin bağlantıları.
- [verified_states.json](tables/verified_states.json): bu dosyadan kontrol edilmiş seçili durumlar.
- [tables/text/](tables/text/): ENS202 için ilgili 11 tablonun sayfa sınırları ve başlıkları korunmuş metin çıkarımı. Bazı özel karakterler bozulabileceğinden şüpheli sütun/işaret için orijinal PDF kullanılır.

Kontrol edilen örnek: A-13, PDF sayfa 24 / basılı 930, R-134a, 800 kPa ve 70°C için **h=306.88 kJ/kg**. Aynı dosyanın A-11 tablosunda h_f(14°C)=70.95 ve h_f(16°C)=73.73; 15°C için sıvı yaklaşımıyla h yaklaşık 72.34 kJ/kg. Eski 8. baskıdaki 306.90/70.94/73.72 değerleriyle karıştırılmaz.

PDF'yi [raw indir](https://raw.githubusercontent.com/bugra053/termodynamic/main/tables/Property_tables.pdf). Doğrudan AI dosyası olarak kullanmak için 7-Cal'de **AI Models → Upload File to AI** üzerinden yükle ve **Active** seç. [Resmî özellik açıklaması](https://www.7-cal.com/full-patch-notes). Bir URL yazmak dosyanın gerçekten okunduğunu garanti etmez.

## Diğer kaynaklar

- `sources/`: dört orijinal tutorial PDF'si; toplam 22 sayfa, görüntü tabanlı.
- `course_reference.md`: öğretmenin yöntemini izleyen konu/soru dizini; eski örneklerin özellik sayıları yerine gerçek ders tablosu kullanılır.
- `data/past_exams.json`: öğrenci bilgileri çıkarılmış 11 çıkmış/örnek soru kaydı.
- `data/recommended_problems.json`: önerilen soru numaraları. Soru numarası tek başına tam soru metni değildir.
- `system_prompt.txt`: kısa temel sistem talimatı.
- `calculator_prompt.txt`: talimat + ders yöntemleri + çıkmışlar + doğrulanmış tablo satırları tek metin.

## Backend araçları

```sh
python3 scripts/build_context.py --repo bugra053/termodynamic --question 'R134a at 800 kPa and 70 C' --example undated-Q5 > context.json
python3 scripts/fetch_cengel.py --table A-13 --render
```

İlk betik sağlayıcıdan bağımsız model girdisi hazırlar; public raw erişim için token gerekmez. İkinci betik repodaki birebir ders PDF'sini SHA256 ile kontrol eder ve ilgili sayfaları görüntüye çevirir; görüntü için Poppler `pdftoppm` gerekir. İkisi de model API'sine çağrı yapmaz. Örnek araması basit kelime eşleştirmesidir; `--example` kesin kayıt seçer.

Görüntü bulanıksa yalnızca kesin kaynak eşleşmesinden veri tamamlanır. Kritik sayı okunamıyorsa tahmin edilmez. Hocanın tablosunu izlemek ve çıktıyı kısaltmak prompt kurallarıdır; gerçek model yanıtını çalışma sorularıyla kontrol etmek gerekir.
