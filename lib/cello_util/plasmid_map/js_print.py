#python3
"""
This file maintians the functions for printing
js features into javascript.
List of features:
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
        pointer:
            new_line_width_bool:
            line_width:
            line_color:
            start_point:
            end_point:
        text:
            text_point:
            text_str:
            new_text_font_bool:
            text_font
    text:
        text_point:
        text_str:
        new_text_font_bool:
        text_font

    center_text:
        plasmid_name:
        plasmid_len:
        text_size
        font_type:

    promoter:
        color
        line_width
        arc_start_angle
        arc_angle
        arc_end_angle
        arc_begin_point
        arc_end_point
        inner_flag_start
        inner_flag_end
        outer_flag_start
        outer_flag_end

    terminator:
        border_color:
        internal_color:
        base_1: list<float> earlier angle point touching circle
        base_2: later angle point touching circle
        armpit_1: point directly above base 1 in the T
        armpit_2: point directly above base 2 in the T
        palm_hand_1: bottom edge of T which is closer to armpit 1
        palm_hand_2: bottom edge of T which is closer to armpit 2
        back_hand_1: highest point on T which is right above palm hand 1
        back_hand_2: highest point on T which is right above palm hand 2

    rbs:
        circle_center:
        radius:
        border_color:
        internal_color
        border_width:

    cds:
        The CDS visual will look like an arrow head ending at the end of the CDS.
        In order to draw this, we need 6 variables. The variables represent:
            var_a: point on plasmid map that outer arrow starts.
            var_b: point outside plasmid map that outer arrow has its peak.
            var_c: point on plasmid map, same as end of cds, where arrow ends.
            var_d: inner complement to a.
            var_e: inner complement to b.
            var_f: inner complement to c.
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

def print_plasmid_arc_forward(js_feat):

        js_str = "//Plasmid Arc Forward\n"
        js_str += "ctx.beginPath();\n"
        js_str += "ctx.lineWidth = '{}'".format(str(js_feat['line_width']))
        js_str += "ctx.strokeStyle = '{}'\n".format(js_feat['internal_color'])
        js_str += "ctx.arc({},{},{},{},{});\n".format(
                str(js_feat['center_x']),
                str(js_feat['center_y']),
                str(js_feat['radius']),
                str(js_feat['arc_start']),
                str(js_feat['arc_end'])
                )
        js_str += "ctx.stroke();\n\n"

        return js_str


def print_plasmid_arc_reverse(js_feat):

        js_str = "//Plasmid Arc Reverse\n"
        js_str += "ctx.beginPath();\n"
        js_str += "ctx.lineWidth = '{}'".format(str(js_feat['line_width']))
        js_str += "ctx.strokeStyle = '{}'\n".format(js_feat['internal_color'])
        js_str += "ctx.arc({},{},{},{},{});\n".format(
                str(js_feat['center_x']),
                str(js_feat['center_y']),
                str(js_feat['radius']),
                str(js_feat['arc_start']),
                str(js_feat['arc_end'])
                )
        js_str += "ctx.stroke();\n\n"

        return js_str

def print_pointer_and_text(js_feat):

    text_dict = js_feat['text']
    pointer_dict = js_feat['pointer']
    js_str = "//Pointer and Text: {}\n".format(text_dict['text_str'])
    js_str += "//\tPointer: \n"
    js_str += "ctx.beginPath();\n"
    js_str += "ctx.lineWidth = '{}'".format(str(pointer_dict['line_width']))
    js_str += "ctx.strokeStyle = '{}'\n".format(pointer_dict['line_color'])
    sp = pointer_dict['start_point']]
    js_str += "ctx.moveTo({},{});\n".format(str(sp[0]),str(sp[1]))
    ep = pointer_dict['end_point']
    js_str += "ctx.lineTo({},{});\n".format(str(ep[0]),str(ep[1]))
    js_str += "ctx.stroke();\n"
    js_str += "//\t Text: \n"
    if text_dict['new_text_font_bool']:
        js_str += 'ctx.font = "{}"\n'.format(text_dict['text_font'])
    js_str += 'ctx.fillText("{}",{},{});\n\n'.format(text_dict['text_str'],
            text_dict['text_point'][0], text_dict['text_point'][1])

    return js_str

"""
Inputs:
        "type" : "center_text",
        "plasmid_name": plasmid_name_str,
        "name_start_x":(float) ,
        "name_start_y":(float) ,
        "length_str": plasmid_length_str,
        "length_start_x":(float) ,
        "length_start_y":(float) ,
        "font_style": (str) ,
        "fill_color": (str)
"""
def print_center_text(js_feat):

    js_str = "//Center Text: \n"
    js_str += 'ctx.font = "{}"\n'.format(js_feat['text_font'])
    js_str += 'ctx.fillStyle = "{}"'.format(js_feat['fill_color'])
    js_str += 'ctx.fillText("{}",{},{});\n\n'.format(js_feat['plasmid_name'],
            js_feat['name_start_x'], js_feat['name_start_y'])
    js_str += 'ctx.fillText("{}",{},{});\n\n'.format(js_feat['length_str'],
            js_feat['length_start_x'], js_feat['length_start_y'])

    return js_str


def print_promoter(js_feat):
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

def print_terminator(js_feat):
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

def print_rbs(js_feat):
        circle_center: 2d-coordinates
        radius: float
        start_angle: float
        end_angle: float
        border_color: str
        internal_color: str
        border_width: int

def print_cds(js_feat):
            a: point on plasmid map that outer arrow starts.
            b: point outside plasmid map that outer arrow has its peak.
            c: point on plasmid map, same as end of cds, where arrow ends.
            d: inner complement to a.
            e: inner complement to b.
            f: inner complement to c.
            internal_color:

def print_gap_arc(js_feat):
        line_width:
        line_color:
        start_angle
        end_angle
        angle:
        center_x:
        center_y:
        radius:

