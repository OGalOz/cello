#python3

import json
import os
import re
import logging
from Bio import SeqIO
from cello_util.truth_table import make_truth_table_from_text

def extract_values_from_params(params, out_fp, cello_config_dict):
    extracted_vars_dict = {}

    extracted_vars_dict['gene_inputs_list'] = get_gene_inputs(params, 
            cello_config_dict)


    extracted_vars_dict['gene_outputs_list'] = get_gene_outputs(params,
            cello_config_dict)


    extracted_vars_dict['truth_table_text'] = get_truth_table_text(params)

    extracted_vars_dict['truth_table'] = make_truth_table_from_text(
            extracted_vars_dict)


    extracted_vars_dict['ucf_info'] = get_ucf_info(params)

    extracted_vars_dict['ucf_info']['additional_info_dict'][
                'output_fp'] = os.path.join(
                cello_config_dict["shared_folder"], 
                cello_config_dict["new_ucf_name"])

    extracted_vars_dict["ucf_params_fp"] = cello_config_dict["ucf_params_fp"]

    extracted_vars_dict['output_info'] = get_output_info(params)

    extracted_vars_dict['inp_out_dict'] = {
            "in_num": len(extracted_vars_dict['gene_inputs_list']),
            "out_num": len(extracted_vars_dict['gene_outputs_list'])
            }

    with open(out_fp, "w") as f:
        f.write(json.dumps(extracted_vars_dict))

    return extracted_vars_dict


def get_gene_inputs(params, cello_config_dict):
    gene_inputs_list = []

    if "promoter_inputs" in params or "custom_promoter_inputs" in params:
        if "promoter_inputs" in params:
            gene_inputs_sub_list = params["promoter_inputs"]
            for item in gene_inputs_sub_list:
                if isinstance(item, dict):
                    item["custom_var"] = False
                    gene_inputs_list.append(item)
                else:
                    raise Exception("Expected template item to be dict, but \
                            instead it is " + str(type(item)))
        if "custom_promoter_inputs" in params:
            custom_promoter_inputs_list = params["custom_promoter_inputs"]
            for item in custom_promoter_inputs_list:
                if isinstance(item, dict):
                    item["custom_var"] = True
                    item["low_RPU"] = item["custom_low_RPU"]
                    item["high_RPU"] = item["custom_high_RPU"]
                    item["inp_promoter_name"] = item["custom_inp_promoter_name"]
                    gene_inputs_list.append(item)
                else:
                    raise Exception("Expected custom item to be dict, but \
                            instead it is " + str(type(item)))
    else:
        raise Exception("Input Promoters not supplied (not in params).")

    if len(gene_inputs_list) > cello_config_dict["max_input_num"]:
        raise Exception("Number of promoter inputs exceeds the maximum alloted \
                amount: {}".format(cello_config_dict["max_input_num"]))

    return gene_inputs_list



def get_gene_outputs(params, cello_config_dict):

    gene_outputs_list = []

    if "gene_outputs" in params or "custom_gene_outputs" in params:
        gene_outputs_list = []
        if "gene_outputs" in params:
            gene_outputs_sub_list = params["gene_outputs"]
            for gene_dict in gene_outputs_sub_list:
                if isinstance(gene_dict, dict):
                    gene_dict["custom_var"] = False
                    gene_outputs_list.append(gene_dict)
                else:
                    raise Exception("Expected template gene output to be \
                            dict, but instead it is " + str(type(gene_dict)))
            #logging.debug(gene_outputs_list)
        if "custom_gene_outputs" in params:
            custom_gene_outputs_list = params["custom_gene_outputs"]
            for gene_dict in custom_gene_outputs_list:
                if isinstance(gene_dict, dict):
                    gene_dict["custom_var"] = True
                    gene_dict["out_gene_name"] = gene_dict["custom_out_gene_name"] 
                    gene_dict["out_DNA_sequence"] = gene_dict["custom_out_DNA_sequence"]
                    gene_outputs_list.append(gene_dict)
                else:
                    raise Exception("Expected custom gene output to be dict, \
                            but instead it is " + str(type(gene_dict)))
    else:
        raise Exception("No gene outputs supplied (in params).")

    if len(gene_outputs_list) > cello_config_dict["max_output_num"]:
        raise Exception("Number of protomer outputs exceeds the maximum alloted \
                amount: {}".format(cello_config_dict["max_output_num"]))



    return gene_outputs_list



def get_truth_table_text(params):

    if "truth_table_text" in params:
        truth_table_text = params["truth_table_text"]
    else:
        raise Exception("Truth Table Text not supplied")

    return truth_table_text




