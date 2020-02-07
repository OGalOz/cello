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

    js_str = "//Plasmid Arc Forward: {}\n".format(js_feat['feat_name'][0])
    js_str += "ctx.beginPath();\n"
    js_str += "ctx.lineWidth = '{}';".format(str(js_feat['line_width']))
    js_str += "ctx.strokeStyle = '{}';\n".format(js_feat['internal_color'])
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
    
    js_str = "//Plasmid Arc Reverse: {}\n".format(js_feat['feat_name'][0])
    js_str += "ctx.beginPath();\n"
    js_str += "ctx.lineWidth = '{}';".format(str(js_feat['line_width']))
    js_str += "ctx.strokeStyle = '{}';\n".format(js_feat['internal_color'])
    js_str += "ctx.arc({},{},{},{},{});\n".format(
            str(js_feat['center_x']),
            str(js_feat['center_y']),
            str(js_feat['radius']),
            str(js_feat['arc_start']),
            str(js_feat['arc_end'])
            )
    js_str += "ctx.stroke();\n\n"

    return js_str


def print_gap_arc(js_feat):
    js_str = "//Plasmid Gap Arc: {}\n".format(js_feat['feat_name'][0])
    js_str += "ctx.beginPath();\n"
    js_str += "ctx.lineWidth = '{}';".format(str(js_feat['line_width']))
    js_str += "ctx.strokeStyle = '{}';\n".format(js_feat['line_color'])
    js_str += "ctx.arc({},{},{},{},{});\n".format(
            str(js_feat['center_x']),
            str(js_feat['center_y']),
            str(js_feat['radius']),
            str(js_feat['start_angle']),
            str(js_feat['end_angle'])
            )
    js_str += "ctx.stroke();\n\n"

    return js_str

def print_pointer_and_text(js_feat):

    text_dict = js_feat['text']
    pointer_dict = js_feat['pointer']
    js_str = "//Pointer and Text: {}\n".format(text_dict['text_str'])
    js_str += "//\tPointer: \n"
    js_str += "ctx.beginPath();\n"
    js_str += "ctx.lineWidth = '{}';".format(str(pointer_dict['line_width']))
    js_str += "ctx.strokeStyle = '{}';\n".format(pointer_dict['line_color'])

    sp = pointer_dict['start_point']

    js_str += "ctx.moveTo({},{});\n".format(str(sp[0]),str(sp[1]))

    ep = pointer_dict['end_point']

    js_str += "ctx.lineTo({},{});\n".format(str(ep[0]),str(ep[1]))
    js_str += "ctx.stroke();\n"
    js_str += "//\t Text: \n"
    if text_dict['new_text_font_bool']:
        js_str += 'ctx.font = "{}";\n'.format(text_dict['text_font'])
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
    js_str += 'ctx.font = "{}";\n'.format(js_feat['font_style'])
    js_str += 'ctx.fillStyle = "{}";'.format(js_feat['fill_color'])
    js_str += 'ctx.fillText("{}",{},{});\n'.format(js_feat['plasmid_name'],
            js_feat['name_start_x'], js_feat['name_start_y'])
    js_str += 'ctx.fillText("{}",{},{});\n\n'.format(js_feat['length_str'],
            js_feat['length_start_x'], js_feat['length_start_y'])

    return js_str


def print_promoter(js_feat):
    js_str = "//Promoter Symbol: {} \n".format(js_feat['feat_name'][0])
    js_str += "ctx.strokeStyle = '{}';\n".format(js_feat["color"])
    js_str += "ctx.lineWidth = {};\n".format(str(js_feat['line_width']))
    js_str += "ctx.beginPath();\n"
    sl = js_feat['p_line_coordinate_start']
    js_str += "ctx.moveTo({},{});\n".format(str(sl[0]),str(sl[1]))
    ab = js_feat['arc_begin_point']
    js_str += "ctx.lineTo({},{});\n".format(str(ab[0]),str(ab[1]))
    js_str += "ctx.stroke();\n"
    js_str += "ctx.beginPath();\n"
    js_str += "ctx.arc({},{},{},{},{});\n".format(
            str(js_feat['center_x']),
            str(js_feat['center_y']),
            str(js_feat['big_radius']),
            str(js_feat['arc_start_angle']),
            str(js_feat['arc_end_angle'])
            )
    js_str += "ctx.stroke();\n"
    #Now for the arrow:
    js_str += "ctx.beginPath();\n"
    fe = js_feat['flags_end']
    ifs = js_feat['inner_flag_start']
    ofs = js_feat['outer_flag_start']
    js_str += "ctx.moveTo({},{});\n".format(str(fe[0]),str(fe[1]))
    js_str += "ctx.lineTo({},{});\n".format(str(ifs[0]),str(ifs[1]))
    js_str += "ctx.stroke();\n"
    js_str += "ctx.moveTo({},{});\n".format(str(fe[0]),str(fe[1]))
    js_str += "ctx.lineTo({},{});\n".format(str(ofs[0]),str(ofs[1]))
    js_str += "ctx.stroke();\n\n"

    return js_str



