#python


"""
Maintainer: ogaloz@lbl.gov
Takes as an input a genbank file - (representing a plasmid).
Maximum Features (in the plasmid) = 100
To-Do:
    Consider: https://sbolstandard.org/wp-content/uploads/2017/04/SBOL-Visual-2.1.pdf
    Make terminator regions contain (T) symbol.
    Make promoter regions contain right angle arrow.
    


"""

from Bio import SeqIO
import os
import logging
import random
import math
import inspect
import json
#from cello_util.plasmid_sbol_visuals import make_sbol_visuals_js
from plasmid_sbol_visuals import make_sbol_visuals_js
 


"""
Inputs:
    gb_file: (str) filepath to genbank file.
    gb_info: (dict)
        name_tag: (str) location in file where name of feature exists (e.g. locus_tag)
        color_tag: (str) [optional] location in file where color of feature exists if at all (e.g. ApEinfo_fwdcolor)
    js_info: (dict)
        circle_radius: (int) Radius size of circle in javascript (eg 200)
        circle_line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) each internal part is an int [x,y]
        pointer_len_short: (float) Length of pointer (shorter version)
        pointer_len_long: (float) Length of pointer (longer version)
        pointer_thick: (int) thickness of pointer
        text_size: (int) Size of text for names of features
        title_text_size: (int) Size of text in the center
        base_html_filepath: (str) filepath to the base html to substitute into.
        promoter_info, etc. dicts which contain info for the SBOL visuals.
Outputs:
    html_str: (str) The string for the entire HTML file

"""
def make_plasmid_graph(gb_file, gb_info, js_info, base_html_filepath, user_output_name):

    plasmid_info, js_feat_list = get_js_feat_list(gb_file, gb_info)
    js_plasmid_str = make_js_canvas_plasmid(js_feat_list, js_info)
    js_pointers_and_names_str = make_js_pointers_and_names(js_feat_list, js_info)
    plasmid_name_center_canvas_str = make_plasmid_name_in_center(js_info, plasmid_info)
    sbol_visuals_js_str = make_sbol_standard_visuals(js_feat_list,js_info, plasmid_info)
    logging.info(js_plasmid_str)
    logging.info(js_pointers_and_names_str )
    logging.info(plasmid_name_center_canvas_str)
    logging.info(sbol_visuals_js_str)
    #return js_plasmid_str + js_pointers_and_names_str + plasmid_name_center_canvas_str + sbol_visuals_js_str

    """
    html_str = create_html_file(plasmid_name, js_plasmid_str, js_pointers_and_names_str, base_html_filepath, user_output_name)
    
    return html_str
    """


