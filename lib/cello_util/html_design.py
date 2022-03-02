#python3

"""
This file takes the output of Cello and prints it out to a nice layout.
Important Information to Present:
    Circuit diagram (wire diagram with blocks) - the main circuit diagram file is:
        wiring_grn.svg
    Plasmid maps
    Expected input range and output range
    List of genetic components used to build the plasmid



Notes:
The SVG files should each be their own page.
xfer.png files represent the Hill function - some have wiring included.
srPr gate represents some kind of output measurement.
The PDF and the png files are replicates, you can leave out one and keep the other.

"""

import os
import logging
import shutil
import traceback
import json
from cello_util.plasmid_map.cello_plasmid_mapper import get_cello_plasmid_map_div 




"""
Inputs:
    results_dir: (str) The path to the folder containing all the output files
        from Cello.
    scratch_dir: (str) The path to the scratch directory
    user_output_name: (str) The user's output name
    config_info: (dict) Information regarding the html
        base_plasmid_info: (str) fixed vocab - "none", "custom" etc.
Outputs:
    html_result_dict: (dict) 
        "result_file_path" : (str) file path to resulting html file. 
        "output_directory": (str) path to resulting output_directory in scratch
            dir.

"""
def build_html(results_dir, scratch_dir, user_output_name, config_info):
    """
    There is a variable amount of png files we need to return to the user. 
    Should we enforce a limit? (10 currently)
    """
    logging.info("Starting to generate html report.")

    output_directory = os.path.join(scratch_dir, "HTML_Report")
    config_info["scratch_dir"] = scratch_dir
    os.makedirs(output_directory, exist_ok=True)
    #The following function adds png files and javascript files.
    update_static_files(output_directory)

    try:
    
        out_files_dict = extract_files_from_folder(results_dir)

        num_plasmids_created = out_files_dict["num_plasmids_created"]
        overview_content = '<h5> ' + str(num_plasmids_created) + \
        " Plasmids Created by Cello. Visualizations provided in the other tabs.</h5>"

        result_file_path = os.path.join(output_directory, 'report.html')
        
        html_template = open(os.path.join(os.path.dirname(__file__), 
            "report_template.html"), "r")
        html_file_str = html_template.read()
        html_template.close()
        
        path_to_wiring_png_file = out_files_dict['wiring_png_file']

        png_diagram_name = get_name_from_path(path_to_wiring_png_file,
                "wiring_png")
        png_display_name = 'Wiring Diagram'
        #We get the wiring link file from the svg file:
        if out_files_dict["wiring_svg_diagram_found"] == True:
            diagram_link = get_name_from_path(out_files_dict['wiring_svg'])
            shutil.copy2(os.path.join(results_dir, diagram_link),
            os.path.join(output_directory, diagram_link))

        else:
            diagram_link = png_diagram_name
        
        shutil.copy2(os.path.join(results_dir, png_diagram_name),
        os.path.join(output_directory, png_diagram_name))
        visualization_content = ''
        visualization_content += '<div class="gallery">'
        visualization_content += '<a target="_blank" href="{}">'.format(diagram_link)
        visualization_content += '<img src="{}" '.format(png_diagram_name)
        visualization_content += 'alt="{}" width="600" height="400">'.format(
        png_display_name)
        visualization_content += '</a><div class="desc">{}</div></div>'.format(
        png_display_name)

        #For each truth graph make one of these
        truth_png_files = out_files_dict['truth_png_files']
        truth_pdf_files = out_files_dict['truth_pdf_files']
        

        #We set the upper limit of different png files to be 10
        k = min(len(truth_png_files), 10)

        for i in range(k):
            truth_graph_dict = truth_png_files[i]

            truth_graph_path = truth_graph_dict['file_path']
            truth_gene_name = truth_graph_dict['gene_name']

            truth_graph_name = get_name_from_path(truth_graph_path,"truth")
            truth_graph_display_name = 'RPU Graph for ' + truth_gene_name

            shutil.copy2(os.path.join(results_dir, truth_graph_name),
            os.path.join(output_directory, truth_graph_name))

            truth_graph_link = truth_graph_name
            #Getting PDF file as a link:
            for i in range(len(truth_pdf_files)):
                pdf_file_dict = truth_pdf_files[i]
                pdf_gene = pdf_file_dict['gene_name']
                if truth_gene_name == pdf_gene:
                    truth_graph_link = get_name_from_path(
                            pdf_file_dict['file_path'] , "truth")
                    shutil.copy2(os.path.join(results_dir, truth_graph_link),
                    os.path.join(output_directory, truth_graph_link))
                    break
            visualization_content += '<div class="gallery">'
            visualization_content += '<a target="_blank" href="{}">'.format(truth_graph_link)
            visualization_content += '<img src="{}" '.format(truth_graph_name)
            visualization_content += 'alt="{}" width="600" height="400">'.format(
            truth_graph_display_name)
            visualization_content += '</a><div class="desc">{}</div></div>'.format(
            truth_graph_display_name)


        #Here add plasmid visualization step - MAPS:
        gbk_files = out_files_dict['gbk_files']
        
        try:
            plasmid_vis_info = config_info
            gb_plasmid_divs_str = make_plasmid_divs(gbk_files, user_output_name,
                    plasmid_vis_info)
        except:
            logging.critical("Failed to make plasmid_divs")
            gb_plasmid_divs_str = ""
            logging.critical(traceback.print_exc())
        try:
            gb_plasmid_buttons_str = make_plasmid_buttons(gbk_files)
        except:
            gb_plasmid_buttons_str = ""
            logging.critical(traceback.print_exc())

        html_file_str = html_file_str.replace('<p>Visualization_Content</p>', visualization_content)
        html_file_str = html_file_str.replace('<p>Overview_Content</p>',overview_content)
        html_file_str = html_file_str.replace('{New_Plasmid_Divs}', gb_plasmid_divs_str)
        html_file_str = html_file_str.replace('{New_Plasmid_Buttons}', gb_plasmid_buttons_str)


        f = open(result_file_path, "w")
        f.write(html_file_str)
        f.close()


    except:
        logging.critical("Creation of HTML file failed at some point " + \
                        "in the function build_html (html_design) .")
        result_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"error.html")

    html_result_dict = {
        "result_file_path" : result_file_path, 
        "output_directory": output_directory
            }

    return html_result_dict





