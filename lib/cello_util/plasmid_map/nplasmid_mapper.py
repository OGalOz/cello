#python3

"""
Process:
    plasmid_mapper takes gbk file, config file, and output name and does the following:
    1. Genbank file goes through "genbank_prepare" preparation:
        (Clears tmp dir)
         a. Remove duplicate sections

    2. "feature_prepare" (prep_py_feat.py) takes Genbank File and prepares two
        json files: plasmid_info.json, and feature_list.json

    3. "refine_features" takes feature_list.json and removes unnecessary features
    and adds in gap features.

    4. js_prepare takes plasmid_info.json, feature_list.json, and config.json
        and creates js_feats.json

    5. canvas_make takes js_feats.json and creates plasmid_js.js

    6. html_prepare takes plasmid_js.js and template.html and creates the final
        html_file

    



"""

import sys
from os import path
from prep_py_feat import feature_prepare
from feature_refine import refine_features
from py_feat_to_js_feat import js_prepare
from features_to_canvas import make_canvas_js
from plasmid_html import html_prepare

def main():
    args = sys.argv
    gbk_input    = args[1] 
    config_fp = args[2] 
    out_fp       = args[3] 
       
    program_dir = path.dirname(path.abspath(__file__))

    #genbank_prepare(gbk_input)
    
    #prepared_genbank_fp = path.join(program_dir, "tmp/prepared_genbank.gbk")

    feature_prepare(gbk_input, config_fp)

    feature_list_fp = path.join(program_dir, "tmp/feature_list.json")
    plasmid_info_fp = path.join(program_dir, "tmp/plasmid_info.json")

    

    js_prepare(feature_list_fp, plasmid_info_fp, config_fp)

    js_feats_fp = path.join(program_dir, "tmp/js_feats.json")
    make_canvas_js(js_feats_fp)

    plasmid_js = path.join(program_dir, "tmp/plasmid_js.js")
    template_html_fp = path.join(program_dir, "template.html")

    html_prepare(plasmid_js, template_html_fp, out_fp)

    return 0


"""
Inputs:
    gbk_input: (str) Filepath to input genbank
"""
def genbank_prepare(gbk_input):


    return 0




if __name__ == "__main__":
    main()