def get_ucf_info(params):

    ucf_info = {}

    if "base_plasmid_info" in params:

        base_plasmid_info = params["base_plasmid_info"]
        ucf_info['base_plasmid_info'] = base_plasmid_info

        #Initializing the additional info dict as False values to be updated
        # later in the program.
        #msd - measurement standard. op - output. cr - circuit. sn - sensor.
        additional_info_dict = {"msd_gb_bool": False, "op_gb_bool": False, 
                "cr_gb_bool": False, "sn_gb_bool": False}


        #We only change things if "custom" - meaning the user is 
        # altering an existing UCF file 
        custom_base_info = {}
        if base_plasmid_info == "custom":

            custom_base_info, additional_info_dict = sub_get_custom_base_info(
                    params, additional_info_dict)
        
        ucf_info['custom_base_info'] = custom_base_info
        ucf_info['additional_info_dict'] = additional_info_dict
    else:
        raise Exception("base_plasmid_info not passed as a parameter - contact Help-Desk.")

    return ucf_info


def sub_get_custom_base_info(params, additional_info_dict):
    custom_base_info = {}
    if "plasmid_output_base" in params:

        plasmid_output_base = params["plasmid_output_base"]
        plasmid_output_genome_base_ref = plasmid_output_base["output_genome_base"]
        plasmid_output_insertion_bp = plasmid_output_base["output_insertion_bp"]
        additional_info_dict["op_gb_bool"] = True
        additional_info_dict["op_mod_loc"] = plasmid_output_insertion_bp 
        #Downloading_genbank file
        genome_info = gfu.genome_to_genbank({"genome_ref": plasmid_output_genome_base_ref})
        output_genome_genbank_fn = genome_info['genbank_file']['file_path']
        op_gb_fp = os.path.join(self.shared_folder, 
                output_genome_genbank_fn)
        #Checking if insertion point is less than length of plasmid:
        op_p_rec = SeqIO.read(open(op_gb_fp,"r"),"genbank")
        custom_base_info['output_gb_fp'] = op_gb_fp
        if not int(plasmid_output_insertion_bp) < len(op_p_rec.seq):
            raise Exception("Output insertion point must be less \
                    than total length of output plasmid.")
    else:
        logging.critical("No plasmid output base given.")

    if "plasmid_circuit_base" in params:
        plasmid_circuit_base = params["plasmid_circuit_base"]
        plasmid_circuit_genome_base_ref = plasmid_circuit_base["circuit_genome_base"]
        plasmid_circuit_insertion_bp = plasmid_circuit_base["circuit_insertion_bp"]
        additional_info_dict["cr_gb_bool"] = True
        additional_info_dict["cr_mod_loc"] = plasmid_circuit_insertion_bp 

        genome_info = gfu.genome_to_genbank({"genome_ref": plasmid_circuit_genome_base_ref})
        circuit_genome_genbank_fn = genome_info['genbank_file']['file_path']
        cr_gb_fp = os.path.join(self.shared_folder, circuit_genome_genbank_fn)
        cr_p_rec = SeqIO.read(open(cr_gb_fp,"r"),"genbank")
        custom_base_info['circuit_gb_fp'] = cr_gb_fp
        if not int(plasmid_circuit_insertion_bp) < len(cr_p_rec.seq):
            raise Exception("Circuit insertion point must be less than total length of circuit plasmid.")
    else:
        raise Exception("custom base circuit plasmid indicated, but none given \
            In choosing custom base, you must provide plasmid circuit \
                info.")

    if "sensor_module_info" in params:
        sensor_module_base = params["sensor_module_info"]
        sensor_module_genome_base_ref = sensor_module_base["sensor_module_base"]
        sensor_insertion_bp = sensor_module_base["sensor_insertion_bp"]
        additional_info_dict["sn_gb_bool"] = True
        additional_info_dict["sn_mod_loc"] = sensor_insertion_bp 
        genome_info = gfu.genome_to_genbank({"genome_ref": sensor_module_genome_base_ref})
        circuit_genome_genbank_fn = genome_info['genbank_file']['file_path']
        sn_gb_fp = os.path.join(self.shared_folder, circuit_genome_genbank_fn)
        sn_p_rec = SeqIO.read(open(sn_gb_fp,"r"),"genbank")
        custom_base_info['sensor_gb_fp'] = sn_gb_fp
        if not int(sensor_insertion_bp) < len(sn_p_rec.seq):
            raise Exception("Sensor insertion point must be less than total length of sensor plasmid.")
    else:
        raise Exception("sensor module info indicated, but none given. \
            In choosing custom base, you must provide sensor module \
                info.")
    return custom_base_info, additional_info_dict




def get_output_info(params):
    output_info = {}

    #Output info
    if "kbase_genome_bool" in params:
        kb_str = params["kbase_genome_bool"]
        if kb_str == "yes":
            kb_genome_bool = True
        elif kb_str == "no":
            kb_genome_bool = False
        else:
            logging.critical("ERROR: Cannot recognize whether to create Genome Object.")
            kb_genome_bool = False
    if "main_output_name" in params:
        main_output_name = params["main_output_name"]
        regex = re.compile('[@ !#$%^&*()<>?/\|}{~:]')
        if regex.search(main_output_name) != None:
            raise Exception("Output name contains illegal characters.")
    else:
        raise Exception("Output Name not supplied (not in params).")

    output_info['kb_genome_bool'] = kb_genome_bool
    output_info['main_output_name'] = main_output_name

    return output_info