"""
Inputs:
    full_path_to_folder: (str) The path to the folder containing all the output 
        files from Cello.
Outputs:
    out_files_dict: (dict)
        wiring_svg: (str) The full path to the wiring svg file.
        wiring_svg_diagram_found: (bool) True if found, False if not.
        wiring_png_file: (str) The full path to the wiring png file.
        png_diagram_found: (bool) True if found, False if not
        truth_png_files: (list) List of dicts, where each contains name of gene 
            and the full path to the png files.
            truth_dict: (dict)
                gene_name: (str) Name of gene
                file_path: (str) Path to file
        truth_png_files_found: (bool) True if found, False if not.
        truth_pdf_files: (list) List of dicts, where each contains name of gene 
            and the full path to the pdf files.
            truth_dict: (dict)
                gene_name: (str) Name of gene
                file_path: (str) Path to file
        truth_pdf_files_found: (bool) True if found, False if not.
        gbk_files: (list) List of all paths to gbk files.
        all_return_files: (list of str) The full paths to all the files.

"""
def extract_files_from_folder(results_dir):

    #Getting files to sort through:
    all_files = os.listdir(results_dir)

    out_files_dict = dict()

    #Extracting Circuit Diagram - filename should end with 'wiring_grn.svg':
    wiring_svg_files = []
    wiring_png_files = []
    truth_pdf_files = []
    truth_png_files = []
    gbk_files = []
    wiring_svg_found = False
    wiring_png_files_found = False
    truth_png_files_found = False
    truth_pdf_files_found = False
    plasmid_ape_files_created = 0
    for f in all_files:
        if "wiring_agrn.svg" in f:
            wiring_svg_files.append(os.path.join(results_dir,f))
            wiring_svg_found = True
        elif "truth.png" in f:
            truth_gene_name = get_gene_name_for_truth_graph(f)
            truth_file_info = {"gene_name" : truth_gene_name, 'file_path': f}
            truth_png_files.append(truth_file_info)
            truth_png_files_found = True
        elif "truth.pdf" in f:
            truth_pdf_name = get_gene_name_for_truth_graph(f)
            truth_file_info = {"gene_name" : truth_pdf_name, 'file_path' : f}
            truth_pdf_files.append(truth_file_info)
            truth_pdf_files_found = True
        elif "wiring_agrn.png" in f:
            wiring_png_files.append(os.path.join(results_dir,f))
            wiring_png_files_found = True
        elif ".ape" in f:
            plasmid_ape_files_created += 1
        elif ".gbk" in f:
            gbk_files.append(os.path.join(results_dir,f))
    if wiring_svg_found:
        out_files_dict['wiring_svg'] = wiring_svg_files[0]
        if len(wiring_svg_files) > 1:
            logging.critical("Multiple wiring svg files found- Returning the first one.")
    if wiring_png_files_found:
        out_files_dict['wiring_png_file'] = wiring_png_files[0]
        if len(wiring_png_files) > 1:
            logging.critical("Multiple wiring grn files found- Returning the first one.")

    out_files_dict['wiring_svg_diagram_found'] = wiring_svg_found
    out_files_dict['png_diagram_found'] = wiring_png_files_found
    out_files_dict['truth_pdf_files_found'] = truth_pdf_files_found
    out_files_dict['truth_pdf_files'] = truth_pdf_files
    out_files_dict['truth_png_files_found'] = truth_png_files_found
    out_files_dict['truth_png_files'] = truth_png_files
    all_output_files = wiring_svg_files + truth_png_files + wiring_png_files
    out_files_dict['all_return_files'] = all_output_files
    out_files_dict["num_plasmids_created"] = plasmid_ape_files_created
    out_files_dict["gbk_files"] = gbk_files

    return out_files_dict



