#python3
"""
This file takes list of features prepared by py_feat_to_js_feat
and converts them into actual javascript.
We are using SVG and d3 js by Mike Bostock.
These are the features and their keys (the name is under "type"):
    plasmid_arc_forward:
        arc_start:
        arc_end:
        arc_angle:
        line_width:
        internal_color:
        center_x:
        center_y:
        radius:
    plasmid_arc_reverse
        arc_start:
        arc_end:
        arc_angle:
        line_width:
        internal_color:
        center_x:
        center_y:
        radius:
    pointer_and_text:
        type: (str) pointer_and_text
        pointer:
            type: (str) "pointer"
            new_line_width_bool: (bool)
            line_width: (int)
            line_color: (str)
            start_point: list<int>
            end_point: list<int>
        text:
            text_point: list<int>
            text_str: (str)
            new_text_font_bool: bool
            text_font: (str)

    text:
        text_point:
        text_str:
        new_text_font_bool:
        text_font

    center_text:
        plasmid_name: (str)
        name_start_x: (float)
        name_start_y: (float)
        length_str: (str)
        length_start_x: (float)
        length_start_y: (float)
        font_style: (str)
        fill_color: (str)

    promoter:
        color
        line_width
        p_line_coordinate_start
        big_radius
        arc_begin_point
        arc_start_angle
        arc_angle
        arc_end_angle
        arc_end_point
        inner_flag_start
        outer_flag_start
        flags_end

    terminator:
        border_color:
        internal_color:
        base_1: list<int> earlier angle point touching circle
        base_2: later angle point touching circle
        armpit_1: point directly above base 1 in the T
        armpit_2: point directly above base 2 in the T
        palm_hand_1: bottom edge of T which is closer to armpit 1
        palm_hand_2: bottom edge of T which is closer to armpit 2
        back_hand_1: highest point on T which is right above palm hand 1
        back_hand_2: highest point on T which is right above palm hand 2

    rbs:
        circle_center: 2d-coordinates
        radius: float
        start_angle: float
        end_angle: float
        border_color: str
        internal_color: str
        border_width: int

    cds:
        The CDS visual will look like an arrow head ending at the end of the CDS.
        In order to draw this, we need 6 variables. The variables represent:
            a: point on plasmid map that outer arrow starts.
            b: point outside plasmid map that outer arrow has its peak.
            c: point on plasmid map, same as end of cds, where arrow ends.
            d: inner complement to a.
            e: inner complement to b.
            f: inner complement to c.
            internal_color:

    gap_arc:
        line_width:
        line_color:
        start_angle
        end_angle
        angle:
        center_x:
        center_y:
        radius:

"""

import json
import logging
from cello_util.plasmid_map.js_svg_print import *
#from js_svg_print import *

def make_svg_js(js_feats_fp, plasmid_js_fp, uniq_dict):

    logging.info("Creating Javascript File from feats file.")

    with open(js_feats_fp) as f:
        js_feats_list = json.loads(f.read())


    javascript_str = "//SVG Code Start \n"
    javascript_str += "const {} = d3.select('#{}');\n\n".format(
            uniq_dict['svg_name'], uniq_dict['svg_id'])


    logging.warning(len(js_feats_list))
    for i in range(len(js_feats_list)):
        js_str = ""
        js_feat = js_feats_list[i]
        typ = js_feat["type"]

        if typ == "plasmid_arc_forward":
            js_str = print_plasmid_arc_forward(js_feat, i)
        elif typ == "plasmid_arc_reverse":
            js_str = print_plasmid_arc_reverse(js_feat, i)

        elif typ == "pointer_and_text":
            js_str = print_pointer_and_text(js_feat, i)

        elif typ == "center_text":
            js_str = print_center_text(js_feat, i)

        elif typ == "promoter":
            js_str = print_promoter(js_feat, i)
        #""" 
        #FOR NOW WE AVOID TERMINATOR SYMBOL
        #elif typ == "terminator":
        #    js_str = print_terminator(js_feat, i)
        #"""
        #""" 
        #FOR NOW WE AVOID RBS SYMBOL
        #elif typ == "rbs":
        #    js_str = print_rbs(js_feat, i)
        #"""
        elif typ == "cds":
            js_str = print_cds(js_feat, i)

        elif typ == "gap_arc":
            js_str = print_gap_arc(js_feat, i)
        else:
            logging.info("Did not recognize feature to translate to javascipt.")
            continue

        javascript_str += "//Feature: {} \n".format(str(i)) + js_str



    #Adding delete box:
    js_str = print_delete_box(js_feats_list[-2])
    javascript_str += "//DELETE BOX \n" + js_str

    #Adding reset box:
    js_str = print_reset_box(js_feats_list[-1])
    javascript_str += "//RESET BOX \n" + js_str


    with open(plasmid_js_fp,"w") as g:
        g.write(javascript_str)

    return 0






