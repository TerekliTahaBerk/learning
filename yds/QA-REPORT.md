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
| **Toplam** | **151** |

Toplamın 121'i beş seçenekli soru/boşluk, 30'u açık kavram/üretim görevidir. Ayrıca 40 aktif hatırlama kartı, temel okuma atölyesinde dört cevaplı görev ve iki isteğe bağlı dönüşüm görevi vardır; bunlar 151'e eklenmemiştir. Dört ana akademik reading pasajına ek olarak tanılama, karma set ve temel atölyede birer kısa pasaj; iki cloze metni vardır. Ders içi çözümlü örnekler sayılmamıştır.

Kelime: 72 akademik madde, 25 çok sözcüklü fiil/ifade, 24 collocation satırı; bazı sözcükler birden fazla bölümde aynı kalıbın farklı kullanımını öğretir. Bunlar 121 benzersiz sözcük sayısı olarak sunulmaz. Alanlar: science, medicine, environment, economics, sociology, psychology, history, archaeology, technology, education, politics, biology.

## Editoryal inceleme

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
| YDS Markdown dosyası | 72; boş dosya veya içeriği eksik yer tutucu yok |
| Yerel Markdown bağlantısı | 589 kontrol; kırık hedef yok |
| Başlangıçtan erişim | 72/72; orphan yok |
| Manifest kapsamı | 72/72 dosya |
| Çoktan seçmeli anahtar | 121/121: beş seçenek, doğru harf/metin eşleşmesi ve açıklama |
| Açık görev anahtarı | 15 kavram + 15 üretim; kabul edilebilir yanıtlar |
| Recall bankası | 40 soru ve açılır yanıt |
| Site üretimi | `python3 site/build.py --out /private/tmp/learning-yds-site` başarılı; 401 sayfa + mevcut 7 PDF |
| YDS HTML ve arama | 72 HTML sayfası; 72 arama girdisi |
| HTML yerel hedefler | YDS sayfaları + ana sayfada 6.793 bağlantı; kırık hedef/anchor yok |
| Mevcut kitaplar | 329 Spanish/AI sayfasında sayfa sırası ve içerik navigasyonu önceki sürümle aynı |
| Git whitespace kontrolü | `git diff --check` başarılı |

Site üretim çıktıları yalnız geçici dizine yazıldı; depoya build dosyası veya bağımlılık eklenmedi. Kontroller Python standart kütüphanesi ve mevcut Pandoc ile çalıştırıldı. Manifesto ve HTML kontrolleri dış kaynakların sürekli erişimini veya dilsel kusursuzluğu garanti etmez.

## Kapsam sınırı ve bakım

Sınavın genel formatı 2026-YDS/1 ÖSYM kılavuzuyla doğrulanmıştır. On türün ayrıntılı adedi ve sırası öğrenci modelidir. Kaynaklar bunu açıkça ayırır. Bu sürüm tam 80 soruluk deneme, puan tahmin modeli veya istatistiksel olarak kalibre edilmiş banka değildir.

Önerilen genişleme: İlk kişisel hata verisinden sonra yeni bağlamlarda Karma Set 02; ardından on türü içeren özgün 80 soruluk deneme ve ayrı ayrıntılı anahtar. Özellikle ileri bağlaç kapsamı, uzun cümlelerde modal nüansı ve çıkarım sorularını artır. Yeni dosyaları manifestoya ve ilgili dizine bağla.
