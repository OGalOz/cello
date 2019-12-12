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



"""
Inputs:
    full_path_to_folder: (str) The path to the folder containing all the output files from Cello.
Outputs:
    out_files_dict: (dict)
        wiring_grn_svg: (str) The full path to the wiring svg file.
        wiring_diagram_found: (bool) True if found, False if not.
        png_files: (list) The full paths to the png files.
        png_files_found: (bool) True if found, False if not.
        all_return_files: (list of str) The full paths to all the files.


"""
def extract_files_from_folder(full_path_to_folder):

    #Getting files to sort through:
    all_files = os.listdir(full_path_to_folder)

    out_files_dict = dict()

    #Extracting Circuit Diagram - filename should end with 'wiring_grn.svg':
    wiring_grn_files = []
    png_files = []
    wiring_grn_found = False
    png_files_found = False
    for f in all_files:
        if "wiring_agrn.svg" in f:
            wiring_grn_files.append(os.path.join(full_path_to_folder,f))
        elif "truth.png" in f:
            png_files.append(os.path.join(full_path_to_folder,f))
    if len(wiring_grn_files) > 0:
        logging.info("Found wiring_agrn_files: ")
        wiring_grn_found = True
        for i in range(len(wiring_grn_files)):
            logging.debug(wiring_grn_files[i])
    else:
        logging.critical("Could not find a wiring_grn file.")
        out_files_dict['wiring_diagram_found'] = False

    if wiring_grn_found:
        if len(wiring_grn_files) == 1:
            out_files_dict['wiring_grn_svg'] = wiring_grn_files[0]
            out_files_dict['wiring_diagram_found'] = True
        else:
            logging.critical("Multiple wiring grn files found- Returning the first one.")
            out_files_dict['wiring_grn_svg'] = wiring_grn_files[0]
            out_files_dict['wiring_diagram_found'] = True

    if len(png_files) == 0:
        logging.critical("No png files found.")
    else:
        png_files_found = True
    
    out_files_dict['png_files_found'] = png_files_found
    out_files_dict['png_files'] = png_files
    all_files = wiring_grn_files + png_files
    out_files_dict['all_return_files'] = all_files

    return out_files_dict


"""
Inputs:
    full_path_to_folder: (str) The path to the folder containing all the output files from Cello.
Outputs:
    out_files_dict (dict):
        wiring_grn_svg: (str) The full path to the file containing the wiring svg file.
"""
def build_html(full_path_to_folder):
    """
    For now this file doesn't do much since we are only returning the already-created SVG
    """

    out_files_dict = extract_files_from_folder(full_path_to_folder)

    return out_files_dict    

    