"""
Inputs:
    gb_file: (str) filepath to genbank file.
    gb_info: (dict)
        name_tag: (str) location in file where name of feature exists (e.g. locus_tag)
        color_tag: (str) [optional] location in file where color of feature exists if at all (e.g. ApEinfo_fwdcolor)
Outputs:
    out_list: (list) contains [plasmid_info, js_feat_list]
      plasmid_info: (dict) 
        plasmid_name: (str) The name of the entire plasmid
        plasmid_length: (int) The total bp content of the plasmid.
        num_features: (int) The total number of features on the plasmid.
      js_feat_list: (list) A list of dicts containing important info for the features, js_feat
        js_feat:(dict)
            percentage: (float)
            name: (str)
            color: (str) [optional]
            start_bp: (int) Start in plasmid in terms of base pairs.
            end_bp: (int) End in plasmid in terms of base pairs.
            start_circle: (list) [x,y] for starting point on canvas.
            end_circle: (list) [x,y] for ending point on canvas.
            bp_len: (int) Length in base pairs.
            pointer_direction: (str) 'out' out of plasmid, 'in' inside plasmid.
            midpoint: (list) list of floats. Defaults to [0,0], should be replaced later. Midpoint location on plasmid map.
            typ:(str) from this list: (ribozyme/promoter/rbs/terminator/scar)
"""
def get_js_feat_list(gb_file, gb_info):

    gb_record = SeqIO.read(open(gb_file,"r"), "genbank")
    plasmid_name = gb_record.name
    p_seq = gb_record.seq
    p_len = len(p_seq)
    p_features = gb_record.features
    p_feat_len = len(p_features)
    plasmid_info = {
        'plasmid_name': plasmid_name,
        'plasmid_length': p_len,
        'num_features': p_feat_len
            }
    if p_feat_len > 100:
        raise ValueError("Too many features in genbank file: " + gb_file)
    js_feat_list = []
    for i in range(p_feat_len):
        feat = p_features[i]
        typ = feat.type
        #We assume location is a property of every feature- without this, file cannot work.
        loc = feat.location
        f_start = loc.nofuzzy_start
        f_end = loc.nofuzzy_end
        f_len = f_end - f_start
        js_feat = {"start_bp":f_start, "end_bp":f_end, "bp_len": f_len, "typ": typ}
        f_percentage = f_len/p_len
        js_feat['percentage'] = f_percentage
        if not isinstance(gb_info, dict):
            raise TypeError("gb_info parameter must be a dict type.")
        f_name = feat.qualifiers[gb_info['name_tag']][0]
        js_feat['name'] = f_name
        if 'color_tag' in gb_info:
            f_color = feat.qualifiers[gb_info['color_tag']][0]
            js_feat['color'] = f_color
        js_feat['pointer_direction'] = 'out'
        js_feat['midpoint'] = [0,0]
        js_feat_list.append(js_feat)

    out_list = [plasmid_info, js_feat_list]
    return out_list



"""
Inputs:
    js_info: (dict)
        circle_radius: (int) Radius size of circle in javascript (eg 200)
        circle_line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) each internal part is an int [x,y]
        pointer_len_short: (float) Length of pointer 
        pointer_len_long: (float) Length of pointer
        pointer_thick: (int) thickness of pointer
        text_size: (int) Text size for names of features

    js_feat_list: (list) A list of dicts containing important info for the features, js_feat
        js_feat:(dict)
            percentage: (float)
            name: (str)
            color: (str) [optional]
            start_bp: (int) Start in plasmid in terms of base pairs.
            end_bp: (int) End in plasmid in terms of base pairs.
            start_circle: (list) [x,y] for starting point on canvas.
            end_circle: (list) [x,y] for ending point on canvas.
            bp_len: (int) Length in base pairs.
            typ:(str) from this list: (ribozyme/promoter/rbs/terminator/scar)

    plasmid_info: (dict)
        plasmid_name: (str) The name of the entire plasmid
        plasmid_length: (int) The total bp content of the plasmid.
        num_features: (int) The total number of features on the plasmid.
     
Outputs:
    op_dict: (dict):
        js_str: (string) A string of the entire <script> part of the javascript referring to "myCanvas" canvas element. 
        js_feat_list: (list)
            percentage: (float)
            name: (str)
            color: (str) [optional]
            start_bp: (int) Start in plasmid in terms of base pairs.
            end_bp: (int) End in plasmid in terms of base pairs.
            bp_len: (int) Length in base pairs.
            start_circle: (list) [x,y] for starting point on canvas.
            end_circle: (list) [x,y] for ending point on canvas.
            midpoint: (list) [x,y] midpoint location of feature (floats or ints)
            pointer_direction: (str) default is 'out', could be 'in' if near to out. Incomplete
            typ:(str) from this list: (ribozyme/promoter/rbs/terminator/scar)
            pointer_len: (float) Length of pointer (either short or long)

"""
def make_js_canvas_plasmid(js_feat_list, js_info):
    if 'circle_radius' not in js_info or 'circle_line_width' not in js_info or 'center_coordinates' not in js_info or 'pointer_thick' not in js_info or 'pointer_len_short' not in js_info or 'pointer_len_long' not in js_info:
        logging.debug(js_info.keys())
        raise ValueError("input js_info must contain 'circle_radius', 'circle_line_width', 'center_coordinates', 'pointer_len', 'pointer_thick', 'pointer_len_short', 'pointer_len_long' values.")
    else:
        radius = js_info['circle_radius']
        l_w = js_info['circle_line_width']
        c_c = js_info['center_coordinates']
        pl_short = js_info['pointer_len_short']
        pl_long = js_info['pointer_len_long']

    js_str = '<script>var c = document.getElementById("myCanvas");var ctx = c.getContext("2d");'
    js_str += "ctx.lineWidth = '" + str(l_w) + "';"


    origin_size = 0.002
    start_point = 0
    end_point = start_point + origin_size
    #Making origin (beginning)
    js_add_str = "ctx.beginPath();"
    c_color = 'black'
    js_add_str += "ctx.strokeStyle = '" + c_color + "';"
    js_start = str(start_point) + " * Math.PI - (Math.PI/2)"
    js_end = str(end_point) + " * Math.PI - (Math.PI/2)"
    js_add_str += "ctx.arc(" + str(c_c[0]) + ", " + str(c_c[1]) + ", " + str(radius) + ", " + js_start + ", " + js_end + ");"
    js_add_str += "ctx.stroke();"
    js_str += js_add_str
    start_point = end_point

    #We find the first segment whose end is after our synthetic starting point.
    start_found = False
    s = 0
    while start_found == False and s < len(js_feat_list):
        feat = js_feat_list[s]
        end_spot = feat['percentage'] * 2
        if end_spot > start_point:
            start_found = True
            feat['percentage'] = feat['percentage'] - (origin_size/2)
        else:
            s += 1
        if s == len(js_feat_list):
            raise Exception("Cannot parse plasmid into Javascript.")

    #old_midpoint_list takes the value of the last midpoints
    #First midpoint is at the top of the circle.
    old_midpoint_list = [c_c[0], c_c[1] - radius]
    old_direction = 'out'
    old_color = 'dark'
    for i in range(s, len(js_feat_list)):
        js_add_str = "ctx.beginPath();"
        js_feat = js_feat_list[i]

        #Getting color
        if 'color' in js_feat:
            c_color = js_feat['color']
        else:
            #We give the element a random color. All high values (A-F) means brighter. 0-10 means darker. We differentiate.
            c_color_list = []
            if old_color == 'dark':
                for j in range(6):
                    c_color_list.append(random.choice(['A','B','C','D','E','F']))
                    old_color = 'bright'
            elif old_color == 'bright':
                for j in range(6):
                    c_color_list.append(random.choice([str(k) for k in range(10)]))
                old_color = 'dark'
            c_color = "#" + str(c_color_list[0]) + str(c_color_list[1]) + str(c_color_list[2]) + str(c_color_list[3])
            c_color += str(c_color_list[4]) + str(c_color_list[5])
            js_feat['color'] = c_color
        js_add_str += "ctx.strokeStyle = '" + c_color + "';"

        #Getting representation of the length of segment (not true length). We keep Pi out of the calculations at first.
        arc_len = js_feat['percentage'] * 2
        end_point = start_point + arc_len
        js_start = str(start_point) + " * Math.PI - (Math.PI/2)"
        js_end = str(end_point) + " * Math.PI - (Math.PI/2)"
        #We calculate starting and ending point in terms of location in the canvas for later use:
        start_theta = (math.pi)*(start_point)
        js_feat['start_circle'] = [c_c[0] + math.floor(radius*(math.cos(start_theta - (math.pi/2)))), c_c[1] + math.floor(radius*(math.sin(start_theta - math.pi/2)))] 
        end_theta = (math.pi)*(end_point)
        js_feat['end_circle'] = [c_c[0] + math.floor(radius*(math.cos(end_theta - (math.pi/2)))), c_c[1] + math.floor(radius*(math.sin(end_theta - math.pi/2)))] 
        js_add_str += "ctx.arc(" + str(c_c[0]) + ", " + str(c_c[1]) + ", " + str(radius) + ", " + js_start + ", " + js_end + ");"
        js_add_str += "ctx.stroke();"
        js_str += js_add_str

        #Calculating the location of the middle of the arc. theta = angle between two points.
        theta = (math.pi)*(start_point + ((end_point - start_point)/2.0))
        start_point = end_point
        new_midpoint_list = [c_c[0] + math.floor(radius*(math.cos(theta - (math.pi/2)))), c_c[1] + math.floor(radius*(math.sin(theta - math.pi/2)))]
        js_feat['midpoint'] = new_midpoint_list
        midpoint_distance = math.sqrt( ((new_midpoint_list[0] - old_midpoint_list[0])**2) + ((new_midpoint_list[1] - old_midpoint_list[1])**2))
        if midpoint_distance < 45:
            if old_direction == 'out':
                js_feat['pointer_direction'] = 'in'
                old_direction = 'in'
            else:
                js_feat['pointer_direction'] = 'out'
                old_direction = 'out'
        else:
            js_feat['pointer_direction'] = 'out'
            old_direction = 'out'
        old_midpoint_list = new_midpoint_list


        #Measuring midpoint distance to two before in order to calculate length of pointer to clear up space.
        if i > s+ 1:
            two_prev_mid = js_feat_list[i-2]['midpoint']
            double_midpoint_distance = math.sqrt(((new_midpoint_list[0] - two_prev_mid[0])**2) + ((new_midpoint_list[1] - two_prev_mid[1])**2))
            if double_midpoint_distance < 60:
                logging.debug(js_feat_list[i-2].keys())
                if js_feat_list[i-2]['pointer_len'] == pl_short:
                    js_feat['pointer_len'] = pl_long
                else:
                    js_feat['pointer_len'] = pl_short
            else:
                js_feat['pointer_len'] = pl_short
        elif i == len(js_feat_list) - 1:
            two_prev_mid = js_feat_list[0]['midpoint']
            double_midpoint_distance = math.sqrt(((new_midpoint_list[0] - two_prev_mid[0])**2) + ((new_midpoint_list[1] - two_prev_mid[1])**2))
            if double_midpoint_distance < 60:
                if js_feat_list[i-2]['pointer_len'] == pl_short:
                    js_feat['pointer_len'] = pl_long
                else:
                    js_feat['pointer_len'] = pl_short
            else:
                js_feat['pointer_len'] = pl_short
        else:
            logging.debug(js_feat_list[i-2].keys())
            js_feat['pointer_len'] = pl_short 


    js_str += "</script>\n"

    return js_str

