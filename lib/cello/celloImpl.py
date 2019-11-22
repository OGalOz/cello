# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import shutil
import logging
from biokbase.workspace.client import Workspace
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil
from installed_clients.GenomeFileUtilClient import GenomeFileUtil
from cello_util.file_maker import make_verilog_case_file_string, make_input_file_str, make_output_file_str
from cello_util.truth_table import make_truth_table_from_text, make_truth_table_from_values
from cello_util.upload import make_kbase_genomes


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
        This example function accepts any number of parameters and returns results in a KBaseReport
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

        #DEBUGGING
        logging.debug("PARAMS")
        logging.debug(params)
        for k in params:
            logging.debug(k)
            logging.debug(params[k])


        #CODE
        # Extracting Values from params
        
        ws_name = params['workspace_name']
        if "gene_inputs" in params:
            gene_inputs_list = params["gene_inputs"]
            #logging.debug(gene_inputs_list)
        else:
            raise Exception("Gene Inputs not supplied (not in params).")
        if "gene_outputs" in params:
            gene_outputs_list = params["gene_outputs"]
            #logging.debug(gene_outputs_list)
        else:
            raise Exception("Gene Outputs not supplied (not in params).")
        if "truth_table_text" in params:
            truth_table_text = params["truth_table_text"]
        else:
            raise Exception("Truth Table Text not supplied")
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
        else:
            raise Exception("Output Name not supplied (not in params).")



        #Creating truth table:
        truth_table = make_truth_table_from_text(gene_inputs_list, gene_outputs_list, truth_table_text)

        #DEBUG
        logging.debug(truth_table)


    

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
            raise Exception("kb_run directory already exists within cello ??? Need new directory to run our verilog files.")

        #CODE
        #Writing input files to Cello:
        module_name = "testname"
        vlog_case_filestring = make_verilog_case_file_string(truth_table,module_name)
        #logging.debug(vlog_case_filestring)
        inputs_filestring = make_input_file_str(gene_inputs_list)
        outputs_filestring = make_output_file_str(gene_outputs_list)
        f = open(os.path.join(cello_kb, "test_verilog.v"), "w")
        f.write(vlog_case_filestring)
        f.close()
        g = open(os.path.join(cello_kb, "test_inputs.txt"),"w")
        g.write(inputs_filestring)
        g.close()
        h = open(os.path.join(cello_kb, "test_outputs.txt"),"w")
        h.write(outputs_filestring)
        h.close()


        #Just running the cello_demo eventually replace cello_demo with cello_kb, and demo with test.
        #cello_demo = os.path.join(cello_dir, 'demo')
        os.chdir(cello_kb)
        op = os.system('mvn -e -f /cello/pom.xml -DskipTests=true -PCelloMain -Dexec.args="-verilog test_verilog.v -input_promoters test_inputs.txt -output_genes test_outputs.txt"')
        logging.debug(op)
        dir_list = os.listdir(cello_kb)
        logging.debug(dir_list)
        output_dirpath = 'placeholder'
        for f in dir_list:
            if f not in ['0xFE_verilog.v', 'test_inputs.txt', 'test_outputs.txt', 'test_verilog.v', 'exports']:
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
        output_files = os.listdir(os.path.join(kb_output_folder,output_folder))
        logging.debug("CELLO OUTPUT FOLDER:")
        logging.debug(output_files)


        if kb_genome_bool == True:
            gfu = GenomeFileUtil(self.callback_url)
            genome_ref_list = make_kbase_genomes(output_files, kb_output_folder, output_folder, gfu, ws_name, main_output_name)
            ext_report_params['objects_created'] = genome_ref_list
        

        dfu = DataFileUtil(self.callback_url)

        file_zip_shock_id = dfu.file_to_shock({'file_path': kb_output_folder,
                                              'pack': 'zip'})['shock_id']

        
        #'path': kb_output_folder
        dir_link = {'shock_id': file_zip_shock_id, 'name': main_output_name + '.zip', 'label':'cello_output_dir', 'description': 'The directory of outputs from cello'}
        ext_report_params['file_links'] = [dir_link]
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
