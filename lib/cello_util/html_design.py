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



"""
Inputs:
    full_path_to_folder: (str) The path to the folder containing all the output files from Cello.
Outputs:
    out_files_dict: (dict)
        wiring_svg: (str) The full path to the wiring svg file.
        wiring_svg_diagram_found: (bool) True if found, False if not.
        wiring_png_file: (str) The full path to the wiring png file.
        png_diagram_found: (bool) True if found, False if not
        truth_png_files: (list) The full paths to the png files.
        truth_png_files_found: (bool) True if found, False if not.
        all_return_files: (list of str) The full paths to all the files.

"""
def extract_files_from_folder(results_dir):

    #Getting files to sort through:
    all_files = os.listdir(results_dir)

    out_files_dict = dict()

    #Extracting Circuit Diagram - filename should end with 'wiring_grn.svg':
    wiring_svg_files = []
    wiring_png_files = []
    truth_png_files = []
    wiring_svg_found = False
    wiring_png_files_found = False
    truth_png_files_found = False
    for f in all_files:
        if "wiring_agrn.svg" in f:
            wiring_svg_files.append(os.path.join(results_dir,f))
            wiring_svg_found = True
        elif "truth.pdf" in f:
            truth_png_files.append(os.path.join(results_dir,f))
            truth_png_files_found = True
        elif "wiring_agrn.png" in f:
            wiring_png_files.append(os.path.join(results_dir,f))
            wiring_png_files_found = True
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

    out_files_dict['truth_png_files_found'] = truth_png_files_found
    out_files_dict['truth_png_files'] = truth_png_files
    all_output_files = wiring_svg_files + truth_png_files + wiring_png_files
    out_files_dict['all_return_files'] = all_output_files

    return out_files_dict


"""
Inputs:
    results_dir: (str) The path to the folder containing all the output files from Cello.
    scratch_dir: (str) The path to the scratch directory
Outputs:
    html_result_dict: (dict) 
        "result_file_path" : (str) file path to resulting html file. 
        "output_directory": (str) path to resulting output_directory in scratch dir.
            }

"""
def build_html(results_dir, scratch_dir):
    """
    There is a variable amount of png files we need to return to the user. Should we enforce a limit?
    """
    logging.info("Starting to generate html report.")
    
    out_files_dict = extract_files_from_folder(results_dir)

    output_directory = os.path.join(scratch_dir, "HTML_Report")
    os.makedirs(output_directory, exist_ok=True)
    result_file_path = os.path.join(output_directory, 'report.html')
    
    html_template = open(os.path.join(os.path.dirname(__file__), "report_template.html"), "r")
    html_file_str = html_template.read()
    html_template.close()
    
    path_to_wiring_png_file = out_files_dict['wiring_png_file']

    png_diagram_name = get_name_from_path(path_to_wiring_png_file,"wiring_png")
    png_display_name = 'Wiring Diagram'
    
    shutil.copy2(os.path.join(results_dir, png_diagram_name),
    os.path.join(output_directory, png_diagram_name))
    visualization_content = ''
    visualization_content += '<div class="gallery">'
    visualization_content += '<a target="_blank" href="{}">'.format(png_diagram_name)
    visualization_content += '<img src="{}" '.format(png_diagram_name)
    visualization_content += 'alt="{}" width="600" height="400">'.format(
    png_display_name)
    visualization_content += '</a><div class="desc">{}</div></div>'.format(
    png_display_name)

    #For each truth graph make one of these
    truth_png_files = out_files_dict['truth_png_files']

    #We set the upper limit of different png files to be 10
    k = min(len(truth_png_files), 10)

    for i in range(k):
        truth_graph_path = truth_png_files[i]

        truth_graph_name = get_name_from_path(truth_graph_path,"truth")
        truth_graph_display_name = 'Truth Graph ' + str(i)

        shutil.copy2(os.path.join(results_dir, truth_graph_name),
        os.path.join(output_directory, truth_graph_name))

        visualization_content += '<div class="gallery">'
        visualization_content += '<a target="_blank" href="{}">'.format(truth_graph_name)
        visualization_content += '<img src="{}" '.format(truth_graph_name)
        visualization_content += 'alt="{}" width="600" height="400">'.format(
        truth_graph_display_name)
        visualization_content += '</a><div class="desc">{}</div></div>'.format(
        truth_graph_display_name)


    html_file_str = html_file_str.replace('<p>Visualization_Content</p>', visualization_content)

    f = open(result_file_path, "w")
    f.write(html_file_str)
    f.close()

    html_result_dict = {
        "result_file_path" : result_file_path, 
        "output_directory": output_directory
            }

    return html_result_dict



"""
Inputs:
    filepath: (str) Full path to the file
    typ: (str) Type of file: 'wiring_png' or 'truth'
"""
def get_name_from_path(filepath, typ):

    #For now we just return the filename
    return filepath.split('/')[-1]












