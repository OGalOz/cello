#python
'''
This file assists plasmid_map_viewer.py by adding detailed functionality, specifically on adding visuals
    to the Plasmid Circle for specific parts (promoter, terminator, CDS, etc).
Consider: https://sbolstandard.org/wp-content/uploads/2017/04/SBOL-Visual-2.1.pdf
Ribozyme can be visualized by a couple of dotted lines attached to a circle.
'''


import math
import logging




"""
Inputs:    

    js_info: (dict)
        circle_radius: (int) Radius size of circle in javascript (eg 300)
        circle_line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) Each internal part is an int [x,y]
        pointer_len: (int) Length of pointer
        pointer_thick: (int) Thickness of pointer
	text_size: (int) Size of text
        title_text_size: (int) Size of title text
    js_feat: (dict)
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
Outputs:
    js_str: (An internal javascript string representing the visuals of this object.)
"""
def make_sbol_visuals_js(js_feat, js_info, gb_info):

    js_str = ''
    types_dict = gb_info['types_dict']
    typ = js_feat['typ']
    if typ in types_dict["promoter"]:
        js_str += make_promoter_visual(js_feat, js_info)
    elif typ in types_dict["terminator"]:
        js_str += make_terminator_visual(js_feat, js_info)
    elif typ in types_dict["rbs"]:
        js_str += make_rbs_visual(js_feat, js_info)
    elif typ in types_dict["cds"]:
        js_str += make_cds_visual(js_feat, js_info)
    elif typ in types_dict["scar"]:
        js_str += make_scar_visual(js_feat, js_info)
    elif typ in types_dict["ribozyme"]:
        js_str += make_ribozyme_visual(js_feat, js_info)
    elif typ in types_dict["backbone"]:
        js_str += make_backbone_visual(js_feat, js_info)
    else:
        logging.critical("\n Could not recognize typ: " + typ + "\n")
        js_str += ""

    return js_str


"""
Inputs:    

    js_info: (dict)
        circle_radius: (int) Radius size of circle in javascript (eg 200)
        circle_line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) Each internal part is an int [x,y]
        pointer_len: (int) Length of pointer
        pointer_thick: (int) Thickness of pointer
	text_size: (int) Size of text
        promoter_info: (dict)
            percent_start: (float) Number between [0,100] that represents how deep into the angle the promoter symbol starts.
                20 if not given.
            prcnt: (float) [necessary if no pixels] percent increase
            pixels: (float) [necessary if no prcnt] pixel length increase
            line_width: (float) [optional] line width of promoter arrow
            arrow_angle: (float) [optional] (in degrees) angle between middle line of arrow and the two flags. 35 if not given. [10,80]
            flag_length: (int) [optional] length of arrow flags in pixels

    js_feat: (dict)
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
Outputs:
    js_str: (An internal javascript string representing the visuals of this object.)
"""
def make_promoter_visual(js_feat, js_info):
    logging.debug("Making Promoter.")

    if 'promoter_info' in js_info:
        promoter_info = js_info['promoter_info']
    else:
        logging.critical("DID NOT FIND PROMOTER INFO: ")
        logging.critical(js_info)
        return ""

    js_str = "//Promoter Symbol:\n"
    js_str += "ctx.strokeStyle = '{}'; ".format(promoter_info['arrow_color'])

    radius = js_info['circle_radius']
    cc = js_info['center_coordinates']
    percent_angle_to_promoter = promoter_info['percent_start']

    relative_angle_to_start = (js_feat['percentage'] * (percent_angle_to_promoter/100))*(math.pi * 2)

    starting_angle = get_angle_from_point(js_feat['start_circle'],cc)
    promoter_symbol_start_angle = starting_angle + relative_angle_to_start
    starting_coordinates = [cc[0] + radius*(math.cos(promoter_symbol_start_angle)),cc[1] + radius*(math.sin(promoter_symbol_start_angle))]

    if 'prcnt' in promoter_info:
        end_line_coordinates =  line_extension_coordinates(cc,starting_coordinates,"prcnt", promoter_info['prcnt'])
    elif 'pixels' in promoter_info:
        end_line_coordinates = line_extension_coordinates(cc,starting_coordinates,"pixels", promoter_info['pixels'])
    else:
        raise Exception("Neither pixels nor percent provided in promoter line extension info dict.")
    if 'line_width' in promoter_info:
        line_width = promoter_info['line_width']
    else:
        line_width = 3
    if 'arrow_angle' in promoter_info:
        arrow_angle = promoter_info['arrow_angle']
        if arrow_angle > 80 or arrow_angle < 10:
            raise Exception("Angle of flags of arrow must be between 10 and 80 degrees.")
    else:
        arrow_angle = 35.0
    if 'flag_length' in promoter_info:
        flag_length = promoter_info['flag_length']
    else:
        flag_length = 10
    



    js_str += 'ctx.lineWidth = ' + str(line_width) + '; '
    js_str += 'ctx.beginPath(); '
    js_str += 'ctx.moveTo('+ str(starting_coordinates[0]) + ',' +  str(starting_coordinates[1]) + '); '
    js_str += 'ctx.lineTo('+ str(end_line_coordinates[0]) + ',' +  str(end_line_coordinates[1]) + '); '
    js_str += 'ctx.stroke(); '

    #Now we must draw an arrow- first we use an extended radius to create an arc around the promoter area.
    #Then we make a small arrow at the end of the promoter region.
    big_radius = math.sqrt(((end_line_coordinates[0] - cc[0])**2) + ((end_line_coordinates[1] - cc[0])**2))
    ending_angle = get_angle_from_point(js_feat['end_circle'],cc)

    #We draw the promoter symbol arc on the canvas:
    js_str +=  'ctx.beginPath();'
    js_str +=  'ctx.arc(' + str(cc[0]) + ',' + str(cc[1]) + ',' + str(big_radius) + ',' + str(promoter_symbol_start_angle)
    js_str += ',' + str(ending_angle) + ');'
    js_str += 'ctx.stroke(); \n'

    #The ending point for the promoter symbol arc:
    p_symbol_end = [cc[0] + big_radius*(math.cos(ending_angle)),cc[1] + big_radius*(math.sin(ending_angle))]
   
    #We make the javascript text for the arrow flags
    js_str += make_arrow(cc ,p_symbol_end, arrow_angle, flag_length, line_width)
    js_str += "\n\n"

    return js_str
    


