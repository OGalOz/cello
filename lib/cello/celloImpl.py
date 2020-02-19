# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import shutil
import logging
import re
from Bio import SeqIO
from biokbase.workspace.client import Workspace
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
from cello_util.file_maker import make_verilog_case_file_string, \
    make_input_file_str, make_output_file_str, make_ucf_file
from cello_util.truth_table import make_truth_table_from_text, \
    make_truth_table_from_values
from cello_util.upload import make_kbase_genomes, turn_ape_to_gbk
from cello_util.html_design import build_html, html_design_test
#from cello_util.plasmid_map_viewer import make_plasmid_graph


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
        report = KBaseReport(self.callback_url)
        ext_report_params = dict()
        ext_report_params["workspace_name"] = params['workspace_name']
        logging.basicConfig(level=logging.DEBUG)
        gfu = GenomeFileUtil(self.callback_url)

        #DEBUGGING
        logging.debug("PARAMS")
        logging.debug(params)
        for k in params:
            logging.debug(k)
            logging.debug(params[k])


        #Deciding if we use UCF in program or not- for now true
        new_ucf_bool = True
        #UCF filepath ucf_filepath variable decided later in the program

        #CODE
        # Extracting Values from params
        
        ws_name = params['workspace_name']
        if "promoter_inputs" in params or "custom_promoter_inputs" in params:
            gene_inputs_list = []
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
        if "truth_table_text" in params:
            truth_table_text = params["truth_table_text"]
        else:
            raise Exception("Truth Table Text not supplied")

        #UCF info - 
        if "base_plasmid_info" in params:
            base_plasmid_info = params["base_plasmid_info"]
            #Initializing the additional info dict as False values to be updated
            # later in the program.
            additional_info_dict = {"msd_gb_bool": False, "op_gb_bool": False, 
                    "cr_gb_bool": False, "sn_gb_bool": False}
            #We only change things if the "custom" - meaning the user is 
            # altering an existing UCF file 
            if base_plasmid_info == "custom":
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
                    if not int(plasmid_circuit_insertion_bp) < len(cr_p_rec.seq):
                        raise Exception("Circuit insertion point must be less than total length of circuit plasmid.")
                else:
                    raise Exception("custom base circuit plasmid indicated, but none given")

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
                    if not int(sensor_insertion_bp) < len(sn_p_rec.seq):
                        raise Exception("Sensor insertion point must be less than total length of sensor plasmid.")
                else:
                    raise Exception("sensor module info indicated, but none given")

        else:
            raise Exception("base_plasmid_info not passed as a parameter - contact Help-Desk.")

        
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

        #Done extracting parameters
        num_inputs = len(gene_inputs_list)
        num_outputs = len(gene_outputs_list)
        inp_out_dict = {"in_num" : num_inputs, "out_num": num_outputs}


        #Creating truth table:
        truth_table = make_truth_table_from_text(gene_inputs_list, gene_outputs_list, truth_table_text)

        #DEBUG
        logging.debug(truth_table)



        #Preparing new UCF (if necessary)
        if new_ucf_bool:
            #naming the filepath belonging to the new UCF which is to be created
            ucf_filepath = os.path.join(self.shared_folder, "tmp_kbase_ucf.json")
            logging.critical("Creating New UCF file: {}".format(ucf_filepath))
            additional_info_dict['output_fp'] = ucf_filepath
            if base_plasmid_info != "none":
                if 'op_gb_fp' in locals():
                    additional_info_dict["op_gb_fp"] = op_gb_fp
                if 'cr_gb_fp' in locals():
                    additional_info_dict["cr_gb_fp"] = cr_gb_fp
                if 'sn_gb_fp' in locals():
                    additional_info_dict["sn_gb_fp"] = sn_gb_fp
            ucfs_params_fp = "/kb/module/lib/cello_util/util_params.json"
            ucf_filepath = make_ucf_file(base_plasmid_info, ucfs_params_fp, additional_info_dict) 
    

        #CODE
        #Setting variables:
        #What folder to zip and return to User
        kb_output_folder = os.path.join(self.shared_folder,"cello_output")
        os.mkdir(kb_output_folder)

        


        #raise Exception("Stop running program for testing purposes.")


        #Actually running cello--------------

        #cello is downloaded by docker to this directory
        cello_dir = '/cello'

        #Creating directory to add verilog, input and output files to. We call it /cello/kb_run
        cello_kb = os.path.join(cello_dir,'kb_run')
        if not os.path.exists(cello_kb):
            os.mkdir(cello_kb)
        else:
            raise Exception("kb_run directory already exists within cello ??? \
                    Need new directory to run our verilog files.")

        #CODE
        #Creating input files to Cello from params:
        module_name = "testname"
        vlog_case_filestring = make_verilog_case_file_string(truth_table,module_name, inp_out_dict)
        inputs_filestring = make_input_file_str(gene_inputs_list)
        outputs_filestring = make_output_file_str(gene_outputs_list)

        #WRITING THE INPUT FILES TO CELLO AND STORING OUTPUT
        f = open(os.path.join(cello_kb, "new_verilog.v"), "w")
        f.write(vlog_case_filestring)
        f.close()
        #shutil.copyfile(os.path.join(cello_kb, "new_verilog.v"), os.path.join(kb_output_folder,"VERILOG_INPUT.v" ))
        g = open(os.path.join(cello_kb, "new_inputs.txt"),"w")
        g.write(inputs_filestring)
        g.close()
        #shutil.copyfile(os.path.join(cello_kb, "new_inputs.txt"), os.path.join(kb_output_folder,"PROMOTERS_INPUT.txt" ))
        h = open(os.path.join(cello_kb, "new_outputs.txt"),"w")
        h.write(outputs_filestring)
        h.close()
        #shutil.copyfile(os.path.join(cello_kb, "new_outputs.txt"), os.path.join(kb_output_folder,"OUTPUTS_INPUT.txt" ))


        '''
        #TEST UCF FILES:
        ucf_filepath = "/kb/module/lib/cello/test_data/minimized_Eco1_with_g_loc.json"
        if not os.path.exists(ucf_filepath):
            raise Exception("UCF filepath does not exist")
        '''

        #RUNNING CELLO:
        os.chdir(cello_kb)
        ucf_command = ""
        if new_ucf_bool:
            ucf_command = "-UCF " + ucf_filepath
        dexec_args = "-verilog new_verilog.v -input_promoters new_inputs.txt" 
        dexec_args += " -output_genes new_outputs.txt " + ucf_command
        op = os.system('mvn -e -f /cello/pom.xml -DskipTests=true ' + \
                '-PCelloMain -Dexec.args="{}"'.format(dexec_args))
        logging.debug("Response from Cello: ")
        logging.debug(op)
        dir_list = os.listdir(cello_kb)
        logging.debug(dir_list)
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
                raise Exception("Expected directory as output from Cello, got a file: " + output_dirpath)
            elif (os.path.isdir(output_dirpath)):
                logging.info("Succesfully produced directory: " + output_dirpath)
                if dir_name[:3] == 'job':
                    logging.info("Directory name begins with job")
                    shutil.move(output_dirpath, kb_output_folder)
            else:
                logging.critical("Unknown destination")
        os.chdir('/kb/module/')

        output_folder = os.listdir(kb_output_folder)[0]
        full_path_output_folder = os.path.join(kb_output_folder,output_folder)

        #Copying input files to output folder.
        shutil.copyfile(os.path.join(cello_kb, "new_verilog.v"), os.path.join(
            full_path_output_folder,"VERILOG_INPUT.v" ))
        shutil.copyfile(os.path.join(cello_kb, "new_inputs.txt"), os.path.join(
            full_path_output_folder,"PROMOTERS_INPUT.txt" ))
        shutil.copyfile(os.path.join(cello_kb, "new_outputs.txt"), os.path.join(
            full_path_output_folder,"OUTPUTS_INPUT.txt" ))
        #The UCF
        shutil.copyfile(ucf_filepath, os.path.join(full_path_output_folder, 
            "UCF.json"))

        output_files = os.listdir(full_path_output_folder)
        logging.debug("CELLO OUTPUT FOLDER:")
        logging.debug(output_files)

        

        if kb_genome_bool == True:
            genome_ref_list = make_kbase_genomes(output_files, kb_output_folder,
                    output_folder, gfu, ws_name, main_output_name)
            ext_report_params['objects_created'] = genome_ref_list
        else:
            #TD: More info in gbk config info
            gbk_config_info = {}
            turn_ape_to_gbk(output_files, kb_output_folder, output_folder, 
                    gbk_config_info)
        

        #We copy the base plasmids if the base plasmid info is "e_coli" or "tetrlaci"
        if base_plasmid_info == "e_coli" or base_plasmid_info == "terlaci":
            shutil.copyfile("/kb/module/lib/cello_util/plasmids/pAN1201.ape", 
                    full_path_output_folder)
            shutil.copyfile("/kb/module/lib/cello_util/plasmids/pAN4020.ape", 
                    full_path_output_folder)

        dfu = DataFileUtil(self.callback_url)
        file_zip_shock_id = dfu.file_to_shock({'file_path': kb_output_folder,
                                              'pack': 'zip'})['shock_id']
       
        #Creating HTML to return to the user
        html_config_info = {
                'base_plasmid_info': base_plasmid_info
                }
        html_result_dict = build_html(full_path_output_folder, 
                self.shared_folder, 
                main_output_name, html_config_info)
        
        report_shock_id = dfu.file_to_shock({
            'file_path': html_result_dict['output_directory'],
                'pack': 'zip'})['shock_id']

        html_report = [{'shock_id': report_shock_id,
                            'name': os.path.basename(html_result_dict['result_file_path']),
                            'label': os.path.basename(html_result_dict['result_file_path']),
                            'description': 'HTML summary report for Cello App'}]

        #'path': kb_output_folder
        dir_link = {'shock_id': file_zip_shock_id, 'name': main_output_name + \
                '.zip', 'label':'cello_output_dir', \
                'description': 'The directory of outputs from cello'}
        ext_report_params['file_links'] = [dir_link]
        ext_report_params['html_links'] = html_report
        ext_report_params['direct_html_link_index'] = 0
        ext_report_params["html_window_height"] = 333
        ext_report_params["report_object_name"] = "kb_cello_report"
        ext_report_params["message"] = ""
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