"""
Info:
  We assume the text box making function is: wrapText(context, text, x, y, maxWidth, lineHeight).
    Called with (for example):
        var maxWidth = 400;
        var lineHeight = 25;
        var x = 500
        var y = 400;
        var text = 'Origin';
        ctx.font = '10pt Calibri';
        ctx.fillStyle = '#333';
        wrapText(ctx, text, x, y, maxWidth, lineHeight);

Inputs:
    js_info: (dict)
        circle_radius: (int) Radius size of circle in javascript (eg 200)
        circle_line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) Each internal part is an int [x,y]
        pointer_len_short: (int) Length of pointer 
        pointer_len_long: (int) Length of pointer
        pointer_thick: (int) Thickness of pointer
	text_size: (int) Size of text
    js_feat_list: (list) A list of dicts containing important info for the features, js_feat
        js_feat:(dict)
            percentage: (float)
            name: (str)
            color: (str) [optional]
            start_bp: (int) Start in plasmid in terms of base pairs.
            end_bp: (int) End in plasmid in terms of base pairs.
            start_circle: (list) [x,y] for starting point on canvas.
            end_circle: (list) [x,y] for ending point on canvas.
            bp_len: (int) Length in base pairs.
            midpoint: (list) [x,y] midpoint location of feature
            pointer_direction: (str) 'out' or 'in'.
            pointer_len: (float) Length of pointer
Outputs:
    js_str: (str) <script> tag representing pointers and names aspect.
"""
def make_js_pointers_and_names(js_feat_list, js_info):
   
    if 'pointer_thick' in js_info:
        p_l_w = js_info['pointer_thick']
    else:
        p_l_w = 1
    js_str = '<script>var c = document.getElementById("myCanvas");var ctx = c.getContext("2d");ctx.lineWidth = "{}";ctx.strokeStyle = "black";'.format(str(p_l_w))
    if "text_size" in js_info:
        text_size = str(js_info['text_size'])
    else:
        text_size = '10'
    js_str += "ctx.font = '" + text_size + "pt Calibri';ctx.fillStyle = '#333';var maxWidth= 50; var lineHeight= 25;"
    
    #Setting useful variables for later:
    cc = js_info['center_coordinates']
    radius = js_info['circle_radius']


    # Making the origin pointer:
    #We define the origin_midpoint as the beginning of the plasmid, not the true midpoint of the origin segment.
    add_js_str = ''
    origin_midpoint = [cc[0], cc[1] - radius]
    pointer_root = [origin_midpoint[0], origin_midpoint[1] - js_info['pointer_len_short']]
    add_js_str += 'ctx.beginPath();'
    add_js_str += 'ctx.moveTo(' + str(pointer_root[0]) + ',' + str(pointer_root[1]) + ');'
    add_js_str += 'ctx.lineTo(' + str(origin_midpoint[0]) + ',' + str(origin_midpoint[1] - 6) + ');'
    add_js_str +=  'ctx.stroke();'
 
    #We add the text box with the name
    add_js_str += 'var text = "' + '0' + '";'
    add_js_str += 'wrapText(ctx, text, ' + str(pointer_root[0] - 5) + ', ' + str(pointer_root[1] - 5) + ', maxWidth, lineHeight);'
    js_str += add_js_str

    #Now we repeat the process for each feature in the plasmid
    for i in range(len(js_feat_list)):
        add_js_str = ''
        c_feat = js_feat_list[i]
        feat_midpoint = c_feat['midpoint']
        pointer_len = c_feat['pointer_len']
        #text_shift is the amount we shift the text. It is based on the text_size. factor is (6/15) * text size. (e.g. text size 15 means shift is 6).
        text_shift = js_info['text_size'] * (6.0/15.0)
        run = float(feat_midpoint[0]) - float(cc[0])
        if run == 0:
            run = 0.00001
        slope = (float(feat_midpoint[1]) - float(cc[1]))/(run)
        d_x = (pointer_len/(math.sqrt(1+slope**2)))
        if  (float(feat_midpoint[0]) - float(cc[0])) >= 0:
            if c_feat['pointer_direction'] == 'out':
                pointer_root = [feat_midpoint[0] + d_x, feat_midpoint[1] + slope*(d_x)]
                pointer_tip = [feat_midpoint[0] + (d_x/8.0), feat_midpoint[1] + slope*(d_x/8.0)]
                text_x = pointer_root[0] + 5
                text_y = pointer_root[1] 
            else:
                pointer_root = [feat_midpoint[0] - d_x, feat_midpoint[1] - slope*(d_x)]
                pointer_tip = [feat_midpoint[0] - (d_x/8.0), feat_midpoint[1] - slope*(d_x/8.0)]
                text_x = pointer_root[0] - text_shift * len(c_feat['name']) - 10
                text_y = pointer_root[1]
        else:
            if c_feat['pointer_direction'] == 'out':
                pointer_root = [feat_midpoint[0] - d_x, feat_midpoint[1] - slope*(d_x)]
                pointer_tip = [feat_midpoint[0] - (d_x/8.0), feat_midpoint[1] - slope*(d_x/8.0)]
                text_x = pointer_root[0] - text_shift * len(c_feat['name']) - 10
                text_y = pointer_root[1]
            else:
                pointer_root = [feat_midpoint[0] + d_x, feat_midpoint[1] + slope*(d_x)]
                pointer_tip = [feat_midpoint[0] + (d_x/8.0), feat_midpoint[1] + slope*(d_x/8.0)]
                text_x = pointer_root[0] + 5
                text_y = pointer_root[1]

        add_js_str += 'ctx.beginPath();'
        add_js_str += 'ctx.moveTo(' + str(pointer_root[0]) + ',' + str(pointer_root[1]) + ');'
        add_js_str += 'ctx.lineTo(' + str(pointer_tip[0]) + ',' + str(pointer_tip[1]) + ');'
        add_js_str +=  'ctx.stroke();'

        #making text box
        # if feature name is too long we cut it short.
        c_name = c_feat['name']
        if len(c_name) > 10:
            c_name = c_name[:9] + "..."
        add_js_str += 'var text = "' + c_name + '";'
        add_js_str += 'wrapText(ctx, text, ' + str(text_x) + ', ' + str(text_y) + ', maxWidth, lineHeight);'
        js_str += add_js_str

    js_str += '</script>\n'

    return js_str


