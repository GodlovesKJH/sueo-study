import re, json, html, sys, subprocess, time
BASE="https://sldict.korean.go.kr"
def get(url):
    for i in range(5):
        r=subprocess.run(["curl","-s","-A","Mozilla/5.0","-m","60",url],capture_output=True)
        s=r.stdout.decode("utf-8","ignore")
        if "수형 설명" in s: return s
        time.sleep(2)
    return ""
def view(no):
    s=get(f"{BASE}/front/sign/signContentsView.do?origin_no={no}&top_category=CTE")
    imgs=re.findall(r'(/multimedia/multimedia_files/convert/[^"\']+?_700X466\.jpg)', s)
    t=re.sub(r"<script.*?</script>","",s,flags=re.S)
    lines=[l.strip() for l in html.unescape(re.sub(r"<[^>]+>","\n",t)).split("\n") if l.strip()]
    desc=""; title=""
    for i,l in enumerate(lines):
        if l=="수형 설명" and i+1<len(lines): desc=lines[i+1]
    m=re.search(r'<dt>\s*한국어\s*</dt>\s*<dd[^>]*>(.*?)</dd>', s, re.S)
    seen=[]; [seen.append(u.replace("/multimedia/multimedia_files/convert/","")) for u in imgs if u.replace("/multimedia/multimedia_files/convert/","") not in seen]
    return seen, desc
out={}
for pair in sys.argv[2:]:
    w,no=pair.split("=")
    imgs,desc=view(no); out[w]=[no,imgs,desc]; print(w,no,len(imgs),desc[:70],flush=True)
json.dump(out,open(sys.argv[1],"w"),ensure_ascii=False)
