# YDS Kalite Denetimi

[Başlangıç](README.md) · [Manifesto](CONTENT-MANIFEST.md) · [Kaynaklar](SOURCES.md)

**Denetim tarihi:** 6 Ekim 2026. Bu rapor yapısal kontrol ile editoryal gözden geçirmeyi ayırır. Dış bağımsız editör veya gerçek YDS güçlük kalibrasyonu yapılmadı.

## İçerik sayımı

| Paket | Puanlanan özgün görev |
|---|---:|
| Vocabulary drill | 4 |
| Grammar drill | 8 |
| İki cloze pasajı | 10 boşluk |
| Sentence completion | 4 |
| İki yönlü translation | 4 |
| Dört reading pasajı | 16 |
| Dialogue | 4 |
| Restatement | 4 |
| Paragraph completion | 4 |
| Irrelevant sentence | 4 |
| Tanılayıcı test | 24 |
| Karma Set 01 | 20 |
| Gramer atölyesi | 45 (15 kavram + 15 üretim + 15 çoktan seçmeli) |
| Yeni kelime/kalıp/anlam testi | 40 |
| **Toplam** | **191** |

Toplamın 161'i beş seçenekli soru/boşluk, 30'u açık kavram/üretim görevidir. Ayrıca 40 aktif hatırlama kartı, temel okuma atölyesinde dört cevaplı görev ve iki isteğe bağlı dönüşüm görevi vardır; bunlar 191'e eklenmemiştir. Dört ana akademik reading pasajına ek olarak tanılama, karma set ve temel atölyede birer kısa pasaj; iki cloze metni vardır. Ders içi çözümlü örnekler sayılmamıştır.

Kelime ana seçkisi: **332 çalışma birimi = 242 tek sözcük başlığı + 50 fiil ifadesi + 40 edat/tamamlayıcı yapısı**. 193 P1, 139 P2. Eski 72 akademik madde bu 332 içinde; tekrar sayılmaz. Eski 25 ifadeli başvuru ve 24 collocation satırı ayrı öğretim açıklamalarıdır; bunları bağımsız yeni kelime/aile olarak toplama. Konu alanları önceki 12 alanı kapsar.

**664 Anki kartı:** 332 tanıma + 332 üretim, UTF-8, üç sütun. Her çalışma birimine ait alanlar, örnek, iki kalıp, aile/tuzak ve kimlik, üretilen Markdown/kartlarla karşılaştırıldı. P07'nin 125 satırındaki 113 farklı yazılı başlık, yazım/ifade varyantları birleştirilerek kapsanıyor. Diğer belgelerdeki bütün seçenekler listelendi iddiası yoktur.

## Editoryal inceleme

- Yeni 40 soru bağlam kanıtı, anlam yönü, tamamlayıcı türü ve çeldirici uyumu açısından gözden geçirildi. Cevap metni/harfi, açıklama ve ilgili kelime bağlantıları eşleşti.
- Her çoktan seçmeli anahtarın işaret ettiği seçenek ve açıklamadaki doğru metin eşleştirildi.
- Cloze'da bütün boşluklarla paragraf anlamı, antecedent ve neden/sonuç yönü incelendi.
- Reading cevapları pasajdaki bilgi veya sınırlandırılmış çıkarımla karşılaştırıldı.
- Çeviriler actor, action, tense, negation, degree, scope ve modal güç açısından karşılaştırıldı.
- Yakın anlamlı/koşullu alternatif riski olan bir kalibrasyon sorusuna açık gereklilik bağlamı eklendi; diagnostic complaint sorusunda reddetme alternatifi değiştirildi.
- Irrelevant sentence örneklerinde geniş konu ilgisi ile dar argüman farkını göstermek için su ve tarım alanına bağlı çeldirici cümleler kullanıldı.
- Reduction seçenekleri tek başına doğal cümleler olacak, fakat ortak-özne koşulunu bozacak şekilde düzeltildi.
- Yanıtlar sorulardan ayrı dosyalarda; aktif hatırlama ve temel atölye cevapları GitHub details içinde.

