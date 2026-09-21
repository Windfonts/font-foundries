#!/usr/bin/env python3
"""字体天下头像全量下载 → avatars/{authorId}.{ext}
站点默认占位图 author-avatar-default.jpg 统一硬链到缓存副本,不重复存。
"""
import json, os, time, urllib.request, threading
from concurrent.futures import ThreadPoolExecutor

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(BASE, 'data', 'authors-index.json')
OUT_DIR = os.path.join(BASE, 'avatars')
DEFAULT_CACHE = os.path.join(OUT_DIR, '_default.jpg')
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
LOCK = threading.Lock()

def fetch(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={'User-Agent': UA})
            with urllib.request.urlopen(req, timeout=20) as r:
                return r.read()
        except Exception:
            if i < tries - 1: time.sleep(1)
    return None

def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    authors = json.load(open(INDEX))
    stats = {'ok': 0, 'default': 0, 'fail': 0}

    def work(a):
        url = a.get('avatar') or ''
        if not url:
            with LOCK: stats['fail'] += 1
            return
        fname = url.rsplit('/', 1)[-1]
        ext = os.path.splitext(fname)[1] or '.jpg'
        dest = os.path.join(OUT_DIR, a['authorId'] + ext)
        if os.path.exists(dest) and os.path.getsize(dest) > 0:
            return  # 断点续传
        if fname == 'author-avatar-default.jpg':
            with LOCK:
                if not os.path.exists(DEFAULT_CACHE):
                    buf = fetch(url)
                    if buf: open(DEFAULT_CACHE, 'wb').write(buf)
                if os.path.exists(DEFAULT_CACHE):
                    try: os.link(DEFAULT_CACHE, dest); stats['default'] += 1
                    except OSError: os.link(DEFAULT_CACHE, dest)
            return
        buf = fetch(url)
        if buf:
            open(dest, 'wb').write(buf)
            with LOCK: stats['ok'] += 1
        else:
            with LOCK: stats['fail'] += 1
            print('FAIL', a['authorId'], a['name'], url, flush=True)
        n = stats['ok'] + stats['default'] + stats['fail']
        if n % 500 == 0:
            with LOCK: print(f"{n}/{len(authors)} real={stats['ok']} default={stats['default']} fail={stats['fail']}", flush=True)

    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(work, authors))
    print(f"FINISHED real={stats['ok']} default={stats['default']} fail={stats['fail']}", flush=True)

if __name__ == '__main__':
    main()