"""
Inputs:    
    js_info: (dict)
        circle_radius: (int) Radius size of circle in javascript (eg 200)
        circle_line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) Each internal part is an int [x,y]
        pointer_len: (int) Length of pointer
        pointer_thick: (int) Thickness of pointer
	text_size: (int) Size of text

        terminator_info: (dict)
            percent_center: (float) between [0,100] indicating where center of T is in region.
            prcnt: (float) [necessary if no pixels] percent increase from center to outer edge of Terminator Symbol
            pixels: (float) [necessary if no prcnt] pixel length increase from circle point to outer edge of Terminator Symbol
            base_width: (float) [optional] Width of inner part of the "T".
            base_height: (float) Height of inner part of the "T"
            top_width: (float) width of the top part of the T.
            top_height: (float) height of the top part of the T.
            internal_color: (str) [optional] Coloring of the inside of the rbs circle.
            border_color: (str) Color of the border of the T.
            border_width: (float) width of the border of the T.

    js_feat: (dict)
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
Outputs:
    js_str: (An internal javascript string representing the visuals of this object.)
"""
def make_terminator_visual(js_feat, js_info):
    """
    The terminator symbol will look like a capital T with filled in color light red: "#EA6062"
    We will use two rectangles and two thin black lines to outline it (size 2)
    There are 8 variables - 8 points that symbolize the T, each is a list of floats.
    We calculate those and then build the rectangle using them.
    """
    logging.debug("Making terminator")
    if "terminator_info" in js_info:
        terminator_info = js_info["terminator_info"]
    else:
        logging.critical("Terminator info not found in js_info.")
        return ""

    radius = js_info['circle_radius']
    cc = js_info['center_coordinates']

    
    js_str = "//Terminator Symbol: \n"
    """
    First, we find the 8 variables.
    """
    percent_center =  terminator_info["percent_center"]
    relative_angle_to_t_center = (js_feat['percentage'] * (percent_center/100))*(math.pi * 2)

    starting_angle = get_angle_from_point(js_feat['start_circle'],cc)
    terminator_symbol_center_angle = starting_angle + relative_angle_to_t_center

    """
    We start using names of variables specific to the terminator symbol shape.
    alpha represents the center of the base of the T on the circle's circumference.
    beta represents the extension of the line from center to alpha where the base of T intersects the top section of the T.
    gamma represents the extension of the same line from center to alpha and beta to the top of the T.
    """

    alpha = [cc[0] + radius*(math.cos(terminator_symbol_center_angle)),cc[1] + radius*(math.sin(terminator_symbol_center_angle))]
    logging.debug("ALPHA:")
    logging.debug(alpha)

    if "base_height" in terminator_info:
        beta = line_extension_coordinates(cc,alpha,"pixels", terminator_info["base_height"])
        logging.debug("BETA:")
        logging.debug(beta)
    else:
        raise Exception("base_height must be included in the terminator info in the config file.")
    if "top_height" in terminator_info:
        gamma = line_extension_coordinates(cc,beta,"pixels", terminator_info["top_height"])
        logging.debug("GAMMA:")
        logging.debug(gamma)
    else:
        raise Exception("top_height must be included in the terminator info in the config file.")

    
    """
    We start finding the variables on the edge of the T that represent it.
    var_a is one base, var_b is intersection from a-base to a-side of top, var_c is a-side bottom corner of top,
    var_d is top a-side corner of top, var_h is base opposite to var_a, var_e is top h-side corner of top, 
    var_f is bottom h-side corner of top, var_g is intersection of base with h-side of top, var_h is base opposite to var_a.
    """
    perpendicular_slope = get_perpendicular_slope(cc, alpha)
    
    if "base_width" in terminator_info:
        b_w = terminator_info["base_width"]
        two_bases_dict = get_points_in_both_directions_from_center_with_slope(alpha, perpendicular_slope, b_w/2)
        var_a = two_bases_dict["with_slope_point"]
        var_h = two_bases_dict["against_slope_point"]
        base_top_intersect_points = get_points_in_both_directions_from_center_with_slope(beta, perpendicular_slope, b_w/2)
        var_b = base_top_intersect_points["with_slope_point"]
        var_g = base_top_intersect_points["against_slope_point"]
    else:
        raise Exception("base_width must be included in terminator_info in json config file.")

    if "top_width" in terminator_info:
        t_w = terminator_info["top_width"]
        two_bottom_top_dict = get_points_in_both_directions_from_center_with_slope(beta, perpendicular_slope, t_w/2)
        var_c = two_bottom_top_dict["with_slope_point"]
        var_f = two_bottom_top_dict["against_slope_point"]
        top_points = get_points_in_both_directions_from_center_with_slope(gamma, perpendicular_slope, t_w/2)
        var_d = top_points["with_slope_point"]
        var_e = top_points["against_slope_point"]
    else:
        raise Exception("top_width must be included in terminator_info in json config file.")


    logging.debug("Vars A through H:")
    logging.debug(str(var_a) + " " +  str(var_b) + " " +  str(var_c) + " " +  str(var_d) + " " +  str(var_e) + " " +  str(var_f) + " " +  str(var_g) + " " +  str(var_h))
    list_of_coordinates = [var_a, var_b, var_c, var_d, var_e, var_f, var_g, var_h]

    js_str += make_javascript_terminator_text(list_of_coordinates, terminator_info)




    
    return js_str





"""
rbs: 'ribosome binding site', also known as 'ribosome entry site'.

Inputs:    
    js_info: (dict)
        circle_radius: (int) Radius size of circle in javascript (eg 200)
        circle_line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) Each internal part is an int [x,y]
        pointer_len: (int) Length of pointer
        pointer_thick: (int) Thickness of pointer
	text_size: (int) Size of text

        ribosome_site_info: (dict)
            percent_center: (float) between [0,100] indicating where center of rbs circle is in region.
            radius: (float) (less than 25) The radius of the rbs half circle.
            border_width: (float) [optional] Width of rbs half-circle border.
            border_color: (str) probably black
            internal_color: (str) hex symbol that has 6 characters preceded by a '#', like "#EA6062"

    js_feat: (dict)
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
Outputs:
    js_str: (An internal javascript string representing the visuals of this object.)
"""