def print_terminator(js_feat):

    #Setting variables:
    base_1 = js_feat['base_1']
    base_2 = js_feat['base_2']
    armpit_1 = js_feat['armpit_1']
    armpit_2 = js_feat['armpit_2']
    palm_hand_1 = js_feat['palm_hand_1']
    palm_hand_2 = js_feat['palm_hand_2']
    back_hand_1 = js_feat['back_hand_1']
    back_hand_2 = js_feat['back_hand_2']


    #Borders:
    js_str = "//Terminator Symbol: {} \n".format(js_feat['feat_name'][0])
    js_str += "//  Borders:\n"
    js_str += 'ctx.strokeStyle = "{}";\n'.format(js_feat['border_color'])
    js_str += "ctx.lineWidth = {};\n".format(str(js_feat['border_width']))

    j_str = "ctx.moveTo({},{});\n".format( str(base_1[0]), str(base_1[1]))
    j_str += "ctx.lineTo({},{});\n".format( str(armpit_1[0]), str(armpit_1[1]))
    j_str += "ctx.lineTo({},{});\n".format( str(palm_hand_1[0]), str(palm_hand_1[1]))
    j_str += "ctx.lineTo({},{});\n".format( str(back_hand_1[0]), str(back_hand_1[1]))
    j_str += "ctx.lineTo({},{});\n".format( str(back_hand_2[0]), str(back_hand_2[1]))
    j_str += "ctx.lineTo({},{});\n".format( str(palm_hand_2[0]), str(palm_hand_2[1]))
    j_str += "ctx.lineTo({},{});\n".format( str(armpit_2[0]), str(armpit_2[1]))
    j_str += "ctx.lineTo({},{});\n".format( str(base_2[0]), str(base_2[1]))
    j_str += "ctx.stroke();\n"
    js_str += j_str

    #Fill
    js_str += "// Fill:\n"
    js_str += "ctx.beginPath();\n"
    js_str += j_str

    js_str += 'ctx.fillStyle = "{}";\n'.format(js_feat['internal_color'])
    js_str += "ctx.closePath();\n"
    js_str += "ctx.fill();\n\n"

    return js_str


def print_rbs(js_feat):

    js_str = "//RBS Symbol: {} \n".format(js_feat['feat_name'][0])
    js_str += "ctx.beginPath();\n"
    #The true at the end means clockwise.
    js_str += "ctx.arc({},{},{},{},{}, true);\n".format(
            str(js_feat['circle_center'][0]),
            str(js_feat['circle_center'][1]),
            str(js_feat['radius']),
            str(js_feat['start_angle']),
            str(js_feat['end_angle'])
        )
    js_str += "ctx.lineWidth = {};\n".format(str(js_feat['border_width']))
    js_str += "ctx.fillStyle = '{}';\n".format(js_feat["internal_color"])
    js_str += "ctx.fill();\n"
    js_str += "ctx.strokeStyle = '{}';\n".format(js_feat["border_color"])
    js_str += "ctx.stroke(); \n\n"
    return js_str
 


def print_cds(js_feat):
    js_str = "//CDS Symbol: {} \n".format(js_feat['feat_name'][0])

    #First Triangle:
    js_str += "ctx.beginPath();\n"
    js_str += "ctx.beginPath(); "
    js_str += "ctx.moveTo({},{}); ".format(str(js_feat['a'][0]),str(js_feat['a'][1]))
    js_str += "ctx.lineTo({},{}); ".format(str(js_feat['b'][0]), str(js_feat['b'][1]))
    js_str += "ctx.lineTo({},{}); ".format(str(js_feat['c'][0]), str(js_feat['c'][1]))
    js_str += "ctx.closePath(); ctx.fillStyle = '{}';".format(js_feat['internal_color']) + \
        "ctx.fill();\n"
    #Second Triangle
    js_str += "ctx.beginPath(); "
    js_str += "ctx.moveTo({},{}); ".format(str(js_feat['d'][0]),str(js_feat['d'][1]))
    js_str += "ctx.lineTo({},{}); ".format(str(js_feat['e'][0]), str(js_feat['e'][1]))
    js_str += "ctx.lineTo({},{}); ".format(str(js_feat['f'][0]), str(js_feat['f'][1]))
    js_str += "ctx.closePath(); ctx.fillStyle = '{}';".format(js_feat['internal_color']) \
            + "ctx.fill(); ctx.beginPath(); \n\n"

    return js_str
    
