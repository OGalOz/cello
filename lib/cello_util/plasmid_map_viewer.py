#python


"""
Omree Gal-Oz 2019
Takes as an input a plasmid file of sorts - (genbank file).
First measurement to consider is length of plasmid (How many bp?)
Then divide it by sections.
You need to create a maximum sections number (200?)

"""

from Bio import SeqIO
import os
import logging
import random
import math

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

"""
def make_plasmid_graph(gb_file, gb_info, js_info):

    js_feat_list = get_js_feat_list(gb_file, gb_info)
    js_plasmid_str = make_js_canvas_plasmid(js_feat_list, js_info)
    logging.debug(js_plasmid_str)
    js_arrows_and_names_str = make_js_arrows_and_names(js_feat_list, js_info)
    logging.debug(js_arrows_and_names_str)
    
    

    return None



"""
Inputs:
    gb_file: (str) filepath to genbank file.
    gb_info: (dict)
        name_tag: (str) location in file where name of feature exists (e.g. locus_tag)
        color_tag: (str) [optional] location in file where color of feature exists if at all (e.g. ApEinfo_fwdcolor)
Outputs:
    js_feat_list: (list) A list of dicts containing important info for the features, js_feat
        js_feat:(dict)
            percentage: (float)
            name: (str)
            color: (str) [optional]
            start_bp: (int) Start in plasmid in terms of base pairs.
            end_bp: (int) End in plasmid in terms of base pairs.
            bp_len: (int) Length in base pairs.
"""
def get_js_feat_list(gb_file, gb_info):

    gb_record = SeqIO.read(open(gb_file,"r"), "genbank")
    p_seq = gb_record.seq
    p_len = len(p_seq)
    p_features = gb_record.features
    p_feat_len = len(p_features)
    if p_feat_len > 200:
        raise Exception("Too many features to create plasmid map in Javascript - must be less than 200.")
    js_feat_list = []
    for i in range(p_feat_len):
        feat = p_features[i]
        loc = feat.location
        f_start = loc.nofuzzy_start
        f_end = loc.nofuzzy_end
        f_len = f_end - f_start
        js_feat = {"start_bp":f_start, "end_bp":f_end, "bp_len": f_len}
        f_percentage = f_len/p_len
        js_feat['percentage'] = f_percentage
        if not isinstance(gb_info, dict):
            raise Exception("gb_info parameter must be a dict type.")
        f_name = feat.qualifiers[gb_info['name_tag']][0]
        js_feat['name'] = f_name
        if 'color_tag' in gb_info:
            f_color = feat.qualifiers[gb_info['color_tag']][0]
            js_feat['color'] = f_color
        js_feat_list.append(js_feat)
    """
    Important values for feature: (what fraction of the whole thing is it?) 
    What is it's name?
    What comes before it and after it?
    Always round down and use up to 5 significant digits.

    """
    return js_feat_list



"""
Inputs:
    js_info: (dict)
        circle_size: (int) Radius size of circle in javascript (eg 200)
        line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) each internal part is an int [x,y]
        arrow_len: (int) Length of arrow
        arrow_thick: (int) thickness of arrow

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
            midpoint: (list) [x,y] midpoint location of feature

"""
def make_js_canvas_plasmid(js_feat_list, js_info):

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
    for i in range(s, len(js_feat_list)):
        js_add_str = "ctx.beginPath();"
        c_feat = js_feat_list[i]

        #Getting color
        if 'color' in c_feat:
            c_color = c_feat['color']
        else:
            #We give the element a random color
            c_color_list = []
            for i in range(6):
                c_color_list.append(random.choice([str(k) for k in range(10)] + ['A','B','C','D','E','F']))
            c_color = "#" + str(c_color_list[0]) + str(c_color_list[1]) + str(c_color_list[2]) + str(c_color_list[3])
            c_color += str(c_color_list[4]) + str(c_color_list[5])
            logging.debug(c_color)
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
        logging.debug(theta)
        midpoint_location = [c_c[0] + math.floor(radius*(math.cos(theta))), c_c[1] + math.floor(radius*(math.sin(theta)))]
        logging.debug("Midpoint Location?")
        logging.debug(midpoint_location)
        c_feat['midpoint'] = midpoint_location


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
        center_coordinates: (list) each internal part is an int [x,y]
        arrow_len: (int) Length of arrow
        arrow_thick: (int) thickness of arrow
    js_feat_list: (list) A list of dicts containing important info for the features, js_feat
        js_feat:(dict)
            percentage: (float)
            name: (str)
            color: (str) [optional]
            start_bp: (int) Start in plasmid in terms of base pairs.
            end_bp: (int) End in plasmid in terms of base pairs.
            bp_len: (int) Length in base pairs.
            midpoint: (list) [x,y] midpoint location of feature
"""
def make_js_arrows_and_names(js_feat_list, js_info):
    
    js_str = '<script>var c = document.getElementById("myCanvas");var ctx = c.getContext("2d");ctx.lineWidth = "2";ctx.strokeStyle = "black";'
    js_str += "ctx.font = '10pt Calibri';ctx.fillStyle = '#333';var maxWidth= 50; var lineHeight= 25;"
    
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
    add_js_str += 'var text = "' + 'origin' + '";'
    add_js_str += 'wrapText(ctx, text, ' + str(arrow_root[0] + 5) + ', ' + str(arrow_root[1]) + ', maxWidth, lineHeight);'
    js_str += add_js_str

    #Now we repeat the process for each feature in the plasmid
    for i in range(len(js_feat_list)):
        add_js_str = ''
        c_feat = js_feat_list[i]
        feat_midpoint = c_feat['midpoint']
        slope = (float(feat_midpoint[1]) - float(cc[1]))/(float(feat_midpoint[0]) - float(cc[0]))
        d_x = (arrow_len/(math.sqrt(1+slope**2)))
        arrow_root = [feat_midpoint[0] + d_x, feat_midpoint[1] + slope*(d_x)]
        #arrow tip should be touching plasmid, not inside it - use slope of arrow.
        arrow_tip = [feat_midpoint[0] + (d_x/8.0), feat_midpoint[1] + slope*(d_x/8.0)]

        add_js_str += 'ctx.beginPath(); canvas_arrow(ctx, ' + str(arrow_root[0]) + ', ' + str(arrow_root[1]) + ', ' + str(arrow_tip[0]) + ', '
        add_js_str += str(arrow_tip[1]) + ');ctx.stroke();'
        #making text box
        add_js_str += 'var text = "' + c_feat['name'] + '";'
        add_js_str += 'wrapText(ctx, text, ' + str(arrow_root[0] + 5) + ', ' + str(arrow_root[1]) + ', maxWidth, lineHeight);'
        js_str += add_js_str

    js_str += '</script>'

    return js_str





    



    return 0


"""
Inputs:
    js_file_path: (str) Path to a file with just javascript functions.
Outputs:
    javascript_functions_tag: (str) tag with all the necessary functions
"""
def get_javascript_functions(js_file_path):
    f = open(js_file_path, "r")
    javascript_functions_tag = f.read()
    f.close()
    return javascript_functions_tag


        












def main():
    test()

    return 0

def test():
    logging.basicConfig(level=logging.DEBUG)
    gb_file = "/Users/omreeg/KBase/apps/cello/data/test_plasmid_output.gbk"
    gb_info = {'name_tag': 'locus_tag'}
    js_info = {'circle_size': 200, 'line_width': 5, 'center_coordinates':[400,400],'arrow_len':50 ,'arrow_thick':2 }
    make_plasmid_graph(gb_file, gb_info, js_info)



    return 0

main()




