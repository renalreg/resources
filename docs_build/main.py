import os
import sys
import lxml.etree as ET
from typing import List
from pathlib import Path

in_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])
xsl_path = Path("stylesheet.xsl")

out_path.mkdir(exist_ok=True)

xslt = ET.parse(xsl_path.as_posix())
transform = ET.XSLT(xslt)


def make_index(title: str, dir_links: List[str], file_links: List[str]):
    file_links.sort()
    dir_links.sort()

    content = f"<html><head><title>{title}</title><link rel='stylesheet' href='https://maxcdn.bootstrapcdn.com/bootstrap/3.3.4/css/bootstrap.min.css' /></head><h1>{title}</h1>"

    content += "<h2>Directories</h2>"
    content += "<ul>"
    if title != in_path:
        content += "<li><a href='../'>..</a></li>"
    for link in dir_links:
        content += f"<li><a href='{link}'>{link}</a></li>"
    content += "</ul>"

    content += "<h2>Files</h2>"
    content += "<ul>"
    for link in file_links:
        basename = link.split(".")[0]
        content += f"<li><a href='{link}'>{basename}</a></li>"
    content += "</ul>"

    content += "</html>"
    return content


for path, dirs, files in os.walk(in_path):

    path_relative_to_base = Path(path).relative_to(in_path)
    page_dir = out_path.joinpath(path_relative_to_base)
    page_dir.mkdir(exist_ok=True)

    file_links = []

    for xsd_file in [f for f in files if f.endswith(".xsd")]:
        base_name = xsd_file.split(".xsd")[0]

        in_file = Path(path).joinpath(xsd_file)
        
        html_filename = f"{base_name}.html"

        out_file = page_dir.joinpath(html_filename)

        file_links.append(html_filename)

        print(out_file)

        dom = ET.parse(in_file.as_posix())
        newdom = transform(dom)

        with open(out_file, "wb") as html:
            html.write(ET.tostring(newdom, pretty_print=True))

    index_path = out_path.joinpath(path_relative_to_base, "index.html")
    with open(index_path, "w") as html:
        html.write(make_index(path, dirs, file_links))
