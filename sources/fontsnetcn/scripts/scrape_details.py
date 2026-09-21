#!/usr/bin/env python3
"""字体天下(fonts.net.cn) 作者详情页全量抓取 → data/authors.jsonl
输入:data/authors-index.json(列表页索引,见 scrape_list.sh)
断点续传:JSONL 里已有的 authorId 跳过。限速:5 workers × 0.75s ≈ 6.7 req/s。
"""
import json, os, re, sys, time, urllib.request, threading
from concurrent.futures import ThreadPoolExecutor

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
INDEX = os.path.join(BASE, 'data', 'authors-index.json')
OUT = os.path.join(BASE, 'data', 'authors.jsonl')
LOCK = threading.Lock()

RE_NAME = re.compile(r'<h2 class="site_author_sh_name">([^<]+)</h2>')
RE_TYPE = re.compile(r'<p class="site_author_sh_type">([^<]+)</p>')
RE_DESC = re.compile(r'<p class="site_author_sh_desc">([^<]*)</p>')

def fetch(url, tries=4):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read().decode('utf-8', 'ignore')
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503) and i < tries - 1:
                time.sleep(2 * (i + 1)); continue
            return None
        except Exception:
            if i < tries - 1: time.sleep(1); continue
            return None
    return None

def main():
    authors = json.load(open(INDEX))
    done = set()
    if os.path.exists(OUT):
        for line in open(OUT):
            try: done.add(json.loads(line)['authorId'])
            except Exception: pass
    todo = [a for a in authors if a['authorId'] not in done]
    print(f'total {len(authors)}, done {len(done)}, todo {len(todo)}', flush=True)
    stats = {'ok': 0, 'fail': 0}

    def work(a):
        time.sleep(0.3)
        html = fetch(f"https://www.fonts.net.cn/author-{a['authorId']}-1.html")
        if html is None:
            with LOCK: stats['fail'] += 1
            return
        name = RE_NAME.search(html); typ = RE_TYPE.search(html); desc = RE_DESC.search(html)
        rec = {
            'authorId': a['authorId'],
            'name': (name.group(1) if name else a['name']).strip(),
            'siteName': a['name'],
            'type': typ.group(1).strip() if typ else '',
            'description': desc.group(1).strip() if desc else '',
            'fonts': a.get('fonts', 0),
            'popularity': a.get('pop', 0),
            'avatarUrl': a.get('avatar', ''),
            'sourceUrl': f"https://www.fonts.net.cn/author-{a['authorId']}-1.html",
            'fetchedAt': '2026-09-21',
        }
        with LOCK:
            with open(OUT, 'a') as f:
                f.write(json.dumps(rec, ensure_ascii=False) + '\n')
            stats['ok'] += 1
            n = stats['ok'] + stats['fail']
            if n % 200 == 0: print(f'{n}/{len(todo)} ok={stats["ok"]} fail={stats["fail"]}', flush=True)

    with ThreadPoolExecutor(max_workers=12) as ex:
        list(ex.map(work, todo))
    print(f'FINISHED ok={stats["ok"]} fail={stats["fail"]}', flush=True)

if __name__ == '__main__':
    main()
