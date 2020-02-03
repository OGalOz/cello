"""
This program takes a genbank file, as provided by KBase, and creates
a UCF file, as described by Cello, to use as an input to Cello.
The UCF is a genbank file. Follows format described here:
    https://science.sciencemag.org/content/sci/suppl/2016/03/30/352.6281.aac7341.DC1/Nielsen.SM.pdf 
    on page 58

The entire file is a list of objects, which looks like this:
 0. header [req]
 1. measurement_std [req]

 2. logic_constraints [req]

 3-N. motif_library (there are many of these) [optional]

 N+1 - M. gates [req] ( many of these, but fewer than motif_library)
 
 M+1 - Q. response_functions [req] ( many of these, same amount as gates)
 
 Q+1 - P. gate_parts [req] ( many of these, same amount as gates)
 
 P+1 - S. parts [req](many of these, more than gates, but less than motif_library)
 
 S+1 - T. gate_toxicity (many of these, same amount as gates) [optional]
 
 T+1 - U. gate_cytometry (many of these, same amount as gates) [optional]
 
 U+1. eugene_rules [optional]
 
 U+2. genetic_locations [optional] (if omitted, the output DNA sequence will contain the circuit components only, and the user will be responsible for deciding and implementing the genetic context of the circuit design. If used, both sensor module and circuit module are required, output module is optional.)

* We create a new header, measurement_std. 
* We copy the logic_constraints, motif_library, gates, response_functions, gate_parts, and parts from an existing UCF file.
* We either build a new genetic_locations dict or copy an existing one and add it to the new UCF.




"""

import sys
import getopt
import os
import datetime
import json
import logging
from Bio import SeqIO

"""
The following is the main function of this file.
Inputs:
    gb_ucf_params: (dict)
        
        Required:
        config_dict: (dict) the dict which contains config info.
            genetic_loc_folder_path: (str) Path to the folder containing the existing genetic location dicts.
            use_existing_genetic_loc: [req] (str) either "no", or the name of an existing genetic_location dict in the right dir.
            msd_gb_bool: [req] (bool) True if new measurement standard
            op_gb_bool: (bool) True if new output plasmid genbank file
            op_mod_loc: (int) Output module location in base pair
            cr_gb_bool: (bool) True if new circuit plasmid genbank file
            cr_mod_loc: (int) Location of circuit module.
            sn_gb_bool: [req] (bool) True if sensor module included.
            optional:
                sn_mod_loc: (int) Location of sensor module.
                sn_mod_gb_name: (str) Name of the sensor module
                sn_mod_json_fp: (str) File path to sensor module json if it exists.

        bs_ucf_fp: (str) the filepath to the base UCF we are using.
        output_fp: (str) Output filepath

        Optional:
        msd_gb_fp: (str) measurement standard genbank filepath
        op_gb_fp: (str)  output plasmid genbank filepath
        cr_gb_fp: (str) circuit plasmid genbank filepath
        sn_gb_fp: (Str) Sensor module genbank filepath

"""
def convert_gb_to_ucf(gb_ucf_params):

    new_json_ucf_list = []

    #Reading params
    config_dict = gb_ucf_params["config_dict"]
    if config_dict["msd_gb_bool"] == True:
        msd_gb_fp = gb_ucf_params["msd_gb_fp"]
    else:
        msd_gb_fp = ""
    if config_dict["op_gb_bool"] == True:
        op_gb_fp = gb_ucf_params["op_gb_fp"]
    else:
        op_gb_fp = ""
    if config_dict["cr_gb_bool"] == True:
        cr_gb_fp = gb_ucf_params["cr_gb_fp"]
    else:
        cr_gb_fp = ""

    if config_dict["sn_gb_bool"] == True:
        sn_gb_fp = gb_ucf_params["sn_gb_fp"]
    else:
        sn_gb_fp = ""

    #The base UCF is the UCF from which we take the collections we aren't creating.
    bs_ucf_fp = gb_ucf_params["bs_ucf_fp"]
    g = open(bs_ucf_fp, "r")
    bs_ucf_filestr = g.read()
    g.close()
    bs_ucf_list = json.loads(bs_ucf_filestr)

    output_fp = gb_ucf_params["output_fp"]


    #Building new UCF

    #Header - Required
    header_dict = header(config_dict)
    new_json_ucf_list.append(header_dict)
    
    #Measurement Standard - Required
    #We copy the measurement standard from an existing UCF file.
    # - the one with plasmid: pAN801star__LacI
    measurement_std_dict = measurement_std(config_dict, bs_ucf_list)
    new_json_ucf_list.append(measurement_std_dict)

    
    #Logic Constraints - Required
    logic_constraints_dict = logic_constraints(bs_ucf_list)
    new_json_ucf_list.append(logic_constraints_dict)

    #Motif library - Optional
    motif_lib_dict = motif_library(bs_ucf_list)
    motif_lib_list = motif_lib_dict["motif_lib_list"]
    next_index = motif_lib_dict["next_index"]
    new_json_ucf_list = new_json_ucf_list + motif_lib_list

    #Gates - required
    gates_dict = gates(bs_ucf_list, next_index)
    gates_list = gates_dict["gates_list"]
    next_index = gates_dict["next_index"]
    new_json_ucf_list = new_json_ucf_list + gates_list

    #Response Functions - req
    response_functions_dict = response_functions(bs_ucf_list, next_index)
    response_functions_list = response_functions_dict["response_functions_list"]
    next_index = response_functions_dict["next_index"]
    new_json_ucf_list = new_json_ucf_list + response_functions_list


    #Gate Parts - req
    gate_parts_dict = gate_parts(bs_ucf_list, next_index)
    gate_parts_list = gate_parts_dict["gate_parts_list"]
    next_index = gate_parts_dict["next_index"]
    new_json_ucf_list = new_json_ucf_list + gate_parts_list

    #Parts - req
    parts_dict = parts(bs_ucf_list, next_index)
    parts_list = parts_dict["parts_list"]
    next_index = parts_dict["next_index"]
    new_json_ucf_list = new_json_ucf_list + parts_list

    
    #Genetic Locations - Optional
    # (This part of the program is more intensive)
    genetic_locations_dict = genetic_locations(config_dict,gb_ucf_params, new_json_ucf_list, bs_ucf_list)
    new_json_ucf_list.append(genetic_locations_dict)


    output_fp = gb_ucf_params['output_fp']
    json_str = json.dumps(new_json_ucf_list, indent=4)
    f = open(output_fp, "w")
    f.write(json_str)
    f.close()



    return output_fp



