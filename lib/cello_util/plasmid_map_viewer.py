#python


"""
Maintainer: ogaloz@lbl.gov
Takes as an input a genbank file - (representing a plasmid).
Maximum Features (in the plasmid) = 100
"""

from Bio import SeqIO
import os
import logging
import random
import math
import inspect



"""
Inputs:
    gb_file: (str) filepath to genbank file.
    gb_info: (dict)
        name_tag: (str) location in file where name of feature exists (e.g. locus_tag)
        color_tag: (str) [optional] location in file where color of feature exists if at all (e.g. ApEinfo_fwdcolor)
    js_info: (dict)
        circle_size: (int) Radius size of circle in javascript (eg 200)
        line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) each internal part is an int [x,y]
        arrow_len: (int) Length of arrow
        arrow_thick: (int) thickness of arrow
        text_size: (int) Size of text for names of features
    base_html_filepath: (str) filepath to the base html to substitute into.
Outputs:
    html_str: (str) The string for the entire HTML file

"""
def make_plasmid_graph(gb_file, gb_info, js_info, base_html_filepath, user_output_name):

    plasmid_name, js_feat_list = get_js_feat_list(gb_file, gb_info)
    js_plasmid_str = make_js_canvas_plasmid(js_feat_list, js_info)
    js_arrows_and_names_str = make_js_arrows_and_names(js_feat_list, js_info)
    html_str = create_html_file(plasmid_name, js_plasmid_str, js_arrows_and_names_str, base_html_filepath, user_output_name)
    
    return html_str



"""
Inputs:
    gb_file: (str) filepath to genbank file.
    gb_info: (dict)
        name_tag: (str) location in file where name of feature exists (e.g. locus_tag)
        color_tag: (str) [optional] location in file where color of feature exists if at all (e.g. ApEinfo_fwdcolor)
Outputs:
    out_list: (list) contains [plasmid_name, js_feat_list]
      plasmid_name: (str) The name of the entire plasmid
      js_feat_list: (list) A list of dicts containing important info for the features, js_feat
        js_feat:(dict)
            percentage: (float)
            name: (str)
            color: (str) [optional]
            start_bp: (int) Start in plasmid in terms of base pairs.
            end_bp: (int) End in plasmid in terms of base pairs.
            bp_len: (int) Length in base pairs.
            arrow_direction: (str) 'out' out of plasmid, 'in' inside plasmid.
            midpoint: (list) list of floats. Defaults to [0,0], should be replaced later. Midpoint location on plasmid map.
"""
def get_js_feat_list(gb_file, gb_info):

    gb_record = SeqIO.read(open(gb_file,"r"), "genbank")
    plasmid_name = gb_record.name
    p_seq = gb_record.seq
    p_len = len(p_seq)
    p_features = gb_record.features
    p_feat_len = len(p_features)
    if p_feat_len > 100:
        raise ValueError("Too many features in genbank file: " + gb_file)
    js_feat_list = []
    for i in range(p_feat_len):
        feat = p_features[i]
        #We assume location is a property of every feature- without this, file cannot work.
        loc = feat.location
        f_start = loc.nofuzzy_start
        f_end = loc.nofuzzy_end
        f_len = f_end - f_start
        js_feat = {"start_bp":f_start, "end_bp":f_end, "bp_len": f_len}
        f_percentage = f_len/p_len
        js_feat['percentage'] = f_percentage
        if not isinstance(gb_info, dict):
            raise TypeError("gb_info parameter must be a dict type.")
        f_name = feat.qualifiers[gb_info['name_tag']][0]
        js_feat['name'] = f_name
        if 'color_tag' in gb_info:
            f_color = feat.qualifiers[gb_info['color_tag']][0]
            js_feat['color'] = f_color
        js_feat['arrow_direction'] = 'out'
        js_feat['midpoint'] = [0,0]
        js_feat_list.append(js_feat)

    out_list = [plasmid_name, js_feat_list]
    return out_list