"""
TD: Estimate length of each letter in pixels, then place word so center of word is in the center of the circle.
Inputs:
    js_info: (dict)
        circle_radius: (int) Radius size of circle in javascript (eg 200)
        circle_line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) Each internal part is an int [x,y]
        pointer_len_short: (float) Length of pointer
        pointer_len_long: (float) Length of pointer
        pointer_thick: (int) Thickness of pointer
	text_size: (int) Size of text
    plasmid_info: (dict)
        plasmid_name: (str) The name of the entire plasmid
        plasmid_length: (int) The total bp content of the plasmid.
        num_features: (int) The total number of features on the plasmid.
Output:
    js_str: (str) A string with the script tag with the code for placing the plasmid name and length in the center.
"""
def make_plasmid_name_in_center(js_info, plasmid_info):

    js_str = '<script>var c = document.getElementById("myCanvas");var ctx = c.getContext("2d");ctx.lineWidth = "2";ctx.strokeStyle = "black";'
    if "title_text_size" in js_info:
        text_size = str(js_info['title_text_size'])
    else:
        text_size = '20'
    js_str += "ctx.font = 'bold " + text_size + "pt Calibri';ctx.fillStyle = '#333';var maxWidth= 50; var lineHeight= 25;"
    
    #Setting useful variables for later:
    cc = js_info['center_coordinates']

    #Getting plasmid name and checking it
    plasmid_name = plasmid_info['plasmid_name']
    if len(plasmid_name) > 35:
        logging.critical("Plasmid name is too long - using placeholder name: 'Plasmid'")
        plasmid_name = "Plasmid"

    #We add the text box with the name, calculating center of word to be center of circle,
    # and each letter has length 12 pixels
    plasmid_name_length = len(plasmid_name)*15
    plasmid_name_start = cc[0] - float(plasmid_name_length)/2
    js_str += 'var text = "' + plasmid_name + '";'
    js_str += 'wrapText(ctx, text, ' + str(plasmid_name_start) + ', ' + str(cc[1] - 15) + ', maxWidth, lineHeight);'

    #Getting length of plasmid and placing it under plasmid name
    plasmid_length = str(plasmid_info['plasmid_length']) + " bp"
    if len(plasmid_length) > 13:
        logging.critical("Plasmid length is over ten, probably a mistake.")
        plasmid_length = '? bp'

    #We add the text box with the length, 20 to the left of center, and 20 below
    plasmid_len_len = len(plasmid_length)*15
    plasmid_len_start = cc[0] - float(plasmid_len_len)/2
    js_str += 'var text = "' + plasmid_length + '";'
    js_str += 'wrapText(ctx, text, ' + str(plasmid_len_start) + ', ' + str(cc[1] + 15) + ', maxWidth, lineHeight);'


    js_str += '</script>\n'

    return js_str


