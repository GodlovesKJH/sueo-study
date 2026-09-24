"""국립국어원 한국수어사전에서 단어별 수형 사진 URL과 수형 설명을 모읍니다."""
import re, json, time, html, sys, urllib.parse, urllib.request

BASE = "https://sldict.korean.go.kr"
UA = {"User-Agent": "Mozilla/5.0"}

def get(url):
    for i in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
                return r.read().decode("utf-8", "ignore")
        except Exception as e:
            time.sleep(2)
    return ""

def search(word):
    s = get(f"{BASE}/front/search/searchAllList.do?searchKeyword={urllib.parse.quote(word)}")
    out = []
    for m in re.finditer(r"href=\"javascript:fnSearchContentsView\('(\d+)', '(\w+)', '\d+'\);\"[^>]*>(.*?)</a>", s, re.S):
        title = re.sub(r"\s+", " ", re.sub("<[^>]+>", "", m.group(3))).strip()
        if title: out.append((m.group(1), m.group(2), html.unescape(title)))
    return out

def view(no, cat):
    s = get(f"{BASE}/front/sign/signContentsView.do?origin_no={no}&top_category={cat}&category=&searchKeyword=&searchCondition=&search_gubun=&museum_type=00&current_pos_index=0")
    imgs = re.findall(r'src="https?://sldict\.korean\.go\.kr(/multimedia/[^"]+/(?:IMG|PIC)[^"]+_700X466\.jpg)"', s)
    t = re.sub(r"<script.*?</script>", "", s, flags=re.S)
    t = html.unescape(re.sub(r"<[^>]+>", "\n", t))
    lines = [l.strip() for l in t.split("\n") if l.strip()]
    desc = ""
    for i, l in enumerate(lines):
        if l == "수형 설명" and i + 1 < len(lines):
            desc = lines[i + 1]; break
    seen = []; [seen.append(u) for u in imgs if u not in seen]
    return seen, desc

# 앱의 단어 → (사전 검색어, 사전 표제어 중 일치시킬 말)
ALIAS = {
    "미안합니다": ("미안하다", "미안하다"), "네": ("예", "예"), "아니요": ("아니다", "아니다"),
    "잘 가": ("안녕하세요", "안녕히 가십시오"), "수고하다": ("수고", "수고"), "아버지": ("아빠", "아버지"),
    "선생님": ("선생", "선생"), "피곤하다": ("피곤", "피곤"), "재미있다": ("재미", "재미"),
    "천천히": ("천천하다", "천천하다"), "예수": ("예수님", "예수님"), "찬양": ("찬송", "찬송"),
    "집안": ("가정", "집안"),
}

def pick(word, results):
    alias = [ALIAS[word][1]] if word in ALIAS else [word]
    best = None
    for no, cat, title in results:
        parts = [p.strip() for p in title.split(",")]
        for a in alias:
            if a in parts:
                score = (0 if cat == "CTE" else 1, parts.index(a), len(parts))
                if best is None or score < best[0]:
                    best = (score, no, cat, title)
    return best

words = json.load(open(sys.argv[1], encoding="utf-8"))
data = {}
for w in words:
    res = search(ALIAS.get(w, (w,))[0]); time.sleep(0.4)
    b = pick(w, res)
    if not b:
        print("NO MATCH", w, [r[2] for r in res][:5]); continue
    _, no, cat, title = b
    imgs, desc = view(no, cat); time.sleep(0.4)
    data[w] = {"no": no, "cat": cat, "title": title, "img": imgs, "desc": desc}
    print(w, "→", title, len(imgs), "imgs |", desc[:40])
json.dump(data, open(sys.argv[2], "w", encoding="utf-8"), ensure_ascii=False, indent=1)
