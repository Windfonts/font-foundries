#!/bin/bash
# 字体天下作者列表全量扒取:221 页,限速 0.2s
for i in $(seq 1 221); do
  out="pages/authors-$i.html"
  if [ -s "$out" ]; then continue; fi
  curl -sL --compressed -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36" \
    "https://www.fonts.net.cn/authors-$i.html" -o "$out"
  sleep 0.2
done
echo "DONE $(ls pages | wc -l) pages"