"""
Inputs:
    js_info: (dict)
        circle_radius: (int) Radius size of circle in javascript (eg 200)
        circle_line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) Each internal part is an int [x,y]
        pointer_len_short: (float) Length of pointer
        pointer_len_long: (float) Length of pointer
        pointer_thick: (int) Thickness of pointer
	text_size: (int) Size of text
    plasmid_info: (dict)
        plasmid_name: (str) The name of the entire plasmid
        plasmid_length: (int) The total bp content of the plasmid.
        num_features: (int) The total number of features on the plasmid.
    js_feat_list: (list) A list of dicts containing important info for the features, js_feat
        js_feat:(dict)
            percentage: (float)
            name: (str)
            color: (str)
            start_bp: (int) Start in plasmid in terms of base pairs.
            end_bp: (int) End in plasmid in terms of base pairs.
            start_circle: (list) [x,y] for starting point on canvas.
            end_circle: (list) [x,y] for ending point on canvas.
            bp_len: (int) Length in base pairs.
            midpoint: (list) [x,y] midpoint location of feature
            pointer_direction: (str) 'out' or 'in'.
            typ: The type of entity
"""
def make_sbol_standard_visuals(js_feat_list,js_info, plasmid_info):

    #As a test, we create a black circle for every start point, and a gray line for every end point
    visuals_str = '<script>\nvar c = document.getElementById("myCanvas");var ctx = c.getContext("2d");\n'

    for js_feat in js_feat_list:
        visuals_str += make_sbol_visuals_js(js_feat, js_info)


    '''
    start_end_str = visuals_str.copy()
    for js_feat in js_feat_list:
        start_js = 'ctx.beginPath();'
        start_js += 'ctx.arc('+str(js_feat['start_circle'][0])+',' + str(js_feat['start_circle'][1])+',4,0,2*Math.PI);'
        start_js += 'ctx.stroke();'
        end_js = 'ctx.beginPath();'
        end_js += 'ctx.arc('+str(js_feat['end_circle'][0])+',' + str(js_feat['end_circle'][1])+',4,0,2*Math.PI);'
        end_js += 'ctx.stroke();'
        start_end_str += start_js + end_js
    start_end_str += '</script>'

    return start_end_str
    '''

    visuals_str += '</script>\n'



    return visuals_str

