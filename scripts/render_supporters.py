from pathlib import Path
import json,html,unicodedata
root=Path(__file__).resolve().parents[1];data=json.loads((root/'supporters.json').read_text())
from datetime import datetime
cutoff=datetime.fromisoformat(data['updated_through'])
zh_cutoff=cutoff.strftime('%Y-%m-%d %H:%M')+'（北京时间）'
en_cutoff=cutoff.strftime('%Y-%m-%d %H:%M')+' (UTC+08:00)'
count=len(data['supporters'])
groups=[('gold','#b78319','#fff9ea','金色','Gold'),('purple','#8556bc','#f8f3ff','紫色','Purple'),('blue','#3275bd','#f0f7ff','蓝色','Blue'),('green','#338768','#eff9f4','绿色','Green'),('standard','#65748b','#f5f7fa','感谢支持','Thank you')]
def width(s):return sum(17 if c == '\u2003' or unicodedata.east_asian_width(c) in 'WF' else 9 for c in s)
for lang in ['zh','en']:
 blocks=[];y=4
 for key,color,bg,zh,en in groups:
  names=[p['name'] for p in data['supporters'] if p['color']==key];lines=[];line=''
  for name in names:
   proposal=line+'\u2003\u2003'+name if line else name
   if width(proposal)>748 and line:lines.append(line);line=name
   else:line=proposal
  if line:lines.append(line)
  h=69+len(lines)*30
  blocks += [f'<rect x="4" y="{y}" width="852" height="{h}" rx="14" fill="{bg}" stroke="{color}" stroke-opacity=".18"/>',f'<rect x="4" y="{y+16}" width="4" height="{h-32}" rx="2" fill="{color}"/>',f'<text x="28" y="{y+31}" font-size="15" font-weight="650" fill="{color}">{zh if lang=="zh" else en}</text>',f'<text x="828" y="{y+31}" text-anchor="end" font-size="12" fill="{color}">{len(names)}'+(' 位支持者' if lang=='zh' else ' supporters')+'</text>']
  for i,line in enumerate(lines):blocks.append(f'<text x="28" y="{y+64+i*30}" font-size="16" fill="{color}" xml:space="preserve">{html.escape(line)}</text>')
  y+=h+12
 svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="860" height="{y}" viewBox="0 0 860 {y}" role="img" aria-label="'+('赞赏支持者名单' if lang=='zh' else 'Supporter list')+'"><g font-family="-apple-system,BlinkMacSystemFont,Segoe UI,PingFang SC,Microsoft YaHei,sans-serif">'+''.join(blocks)+'</g></svg>'
 (root/f'assets/supporters-{lang}.svg').write_text(svg)
for name in ['README.md','README.zh-CN.md','README.en.md']:
 p=root/name;s=p.read_text();en=name=='README.en.md';a=s.index('\n## Thank you for your support' if en else '\n## 感谢每一份支持');s=s[:a]
 s+=('\n## Thank you for your support\n\nEvery contribution helps keep these projects moving. **{count} supporter entries** · Records through {en_cutoff}\n\n![Supporter names grouped by appreciation color](assets/supporters-en.svg)\n\nNames are separated by spaces. Name colors reflect cumulative contributions as a gesture of thanks; payment amounts and avatars are not published. [View the data used by the app](supporters.json).\n' if en else '\n## 感谢每一份支持\n\n每一份支持，都在帮助这些小工具继续前进。**{count} 个展示条目** · 记录截止 {zh_cutoff}\n\n![按赞赏颜色分组的支持者名单](assets/supporters-zh.svg)\n\n名字之间留白排列，昵称颜色按累计赞赏金额区分，仅用于表达感谢；不公开金额或头像。[查看 App 同步名单](supporters.json)。\n');s=s.replace('{count}',str(count)).replace('{zh_cutoff}',zh_cutoff).replace('{en_cutoff}',en_cutoff)
 s+='\n<details>\n<summary>'+('Searchable text list' if en else '展开文字名单（可搜索昵称）')+'</summary>\n\n'
 for key,color,bg,zh,en_title in groups:
  names=[person['name'] for person in data['supporters'] if person['color']==key]
  if names:
   escaped=[person.replace('\\','\\\\').replace('*','\\*').replace('_','\\_').replace('<','&lt;').replace('>','&gt;') for person in names]
   s+='**'+(en_title if en else zh)+'**\n\n'+'　'.join(escaped)+'\n\n'
 s+='</details>\n'
 p.write_text(s)
print('Generated two SVG supporter panels; no names omitted')
