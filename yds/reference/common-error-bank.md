# Ortak Hatalar ve Kişisel Hata Günlüğü

[Başlangıç](../README.md) · [Temeller](../fundamentals/README.md) · [Aktif hatırlama](active-recall-bank.md)

## Sınıflandırma

| Etiket | Hata türü | Düzeltme aracı |
|---|---|---|
| Vocabulary | Anlam/polarity | Bağlam kartı ve karşı örnek |
| Collocation | Doğru sözcük, yanlış birliktelik | Kalıbı bütün olarak çağır |
| Tense | Referans zamanı/görünüş | Zaman çizgisi |
| Preposition | Yön veya kalıp | result from/in; sözlük tamamlayıcı |
| Connector | Yapı veya anlam ilişkisi | Clause/noun/transition ayrımı |
| Relative clause | Yanlış eksik öge veya niteleme | İsim + görev haritası |
| Translation | Kapsam/negation/modal | Sekiz alanlı karşılaştırma |
| Reading inference | Metnin ötesine geçme | Kanıt cümlesi + iddia gücü |
| Restatement | actor/time/degree değişimi | Değişmezleri yaz |
| Cloze | Sadece yerel okuma | Paragrafın iki tarafını tekrar oku |
| Attention error | Kural biliniyor, not/except kaçtı | Kök ve sınırlayıcı kelime kontrolü |

Modal, passive, gerund gibi alt etiketi ekleyebilirsin. Bir soru birden çok nedenle yanlış olabilir; baskın nedeni ve ikincili ayrı yaz. “Dikkatsizlik” genel kaçış etiketi olmasın.

## Türkçe konuşanlar için yaygın onarımlar

| Hatalı | Doğru | Neden |
|---|---|---|
| an information | some information / a piece of information | Sayılamaz isim |
| discuss about the issue | discuss the issue | Doğrudan nesne |
| depends of the result | depends on the result | Lexical preposition |
| I know where did they work | I know where they worked | Dolaylı soru word order |
| despite of the cost | despite the cost | Despite of almaz |
| avoid to publish | avoid publishing | Verb + gerund |
| is happened | happened | Geçişsiz fiil passive değil |
| the evidence are clear | the evidence is clear | Evidence sayılamaz tekil uyum |
| since 2018 ile otomatik past | Referans zamanına göre tense | Türkçe karşılık perfect seçimini belirlemez |

## Tamamlanmış örnek kayıt

**Kimlik:** Örnek; puanlanan test kaydı değil  
**Question type:** Preposition / vocabulary  
**My answer:** result in heat  
**Correct answer:** result from heat  
**Why I was wrong:** Sonucu ve nedeni ters okudum.  
**Rule / vocabulary:** from sonrası neden; in sonrası sonuç  
**Correct reasoning:** damage sonuç, heat neden; Damage resulted from heat.  
**Yeni karşı örnek:** Heat resulted in damage.  
**Güven / süre:** düşük / 50 saniye  
**Review date:** Kaydı oluşturduktan 1, 7, 21 gün sonra  
**Referans:** [Edatlar](10-prepositions.md)

## Kopyalanabilir Error Entry

```markdown
## Error Entry — tarih / soru kimliği

**Question type:**
**Hata etiketi / alt etiket:**
**My answer:**
**Correct answer:**
**Why I was wrong:**
**Rule / vocabulary:**
**Metindeki kanıt:**
**Correct reasoning:**
**En yakın çeldiricinin kusuru:**
**Yeni örnek / karşı örnek:**
**Güven / süre:**
**Review date:**
**Yeni bağlamda tekrar sonucu:**
**İlgili referans bağlantısı:**
```

## Açık kapatma

Önce kaydı kapatıp hatalı akıl yürütmeyi ve kuralı söyle. Sonra yeni cümlede uygula. İki farklı bağlamda ve bir hafta sonra doğru gerekçe üretirsen hatayı kapat; eski kaydı silme. Tekrarlanan iki etiketi [Roadmap Evre 7](../ROADMAP.md) önceliği yap.
