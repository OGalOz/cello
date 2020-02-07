#python3

"""
Takes template and inserts javascript into template html
"""

"""
Inputs:
    plasmid_js: (str) filepath to file containing javascript string.
    out_fp: (str) filepath to where we'll write the file out.
"""
def html_prepare(plasmid_js_fp, template_html_fp, out_fp):

    with open (plasmid_js_fp, "r") as f:
        js_str = f.read()
    with open(template_html_fp, "r") as g:
        html_str = g.read()
    
    html_and_js_str = html_str.replace("{--Insert JS--}", js_str)

    with open(out_fp, "w") as h:
        h.write(html_and_js_str)



    return 0

