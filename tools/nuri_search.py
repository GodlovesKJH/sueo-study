import json, sys, subprocess, time
def post(w):
    for i in range(4):
        r=subprocess.run(["curl","-s","-A","Mozilla/5.0","-m","40","-X","POST","https://ksldict.korean.go.kr/kslserv/search/getSignWordList.do",
          "--data-urlencode",f"searchWord={w}","-d","searchType=kr","-d","limit=20","-d","pagingNum=1"],capture_output=True)
        try: return json.loads(r.stdout)
        except Exception: time.sleep(2)
    return {}
out={}
for w in sys.argv[2:]:
    d=post(w); L=[]
    for x in (d.get("list") or []):
        L.append([x.get("signWordId"), x.get("corExprsCn"), (x.get("signMainVideo") or {}).get("fileThumbnailPath")])
    out[w]=L; print(w, [(a,b[:50] if b else b) for a,b,c in L[:6]], flush=True)
json.dump(out,open(sys.argv[1],"w"),ensure_ascii=False)