def make_rbs_visual(js_feat, js_info):
    """
    The ribosome binding/entry site symbol will look like a half circle with filled in color light purple.
    We calculate the center point of the rbs circle. Then we find the angle of the line perpendicular to the center 
    of the plasmid map circle.
    """
    logging.debug("Making rbs")
    if "ribosome_site_info" in js_info:
        rbs_info = js_info["ribosome_site_info"]
    else:
        logging.critical("Ribosome Site Info not found in js_info.")
        return ""

    radius = js_info['circle_radius']
    cc = js_info['center_coordinates']

    
    js_str = "//RBS Symbol: \n"
    """
    First, we find the center of the rbs circle we will make.
    """
    percent_center = rbs_info["percent_center"]
    relative_angle_to_t_center = (js_feat['percentage'] * (percent_center/100))*(math.pi * 2)

    starting_angle = get_angle_from_point(js_feat['start_circle'],cc)
    rbs_symbol_center_angle = starting_angle + relative_angle_to_t_center
    rbs_circle_center = [cc[0] + radius*(math.cos(rbs_symbol_center_angle)),cc[1] + radius*(math.sin(rbs_symbol_center_angle))]
    
    #Notice, here we add some distance from center of plasmid circle to the center of the rbs circle in order
    #  to get the circle to sit on top of the plasmid visual, and not inside it.
    extension_length = js_info['circle_line_width']/2
    rbs_circle_center = line_extension_coordinates(cc,rbs_circle_center,"pixels", extension_length)

    start_angle = get_angle_from_point(rbs_circle_center, cc) + (math.pi/2)

    js_str += make_javascript_rbs_text(rbs_circle_center, start_angle, rbs_info)

    return js_str




"""
cds: 'Coding Sequence', also known as ORF or Gene.

Inputs:    
    js_info: (dict)
        circle_radius: (int) Radius size of circle in javascript (eg 200)
        circle_line_width: (int) Thickness of line in plasmid
        center_coordinates: (list) Each internal part is an int [x,y]
        pointer_len: (int) Length of pointer
        pointer_thick: (int) Thickness of pointer
	text_size: (int) Size of text

        cds_info: (dict)
            percent_start: (float) between [0,100] indicating where the start of the arrow is, normally 85.
            arrow_height: (float) [1,25] Indicates how far from the plasmid circle the arrow extends.
    js_feat: (dict)
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
Outputs:
    js_str: (An internal javascript string representing the visuals of this object.)
"""

def make_cds_visual(js_feat, js_info):
    """
    The CDS visual will look like an arrow head ending at the end of the CDS.
    In order to draw this, we need 6 variables. The variables represent:
        var_a: point on plasmid map that outer arrow starts.
        var_b: point outside plasmid map that outer arrow has its peak.
        var_c: point on plasmid map, same as end of cds, where arrow ends.
        var_d: inner complement to a.
        var_e: inner complement to b.
        var_f: inner complement to c.
    """
    logging.debug("Making CDS Visual")
    if "cds_info" in js_info:
        cds_info = js_info["cds_info"]
    else:
        logging.critical("CDS Info not found in js_info.")
        logging.critical(js_info.keys())
        return ""

    radius = js_info['circle_radius']
    cc = js_info['center_coordinates']

    
    js_str = "//CDS Symbol: \n"
    """
    First, we find the start of the CDS arrow we will make.
    """
    percent_start = cds_info["percent_start"]
    relative_angle_to_t_center = (js_feat['percentage'] * (percent_start/100))*(math.pi * 2)

    starting_angle = get_angle_from_point(js_feat['start_circle'],cc)
    cds_symbol_start_angle = starting_angle + relative_angle_to_t_center
    cds_symbol_start_point = [cc[0] + radius*(math.cos(cds_symbol_start_angle)),cc[1] + radius*(math.sin(cds_symbol_start_angle))]
    var_a = line_extension_coordinates(cc,cds_symbol_start_point,"pixels", js_info['circle_line_width']/2)
    var_b = line_extension_coordinates(cc,var_a,"pixels",cds_info["arrow_height"])
    var_c = line_extension_coordinates(cc,js_feat['end_circle'],"pixels", js_info['circle_line_width']/2)
    var_d = line_extension_coordinates(var_a, cds_symbol_start_point,"pixels", js_info['circle_line_width']/2)
    var_e = line_extension_coordinates(var_a,var_d,"pixels",cds_info["arrow_height"])
    var_f = line_extension_coordinates(var_c, js_feat['end_circle'],"pixels", js_info['circle_line_width']/2)

    #Outer Triangle
    js_str += "ctx.beginPath(); "
    js_str += "ctx.moveTo({},{}); ".format(str(var_a[0]),str(var_a[1]))
    js_str += "ctx.lineTo({},{}); ".format(str(var_b[0]), str(var_b[1]))
    js_str += "ctx.lineTo({},{}); ".format(str(var_c[0]), str(var_c[1]))
    js_str += "ctx.closePath(); ctx.fillStyle = '{}'; ctx.fill(); \n".format(js_feat['color'])
    #Inner Triangle
    js_str += "ctx.beginPath(); "
    js_str += "ctx.moveTo({},{}); ".format(str(var_d[0]),str(var_d[1]))
    js_str += "ctx.lineTo({},{}); ".format(str(var_e[0]), str(var_e[1]))
    js_str += "ctx.lineTo({},{}); ".format(str(var_f[0]), str(var_f[1]))
    js_str += "ctx.closePath(); ctx.fillStyle = '{}'; ctx.fill(); ctx.beginPath(); \n\n".format(js_feat['color'])

    return js_str








#Unsure of visuals for the following
def make_scar_visual(js_feat, js_info):

    return ""


def make_ribozyme_visual(js_feat, js_info):

    return ""

def make_backbone_visual(js_feat, js_info):

    return ""






"""
Inputs:
    A: (list) list of floats [x,y] starting point.
    B: (list) list of floats [a,b] ending point.
Outputs:
    slope: (float) represents slope from A to B.
"""
def calculate_slope(A,B):

    logging.debug("Calculating Slope: ")
    logging.debug("Start Point: ({},{})".format(A[0], A[1]))
    logging.debug("End Point: ({},{})".format(B[0], B[1]))

    if B[0] >= A[0]:
        rise = (B[1] - A[1])
        run = B[0] - A[0]
    else: #B[0] < A[0]
        rise = (A[1] - B[1])
        run = A[0] - B[0]
    if run == 0:
        if rise == 0:
            raise Exception("A = B, cannot calculate slope")
        run = 0.000001
    slope = rise/run
    logging.debug("Slope: {}".format(str(slope)))
    return slope



