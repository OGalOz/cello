# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import logging
import json
from Bio import SeqIO
from biokbase.workspace.client import Workspace
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
from cello_util.var_extraction import extract_values_from_params
from cello_util.run_cello_program_util import run_cello_program, \
    handle_cello_response
from cello_util.maintenance import make_input_files, \
    copy_input_files_to_output_folder
from cello_util.upload import make_kbase_genomes, turn_ape_to_gbk
from cello_util.html_design import build_html, html_design_test


#END_HEADER


class cello:
    '''
    Module Name:
    cello

    Module Description:
    A KBase module: cello
    '''

    ######## WARNING FOR GEVENT USERS ####### noqa
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    ######################################### noqa
    VERSION = "0.0.1"
    GIT_URL = "https://github.com/OGalOz/cello"
    GIT_COMMIT_HASH = ""

    #BEGIN_CLASS_HEADER
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.callback_url = os.environ['SDK_CALLBACK_URL']
        self.shared_folder = config['scratch']
        logging.basicConfig(format='%(created)s %(levelname)s: %(message)s',
                            level=logging.DEBUG)
        self.ws_url = config['workspace-url']
        #END_CONSTRUCTOR
        pass


    def run_cello(self, ctx, params):
        """
        This function accepts any number of parameters and returns results in a 
        KBaseReport.
        :param params: instance of mapping from String to unspecified object
        :returns: instance of type "ReportResults" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: output
        #BEGIN run_cello

        logging.basicConfig(level=logging.DEBUG)
        ext_report_params = {
                "workspace_name": params['workspace_name']
                }

        #Making a directory to store variables in JSON
        variables_json_dir = os.path.join(self.shared_folder,
                "variables_json_tmp")
        os.mkdir(variables_json_dir)

        #What folder to zip and return to User
        kb_output_folder = os.path.join(self.shared_folder,"cello_output")
        os.mkdir(kb_output_folder)

        #Making config dict
        cello_config_fp = os.path.join(os.path.dirname(
            os.path.realpath(__file__)), "cello_config.json")
        with open(cello_config_fp, "r") as f:
            cello_config_dict = json.loads(f.read())


        cello_config_dict["shared_folder"] = self.shared_folder

        extracted_vars_fp = os.path.join(variables_json_dir,
                cello_config_dict["extracted_vars_json_fn"])
        

        #extracting program parameters from params given by User
        extracted_vars_dict = extract_values_from_params(params, 
                extracted_vars_fp, cello_config_dict)




        cello_kb = cello_config_dict['cello_kb']
        if not os.path.exists(cello_kb):
            os.mkdir(cello_kb)
        else:
            raise Exception("kb_run directory already exists within cello ?! \
                    Need new directory to run our verilog files.")



        #CODE
        #Creating input files to Cello from params:
        #NOTE changes are made to extracted_vars_dict
        extracted_vars_dict = make_input_files(extracted_vars_dict, 
                cello_config_dict)

        #RUNNING CELLO:
        os.chdir(cello_kb)
        # Again changes are made to extracted_vars_dict
        # This is where UCF file is made/configured!!!
        extracted_vars_dict = run_cello_program(extracted_vars_dict, 
                cello_config_dict, cello_kb)

        #Handling Cello's Work
        handle_cello_response(cello_kb, kb_output_folder)

        #Returning to former dir
        os.chdir(cello_config_dict['main_dir'])


        output_folder = os.listdir(kb_output_folder)[0]
        final_op_dir = os.path.join(kb_output_folder,output_folder)

        copy_input_files_to_output_folder(final_op_dir, cello_kb, 
                extracted_vars_dict, cello_config_dict)



        #KBASE GENOME WORK BEGIN: ---------------------------------------------
        output_files = os.listdir(final_op_dir)
        gfu = GenomeFileUtil(self.callback_url)
        kb_genome_bool = extracted_vars_dict["output_info"]["kb_genome_bool"]
        gbk_config_info = {
                    "max_kbase_genomes": cello_config_dict["max_kbase_genomes"],
                    "max_gbks": cello_config_dict["max_gbk_files_from_ape"]
        }

        if kb_genome_bool == True:
            try:
                genome_ref_list = make_kbase_genomes(output_files, 
                    kb_output_folder,
                    output_folder, 
                    gfu, 
                    params['workspace_name'], 
                    extracted_vars_dict['output_info']['main_output_name'], 
                    gbk_config_info)
            except:
                logging.warning("Could not make KBase Genomes.")
                genome_ref_list = []
            ext_report_params['objects_created'] = genome_ref_list
        else:
            turn_ape_to_gbk(output_files, kb_output_folder, output_folder, 
                    gbk_config_info)
       
        #KBASE GENOME WORK END: ---------------------------------------------





        dfu = DataFileUtil(self.callback_url)
        file_zip_shock_id = dfu.file_to_shock({'file_path': kb_output_folder,
                                              'pack': 'zip'})['shock_id']
       
        #Creating HTML to return to the user
        html_config_info = {
                'base_plasmid_info': extracted_vars_dict["ucf_info"][
                    "base_plasmid_info"]
                }

        html_result_dict = build_html(final_op_dir, 
                self.shared_folder, 
                extracted_vars_dict['output_info']['main_output_name'],
                html_config_info)
        
        report_shock_id = dfu.file_to_shock({
            'file_path': html_result_dict['output_directory'],
                'pack': 'zip'})['shock_id']

        html_report = [{'shock_id': report_shock_id,
                            'name': os.path.basename(html_result_dict['result_file_path']),
                            'label': os.path.basename(html_result_dict['result_file_path']),
                            'description': 'HTML summary report for Cello App'}]

        #'path': kb_output_folder
        main_output_name = extracted_vars_dict['output_info']['main_output_name']
        dir_link_dict = {
                'shock_id': file_zip_shock_id, 
                'name': main_output_name + '.zip', 
                'label':'cello_output_dir',
                'description': 'The directory of outputs from cello'
                }
        ext_report_params['file_links'] = [dir_link_dict]
        ext_report_params['html_links'] = html_report
        ext_report_params['direct_html_link_index'] = 0
        ext_report_params["html_window_height"] = 333
        ext_report_params["report_object_name"] = "kb_cello_report"
        ext_report_params["message"] = ""

        report = KBaseReport(self.callback_url)
        report_info = report.create_extended_report(ext_report_params)
        output = {
            'report_name': report_info['name'],
            'report_ref': report_info['ref']
        }
        #END run_cello

        # At some point might do deeper type checking...
        if not isinstance(output, dict):
            raise ValueError('Method run_cello return value ' +
                             'output is not type dict as required.')
        # return the results
        return [output]
    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK",
                     'message': "",
                     'version': self.VERSION,
                     'git_url': self.GIT_URL,
                     'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
