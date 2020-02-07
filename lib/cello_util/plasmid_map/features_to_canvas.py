#python3
"""
This file takes list of features prepared by py_feat_to_js_feat
and converts them into actual javascript.
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
from js_print import *

def make_canvas_js(js_feats_fp):
    with open(js_feats_fp) as f:
        js_feats_list = json.loads(f.read())


    javascript_str = "//Canvas Code Start \n"
    for i in len(js_feats_list):
        js_feat = js_feats_list[i]
        if js_feat["type"] == "plasmid_arc_forward":
            js_str = print_plasmid_arc_forward(js_feat)
        elif js_feat["type"] == "plasmid_arc_reverse":
            js_str = print_plasmid_arc_reverse(js_feat)

        elif js_feat["type"] == "pointer_and_text":
            js_str = print_pointer_and_text(js_feat)

        elif js_feat["type"] == "center_text":
            js_str = print_center_text(js_feat)

        elif js_feat["type"] == "promoter":
            js_str = print_promoter(js_feat)

        elif js_feat["type"] == "terminator":
            js_str = print_terminator(js_feat)

        elif js_feat["type"] == "rbs":
            js_str = print_rbs(js_feat)

        elif js_feat["type"] == "cds":
            js_str = print_cds(js_feat)

        elif js_feat["type"] == "gap_arc":
            js_str = print_gap_arc(js_feat)

        else:
            logging.info("Did not recognize feature to translate to javascipt.")

        javascript_str += "//Feature: {} + \n".format(str(i)) + js_str

    return  