"""
Inputs:
    A: (list) list of floats [x,y] starting point.
    B: (list) list of floats [a,b] ending point (add extension to these coordinates).
    prcnt_pixel_indicator: (str) limited vocab to "prcnt" or "pixels"
    prcnt: (float) -1.0<p<1.0 [necessary if no pixels] A float representing the percent increase/decrease in length you want in the line.
    pixels: (int) [necessary if no pixels] An integer representing increase/decrease in length in pixels if wanted.
Outputs:
    ext_c: (list) A list of floats [c,d] representing an extension of the line
"""
def line_extension_coordinates(A,B,prcnt_pixel_indicator, prcnt_or_pixels_value):
    if prcnt_pixel_indicator == "prcnt":
        prcnt = prcnt_or_pixels_value
        if prcnt > 1.0 or prcnt < -1.0:
            raise Exception("Percent must be decimal point between -1 and 1")
        line_length = math.sqrt(((A[0] - B[0])**2) + ((A[1] - B[1])**2))
        change_length = prcnt * (line_length)
    elif prcnt_pixel_indicator == "pixels":
        pixels = prcnt_or_pixels_value
        if abs(pixels) > 600:
            raise ValueError("pixel change must be less than 600")
        change_length = pixels
    else:
        raise Exception("Did not recognize prcnt_pixel_indicator, must be one of prcnt or pixels")

    slope = calculate_slope(A,B)
    if B[0] >= A[0]:
        if change_length >= 0:
            d_x = (change_length/math.sqrt(1+(slope**2)))
            d_y = slope * d_x
            ext_c = [B[0] + d_x, B[1] + d_y]
        else: #change_length < 0:
            change_length = -1 * change_length
            d_x = (change_length/math.sqrt(1+(slope**2)))
            d_y = slope * d_x
            ext_c = [B[0] - d_x, B[1] - d_y]
    else: #B[0] < A[0]
        if change_length >= 0:
            d_x = (change_length/math.sqrt(1+(slope**2)))
            d_y = slope * d_x
            ext_c = [B[0] - d_x, B[1] - d_y]
        else: #change_length < 0:
            d_x = (change_length/math.sqrt(1+(slope**2)))
            d_y = slope * d_x
            ext_c = [B[0] + d_x, B[1] + d_y]
    return ext_c









    



"""
Inputs:
    a: (list) [x,y]
    b: (list) [x,y]
"""
def calc_dist(a,b):
    return math.sqrt( (a[0]-b[0])**2 + (a[1] - b[1])**2 )


"""
Inputs: 
    circle_coordinates: (list) floats [x,y] for a point on the circle.
    center_coordinates: (list) floats [x,y] for the center of the circle.
Output:
    theta: (float) The angle to the point

"""
def get_angle_from_point(circle_coordinates ,center_coordinates):
   
    d_y = (circle_coordinates[1] - center_coordinates[1])
    d_x = circle_coordinates[0] - center_coordinates[0]
    theta = math.atan2(d_y, d_x)

    return theta

"""
Inputs:
    A: (list) coordinates of a point in the canvas [x,y] (Would normally be the center)
    B: (list) coordinates of a point in the canvas [x,y] (Would normally be the outer point on a circle)
Outputs:
    p_slope: (float) The perpendicular slope

"""
def get_perpendicular_slope(A,B):
    slope = calculate_slope(A,B)
    logging.debug("original slope: {}".format(str(slope)))
    if slope != 0:
        p_slope = (-1/slope)
        return p_slope
    else:
        if A[0] < B[0]:
            return -10000
        elif B[0] < A[0]:
            return 10000
        else:
            raise Exception("A = B, cannot calculate slope")

"""
Inputs:
    A and B are points to which the arrow will be drawn perpendicularly
    A: (list) coordinates of a point in the canvas [x,y] (Would normally be the center)
    B: (list) coordinates of a point in the canvas [x,y] (Would normally be the outer point on a circle)
    arrow_angle: (float) (in degrees) between 10 and 80. 
    flag_length: (float) length of the flag
    Outputs:
    js_str: (str) A string representing an arrow pointing from the circle

"""
def make_arrow(A,B,arrow_angle, flag_length, line_width):
    #B is ending point for the arrow.
    # Angles for the arrow must be calculated using the perpendicular slope - (from center to end of promoter symbol)
    slope = get_perpendicular_slope(A,B)
    logging.debug("Slope: {}".format(str(slope)))
    rotation_angle = math.atan(slope)
    logging.debug("Rotation angle: ")
    logging.debug(rotation_angle)

    #The following part is confusing, do not rely on Cartesian coordinates. The y coordinates here are flipped (ascending is descending on graph).
    if slope > 0:
        #This means slope is actually descending visually
        if B[0] > A[0]:
            #We are in the 1st quadrant.
            logging.debug("1st quadrant.")
            flag_a_1 = [flag_length*math.cos((180+arrow_angle)*(math.pi/180)), flag_length*math.sin((180+arrow_angle)*(math.pi/180))]
            flag_a_2 = perform_rotation(flag_a_1, rotation_angle)
            flag_b_1 = [flag_length*math.cos((180-arrow_angle)*(math.pi/180)), flag_length*math.sin((180-arrow_angle)*(math.pi/180))]
            flag_b_2 = perform_rotation(flag_b_1, rotation_angle)

        elif B[0] < A[0]:
            #We are in the 3rd quadrant.
            logging.debug("3rd quadrant.")
            flag_a_1 = [flag_length*math.cos((arrow_angle)*(math.pi/180)), flag_length*math.sin((arrow_angle)*(math.pi/180))]
            flag_a_2 = perform_rotation(flag_a_1, rotation_angle)
            flag_b_1 = [flag_length*math.cos(((-1)*arrow_angle)*(math.pi/180)), flag_length*math.sin(((-1)*arrow_angle)*(math.pi/180))]
            flag_b_2 = perform_rotation(flag_b_1, rotation_angle)

    elif slope < 0:
        #Visually ascending slope
        if B[0] > A[0]:
            #We are in the fourth quadrant.
            logging.debug("4th quadrant.")
            flag_a_1 = [flag_length*math.cos((arrow_angle)*(math.pi/180)), flag_length*math.sin((arrow_angle)*(math.pi/180))]
            flag_a_2 = perform_rotation(flag_a_1, rotation_angle)
            flag_b_1 = [flag_length*math.cos(((-1)*arrow_angle)*(math.pi/180)), flag_length*math.sin(((-1)*arrow_angle)*(math.pi/180))]
            flag_b_2 = perform_rotation(flag_b_1, rotation_angle)

        elif B[0] < A[0]:
            #We are in the second quadrant.
            logging.debug("2nd quadrant.")
            flag_a_1 = [flag_length*math.cos((180+arrow_angle)*(math.pi/180)), flag_length*math.sin((180+arrow_angle)*(math.pi/180))]
            flag_a_2 = perform_rotation(flag_a_1, rotation_angle)
            flag_b_1 = [flag_length*math.cos((180-arrow_angle)*(math.pi/180)), flag_length*math.sin((180-arrow_angle)*(math.pi/180))]
            flag_b_2 = perform_rotation(flag_b_1, rotation_angle)

    elif slope == 0:
        if B[1] > A[1]:
            #The arrow is drawn at the bottom of the circle (origin) towards the right
            arrow_start = [B[0] - pixels, B[1]]
        elif B[1] < A[1]:
            #The arrow is drawn at the top of the circle towards the left.
            arrow_start = [B[0] + pixels, B[1]]
    js_str = make_js_canvas_arrow(B, flag_a_2, flag_b_2, line_width)
    return js_str



