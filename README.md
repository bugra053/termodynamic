# ENS202 thermodynamics study references

Kısa çözüm formatı, ders örnekleri, çıkmış soru transkripsiyonları ve **yalnızca doğrulanmış Çengel tablolarını** kullanma kuralı.

## İçerik

- `system_prompt.txt`: İngilizce; denklem → sayısal yerleştirme → sonuç. Her alt soru için genellikle 2–4 kısa satır; gerekli süreç veya tablo adımları korunur.
- `course_reference.md`: Dört tutorial'dan yöntem özeti ve sayfa dizini. Tam transkripsiyon değildir.
- `data/past_exams.json`: 2023, 2024 ve tarihi görünmeyen devam sayfasındaki okunabilir sorular; 11 kayıt. Aynı görünen 2023 sayfası tekilleştirilmiştir. Adlar ve öğrenci numaraları alınmamıştır. Öğrenci cevapları çözüm anahtarı sayılmaz.
- `data/recommended_problems.json`: Bölüm 1–4 önerilen soru numaraları ve C işaretli kavramsal sorular bilgisi. Soru numaraları, soruların tam metninin mevcut olduğu anlamına gelmez.
- `sources/`: Kullanıcının verdiği dört orijinal tutorial PDF'si. Dosyalar görüntü tabanlıdır; şekil ve ayrıntılar için sayfa görüntüleri gerekir.
- `tables/source.json`: Çengel & Boles, 8. baskı SI eki için resmî yayınevi bağlantısı, dosya özeti ve doğrulanmış tablo sayfa dizini.
- `tables/verified_states.json`: Bazı çıkmış sorular için orijinal tabloların ilgili satırlarından doğrulanan 10 durum/özellik kaydı. Eksiksiz tablo değildir.
- `scripts/build_context.py`: Yerel dosyalardan veya GitHub reposunun raw içerik yanıtından modele verilecek JSON'u hazırlar.
- `scripts/fetch_cengel.py`: Resmî Çengel ekini yerel önbelleğe indirir ve istenen tablonun gerçek sayfalarını görüntüye çevirebilir.

## Çengel şartı

