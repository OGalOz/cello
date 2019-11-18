# -*- coding: utf-8 -*-
#BEGIN_HEADER
import os
import shutil
import logging
from biokbase.workspace.client import Workspace
from installed_clients.KBaseReportClient import KBaseReport
from installed_clients.DataFileUtilClient import DataFileUtil
from cello_util.file_maker import make_verilog_case_file_string, make_input_file_str, make_output_file_str


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


        #DEBUGGING
        logging.debug("PARAMS")
        logging.debug(params)
        for k in params:
            logging.debug(k)
            logging.debug(params[k])

        #CODE
        if "gene_inputs" in params:
            gene_inputs_list = params["gene_inputs"]
            logging.debug(gene_inputs)
        else:
            raise Exception("gene_inputs not in params.")

        if "gene_outputs" in params:
            gene_outputs_list = params["gene_outputs"]
            logging.debug(gene_outputs)
        else:
            raise Exception("gene_outputs not in params.")



        
        #CODE
        #Setting variables:
        #What folder to zip and return to User
        kb_output_folder = os.path.join(self.shared_folder,"cello_output")
        os.mkdir(kb_output_folder)

        


        raise Exception("Stop running program - Testing.")


        #Actually running cello:
        cello_dir = '/cello'

        #Creating directory to add verilog, input and output files to. We call it /cello/kb_run
        cello_kb = os.path.join(cello_dir,'kb_run')
        if not os.path.exists(cello_kb):
            os.mkdir(cello_kb)
        else:
            raise Exception("kb_run directory already exists within cello ??? Need new directory to run our verilog files.")


        #Just running the cello_demo eventually replace cello_demo with cello_kb
        cello_demo = os.path.join(cello_dir, 'demo')
        os.chdir(cello_demo)
        op = os.system('mvn -e -f /cello/pom.xml -DskipTests=true -PCelloMain -Dexec.args="-verilog demo_verilog.v -input_promoters demo_inputs.txt -output_genes demo_outputs.txt"')
        logging.debug(op)
        dir_list = os.listdir(cello_demo)
        logging.debug(dir_list)
        output_dirpath = 'placeholder'
        for f in dir_list:
            if f not in ['0xFE_verilog.v', 'demo_inputs.txt', 'demo_outputs.txt', 'demo_verilog.v', 'exports']:
                output_dirpath = os.path.join(cello_demo, f)
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

        logging.debug(os.listdir(kb_output_folder))

        dfu = DataFileUtil(self.callback_url)

        file_zip_shock_id = dfu.file_to_shock({'file_path': kb_output_folder,
                                              'pack': 'zip'})['shock_id']

        
        #'path': kb_output_folder
        dir_link = {'shock_id': file_zip_shock_id, 'name':'Cello_Output.zip', 'label':'cello_dir', 'description': 'The directory of outputs from cello'}
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