"""
Inputs:
    gbk_files: (list) A list of full paths to the gbk files.
    user_output_name: (str)
    plasmid_vis_info: (dict)
        base_plasmid_info: (str) none, custom, etc
Output:
    plasmid_divs_str: (str) A string to insert into report html.
"""
def make_plasmid_divs(gbk_files, user_output_name, plasmid_vis_info):

    #We place basic parameters on the design of the plasmid map:
    base_div_html_fp = os.path.join(os.path.dirname(__file__), 
            "plasmid_map/div_svg_template.html")
    config_filepath = os.path.join(os.path.dirname(__file__), 
            "plasmid_map/config.json")
    with open(config_filepath, "r") as cf:
        config_dict = json.loads(cf.read())
 
    if plasmid_vis_info["base_plasmid_info"] == "none":
        #If there are expected to be big CDs, we make the arrow smaller.
        #Instead of 85 percent, it will be 96 percent
        config_dict['js_info']['cds_info']['percent_start'] = 96 

    plasmid_divs_str = ''
    #We set a maximum number of files to be made (6):
    k = min(len(gbk_files), 6)
    for i in range(k):
        gb_file = gbk_files[i]
        uniq_dict = {
            "file_num": i,
            "uniq_id": "prfx_" + str(i),
            "svg_id": "svg-" + str(i),
            "svg_name": "svg_" + str(i),
            "tmp_name": "plasmid_tmp_" + str(i),
            "scratch_dir": plasmid_vis_info["scratch_dir"]


                }
        try:
            plasmid_map_dict = get_cello_plasmid_map_div(gb_file, 
                    base_div_html_fp, config_filepath, uniq_dict)
        except:
            logging.critical("FAILED TO MAKE VISUALIZATION: {}".format(gb_file))
            logging.critical(traceback.print_exc())
            break
        plasmid_map_div_html = plasmid_map_dict["complete_div_str"]
        plasmid_map_name = plasmid_map_dict["plasmid_name"]
        plasmid_map_div_html = plasmid_map_div_html.replace("Plasmid_Name_Here",
                user_output_name + "_" + plasmid_map_name)
        plasmid_map_div_html = plasmid_map_div_html.replace('id="Plasmid_Div_Id_Here"',
                'id="Plasmid_Map_' + str(i+1) + '"')
        plasmid_map_div_html = plasmid_map_div_html.replace('SVG_ID_HERE','my_svg_' + \
                str(i+1))


        plasmid_divs_str += plasmid_map_div_html + '\n\n\n'

    return plasmid_divs_str


