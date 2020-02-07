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
        and creates plasmid_js.js
    4. html_prepare takes plasmid_js.js and template.html and creates the final
        html_file

    



"""

import sys
from os import path
from prepare_features import feature_prepare

def main():
    args = sys.argv
    args[1] = gbk_input
    args[2] = config_input
    args[3] = out_fp
       
    program_dir = path.dirname(path.abspath(__file__))

    genbank_prepare(gbk_input)
    
    prepared_genbank_fp = path.join(program_dir, "tmp/prepared_genbank.gbk")

    feature_prepare(prepared_genbank_fp, config_fp)

    feature_list_fp = path.join(program_dir, "tmp/feature_list.json")
    plasmid_info_fp = path.join(program_dir, "tmp/plasmid_info.json")

    canvas_prepare(feature_list_fp, plasmid_info_fp, config_input)

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
    feature_list_fp: (str) file path to feature list json file.
    plasmid_info_fp: (str) file path to plasmid info json file.
    config_input: (str) file path to config info json file
"""
def canvas_prepare(feature_list_fp, plasmid_info_fp, config_input):

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


