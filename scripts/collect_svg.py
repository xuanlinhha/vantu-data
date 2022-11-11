from pathlib import Path
import json, os
from html_minifier.minify import Minifier

ROOT = Path().resolve().parent

def file_exists(file):
  repo = "/Users/xuanlinhha/Documents/Workspace/Chinese/makemeahanzi/"
  folders = ["svgs", "svgs-still"]
  for f in folders:
    file_path = os.path.join(repo, f, file)
    if (os.path.exists(file_path)):
      return True, file_path
  return False, ""

def write_html(html, file):
  folder = "/Users/xuanlinhha/Documents/Workspace/Chinese/svg/"
  f = open(os.path.join(folder, file), "w")
  f.write(html)
  f.close()

def copy_svgs():
  f = open(os.path.join(ROOT, "data", "Chars.json"), "r")
  chars = json.load(f)
  no_svgs = []
  minifier = Minifier()
  for c in chars:
    svg = str(ord(c)) + ".svg"
    exist, file_path = file_exists(svg)
    if not exist:
      no_svgs.append(c)
    else:
      tmp = open(file_path, "r")
      minifier.html = tmp.read()
      html = minifier.minify()
      write_html(html, svg)

# copy_svgs()

def add_svg():
  f = open(os.path.join(ROOT, "data", "export.json"), "r")
  lines = f.readlines()
  f.close
  new_lines = []
  folder = "/Users/xuanlinhha/Documents/Workspace/Chinese/svg/"
  for line in lines:
    p = json.loads(line)
    p["svg"] = None
    if len(p["han"]) == 1:
      svg_file = os.path.join(folder, str(ord(p["han"])) + ".svg")
      if (os.path.exists(svg_file)):
        f = open(svg_file, "r")
        svg = f.read()
        f.close
        p["svg"] = svg
    new_lines.append(json.dumps(p) + os.linesep)
  f = open(os.path.join(ROOT, "data", "with_svg.json"), "w")
  f.writelines(new_lines)
  f.close

add_svg()
