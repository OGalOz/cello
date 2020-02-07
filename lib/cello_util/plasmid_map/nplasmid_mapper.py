#python3

"""
Process:
    plasmid_mapper takes gbk file, config file, and output name and does the following:
    1. Genbank file goes through "genbank_prepare" preparation:
        (Clears tmp dir)
         a. Remove duplicate sections

    2. "feature_prepare" takes Genbank File and prepares two
        json files: plasmid_info.json, and feature_list.json

    3. canvas_prepare takes plasmid_info.json, feature_list.json, and config.json
        and creates js_feats.json

    4. canvas_make takes js_feats.json and creates plasmid_js.js

    5. html_prepare takes plasmid_js.js and template.html and creates the final
        html_file

    



"""

import sys
from os import path
from prepare_features import feature_prepare
from py_feat_to_js_feat import canvas_prepare
from features_to_canvas import make_canvas_js

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



    canvas_prepare(feature_list_fp, plasmid_info_fp, config_fp)

    js_feats_fp = path.join(program_dir, "tmp/js_feats.json")
    make_canvas_js(js_feats_fp)

    plasmid_js = path.join(program_dir, "tmp/plasmid_js.js")

    html_prepare(plasmid_js, out_fp)

    return 0


"""
Inputs:
    gbk_input: (str) Filepath to input genbank
"""
def genbank_prepare(gbk_input):


    return 0







"""
Inputs:
    plasmid_js: (str) filepath to file containing javascript string.
    out_fp: (str) filepath to where we'll write the file out.
"""
def html_prepare(plasmid_js_fp, out_fp):


    return 0


if __name__ == "__main__":
    main()


