import re, json, html, sys, subprocess, urllib.parse, time
BASE="https://sldict.korean.go.kr"
def get(url):
    for i in range(5):
        r=subprocess.run(["curl","-s","-A","Mozilla/5.0","-m","60",url],capture_output=True)
        s=r.stdout.decode("utf-8","ignore")
        if len(s)>1000: return s
        time.sleep(2)
    return ""
def search(w):
    s=get(f"{BASE}/front/search/searchSignCteList.do?searchKeyword={urllib.parse.quote(w)}&search_gubun=cte&pageIndex=1")
    out=[]
    for m in re.finditer(r"fnSearchContentsView\('(\d+)', '(\w+)', '\d+'\);\"[^>]*>(.*?)</a>", s, re.S):
        t=html.unescape(re.sub(r"\s+"," ",re.sub("<[^>]+>","",m.group(3)))).strip()
        if t: out.append([m.group(1),m.group(2),t])
    return out
res={}
for w in sys.argv[2:]:
    res[w]=search(w); print(w, res[w][:6], flush=True)
json.dump(res,open(sys.argv[1],"w"),ensure_ascii=False)