"""
Inputs:
    A and B are points to which the arrow will be drawn perpendicularly
    A: (list) coordinates of a point in the canvas [x,y] (Would normally be the center)
    B: (list) coordinates of a point in the canvas [x,y] (Would normally be the outer point on a circle)
    arrow_angle: (float) (in degrees) between 10 and 80. 
    flag_length: (float) length of the flag
Outputs:
        arrow_dict:
            inner_flag_start: list<int>
            outer_flag_start: list<int>
            flags_end: list<int>

"""
def calculate_arrow_values(A,B,arrow_angle, flag_length, line_width):
    #B is ending point for the arrow.
    # Angles for the arrow must be calculated using the perpendicular slope - (from center to end of promoter symbol)
    slope = get_perpendicular_slope(A,B)
    logging.debug("Slope: {}".format(str(slope)))
    rotation_angle = math.atan(slope)
    logging.debug("Rotation angle: ")
    logging.debug(rotation_angle)

    #The following part is confusing, do not rely on Cartesian coordinates. The y coordinates here are flipped (ascending is descending on graph).
    if slope > 0:
        #This means slope is actually descending visually
        if B[0] > A[0]:
            #We are in the 1st quadrant.
            logging.debug("1st quadrant.")
            flag_a_1 = [flag_length*math.cos((180+arrow_angle)*(math.pi/180)), flag_length*math.sin((180+arrow_angle)*(math.pi/180))]
            flag_a_2 = perform_rotation(flag_a_1, rotation_angle)
            flag_b_1 = [flag_length*math.cos((180-arrow_angle)*(math.pi/180)), flag_length*math.sin((180-arrow_angle)*(math.pi/180))]
            flag_b_2 = perform_rotation(flag_b_1, rotation_angle)

        elif B[0] < A[0]:
            #We are in the 3rd quadrant.
            logging.debug("3rd quadrant.")
            flag_a_1 = [flag_length*math.cos((arrow_angle)*(math.pi/180)), flag_length*math.sin((arrow_angle)*(math.pi/180))]
            flag_a_2 = perform_rotation(flag_a_1, rotation_angle)
            flag_b_1 = [flag_length*math.cos(((-1)*arrow_angle)*(math.pi/180)), flag_length*math.sin(((-1)*arrow_angle)*(math.pi/180))]
            flag_b_2 = perform_rotation(flag_b_1, rotation_angle)

    elif slope < 0:
        #Visually ascending slope
        if B[0] > A[0]:
            #We are in the fourth quadrant.
            logging.debug("4th quadrant.")
            flag_a_1 = [flag_length*math.cos((arrow_angle)*(math.pi/180)), flag_length*math.sin((arrow_angle)*(math.pi/180))]
            flag_a_2 = perform_rotation(flag_a_1, rotation_angle)
            flag_b_1 = [flag_length*math.cos(((-1)*arrow_angle)*(math.pi/180)), flag_length*math.sin(((-1)*arrow_angle)*(math.pi/180))]
            flag_b_2 = perform_rotation(flag_b_1, rotation_angle)

        elif B[0] < A[0]:
            #We are in the second quadrant.
            logging.debug("2nd quadrant.")
            flag_a_1 = [flag_length*math.cos((180+arrow_angle)*(math.pi/180)), flag_length*math.sin((180+arrow_angle)*(math.pi/180))]
            flag_a_2 = perform_rotation(flag_a_1, rotation_angle)
            flag_b_1 = [flag_length*math.cos((180-arrow_angle)*(math.pi/180)), flag_length*math.sin((180-arrow_angle)*(math.pi/180))]
            flag_b_2 = perform_rotation(flag_b_1, rotation_angle)

    flag_a_2 = [B[0] + flag_a_2[0], B[1] + flag_a_2[1]]
    flag_b_2 = [B[0] + flag_b_2[0], B[1] + flag_b_2[1]]

    arrow_dict = {
            "flags_end": B,
            "inner_flag_start" : flag_a_2,
            "outer_flag_start" : flag_b_2,

            }
    return arrow_dict


"""
Inputs:
    center_point: (list) floats coordinates of the center point in the canvas [x,y] (arrow destination)
    flag_a: (list) floats coordinates of a point in the canvas [x,y] (arrow flag a end)
    flag_b: (list) floats coordinates of a point in the canvas [x,y] (arrow flag b end)
Outputs:
    js_str: (str) A string representing an arrow pointing from the circle
"""
def make_js_canvas_arrow(center_point, flag_a, flag_b, line_width):
    start = center_point
    js_str = 'ctx.lineWidth = {};'.format(str(line_width))
    js_str += 'ctx.moveTo({},{});'.format(str(start[0]), str(start[1]))
    end_a = [start[0] + flag_a[0], start[1] + flag_a[1]]
    js_str += 'ctx.lineTo({},{});'.format(str(end_a[0]), str(end_a[1]))
    js_str += 'ctx.stroke();'
    js_str += 'ctx.moveTo({},{});'.format(str(start[0]), str(start[1]))
    end_b = [start[0] + flag_b[0], start[1] + flag_b[1]]
    js_str += 'ctx.lineTo({},{});'.format(str(end_b[0]), str(end_b[1]))
    js_str += 'ctx.stroke();'
    return js_str
    