"""
Inputs:
    config_dict: (dict) The config file converted to a dictionary.
Outputs:
    header_dict: (dict) The object that represents the header part of the UCF file.
"""
def header(config_dict):
    header_dict = {'collection': 'header'}
    
    #version
    header_dict['version'] = 'KBase-placeholder'

    #date
    d = datetime.datetime.today()
    header_dict['date'] = "{}-{}-{}".format(d.year, d.month, d.day)

    #author
    header_dict['author'] = ["KBase-placeholder"]


    #organism
    header_dict['organism'] = "Unknown"


    header_dict["genome"] = "KBase-placeholder"

    header_dict['media'] = "KBase-placeholder"

    header_dict["media"] = "KBase-placeholder"

    #temperature (in degrees Celsius)
    #Unsure of the effects of this, keeping it at 37 for now.
    header_dict['temperature'] = "37"

    #growth
    header_dict['growth'] = "KBase-placeholder"

    return header_dict




"""
Inputs:
    config_dict: (dict) Dictionary containing info.
    bs_ucf_list: (list) The list of the entire base ucf file.


"""
def measurement_std(config_dict, bs_ucf_list):
    msd = {"collection": "measurement_std"}

    if config_dict["msd_gb_bool"] == True:
        #Create new msd
        g = open(msd_gb_fp, "r")
        genbank_filestr = g.read()
        g.close()

        #signal carrier units are measured in Relative Expression Units
        msd["signal_carrier_units"] = "RPU"
        
        msd["plasmid_description"] = "KBase-placeholder"
    
        #all lines of the Genbank file (not shown) for the measurement standard plasmid
        msd['plasmid_sequence'] = genbank_filestr.split("\n")
    
        msd["normalization_instructions"] = "KBase-placeholder"

    else:
        base_msd = bs_ucf_list[1]
        if base_msd["collection"] != "measurement_std":
            raise Exception("Base UCF file does not have regular format. Review the base UCF file.")
        msd = base_msd



    return msd




#We borrow the logic constraints collection from the base ucf dict
def logic_constraints(bs_ucf_list):
    logic_constraints_dict = bs_ucf_list[2]

    if logic_constraints_dict["collection"] != "logic_constraints":
        raise Exception("Base UCF file does not have regular format. Review the base UCF file.")

    return logic_constraints_dict

    
def motif_library(bs_ucf_list):
    
    still_motif_library = True
    new_motif_library_list = []
    i = 3
    l = len(bs_ucf_list)
    while still_motif_library and i < l:
        current_motif_library_dict = bs_ucf_list[i]
        if current_motif_library_dict["collection"] != "motif_library":
            still_motif_library = False
        else:
            new_motif_library_list.append(current_motif_library_dict)
            i += 1

    if i == 3:
        raise Exception("No motif_library dicts found in base UCF file")

    motif_dict = {
            "motif_lib_list": new_motif_library_list,
            "next_index": i
            }

    return motif_dict



