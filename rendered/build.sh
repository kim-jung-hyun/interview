#!/bin/bash
# rendered/ 재생성. interview/rendered 에서 실행한다.
set -e
cd "$(dirname "$0")"
echo "[1/3] 그림 재렌더"
cd ../manager/figures
for f in baseline lifecycle responsibility architecture rmf_cycle; do
  dot -Tsvg $f.dot -o $f.svg; dot -Tpng -Gdpi=110 $f.dot -o $f.png
done
cd ../../rendered
echo "[2/3] 개별 HTML/DOCX"
for f in ../manager/*.md; do
  b=$(basename "$f" .md)
  pandoc "$f" -f gfm -t html5 --standalone --metadata title="$b" --css style.css -o "$b.html"
  pandoc "$f" -f gfm -t docx -o "$b.docx"
done
echo "[3/3] 통합본"
python3 ../make_all.py
pandoc _all.md -f gfm -t html5 --standalone --toc --toc-depth=2 \
  --metadata title="거버넌스 매니저 인터뷰 자료" --css style.css --self-contained -o ALL.html
pandoc _all.md -f gfm -t docx --toc --toc-depth=2 -o ALL.docx
echo "완료 — ALL.html 을 브라우저로 열면 된다"