"""
Inputs:
    point: (list) [x,y] location of point in the plane.
    angle: (float) Angle in radians to shift point.
Outputs:
    rotated_point: (list) [x,y] location of rotated point in the plane.
"""
def perform_rotation(point, angle):
    x_coordinate = (math.cos(angle)*point[0]) - (math.sin(angle)*point[1])
    y_coordinate = (math.sin(angle)*point[0]) + (math.cos(angle)*point[1])
    return [x_coordinate, y_coordinate]
    

"""
Inputs:
    center_point: (list) A list of coordinates for the point from which we calculate the distances.
    slope: (float) The rise over run of the line on which we're returning the points.
    pixels: (float) The distance from the center_point in the direction of the slope.

Outputs:
    points_dict: (dict)
        with_slope_point: (list) Coordinates for the point that goes in the direction of the slope.
        against_slope_point: (list) Coordinates for the point that goes against the direction of the slope.
"""
def get_points_in_both_directions_from_center_with_slope(center_point, slope, pixels):
    
    dx = pixels/(math.sqrt(1+slope**2))
    dy = dx*slope
    with_slope_point = [center_point[0] + dx, center_point[1] + dy]
    against_slope_point = [center_point[0] - dx, center_point[1] - dy]    

    points_dict = {
            "with_slope_point": with_slope_point,
            "against_slope_point": against_slope_point
            }

    return points_dict


"""
Inputs:
    list_of_coordinates: (list) A list of 8 coordinates on the outside of the terminator symbol.
        coordinate: (list) [A,B] X, Y representation of coordinates.
    terminator_info: (dict)
            percent_center: (float) between [0,100] indicating where center of T is in region.
            prcnt: (float) [necessary if no pixels] percent increase from center to outer edge of Terminator Symbol
            pixels: (float) [necessary if no prcnt] pixel length increase from circle point to outer edge of Terminator Symbol
            base_width: (float) [optional] Width of inner part of the "T".
            inner_length: (float) [optional] Length of inner part of the "T".
            outer_width: (float) [optional] Width of top part of "T"
            internal_color: (str) hex symbol that has 6 characters preceded by a '#', like "#EA6062"
            border_color: (str) e.g. black
            border_width: float [1,8]

Outputs:
    j_str: (str) A string representing the terminator symbol in that location.

"""
def make_javascript_terminator_text(list_of_coordinates, terminator_info):

    #First we make the borders of the terminator symbol
    j_str = 'ctx.strokeStyle = "{}"; '.format(terminator_info["border_color"])
    j_str += "ctx.lineWidth = {}; ".format(str(terminator_info["border_width"]))
    start_point = list_of_coordinates[0]
    j_str += "ctx.moveTo({},{}); ".format(str(start_point[0]), str(start_point[1]))
    for i in range(1,len(list_of_coordinates)):
        current_point = list_of_coordinates[i]
        j_str += "ctx.lineTo({},{}); ".format(str(current_point[0]), str(current_point[1]))
    j_str += "ctx.stroke(); \n"
    j_str += "ctx.beginPath(); "
    j_str += "ctx.moveTo({},{}); ".format(str(start_point[0]), str(start_point[1]))
    for i in range(1,len(list_of_coordinates)):
        current_point = list_of_coordinates[i]
        j_str += "ctx.lineTo({},{}); ".format(str(current_point[0]), str(current_point[1]))
    j_str += 'ctx.fillStyle = "{}"; '.format(terminator_info["internal_color"])
    j_str += "ctx.closePath(); ctx.fill(); \n\n"

    return j_str
   


"""
Inputs:
    rbs_circle_center: (list) [x,y] coordinates for center of the rbs circle.
    starting_angle: (float) Angle at which the semi circle starts.
    rbs_info: (dict)
            radius: (float) (less than 25) The radius of the rbs half circle.
            border_width: (float) [optional] Width of rbs half-circle border.
            border_color: (str) probably black
            internal_color: (str) hex symbol that has 6 characters preceded by a '#', like "#EA6062"

Outputs:
    js_str: (string) The string that represents the ribosome semi-circle symbol.
"""
def make_javascript_rbs_text(rbs_circle_center, starting_angle, rbs_info):
    js_str = "ctx.beginPath();"
    js_str += "ctx.arc({}, {}, {}, {}, {}, true); ctx.closePath(); ".format(str(rbs_circle_center[0]),
            str(rbs_circle_center[1]),str(rbs_info['radius']), str(starting_angle),
            str(starting_angle - math.pi) )
    js_str += "ctx.lineWidth = {}; ".format(str(rbs_info['border_width']))
    js_str += "ctx.fillStyle = '{}'; ".format(rbs_info["internal_color"])
    js_str += "ctx.fill(); "
    js_str += "ctx.strokeStyle = '{}';".format(rbs_info["border_color"])
    js_str += "ctx.stroke(); \n\n"
    return js_str

"""
Inputs:
    feature_dict: (dict from feature_list.json)
    config_dict: (dict from config.json)
Output:
    js_object:
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

"""
def calculate_pointer_and_text(feature_dict, config_dict):

    
    js_info = config_dict["js_info"]

    js_object = {"type": "pointer_and_text"}
    pointer_dict = {"type": "pointer"}
    pointer_dict['new_line_width_bool'] = False
    pointer_dict['line_width'] = js_info['pointer_thick']
    pointer_dict['line_color'] = js_info['pointer_color']
    end_point = feature_dict["point_mid"]
    pointer_dict['end_point'] = end_point

    line_length = js_info["pointer_len_" + feature_dict["feat_pointer_len"]]

    if feature_dict["feat_pointer_direction"] == "out":
        start_key = "with_slope_point"
    else:
        start_key = "against_slope_point"
    points_options = get_points_in_both_directions_from_center_with_slope(
            end_point, 
            calculate_slope(js_info['center_coordinates'], end_point), 
            line_length)
    start_point = points_options[start_key]
    pointer_dict["start_point"] = start_point
    js_object["pointer"] = pointer_dict

    
    text_changes = line_extension_coordinates(end_point, start_point, 
            "pixels", js_info["pointer_distance"])
    text_dict = {"type": "text"}
    text_dict["text_point"] = [text_changes[0] , text_changes[1]]
    text_dict["text_str"] = feature_dict["feat_name"][0] + " ({})".format(feature_dict["bp_len"])
    text_dict["new_text_font_bool"] = False
    text_dict["text_font"] = str(js_info["text_size"]) + "pt Calibri"
    js_object["text"] = text_dict

    return js_object