def gates(bs_ucf_list, next_index):

    still_gates = True
    new_gates_list = []
    i = next_index
    l = len(bs_ucf_list)
    while still_gates and i < l:
        current_gates_dict = bs_ucf_list[i]
        if current_gates_dict["collection"] != "gates":
            still_gates = False
        else:
            new_gates_list.append(current_gates_dict)
            i += 1

    if i == next_index:
        raise Exception("No gates dicts found in base UCF file")

    gates_dict = {
            "gates_list": new_gates_list,
            "next_index": i
            }
    if len(new_gates_list) == 0:
        raise Exception("Base UCF file may contain no gates, or otherwise different ordering in the file.")   

    return gates_dict
    

def response_functions(bs_ucf_list, next_index):

    still_response_functions = True
    new_response_functions_list = []
    i = next_index
    l = len(bs_ucf_list)
    while still_response_functions and i < l:
        current_response_functions_dict = bs_ucf_list[i]
        if current_response_functions_dict["collection"] != "response_functions":
            still_response_functions = False
        else:
            new_response_functions_list.append(current_response_functions_dict)
            i += 1

    if i == next_index:
        raise Exception("No response_functions dicts found in base UCF file")

    response_functions_dict = {
            "response_functions_list": new_response_functions_list,
            "next_index": i
            }
    if len(new_response_functions_list) == 0:
        raise Exception("Base UCF file may contain no response_functions, or otherwise different ordering in the file.")   

    return response_functions_dict



def gate_parts(bs_ucf_list, next_index):

    still_gate_parts = True
    new_gate_parts_list = []
    i = next_index
    l = len(bs_ucf_list)
    while still_gate_parts and i < l:
        current_gate_parts_dict = bs_ucf_list[i]
        if current_gate_parts_dict["collection"] != "gate_parts":
            still_gate_parts = False
        else:
            new_gate_parts_list.append(current_gate_parts_dict)
            i += 1

    if i == next_index:
        raise Exception("No gate_parts dicts found in base UCF file")

    gate_parts_dict = {
            "gate_parts_list": new_gate_parts_list,
            "next_index": i
            }
    if len(new_gate_parts_list) == 0:
        raise Exception("Base UCF file may contain no gate_parts, or otherwise different ordering in the file.")   

    return gate_parts_dict




def parts(bs_ucf_list, next_index):

    still_parts = True
    new_parts_list = []
    i = next_index
    l = len(bs_ucf_list)
    while still_parts and i < l:
        current_parts_dict = bs_ucf_list[i]
        if current_parts_dict["collection"] != "parts":
            still_parts = False
        else:
            new_parts_list.append(current_parts_dict)
            i += 1

    if i == next_index:
        raise Exception("No parts dicts found in base UCF file")

    parts_dict = {
            "parts_list": new_parts_list,
            "next_index": i
            }
    if len(new_parts_list) == 0:
        raise Exception("Base UCF file may contain no parts, or otherwise different ordering in the file.")   

    return parts_dict



def genetic_locations(config_dict, gb_ucf_params, new_json_ucf_list, bs_ucf_list):

    if config_dict["use_existing_genetic_loc"] == "no":
        genetic_locations_dict = {"collection": "genetic_locations"}
        locations_list = []

        #Output Module Info
        if "op_gb_fp" in gb_ucf_params:
            
            op_gb_fp = gb_ucf_params["op_gb_fp"]
            if not os.path.exists(op_gb_fp):
                raise Exception("Output Genbank File does not exist.")
            g = open(op_gb_fp, "r")
            op_gb_filestr = g.read()
            op_file_list = op_gb_filestr.split("\n")
            g.close()
            op_file_name = op_gb_fp.split("/")[-1]
            file_dict = {"file" : op_file_list, "name": op_file_name}
            locations_list.append(file_dict)
            op_mod_loc = config_dict['op_mod_loc']
            output_module_loc_dict = {"location_name" : op_file_name, "bp_start": op_mod_loc, "bp_end": op_mod_loc, "unit_conversion": 0.4}
            output_module_location_list = [output_module_loc_dict]
            genetic_locations_dict["output_module_location"] = output_module_location_list
        if "cr_gb_fp" in gb_ucf_params:
            
            cr_gb_fp = gb_ucf_params["cr_gb_fp"]

            if not os.path.exists(cr_gb_fp):
                raise Exception("Circuit Genbank File does not exist.")
            g = open(cr_gb_fp, "r")
            cr_gb_filestr = g.read()
            cr_file_list = cr_gb_filestr.split("\n")
            g.close()
            cr_file_name = cr_gb_fp.split("/")[-1]
            file_dict = {"file" : cr_file_list, "name": cr_file_name}
            locations_list.append(file_dict)
            cr_mod_loc = config_dict['cr_mod_loc']
            circuit_module_loc_dict = {"location_name" : cr_file_name, "bp_start": cr_mod_loc, "bp_end": cr_mod_loc}
            circuit_module_location_list = [circuit_module_loc_dict]
            genetic_locations_dict["circuit_module_location"] = circuit_module_location_list


        if "sn_gb_fp" in gb_ucf_params:
            
            sn_gb_fp = gb_ucf_params["sn_gb_fp"]

            if not os.path.exists(sn_gb_fp):
                raise Exception("Sensor Genbank File does not exist.")
            g = open(sn_gb_fp, "r")
            sn_gb_filestr = g.read()
            sn_file_list = sn_gb_filestr.split("\n")
            g.close()
            sn_file_name = sn_gb_fp.split("/")[-1]
            file_dict = {"file" : sn_file_list, "name": sn_file_name}
            locations_list.append(file_dict)
            sn_mod_loc = config_dict['sn_mod_loc']
            sensor_module_loc_dict = {"location_name" : sn_file_name, "bp_start": sn_mod_loc, "bp_end": sn_mod_loc}
            sensor_module_location_list = [sensor_module_loc_dict]
            genetic_locations_dict["sensor_module_location"] = sensor_module_location_list


        #Removing duplicates from locations_list:
        locations_list = remove_duplicates_from_locations_list(locations_list)

        genetic_locations_dict["locations"] = locations_list
    else:
        genetic_locations_json_fp = os.path.join(config_dict["genetic_loc_folder_path"], config_dict["use_existing_genetic_loc"])
        f = open(genetic_location_json_fp, "r")
        gl_filestr = f.read()
        f.close()
        genetic_locations_dict = json.loads(gl_filestr)


    return genetic_locations_dict
        