"""
Inputs:
    HTML_Report_dir: (str) The path to the directory
"""
def update_static_files(HTML_Report_dir):
    #Vars (Paths):
    delete_img = "/kb/module/static/delete_img.png"
    reset_img = "/kb/module/static/reset_img.png" 
    js_files = [ "/kb/module/static/js/d3-dispatch.v1.min.js",
        "/kb/module/static/js/d3-drag.v1.min.js",
        "/kb/module/static/js/d3-selection.v1.min.js",
        "/kb/module/static/js/d3.min.js"
            ]
    sh_ret = shutil.copyfile(delete_img, os.path.join(HTML_Report_dir, 
            "delete_img.png"))
    logging.debug("NEW FILE COPY: {}".format(sh_ret))
    sh_ret = shutil.copyfile(reset_img, os.path.join(HTML_Report_dir, 
            "reset_img.png"))
    logging.debug("NEW FILE COPY: {}".format(sh_ret))

    for js_file in js_files:
        js_file_name = js_file.split('/')[-1]
        shutil.copyfile(js_file, os.path.join(HTML_Report_dir, js_file_name))






"""
Inputs:
    gbk_files: (list) A list of full paths to the gbk files.

Output:
    plasmid_buttons_str: (str) A string to insert into report html.
"""
def make_plasmid_buttons(gbk_files):
    plasmid_buttons_str = ''
    k = min(len(gbk_files), 6)
    for i in range(k):
        new_id = "Plasmid_Map_" + str(i+1)
        new_button = '<button class="tablinks" onclick="openTab(event, ' + \
                "'" + new_id + "')" + \
        '">' + new_id.replace("_", " ") + "</button>\n"
        plasmid_buttons_str += new_button

    return plasmid_buttons_str



"""
Inputs:
    filepath: (str) Full path to the file
    typ: (str) Type of file: 'wiring_png' or 'truth'
"""
def get_name_from_path(filepath, typ = None):

    #For now we just return the filename
    return filepath.split('/')[-1]


"""
Input: 
    filename: (str) Just the filename (not filepath). Getting name of gene from cello's production
    of a filename. Normally it looks like: job_1576197897501_A000_BFP_truth.png, we need "BFP" so we
     split by "_" and take the fourth index until the last index

"""
def get_gene_name_for_truth_graph(filename):

    return "".join((filename.split("_"))[3:-1])



def html_design_test():
    this_dir = os.path.dirname(os.path.realpath(__file__))
    gbk_files = [os.path.join(this_dir,"tst/job_1581723951170_A000_plasmid_circuit_P000.gbk"), 
            os.path.join(this_dir,"tst/job_1581723951170_A000_plasmid_output_P000.gbk")]
    user_output_name = ""
    plasmid_vis_info = {
        "base_plasmid_info": "custom"
            }
    gb_plasmid_divs_str = make_plasmid_divs(gbk_files, user_output_name, plasmid_vis_info)

#if __name__ == "__main__":
#    html_design_test()








