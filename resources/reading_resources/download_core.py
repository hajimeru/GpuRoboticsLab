import urllib.request,json,hashlib,zipfile,concurrent.futures
from pathlib import Path
root=Path(__file__).resolve().parent
groups=[('06_Modern_Robotics','Modern Robotics','https://hades.mech.northwestern.edu/index.php/Modern_Robotics',[
('Modern_Robotics_preprint_2019.pdf','https://hades.mech.northwestern.edu/images/2/25/MR-v2.pdf','官方免费完整预印本'),('practice_exercises.pdf','https://hades.mech.northwestern.edu/images/e/ef/MR_practice_exercises.pdf','练习及解答'),('ModernRobotics_code.zip','https://codeload.github.com/NxRLab/ModernRobotics/zip/refs/heads/master','配套代码')]),
('10_Introduction_to_Applied_Linear_Algebra','Introduction to Applied Linear Algebra','https://stanford.edu/~boyd/vmls/',[(n,'https://stanford.edu/~boyd/vmls/'+u,t) for n,u,t in [('VMLS_full_book.pdf','vmls.pdf','官方免费全文'),('lecture_slides.pdf','vmls-slides.pdf','讲义'),('julia_companion.pdf','vmls-julia-companion.pdf','Julia配套教材'),('additional_exercises.pdf','vmls-additional-exercises.pdf','补充练习')]]),
('12_Planning_Algorithms','Planning Algorithms','https://lavalle.pl/planning/',[('Planning_Algorithms_full_book.pdf','https://lavalle.pl/planning/bookbig.pdf','官方免费全文')]),
('16_Algorithms_for_Optimization','Algorithms for Optimization','https://algorithmsbook.com/optimization/',[('Algorithms_for_Optimization_1e.pdf','https://algorithmsbook.com/optimization/files/optimization-1e.pdf','官方免费全文（2019第一版，匹配书单）'),('algforopt_notebooks.zip','https://codeload.github.com/algorithmsbooks/algforopt-notebooks/zip/refs/heads/master','配套代码')])]
def group(g):
 folder,title,source,items=g
 d=root/folder;d.mkdir(exist_ok=True)
 result=[]
 for name,url,kind in items:
  row=dict(title=title,source=source,url=url,path=name,type=kind)
  try:
   data=urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'}),timeout=90).read()
   if name.endswith('.pdf') and not data.startswith(b'%PDF'): raise ValueError('not a PDF')
   (d/name).write_bytes(data)
   if name.endswith('.zip'):
    with zipfile.ZipFile(d/name) as z:
     if z.testzip():raise ValueError('bad zip')
   row.update(status='downloaded',bytes=len(data),sha256=hashlib.sha256(data).hexdigest())
   print(folder,name,len(data),flush=True)
  except Exception as e:row.update(status='failed',error=str(e));print(name,str(e),flush=True)
  result.append(row)
 (d/'metadata.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:list(pool.map(group,groups))
