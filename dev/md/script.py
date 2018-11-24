import os
from pathlib import Path

md_files = Path("./").glob("*.md")

#filename = "test"

csspath = "./text.css"

for md in md_files:
    filename = md.stem
    cmd = f"pandoc -f markdown -t html5 ./{filename}.md --filter=./convertlinks.py -c {csspath} -o {filename}.html"
    os.system(cmd)