"""
Inputs:
    feature_dict: (dict from feature_list.json)
    config_dict: (dict from config.json)
Outputs:
    coordinates - list<float>
    js_object:
        type: (str) "promoter"
        color: (str)
        line_width: (int)
        p_line_coordinate_start: list<float>
        big_radius: (int)
        arc_begin_point: list<float>
        arc_start_angle: list<float>
        arc_angle: (float)
        arc_end_angle: (float)
        arc_end_point: list<float>
        inner_flag_start: list<float>
        outer_flag_start: list<float>
        flags_end: list<float>
"""
def calculate_promoter_feature(feature_dict, config_dict):
    js_object = {"type": "promoter"}
    js_info = config_dict['js_info']
    promoter_info = js_info['promoter_info']
    js_object["color"] = promoter_info["arrow_color"]
    js_object["line_width"] = promoter_info["line_width"]

    if feature_dict['feat_strand'] == -1:
        radius = js_info['complementary_radius']
    else:
        radius = js_info['circle_radius']

    cc = js_info['center_coordinates']
    js_object['center_x'] = cc[0]
    js_object['center_y'] = cc[1]
    js_object['feat_name'] = feature_dict['feat_name']

    percent_angle_to_promoter = promoter_info['percent_start']

    relative_angle_to_start = (feature_dict['plasmid_percentage'] * (percent_angle_to_promoter/100))*(math.pi * 2)

    starting_angle = get_angle_from_point(feature_dict['point_start'],cc)
    promoter_symbol_start_angle = starting_angle + relative_angle_to_start
    starting_coordinates = [cc[0] + radius*(math.cos(promoter_symbol_start_angle)),cc[1] + \
            radius*(math.sin(promoter_symbol_start_angle))]
    

    if 'prcnt' in promoter_info:
        end_line_coordinates =  line_extension_coordinates(cc,starting_coordinates,"prcnt", promoter_info['prcnt'])
    elif 'pixels' in promoter_info:
        end_line_coordinates = line_extension_coordinates(cc,starting_coordinates,"pixels", promoter_info['pixels'])
    else:
        raise Exception("Neither pixels nor percent provided in promoter line extension info dict.")
    if 'line_width' in promoter_info:
        line_width = promoter_info['line_width']
    else:
        line_width = 3
    if 'arrow_angle' in promoter_info:
        arrow_angle = promoter_info['arrow_angle']
        if arrow_angle > 80 or arrow_angle < 10:
            raise Exception("Angle of flags of arrow must be between 10 and 80 degrees.")
    else:
        arrow_angle = 35.0
    if 'flag_length' in promoter_info:
        flag_length = promoter_info['flag_length']
    else:
        flag_length = 10


    js_object['p_line_coordinate_start'] = starting_coordinates
    js_object['arc_begin_point'] = end_line_coordinates
    js_object["arc_start_angle"] = promoter_symbol_start_angle


    #Now we must draw an arrow- first we use an extended radius to create an arc around the promoter area.
    #Then we make a small arrow at the end of the promoter region.
    big_radius = math.sqrt(((end_line_coordinates[0] - cc[0])**2) + ((end_line_coordinates[1] - cc[0])**2))
    js_object["big_radius"] = big_radius
    ending_angle = get_angle_from_point(feature_dict['point_end'],cc)
    js_object["arc_end_angle"] = ending_angle


    #The ending point for the promoter symbol arc:
    p_symbol_end = [cc[0] + big_radius*(math.cos(ending_angle)),cc[1] + big_radius*(math.sin(ending_angle))]
    js_object["arc_end_point"] = p_symbol_end

    #We make the javascript text for the arrow flags
    arrow_dict = calculate_arrow_values(cc ,p_symbol_end, arrow_angle, flag_length, line_width)

    for k in arrow_dict.keys():
        js_object[k] = arrow_dict[k]

    return js_object





def calculate_terminator_feature(feature_dict, config_dict):
    """
    The terminator symbol will look like a capital T with filled in color light red: "#EA6062"
    We will use two rectangles and two thin black lines to outline it (size 2)
    There are 8 variables - 8 points that symbolize the T, each is a list of floats.
    We calculate those and then build the rectangle using them.
    """
    logging.debug("Making terminator")
    js_info = config_dict["js_info"]
    if "terminator_info" in js_info:
        terminator_info = js_info["terminator_info"]
    else:
        raise Exception("terminator info not in config.json")

    if feature_dict["feat_strand"] == 1:
        radius = js_info['circle_radius']
    else:
        radius = js_info['complementary_radius']

    cc = js_info['center_coordinates']

    
    """
    First, we find the 8 variables.
    """
    percent_center =  terminator_info["percent_center"]
    relative_angle_to_t_center = (feature_dict['plasmid_percentage'] * (percent_center/100))*(math.pi * 2)

    starting_angle = get_angle_from_point(feature_dict['point_start'],cc)
    terminator_symbol_center_angle = starting_angle + relative_angle_to_t_center

    """
    We start using names of variables specific to the terminator symbol shape.
    alpha represents the center of the base of the T on the circle's circumference.
    beta represents the extension of the line from center to alpha where the base of T intersects the top section of the T.
    gamma represents the extension of the same line from center to alpha and beta to the top of the T.
    """

    alpha = [cc[0] + radius*(math.cos(terminator_symbol_center_angle)),cc[1] + radius*(math.sin(terminator_symbol_center_angle))]
    logging.debug("ALPHA:")
    logging.debug(alpha)

    if "base_height" in terminator_info:
        beta = line_extension_coordinates(cc,alpha,"pixels", terminator_info["base_height"])
        logging.debug("BETA:")
        logging.debug(beta)
    else:
        raise Exception("base_height must be included in the terminator info in the config file.")
    if "top_height" in terminator_info:
        gamma = line_extension_coordinates(cc,beta,"pixels", terminator_info["top_height"])
        logging.debug("GAMMA:")
        logging.debug(gamma)
    else:
        raise Exception("top_height must be included in the terminator info in the config file.")

    
    """
    We start finding the variables on the edge of the T that represent it.
    var_a is one base, var_b is intersection from a-base to a-side of top, var_c is a-side bottom corner of top,
    var_d is top a-side corner of top, var_h is base opposite to var_a, var_e is top h-side corner of top, 
    var_f is bottom h-side corner of top, var_g is intersection of base with h-side of top, var_h is base opposite to var_a.
    """
    perpendicular_slope = get_perpendicular_slope(cc, alpha)
    
    if "base_width" in terminator_info:
        b_w = terminator_info["base_width"]
        two_bases_dict = get_points_in_both_directions_from_center_with_slope(alpha, perpendicular_slope, b_w/2)
        var_a = two_bases_dict["with_slope_point"]
        var_h = two_bases_dict["against_slope_point"]
        base_top_intersect_points = get_points_in_both_directions_from_center_with_slope(beta, perpendicular_slope, b_w/2)
        var_b = base_top_intersect_points["with_slope_point"]
        var_g = base_top_intersect_points["against_slope_point"]
    else:
        raise Exception("base_width must be included in terminator_info in json config file.")

    if "top_width" in terminator_info:
        t_w = terminator_info["top_width"]
        two_bottom_top_dict = get_points_in_both_directions_from_center_with_slope(beta, perpendicular_slope, t_w/2)
        var_c = two_bottom_top_dict["with_slope_point"]
        var_f = two_bottom_top_dict["against_slope_point"]
        top_points = get_points_in_both_directions_from_center_with_slope(gamma, perpendicular_slope, t_w/2)
        var_d = top_points["with_slope_point"]
        var_e = top_points["against_slope_point"]
    else:
        raise Exception("top_width must be included in terminator_info in json config file.")

    list_of_coordinates = [var_a, var_b, var_c, var_d, var_e, var_f, var_g, var_h]

    js_object = {"type": "terminator",
            "border_color": terminator_info["border_color"],
            "internal_color": terminator_info["internal_color"],
            "border_width": terminator_info['border_width'],
            "feat_name": feature_dict['feat_name'],
            "base_1": var_a,
            "armpit_1": var_b,
            "palm_hand_1":var_c,
            "back_hand_1": var_d,
            "back_hand_2": var_e,
            "palm_hand_2": var_f,
            "armpit_2": var_g,
            "base_2": var_h,
            }

    return js_object


