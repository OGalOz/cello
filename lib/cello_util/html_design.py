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
        wiring_grn_svg: (str) The full path to the file containing the wiring svg file.
"""
def extract_files_from_folder(full_path_to_folder):

    #Getting files to sort through:
    all_files = os.listdir(full_path_to_folder)

    out_files_dict = dict()

    #Extracting Circuit Diagram:
    wiring_grn_files = []
    wiring_grn_found = False
    for f in all_files:
        if f[-15:] == "wiring_agrn.svg":
            wiring_grn_files.append(os.path.join(full_path_to_folder,f))

    if len(wiring_grn_files) > 0:
        logging.info("Found wiring_grn_files: ")
        wiring_grn_found = True
        for i in range(len(wiring_grn_files)):
            logging.debug(wiring_grn_files[i])
    else:
        logging.critical("Could not find a wiring_agrn file.")

    if wiring_grn_found:
        if len(wiring_grn_files) == 1:
            out_files_dict['wiring_grn_svg'] = wiring_grn_files[0]
        else:
            raise Exception("Multiple wiring grn files found.")


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

    













