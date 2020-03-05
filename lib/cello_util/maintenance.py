#python3


import os
import shutil
from cello_util.file_maker import make_verilog_case_file_string, \
        make_input_file_str, make_output_file_str 



def make_input_files(extracted_vars_dict, cello_config_dict):
    cello_kb = cello_config_dict['cello_kb']
    #Creating input files to Cello from params:
    vlog_case_filestring = make_verilog_case_file_string(
            extracted_vars_dict['truth_table'],
            cello_config_dict['verilog_module_name'],
            extracted_vars_dict['inp_out_dict'])
    with open(os.path.join(cello_kb, "new_verilog.v"), "w") as f:
        f.write(vlog_case_filestring)

    extracted_vars_dict['inputs_filestring'] = make_input_file_str(
            extracted_vars_dict['gene_inputs_list'])
    with open(os.path.join(cello_kb, "new_inputs.txt"),"w") as f:
        f.write(extracted_vars_dict['inputs_filestring'])

    extracted_vars_dict['outputs_filestring'] = make_output_file_str(
            extracted_vars_dict['gene_outputs_list'])
    with open(os.path.join(cello_kb, "new_outputs.txt"),"w") as f:
        f.write(extracted_vars_dict['outputs_filestring'])

    return extracted_vars_dict



def copy_input_files_to_output_folder(final_op_dir, cello_kb, 
        extracted_vars_dict, cello_config_dict):
    shutil.copyfile(os.path.join(cello_kb, "new_verilog.v"), os.path.join(
        final_op_dir,"VERILOG_INPUT.v" ))
    shutil.copyfile(os.path.join(cello_kb, "new_inputs.txt"), os.path.join(
        final_op_dir,"PROMOTERS_INPUT.txt" ))
    shutil.copyfile(os.path.join(cello_kb, "new_outputs.txt"), os.path.join(
        final_op_dir,"OUTPUTS_INPUT.txt" ))
    #The UCF
    shutil.copyfile(extracted_vars_dict['ucf_info']['additional_info_dict'][
            'output_fp'], 
            os.path.join(final_op_dir, "UCF.json"))

    #We copy the base plasmids if the base plasmid info is ecoli or tetrlaci
    base_plasmid_info = extracted_vars_dict["ucf_info"]["base_plasmid_info"] 
    if base_plasmid_info == "e_coli" or base_plasmid_info == "terlaci":
        shutil.copyfile(cello_config_dict["plasmids_info"]["filepaths"]["pAN1201"], 
                os.path.join(final_op_dir,"pAN12021.ape"))
        shutil.copyfile(cello_config_dict["plasmids_info"]["filepaths"]["pAN4020"],
                os.path.join(final_op_dir,"pAN4020.ape"))