Resmî kaynak: [McGraw Hill — Çengel & Boles, 8/e, Appendices](https://glencoe.mheducation.com/sites/0073398179/information_center_view0/appendices.html).

Ders duyurusu beşinci baskıyı adlandırıyor ve başka baskılara izin veriyor. Bu repoda doğrulanmış resmî kaynak sekizinci baskıdır. Baskılar arası soru numaraları ve bazı özellik değerleri değişebilir; eşleştirme tam soru metnine ve gerçek tablo başlığına göre yapılmalı.

Tablo isteyen çözümde yalnızca doğrulanmış Çengel satırları kullanılmalı. Başka veritabanı, çevrimiçi hesaplayıcı veya model hafızasındaki sayılar Çengel verisi diye sunulmamalı. Gerekli durum bu küçük veri kümesinde yoksa orijinal Çengel sayfası okunmalı. Veri yoksa sonuç uydurulmaz.

Yayınevinin ekinin tam kopyası repoya eklenmemiştir; yardımcı betik doğrudan resmî kaynaktan indirir. Dosya `.cache/` altında kalır ve Git'e gönderilmez. Ham PDF metin çıkarımında eksi işaretleri ve sütunlar bozulabilir; gerekli durumda orijinal tablo görüntüsünü modele ekle. Genel ders özetindeki münferit eski örnek değerleri, yeni bir durum için bu doğrulanmış tablo kaynağının yerine geçmez.

## Yerel kullanım

Python 3 yeterlidir. Tablo sayfalarını görüntüye çevirmek için ayrıca Poppler içindeki `pdftoppm` gerekir.

```sh
python3 scripts/build_context.py --question 'R134a at 800 kPa and 120 C: find volume and internal energy' --example 2024-Q3 > context.json
python3 scripts/fetch_cengel.py --table A-13 --render
```

İlk komut `system_prompt`, `question` ve `course_context` alanları üretir. İkinci komut gerçek Çengel PDF'sini ve ilgili tablo sayfalarının yerel görüntü yollarını verir.

Model isteğinde:

1. `system_prompt` içeriğini sağlayıcının sistem/talimat alanına koy.
2. `course_context` içeriğini referans veri, `question` içeriğini güncel soru olarak gönder.
3. Doğrulanmış satırlar yeterli değilse ilgili gerçek tablo görüntülerini sağlayıcının görüntü/dosya alanıyla ekle. Dosya yolu veya URL yazmak görüntü eklemek değildir.
4. Modelin kısa yanıtını göster; kullanılan kaynak, tablo ve sayfaları istersen backend'de ayrı kaydet.

Betik bir modele API çağrısı yapmaz. Model sağlayıcısı ve mevcut uygulama kodu bu repo içinde yapılandırılmamıştır.

## 7-Cal Custom Prompt alanına ekleme

Repo public; raw bağlantılar için giriş veya token gerekmez.

- **Yalnızca talimatlar:** [system_prompt.txt raw](https://raw.githubusercontent.com/bugra053/termodynamic/main/system_prompt.txt).
- **Talimat + ders yöntemleri + çıkmışlar + seçili Çengel verileri tek metin:** [calculator_prompt.txt raw](https://raw.githubusercontent.com/bugra053/termodynamic/main/calculator_prompt.txt).

Create Custom Prompt ekranında Title alanına `ENS202` yaz. Yukarıdaki raw dosyalardan birini aç; dosyanın **metninin tamamını** kopyalayıp Content alanındaki eski metnin yerine yapıştır ve kaydet. İçerik alanına yalnızca URL yazmak dosyayı otomatik olarak modele vermez. Tek metin sürümü uzundur; platform bir uzunluk hatası verirse yalnızca system_prompt.txt kullan ve kaynakları PDF yükleme özelliğiyle sağla. Platformdaki prompt uzunluk sınırı burada doğrulanmadı.

7-Cal'in resmî [sürüm notları](https://www.7-cal.com/full-patch-notes), AI Models bölümünde AI için PDF yüklemeyi ve dosyayı Active seçmeyi açıklıyor. Bu alan, cihazda dosya saklayan Documents alanından farklı olabilir. Güncel sınır olarak 5 PDF, toplam 100 sayfa veya 10 MB belirtiliyor. Dört tutorial toplam 22 sayfa; resmî Çengel SI eki 50 sayfa. Dosyaları kullandırmak için ilgili PDF'leri AI dosyası olarak yükleyip etkinleştir. Bu repo 7-Cal hesabını otomatik yapılandırmaz.

Tek metin dosyası bütün şekilleri ve tam Çengel tablolarını içermez. Gerekli özellik veri kümesinde yoksa gerçek tablo sayfası sağlanmalıdır. [Resmî Çengel SI eki](https://glencoe.mheducation.com/sites/dl/free/0073398179/1042936/Appendix1_SIunits.pdf) indirilebilir; tam PDF repoda yeniden yayımlanmıyor.

## Backend'den raw içerik erişimi

```sh
python3 scripts/build_context.py --repo bugra053/termodynamic --ref main --question 'Water at 10 bar and 400 C, cooled then piston blocked' --example shared-Q4 > context.json
```

Public dosyalar `https://raw.githubusercontent.com/bugra053/termodynamic/main/` altından okunabilir. Betik GitHub Contents API'nin raw yanıtını kullanır; public repo için token zorunlu değildir. İsteğe bağlı GITHUB_TOKEN veya GH_TOKEN API kotasını yükseltmek veya private erişim için backend ortamında tutulabilir; istemci koduna yazılmamalıdır.

Bir URL'yi sistem promptuna koymak erişim veya otomatik güncelleme sağlamaz. İstek anında backend dosyayı indirmelidir. Sabit bir sürüm için `--ref` alanına commit SHA'sı verilebilir.

Örnek seçimi basit kelime eşleştirmesidir. Tam soru görüntülerinde önce metin okunmalı veya çıkarılmalı. Kesin eşleştirme için `--example` kullanılabilir; üretim uygulamasında daha güçlü arama eklenebilir.

## Kaynak kontrolleri

- Tutorial 4'ün ilk üç örneği tutorial 3'ün ilk üç örneğini tekrarlar; bağımsız kanıt sayılmaz.
- İlk eski el yazısı görüntüsü tutorial 3'ün 4–6(b) sorusuna aitse 27.6 kJ hesabı doğru süreç yoluna uymaz: sabit basınçta durdurucuya kadar hareket + sabit hacimde soğumada sıkıştırma işi girdisi 36.79 kJ'dür. Görüntünün soru metni görünmediği için eşleşme koşulludur.
- Sabit hacimde sıfır olan sınır işidir; elektrik veya karıştırıcı işi sıfır olmak zorunda değildir.
- Çözümler kısa tutulur; fiziksel doğruluk, tablo doğrulaması ve istenen bütün alt sorular uzunluk hedefinden önce gelir.
