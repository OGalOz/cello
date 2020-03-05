#python3

import os
import logging
import shutil
from cello_util.file_maker import make_ucf_file


def run_cello_program(extracted_vars_dict, cello_config_dict, cello_kb_dir):

    os.chdir(cello_kb_dir)
    ucf_command = ""
    if cello_config_dict['new_ucf_bool']:
        ucf_filepath = make_ucf_file(extracted_vars_dict)
        ucf_command = "-UCF " + ucf_filepath 
    dexec_args = "-verilog new_verilog.v -input_promoters new_inputs.txt" 
    dexec_args += " -output_genes new_outputs.txt " + ucf_command
    cello_output = os.system('mvn -e -f /cello/pom.xml -DskipTests=true ' + \
            '-PCelloMain -Dexec.args="{}"'.format(dexec_args))
    logging.info("Response from Cello: {}".format(cello_output))
    extracted_vars_dict["ucf_info"]['additional_info_dict'][
            'output_fp'] = ucf_filepath

    return extracted_vars_dict


def handle_cello_response(cello_kb, kb_output_folder):
    dir_list = os.listdir(cello_kb)
    output_dirpath = 'placeholder'
    existing_files = ['0xFE_verilog.v', 'new_inputs.txt', 'new_outputs.txt',
            'new_verilog.v', 'exports'] 
    for f in dir_list:
        if f not in existing_files:
            output_dirpath = os.path.join(cello_kb, f)
            dir_name = f
            logging.debug(output_dirpath)
            break
    if output_dirpath == 'placeholder':
        raise Exception("did not get output from Cello")
    else:
        if (os.path.isfile(output_dirpath)):
            raise Exception("Expected directory as output from Cello, \
                    got a file: " + output_dirpath)
        elif (os.path.isdir(output_dirpath)):
            logging.info("Succesfully produced directory: " + output_dirpath)
            if dir_name[:3] == 'job':
                logging.info("Directory name begins with job")
                shutil.move(output_dirpath, kb_output_folder)
        else:
            logging.critical("Unknown destination")