## Yapısal kontrol

| Kontrol | Sonuç |
|---|---|
| YDS Markdown dosyası | 81; boş dosya veya içeriği eksik yer tutucu yok |
| Yerel Markdown bağlantısı | Bütün hedefler kontrol edildi; kırık hedef yok |
| Başlangıçtan erişim | 81/81; orphan yok |
| Manifest kapsamı | 81 Markdown + JSON/Anki/üretici; dosyalar bağlantılı |
| Çoktan seçmeli anahtar | 161/161: beş seçenek, doğru harf/metin eşleşmesi ve açıklama |
| Açık görev anahtarı | 15 kavram + 15 üretim; kabul edilebilir yanıtlar |
| Recall bankası | 40 soru ve açılır yanıt |
| Kelime veri/kart bütünlüğü | 332 tekil kimlik/başlık, 664 üç alanlı kart; P07 kapsamı eksiksiz |
| Tarihli plan | 47 gün; 332 kimlik birer kez taranıyor; deneme ve son dört günde yeni yük yok |
| Site üretimi | `python3 site/build.py --out /private/tmp/learning-yds-site` başarılı; 410 sayfa + mevcut 7 PDF |
| YDS HTML ve arama | 81 HTML sayfası; 81 arama girdisi |
| HTML yerel hedefler | YDS sayfaları + ana sayfa, veri indirmeleri ve bölüm içi kimlik bağlantıları; kırık hedef/anchor yok |
| Mevcut kitaplar | 329 Spanish/AI sayfasında sayfa sırası ve içerik navigasyonu önceki sürümle aynı |
| Git whitespace kontrolü | `git diff --check` başarılı |

İlk içerik denetiminde site çıktıları geçici dizine yazıldı. Vercel yayın entegrasyonunda mevcut üretim mimarisi gereği `site-dist/` yeniden üretildi ve içerikle birlikte sürümlendi; yeni bağımlılık eklenmedi. Kontroller Python standart kütüphanesi ve mevcut Pandoc ile çalıştırıldı. Manifesto ve HTML kontrolleri dış kaynakların sürekli erişimini veya dilsel kusursuzluğu garanti etmez.

## Kapsam sınırı ve bakım

Sınavın genel formatı 2026-YDS/1 ÖSYM kılavuzuyla doğrulanmıştır. On türün ayrıntılı adedi ve sırası öğrenci modelidir. Kaynaklar bunu açıkça ayırır. Bu sürüm tam 80 soruluk deneme, puan tahmin modeli veya istatistiksel olarak kalibre edilmiş banka değildir.

Önerilen genişleme: İlk kişisel hata verisinden sonra yeni bağlamlarda Karma Set 02; ardından on türü içeren özgün 80 soruluk deneme ve ayrı ayrıntılı anahtar. Özellikle ileri bağlaç kapsamı, uzun cümlelerde modal nüansı ve çıkarım sorularını artır. Yeni dosyaları manifestoya ve ilgili dizine bağla.


## PDF ve önizleme kontrolü

Sekiz dosya/yedi benzersiz belge, 155 benzersiz sayfa. 148 tarama sayfası OCR ile işlendi; P02/P03 birebir kopya SHA-256 ile saptandı. Kapak, kelime ve anahtar sayfası örnekleri görüntü üzerinden incelendi. Dilsel riskli maddeler [değerlendirme raporunda](SOURCE-REVIEW.md), kontrol edilen sözlük bağlantılarıyla gösterildi. OCR'nin harf/kelime doğruluğu ve yerel anahtarların tümü bağımsız doğrulanmış değildir.

Kelime merkezi ve edat bölümüne geçiş yerel tarayıcıda kontrol edildi; Türkçe karakterler, tablolar ve bölüm bağlantıları okunabilir. Özgün kaynak PDF'leri ve OCR dökümleri depoya alınmadı. Kelime üreticisi ana JSON'dan yeniden çalıştırıldı. Denetim, Anki uygulamasında gerçek içe aktarma veya ilerideki sınav puanı kalibrasyonu içermez.
