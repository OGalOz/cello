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

    5. features_to_svg takes js_feats.json and creates plasmid_js.js

    6. html_prepare takes plasmid_js.js and template.html and creates the final
        html_file

    



"""

import sys
import os
from os import path
import shutil
from cello_util.plasmid_map.prepare_gbk import genbank_prep 
from cello_util.plasmid_map.prep_py_feat import feature_prepare
from cello_util.plasmid_map.feature_refine import refine_features
from cello_util.plasmid_map.py_feat_to_js_feat import js_prepare
from cello_util.plasmid_map.features_to_svg import make_svg_js
from cello_util.plasmid_map.plasmid_html import html_prepare, div_html_prepare


def get_cello_plasmid_map_div(gbk_input,base_div_html_fp, config_fp, uniq_dict):
       

    program_dir = path.dirname(path.abspath(__file__))


    prepared_genbank_fp = path.join(program_dir, "tmp/prepared_genbank.gbk")

    old_gb_name = genbank_prep(gbk_input, config_fp, prepared_genbank_fp)
    

    feature_list_fp = path.join(program_dir, "tmp/feature_list.json")

    plasmid_info_fp = path.join(program_dir, "tmp/plasmid_info.json")

    feature_prepare(prepared_genbank_fp, config_fp, feature_list_fp, 
            plasmid_info_fp, old_gb_name)


    js_feats_fp = path.join(program_dir, "tmp/js_feats.json")

    js_prepare(feature_list_fp, plasmid_info_fp, config_fp, js_feats_fp, 
            uniq_dict)

    plasmid_js_fp = path.join(program_dir, "tmp/plasmid_js.js")
    make_svg_js(js_feats_fp, plasmid_js_fp, uniq_dict)

    template_html_fp = path.join(program_dir, base_div_html_fp)

    html_dict = div_html_prepare(plasmid_js_fp, template_html_fp, config_fp, 
            plasmid_info_fp, uniq_dict)

    #We copy all the contents of the folder to a tmp folder in the scratch dir
    shutil.copytree(path.join(program_dir, "tmp"),
    path.join(uniq_dict["scratch_dir"],uniq_dict["tmp_name"]))

    return html_dict


def main():
    args = sys.argv
    gbk_input    = args[1] 
    config_fp = args[2] 
    out_fp       = args[3] 
       
    program_dir = path.dirname(path.abspath(__file__))

    genbank_prep(gbk_input, config_fp)
    
    prepared_genbank_fp = path.join(program_dir, "tmp/prepared_genbank.gbk")

    feature_list_fp = path.join(program_dir, "tmp/feature_list.json")

    plasmid_info_fp = path.join(program_dir, "tmp/plasmid_info.json")

    feature_prepare(prepared_genbank_fp, config_fp, feature_list_fp, plasmid_info_fp)


    js_feats_fp = path.join(program_dir, "tmp/js_feats.json")

    js_prepare(feature_list_fp, plasmid_info_fp, config_fp, js_feats_fp, 
            uniq_dict)

    plasmid_js_fp = path.join(program_dir, "tmp/plasmid_js.js")
    make_svg_js(js_feats_fp, plasmid_js_fp)

    template_html_fp = path.join(program_dir, "div_svg_template.html")

    html_prepare(plasmid_js_fp, template_html_fp, out_fp, config_fp)

    return 0


if __name__ == "__main__":
    main()


