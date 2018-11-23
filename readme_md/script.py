import os

filename = "test"

csspath = "./text.css"

cmd = f"pandoc -f markdown -t html5 ./{filename}.md --filter=./convertlinks.py -c {csspath} -o {filename}.html"

os.system(cmd)