"""   
#locations_list: (list)
    file_dict: (dict)
        file: (list) List of genbank file
        name: (str) Name of genbank file
""" 
def remove_duplicates_from_locations_list(locations_list):
    logging.info("locations_list before removal of duplicates: ")
    logging.info([x["name"] for x in locations_list])
    names_list = []
    duplicates = []
    for i in range(len(locations_list)):
        crnt_name = locations_list[i]["name"]
        if crnt_name in names_list:
            duplicates.append(i)
        else:
            names_list.append(crnt_name)
    sorted(duplicates, reverse=True)
    for dup in duplicates:
        del locations_list[dup]

    logging.info("locations_list after removal of duplicates: ")
    logging.info([x["name"] for x in locations_list])

    return locations_list






def test():

    logging.basicConfig(level=logging.DEBUG)

    test_config_dict_1 = {
          'msd_gb_bool': True,      
          'op_gb_bool': True,
          'cr_gb_bool': True,
            }
    test_config_dict_2 = {
          'msd_gb_bool': False,       
          'op_gb_bool': False,
          'cr_gb_bool': False,
            }

    test_config_dict_3 = {
            'msd_gb_bool': False,
            'op_gb_bool': True,
            'op_mod_loc': 300,
            'cr_gb_bool': True,
            'cr_mod_loc': 100,
            'sensor_mod_bool': False,
            'use_existing_genetic_loc': "no"

            }

    base_ucf_filepath = '/Users/omreeg/KBase/apps/cello/lib/cello_util/UCF/Eco1C1G1T0.UCF.json'

    test_dict = {

        'config_dict': test_config_dict_3,
        'bs_ucf_fp': base_ucf_filepath,
        'output_fp': "My_Test_1_28",
        'msd_gb_fp': "",
        'op_gb_fp': os.path.join(os.path.dirname(os.path.abspath(__file__)),'plasmids/pAN4020.ape'),
        'cr_gb_fp': os.path.join(os.path.dirname(os.path.abspath(__file__)),'plasmids/pAN1201.ape')
            }

    convert_gb_to_ucf(test_dict)


"""
Inputs:
    -msd measurement_standard_genbank_filepath.gb
    -op output_plasmid_genbank_filepath.gb
    -cr circuit_genbank_filepath.gb
    -bs base_ucf_filepath.json
    -con config_filepath.json
    -out out_UCF_filepath.json


"""
def main():

    test() 

    """
    msd_genbank_fp = args[1]
    output_genbank_fp = args[2]
    circuit_genbank_fp = args[3]
    base_ucf_fp = args[4]
    config_fp = args[5] 
    out_UCF_fp = args[6]



    #Convert json files to dicts
    f = open(base_ucf_fp, "r")
    base_ucf_str =  f.read()
    f.close()
    base_ucf_dict = json.loads(base_ucf_str)
    
    f = open(config_fp, "r")
    config_str =  f.read()
    f.close()
    config_dict = json.loads(config_str)


    convert_gb_to_ucf(msd_genbank_fp, base_ucf_dict, config_dict, out_UCF_fp)
    """

if __name__ == "__main__":
    main()