def calculate_rbs_feature(feature_dict, config_dict):
    js_info = config_dict["js_info"]

    """
    The ribosome binding/entry site symbol will look like a half circle with filled in color light purple.
    We calculate the center point of the rbs circle. Then we find the angle of the line perpendicular to the center 
    of the plasmid map circle.
    """
    logging.debug("Making rbs")
    if "ribosome_site_info" in js_info:
        rbs_info = js_info["ribosome_site_info"]
    else:
        raise Exception("Ribosome Site Info not found in js_info.")
    

    if feature_dict["feat_strand"] == 1:
        radius = js_info['circle_radius']
    else:
        radius = js_info['complementary_radius']

    cc = js_info['center_coordinates']

    
    """
    First, we find the center of the rbs circle we will make.
    """
    percent_center = rbs_info["percent_center"]
    relative_angle_to_t_center = (feature_dict['plasmid_percentage'] * \
            (percent_center/100))*(math.pi * 2)

    starting_angle = feature_dict['angle_start'] 
    rbs_symbol_center_angle = starting_angle + relative_angle_to_t_center
    rbs_circle_center = [cc[0] + radius*(math.cos(rbs_symbol_center_angle)),cc[1] + radius*(math.sin(rbs_symbol_center_angle))]
    
    #Notice, here we add some distance from center of plasmid circle to the center of the rbs circle in order
    #  to get the circle to sit on top of the plasmid visual, and not inside it.
    extension_length = js_info['circle_line_width']/2
    rbs_circle_center = line_extension_coordinates(cc,rbs_circle_center,"pixels", extension_length)

    #We add math.pi/2 to make the angle perpendicular to circle
    start_angle = get_angle_from_point(rbs_circle_center, cc) + (math.pi/2)

    js_object = {
            "type": "rbs",
            "radius": rbs_info["radius"],
            "feat_name": feature_dict['feat_name'],
            "circle_center": rbs_circle_center,
            "start_angle": start_angle,
            "end_angle": start_angle + math.pi,
            "border_color": rbs_info["border_color"],
            "internal_color": rbs_info["internal_color"],
            "border_width": rbs_info["border_width"],
            }

    return js_object


def calculate_cds_feature(feature_dict, config_dict):
    js_info = config_dict["js_info"]

    """
    The CDS visual will look like an arrow head ending at the end of the CDS.
    In order to draw this, we need 6 variables. The variables represent:
        var_a: point on plasmid map that outer arrow starts.
        var_b: point outside plasmid map that outer arrow has its peak.
        var_c: point on plasmid map, same as end of cds, where arrow ends.
        var_d: inner complement to a.
        var_e: inner complement to b.
        var_f: inner complement to c.
    """
    logging.debug("Making CDS Visual")

    if "cds_info" in js_info:
        cds_info = js_info["cds_info"]
    else:
        raise Exception("CDS Info not found in js_info.")

    


    if feature_dict["feat_strand"] == 1:
        complement_bool = False
        radius = js_info['circle_radius']
    else:
        radius = js_info['complementary_radius']
        complement_bool = True

    cc = js_info['center_coordinates']




    
    """
    First, we find the start of the CDS arrow we will make.
    """
    percent_start = cds_info["percent_start"]
    if complement_bool:
        percent_start = 100 - percent_start
        arrow_end = feature_dict['point_start']
    else:
        arrow_end = feature_dict['point_end']

    relative_angle_to_t_center = (feature_dict['plasmid_percentage'] * (percent_start/100))*(math.pi * 2)

    starting_angle = get_angle_from_point(feature_dict['point_start'],cc)
    cds_symbol_start_angle = starting_angle + relative_angle_to_t_center
    cds_symbol_start_point = [cc[0] + radius*(math.cos(cds_symbol_start_angle)),cc[1] + radius*(math.sin(cds_symbol_start_angle))]
    var_a = line_extension_coordinates(cc,cds_symbol_start_point,"pixels", js_info['circle_line_width']/2)
    var_b = line_extension_coordinates(cc,var_a,"pixels",cds_info["arrow_height"])
    var_c = line_extension_coordinates(cc,arrow_end,"pixels", js_info['circle_line_width']/2)
    var_d = line_extension_coordinates(var_a, cds_symbol_start_point,"pixels", js_info['circle_line_width']/2)
    var_e = line_extension_coordinates(var_a,var_d,"pixels",cds_info["arrow_height"])
    var_f = line_extension_coordinates(var_c, arrow_end, "pixels", js_info['circle_line_width']/2)

    js_object = {
        "type": "cds",
        "feat_name": feature_dict['feat_name'],
        "internal_color": feature_dict["feat_color"], 
        "a": var_a ,
        "b": var_b,
        "c": var_c,
        "d": var_d,
        "e": var_e,
        "f": var_f,
    }

    return js_object

