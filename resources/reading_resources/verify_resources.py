from pathlib import Path
import json,hashlib,zipfile,tarfile
from pypdf import PdfReader
root=Path(__file__).parent
results=[]
for p in sorted(root.glob('*/*')):
 if p.suffix.lower() not in ['.pdf','.zip','.gz','.ps','.m','.tgz','.tar']:continue
 row={'file':p.relative_to(root).as_posix(),'bytes':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
 try:
  if p.suffix=='.pdf':
   r=PdfReader(p);row['pages']=len(r.pages);row['first_page_text']=r.pages[0].extract_text()[:200]
  elif p.suffix=='.zip':
   with zipfile.ZipFile(p) as z:
    assert z.testzip() is None
    row['entries']=len(z.namelist())
  elif p.name.endswith(('.tar.gz','.tgz')):
   with tarfile.open(p) as t:row['entries']=len(t.getmembers())
  elif p.suffix=='.ps':assert p.read_bytes().startswith(b'%!PS')
  row['validation']='ok'
 except Exception as e:row.update(validation='failed',error=str(e))
 results.append(row)
(root/'verification.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'files':len(results),'bytes':sum(x['bytes'] for x in results),'pdfs':sum('pages' in x for x in results),'failures':[x for x in results if x['validation']!='ok']},ensure_ascii=False))