"""
Inputs:
    js_info: (dict)
        circle_size: (int) Radius size of circle in javascript (eg 200)
        line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) each internal part is an int [x,y]
        arrow_len: (int) Length of arrow
        arrow_thick: (int) thickness of arrow
        text_size: (int) Text size for names of features

    js_feat_list: (list) A list of dicts containing important info for the features, js_feat
        js_feat:(dict)
            percentage: (float)
            name: (str)
            color: (str) [optional]
            start_bp: (int) Start in plasmid in terms of base pairs.
            end_bp: (int) End in plasmid in terms of base pairs.
            bp_len: (int) Length in base pairs.
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
            midpoint: (list) [x,y] midpoint location of feature (floats or ints)
            arrow_direction: (str) default is 'out', could be 'in' if near to out. Incomplete

"""
def make_js_canvas_plasmid(js_feat_list, js_info):
    if 'circle_size' not in js_info or 'line_width' not in js_info or 'center_coordinates' not in js_info or 'arrow_len' not in js_info or 'arrow_thick' not in js_info:
        raise ValueError("input js_info must contain 'circle_size', 'line_width', 'center_coordinates', 'arrow_len', 'arrow_thick' values.")
    else:
        radius = js_info['circle_size']
        l_w = js_info['line_width']
        c_c = js_info['center_coordinates']

    js_str = '<script>var c = document.getElementById("myCanvas");var ctx = c.getContext("2d");'
    js_str += "ctx.lineWidth = '" + str(l_w) + "';"

    origin_size = 0.002
    start_point = 0
    end_point = start_point + origin_size
    #Making origin (beginning)
    js_add_str = "ctx.beginPath();"
    c_color = 'black'
    js_add_str += "ctx.strokeStyle = '" + c_color + "';"
    js_start = str(start_point) + " * Math.PI"
    js_end = str(end_point) + " * Math.PI"
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
    old_midpoint_list = [c_c[0] + radius, c_c[1]]
    old_direction = 'out'
    old_color = 'dark'
    for i in range(s, len(js_feat_list)):
        js_add_str = "ctx.beginPath();"
        c_feat = js_feat_list[i]

        #Getting color
        if 'color' in c_feat:
            c_color = c_feat['color']
        else:
            #We give the element a random color. All high values (A-F) means brighter. 0-10 means darker. We differentiate.
            c_color_list = []
            if old_color == 'dark':
                for i in range(6):
                    c_color_list.append(random.choice(['A','B','C','D','E','F']))
                    old_color = 'bright'
            elif old_color == 'bright':
                for i in range(6):
                    c_color_list.append(random.choice([str(k) for k in range(10)]))
                old_color = 'dark'
            c_color = "#" + str(c_color_list[0]) + str(c_color_list[1]) + str(c_color_list[2]) + str(c_color_list[3])
            c_color += str(c_color_list[4]) + str(c_color_list[5])
        js_add_str += "ctx.strokeStyle = '" + c_color + "';"

        #Getting representation of the length of segment (not true length). We keep Pi out of the calculations for now.
        arc_len = c_feat['percentage'] * 2
        end_point = start_point + arc_len
        js_start = str(start_point) + " * Math.PI"
        js_end = str(end_point) + " * Math.PI"
        js_add_str += "ctx.arc(" + str(c_c[0]) + ", " + str(c_c[1]) + ", " + str(radius) + ", " + js_start + ", " + js_end + ");"
        js_add_str += "ctx.stroke();"
        js_str += js_add_str

        #Calculating the location of the middle of the arc. theta = angle between two points.
        theta = (math.pi)*(start_point + ((end_point - start_point)/2.0))
        start_point = end_point
        new_midpoint_list = [c_c[0] + math.floor(radius*(math.cos(theta))), c_c[1] + math.floor(radius*(math.sin(theta)))]
        c_feat['midpoint'] = new_midpoint_list
        midpoint_distance = math.sqrt( ((new_midpoint_list[0] - old_midpoint_list[0])**2) + ((new_midpoint_list[1] - old_midpoint_list[1])**2))
        if midpoint_distance < 45:
            if old_direction == 'out':
                c_feat['arrow_direction'] = 'in'
                old_direction = 'in'
            else:
                c_feat['arrow_direction'] = 'out'
                old_direction = 'out'
        else:
            c_feat['arrow_direction'] = 'out'
            old_direction = 'out'
        old_midpoint_list = new_midpoint_list

    js_str += "</script>"

    return js_str

