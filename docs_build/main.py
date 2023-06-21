import os
import re
import sys
from pathlib import Path
from typing import List

import lxml.etree as ET

in_path = Path(sys.argv[1])
out_path = Path(sys.argv[2])
xsl_path = Path(__file__).parent.joinpath("stylesheet.xsl")

out_path.mkdir(exist_ok=True)

xslt = ET.parse(xsl_path.as_posix())
transform = ET.XSLT(xslt)

type_paths = {}


def replace_strings(html_document, lookup_dict):
    pattern = r'XXX(\w+)YYY'  # Regular expression pattern to match XXXValueYYY
    
    if isinstance(html_document, bytes):
            html_document = html_document.decode()

    def replace(match):
        value = match.group(1)
        
        type_path = lookup_dict.get(value, None)

        if type_path:
            replacement = f"<A HREF='{type_path}'>Type: {value}</A>"
        else:
            replacement = f"Type: {value}"

        return replacement

    replaced_html = re.sub(pattern, replace, html_document)

    return replaced_html


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

    for xsd_file in [f for f in files if f.endswith(".xsd")]:
    
        in_file = Path(path).joinpath(xsd_file)
        dom = ET.parse(in_file.as_posix())
        
        namespace = "http://www.w3.org/2001/XMLSchema"
        xpath_expr = "//xs:complexType/@name|//xs:simpleType/@name"
        xsd_types = dom.xpath(xpath_expr, namespaces={"xs": namespace})
        
        for xsd_type in xsd_types:
            type_path = str(in_file).replace('schema/ukrdc/', '')
            
            # HACK: This only fixes a specific case.
            type_path_list = type_path.split('/')
            if type_path_list[0] == type_path_list[1]:
                type_path = "/".join(type_path_list[1:])
            # type_path.replace('Types/Types/', 'Types/')
            
            type_paths[xsd_type] = str(type_path)[:-4] + ".html"

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
        
        html_string = ET.tostring(newdom, pretty_print=True)
        
        # TODO: This doesn't work if the definition is in a different
        # file in the same folder as it's being used in.
        # The replace function needs to take account of the current path.
        html_string = replace_strings(html_string, type_paths)

        with open(out_file, "w") as html_file:
            html_file.write(html_string)

    index_path = out_path.joinpath(path_relative_to_base, "index.html")
    with open(index_path, "w") as html:
        html.write(make_index(path, dirs, file_links))