"""


"""
def create_html_file(plasmid_name, js_plasmid_str, js_pointers_and_names_str, base_html_filepath, user_output_name):
    f = open(base_html_filepath, "r")
    file_str = f.read()
    f.close()

    if "job_" == plasmid_name[:4]:
        plasmid_title = user_output_name + " " + " ".join(plasmid_name.split("_")[3:])
    else:
        plasmid_title = user_output_name + " " + plasmid_name
    file_str = file_str.replace('Plasmid_Name_Here',plasmid_title)
    file_str = file_str.replace('{--Insert Code--}' , js_plasmid_str + '\n' + js_pointers_and_names_str )

    return file_str


def convert_canvas_to_img_js():
    """
    // Converts canvas to an image
    function convertCanvasToImage(canvas) {
	var image = new Image();
	image.src = canvas.toDataURL("image/png");
	return image;
        }

    """
    return None









def main():
    test()

    return 0

def test():
    logging.basicConfig(level=logging.DEBUG)
    gb_file = "/Users/omreeg/KBase/apps/cello/data/test_2_circuit.gbk"
    base_html_filepath = "/Users/omreeg/KBase/apps/cello/lib/cello_util/plasmid_html_base.html"
    config_filepath = os.path.join(os.getcwd(),'plasmid_map_config.js')
    f = open(config_filepath, "r")
    file_str = f.read()
    f.close()
    config_dict = json.loads(file_str)
    
    gb_info = config_dict['genbank_info']
    js_info = config_dict["design_info"]
    user_output_name = "New_Test"
    final_html_str = make_plasmid_graph(gb_file, gb_info, js_info, base_html_filepath, user_output_name)
    logging.debug(final_html_str)

    return 0

main()




