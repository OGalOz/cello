#python3


"""
This file takes features_list and plasmid_info json files and creates pre-javascript features,
divided into sections by type:
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
        plasmid_name:
        plasmid_len:
        text_size:
        font_type:

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

from Bio import SeqIO
import json
from plasmid_sbol_visuals import *




"""
Inputs:
    feature_list_fp: (str) file path to feature list json file.
    plasmid_info_fp: (str) file path to plasmid info json file.
    config_fp: (str) file path to config info json file
"""
def canvas_prepare(feature_list_fp, plasmid_info_fp, config_fp):
    with open(feature_list_fp, "r") as f:
        feature_dict_list = json.loads(f.read())

    with open(plasmid_info_fp, "r") as f:
        plasmid_info = json.loads(f.read())

    with open(config_fp, "r") as f:
        config_dict = json.loads(f.read())


    javascript_object_list = create_javascript_object_list(feature_dict_list,
            plasmid_info, config_dict)

    with open("tmp/js_feats.json", "w") as f:
        f.write(json.dumps(javascript_object_list, indent=2, sort_keys=True))
    

    return 0 


def create_javascript_object_list(feature_dict_list, plasmid_info, config_dict):
   
    javascript_object_list = []
    types_dict = config_dict["genbank_info"]["types_dict"]

    for feature_dict in feature_dict_list:
        arc_object = create_arc(feature_dict, config_dict)
        javascript_object_list.append(arc_object)
        pointer_and_text_object = calculate_pointer_and_text(feature_dict, 
                config_dict)
        javascript_object_list.append(pointer_and_text_object)

        feat_type = feature_dict['feat_type']
        
        #Note, all the functions that begin with "calculate"
        # come from plasmid_sbol_visuals
        if feat_type in types_dict["promoter"]:
            javascript_object_list.append(calculate_promoter_feature(feature_dict, config_dict))
        elif feat_type in types_dict["terminator"]:
            javascript_object_list.append(calculate_terminator_feature(feature_dict, config_dict))
        elif feat_type in types_dict["rbs"]:
            javascript_object_list.append(calculate_rbs_feature(feature_dict, config_dict))
        elif feat_type in types_dict["cds"]:
            javascript_object_list.append(calculate_cds_feature(feature_dict, config_dict))
        elif feat_type in types_dict["scar"]:
            pass
        elif feat_type in types_dict["ribozyme"]:
            pass
        elif feat_type in types_dict["backbone"]:
            pass
        elif feat_type in types_dict["misc_feature"]:
            pass
        else:
            logging.critical("Did not recognize type of feature: \
                    {}".format(feat_type))


    plasmid_name_object = create_center_text(plasmid_info, config_dict)
    javascript_object_list.append(plasmid_name_object)

    return javascript_object_list

def create_arc(feature_dict, config_dict):
    
    feat_type = feature_dict['feat_type']
    if feat_type not in config_dict["genbank_info"]["gap_names"]:
        #Regular arc
        if feature_dict['feat_strand'] == 1:
            #Positive arc
            js_object = {
                    "type": "plasmid_arc_forward",
                    "arc_start": feature_dict['angle_start'],
                    "arc_end": feature_dict['angle_end'],
                    "arc_angle":feature_dict['angle_end'] - feature_dict['angle_start'],
                    "line_width": config_dict['js_info']['circle_line_width'],
                    "internal_color":feature_dict['feat_color'],
                    "center_x":config_dict['js_info']['center_coordinates'][0],
                    "center_y":config_dict['js_info']['center_coordinates'][1],
                    "radius": config_dict['js_info']['circle_radius']
            }


        else:
            #Complementary arc
            js_object = {
                    "type": "plasmid_arc_reverse",
                    "arc_start": feature_dict['angle_start'],
                    "arc_end": feature_dict['angle_end'],
                    "arc_angle":feature_dict['angle_end'] - feature_dict['angle_start'],
                    "line_width": config_dict['js_info']['circle_line_width'],
                    "internal_color":feature_dict['feat_color'],
                    "center_x":config_dict['js_info']['center_coordinates'][0],
                    "center_y":config_dict['js_info']['center_coordinates'][1],
                    "radius": config_dict['js_info']['complementary_radius']
            }

    else:
        #gap arc
        js_object = {
                    "type": "gap_arc",
                    "arc_start": feature_dict['angle_start'],
                    "arc_end": feature_dict['angle_end'],
                    "arc_angle":feature_dict['angle_end'] - feature_dict['angle_start'],
                    "line_width": config_dict['js_info']['gap_arc_info']['circle_line_width'],
                    "internal_color": config_dict['js_info']['gap_arc_info']['color'], 
                    "center_x":config_dict['js_info']['center_coordinates'][0],
                    "center_y":config_dict['js_info']['center_coordinates'][1],
                    "radius": config_dict['js_info']['circle_radius']
            }

    return js_object


def create_center_text(plasmid_info, config_dict):

    js_info = config_dict['js_info']
    plasmid_name_str = plasmid_info['plasmid_name']
    cc = js_info['center_coordinates']

    if "max_title_length" in js_info:
        max_t_len = js_info["max_title_length"]
    else:
        max_t_len = 45
    if len(plasmid_name_str) > max_t_len:
        logging.critical("Plasmid name is too long - using placeholder name: 'Plasmid'")
        plasmid_name_str = "Plasmid"

    #We add the text box with the name, calculating center of the word to be center of circle,
    # and each letter has length 12 pixels
    plasmid_name_length = len(plasmid_name_str)*15
    plasmid_name_start = cc[0] - float(plasmid_name_length)/2

    #Getting length of plasmid and placing it under plasmid name
    plasmid_length_str = str(plasmid_info['plasmid_length']) + " bp"
    if len(plasmid_length_str) > 13:
        logging.warning("Plasmid string length is over ten digits.")
        plasmid_length = '? bp'

    #We add the text box with the length, 20 to the left of center, and 20 below
    plasmid_length_str_len = len(plasmid_length_str)*15
    plasmid_length_str_start = cc[0] - float(plasmid_length_str_len)/2

    font_style = "bold {}pt Calibri".format(js_info['title_text_size'])

    center_text_obj = {
        "type" : "center_text",
        "plasmid_name": plasmid_name_str,
        "name_start_x": plasmid_name_start,
        "name_start_y": cc[1] - 15,
        "length_str": plasmid_length_str,
        "length_start_x": plasmid_length_str_start,
        "length_start_y": cc[1] + 15,
        "font_style": font_style,
        "fill_color": js_info["title_text_color"]
    }


    return center_text_obj 

