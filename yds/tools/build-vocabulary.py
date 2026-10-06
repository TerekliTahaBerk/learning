#!/usr/bin/env python3
"""Render vocabulary Markdown and native Anki import from the reviewed JSON master.

Run from any directory: python3 yds/tools/build-vocabulary.py
No source PDFs or external dependencies are needed.
"""
from pathlib import Path
import json, csv, html
V = Path(__file__).resolve().parents[1] / 'fundamentals/vocabulary'
entries = json.loads((V / 'vocabulary-master.json').read_text(encoding='utf-8'))
required = {'id', 'head', 'pos', 'tr', 'en', 'chunks', 'example', 'family', 'trap', 'tier', 'category', 'source_presence'}
if not entries or any(set(e) != required or any(not isinstance(v, str) or not v.strip() for v in e.values()) for e in entries):
    raise ValueError('Every vocabulary record must contain all non-empty string fields.')
if len({e['id'] for e in entries}) != len(entries) or len({e['head'] for e in entries}) != len(entries):
    raise ValueError('Duplicate ID or headword.')
if any(e['tier'] not in {'P1', 'P2'} or e['category'] not in {'core', 'advanced', 'adverbs', 'phrases', 'patterns'} for e in entries):
    raise ValueError('Unknown priority or category.')
labels={'core':('01-core-academic','Çekirdek akademik kelimeler'),'advanced':('02-exam-vocabulary','PDF destekli kelimeler ve anlam farkları'),'adverbs':('03-adverbs','Zarflar: derece, zaman ve tutum'),'phrases':('04-verb-phrases','Çok sözcüklü fiiller'),'patterns':('05-preposition-patterns','Edat ve tamamlayıcı kalıpları')}
for cat,(slug,title) in labels.items():
 selected=[e for e in entries if e['category']==cat]
 s=f'# {title}\n\n[Kelime merkezi](README.md) · [47 günlük plan](../../strategy/2026-11-22-study-plan.md) · [Kaynak değerlendirmesi](../../SOURCE-REVIEW.md)\n\n{len(selected)} birim. P1 önce, P2 sonra; öncelik sınavda çıkma olasılığı değildir. PDF izi bir sözcüğün belgede bulunmasını gösterir; doğru cevap veya sıklık iddiası değildir. Kalıp başlıkları her zaman kaynakta aynen bulunmayabilir. Tanım ve örnekler özgündür.\n\n'
 s+=' · '.join(f'[{e["id"]} {e["head"]}](#{e["id"].lower()})' for e in selected)+'\n\n'
 for e in selected:
  s+=f'<a id="{e["id"].lower()}"></a>\n\n### {e["id"]} — {e["head"]}\n\n**Öncelik / tür / TR:** {e["tier"]} · {e["pos"]} · {e["tr"]}  \n**EN:** {e["en"]}  \n**Kalıplar:** {e["chunks"]}  \n**Özgün örnek:** {e["example"]}  \n**Aile:** {e["family"]}  \n**Ayrım / tuzak:** {e["trap"]}  \n**PDF izi:** {e["source_presence"]}\n\n'
 (V/(slug+'.md')).write_text(s.rstrip() + '\n')

# Native Anki text import, one recognition + one production note per study unit.
with (V/'anki-import.txt').open('w') as f:
 f.write('#separator:Tab\n#html:true\n#columns:Front\tBack\tTags\n#tags column:3\n')
 writer=csv.writer(f,delimiter='\t',lineterminator='\n')
 for e in entries:
  esc=lambda s:html.escape(s)
  back='<br>'.join(esc(e[k]) for k in ['tr','en','chunks','example','family','trap'])
  writer.writerow([esc(e['head'])+' ('+esc(e['pos'])+')',back,e['id']+' '+e['tier']+' yds-recognition'])
  # Use a pattern prompt instead of copying exam stems or a context-free synonym card.
  writer.writerow([esc(e['tr'])+'<br>İngilizce çalışma birimini ve bir kalıbını hatırla. '+e['id'],esc(e['head'])+'<br>'+esc(e['chunks'])+'<br>'+esc(e['trap']),e['id']+' '+e['tier']+' yds-production'])
print(f'Rendered {len(entries)} units and {2 * len(entries)} Anki cards.')