"""
Info:
  We assume the arrow making function is: canvas_arrow(context, fromx, fromy, tox, toy).
    Called with (for example): 
        ctx.beginPath();
        canvas_arrow(ctx, fromx, fromy, tox, toy);
        ctx.stroke();
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
        circle_size: (int) Radius size of circle in javascript (eg 200)
        line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) Each internal part is an int [x,y]
        arrow_len: (int) Length of arrow
        arrow_thick: (int) Thickness of arrow
	text_size: (int) Size of text
    js_feat_list: (list) A list of dicts containing important info for the features, js_feat
        js_feat:(dict)
            percentage: (float)
            name: (str)
            color: (str) [optional]
            start_bp: (int) Start in plasmid in terms of base pairs.
            end_bp: (int) End in plasmid in terms of base pairs.
            bp_len: (int) Length in base pairs.
            midpoint: (list) [x,y] midpoint location of feature
            arrow_direction: (str) 'out' or 'in'.
"""
def make_js_arrows_and_names(js_feat_list, js_info):
    
    js_str = '<script>var c = document.getElementById("myCanvas");var ctx = c.getContext("2d");ctx.lineWidth = "2";ctx.strokeStyle = "black";'
    if "text_size" in js_info:
        text_size = str(js_info['text_size'])
    else:
        text_size = '10'
    js_str += "ctx.font = '" + text_size + "pt Calibri';ctx.fillStyle = '#333';var maxWidth= 50; var lineHeight= 25;"
    
    #Setting useful variables for later:
    cc = js_info['center_coordinates']
    arrow_len = js_info['arrow_len']


    # Making the origin arrow:
    #We define the origin_midpoint as the beginning of the plasmid, not the true midpoint of the origin segment.
    add_js_str = ''
    origin_midpoint = [cc[0] + js_info['circle_size'] , cc[1]]
    slope = (origin_midpoint[1] - cc[1])/(origin_midpoint[0] - cc[0])
    d_x = (arrow_len/(math.sqrt(1+slope**2)))
    arrow_root = [origin_midpoint[0] + d_x, origin_midpoint[1] + slope*(d_x)]
    add_js_str += 'ctx.beginPath(); canvas_arrow(ctx, ' + str(arrow_root[0]) + ', ' + str(arrow_root[1]) + ', ' + str(origin_midpoint[0] + 6) + ', '
    add_js_str += str(origin_midpoint[1]) + ');ctx.stroke();'
    #We add the text box with the name
    add_js_str += 'var text = "' + 'start' + '";'
    add_js_str += 'wrapText(ctx, text, ' + str(arrow_root[0] + 5) + ', ' + str(arrow_root[1]) + ', maxWidth, lineHeight);'
    js_str += add_js_str

    #Now we repeat the process for each feature in the plasmid
    for i in range(len(js_feat_list)):
        add_js_str = ''
        c_feat = js_feat_list[i]
        feat_midpoint = c_feat['midpoint']
        slope = (float(feat_midpoint[1]) - float(cc[1]))/(float(feat_midpoint[0]) - float(cc[0]))
        d_x = (arrow_len/(math.sqrt(1+slope**2)))
        if  (float(feat_midpoint[0]) - float(cc[0])) >= 0:
            if c_feat['arrow_direction'] == 'out':
                arrow_root = [feat_midpoint[0] + d_x, feat_midpoint[1] + slope*(d_x)]
                arrow_tip = [feat_midpoint[0] + (d_x/8.0), feat_midpoint[1] + slope*(d_x/8.0)]
                text_x = arrow_root[0] + 5
                text_y = arrow_root[1] + 5 
            else:
                arrow_root = [feat_midpoint[0] - d_x, feat_midpoint[1] - slope*(d_x)]
                arrow_tip = [feat_midpoint[0] - (d_x/8.0), feat_midpoint[1] - slope*(d_x/8.0)]
                text_x = arrow_root[0] - 6 * len(c_feat['name']) - 10
                text_y = arrow_root[1] - 5
        else:
            if c_feat['arrow_direction'] == 'out':
                arrow_root = [feat_midpoint[0] - d_x, feat_midpoint[1] - slope*(d_x)]
                arrow_tip = [feat_midpoint[0] - (d_x/8.0), feat_midpoint[1] - slope*(d_x/8.0)]
                text_x = arrow_root[0] - 6 * len(c_feat['name']) - 10
                text_y = arrow_root[1] - 5
            else:
                arrow_root = [feat_midpoint[0] + d_x, feat_midpoint[1] + slope*(d_x)]
                arrow_tip = [feat_midpoint[0] + (d_x/8.0), feat_midpoint[1] + slope*(d_x/8.0)]
                text_x = arrow_root[0] + 5
                text_y = arrow_root[1] + 5

        add_js_str += 'ctx.beginPath(); canvas_arrow(ctx, ' + str(arrow_root[0]) + ', ' + str(arrow_root[1]) + ', ' + str(arrow_tip[0]) + ', '
        add_js_str += str(arrow_tip[1]) + ');ctx.stroke();'
        #making text box
        add_js_str += 'var text = "' + c_feat['name'] + '";'
        add_js_str += 'wrapText(ctx, text, ' + str(text_x) + ', ' + str(text_y) + ', maxWidth, lineHeight);'
        js_str += add_js_str

    js_str += '</script>'

    return js_str



"""


"""
def create_html_file(plasmid_name, js_plasmid_str, js_arrows_and_names_str, base_html_filepath, user_output_name):
    f = open(base_html_filepath, "r")
    file_str = f.read()
    f.close()

    if "job_" == plasmid_name[:4]:
        plasmid_title = user_output_name + " " + " ".join(plasmid_name.split("_")[3:])
    else:
        plasmid_title = user_output_name + " " + plasmid_name
    file_str = file_str.replace('Plasmid_Name_Here',plasmid_title)
    file_str = file_str.replace('{--Insert Code--}' , js_plasmid_str + '\n' + js_arrows_and_names_str )

    return file_str












def main():
    #test()

    return 0

def test():
    logging.basicConfig(level=logging.DEBUG)
    gb_file = ""
    base_html_filepath = ""
    gb_info = {'name_tag': 'locus_tag'}
    js_info = {'circle_size': 200, 
            'line_width': 5, 
            'center_coordinates':[400,400],
            'arrow_len':70 ,
            'arrow_thick':2,
            'text_size' : 15}
    final_html_str = make_plasmid_graph(gb_file, gb_info, js_info, base_html_filepath)
    logging.debug(final_html_str)

    return 0

#main()




