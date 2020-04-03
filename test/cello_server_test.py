# -*- coding: utf-8 -*-
import os
import time
import unittest
import copy
from configparser import ConfigParser

from cello.celloImpl import cello
from cello.celloServer import MethodContext
from cello.authclient import KBaseAuth as _KBaseAuth

from installed_clients.WorkspaceClient import Workspace


class celloTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = os.environ.get('KB_AUTH_TOKEN', None)
        config_file = os.environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('cello'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'cello',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = Workspace(cls.wsURL)
        cls.serviceImpl = cello(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']
        suffix = int(time.time() * 1000)
        cls.wsName = "test_CelloTest_" + str(suffix)
        ret = cls.wsClient.create_workspace({'workspace': cls.wsName})  # noqa

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods

        gene_input_1 = {"inp_promoter_name": "pTac", "low_RPU" : "0.1", 
                "high_RPU": "3.0"}
        gene_input_2 = {"inp_promoter_name": "pTet", "low_RPU" : "0.02", 
                "high_RPU": "2.0"}

        gene_inputs = [gene_input_1, gene_input_2]

        gene_output_1 = {"out_gene_name": "YFP"}
        gene_outputs = [gene_output_1]

       
        truth_table_text =    ' pTac, pTet, YFP & 0, 0, 1 & 0, 1, 0 & 1,0,1 & 1,1,0'

        #base_plasmid_info can be one of "none", "e_coli", "tetrlaci", 
        # "bacteroides_theta_5482", "custom"
        base_plasmid_info = "bacteroides_theta_5482" #info

        plasmid_output_genome_base = "33901/141/1"  #pAN4020
        plasmid_output_insertion_bp = "953"

        plasmid_circuit_genome_base = "33901/139/1" #pAN1201 
        plasmid_circuit_insertion_bp = "54"

        sensor_module_base = "33901/139/1" #pAN1201
        sensor_insertion_bp = "150"

        plasmid_output_base = {"output_genome_base": plasmid_output_genome_base,
                "output_insertion_bp": plasmid_output_insertion_bp}
        plasmid_circuit_base =  {"circuit_genome_base": plasmid_circuit_genome_base,
                "circuit_insertion_bp": plasmid_circuit_insertion_bp} 
        
        sensor_module_info = {"sensor_module_base": sensor_module_base, 
                "sensor_insertion_bp": sensor_insertion_bp}
        

        main_output_name = "Test_4_3_20"

        #no or yes
        kbase_genome_bool = "no"

        ret = self.serviceImpl.run_cello(self.ctx, {
                                                    'workspace_name': self.wsName,
                                                    'main_output_name': main_output_name,
                                                    "kbase_genome_bool": kbase_genome_bool,
                                                    'promoter_inputs' : gene_inputs,
                                                    'gene_outputs' : gene_outputs,
                                                    'truth_table_text' : truth_table_text,
                                                    'base_plasmid_info': base_plasmid_info,
                                                    'plasmid_output_base': plasmid_output_base,
                                                    'plasmid_circuit_base': plasmid_circuit_base,
                                                    'sensor_module_info': sensor_module_info,
                                                    })


def params_alternate_bases():

    return ["none", "e_coli", "tetrlaci", "custom"]

def params_custom_inputs(custom_bool):
    if custom_bool == True:
        return ["pNew_1", "pNew_2", "pNew_3"]
    else:
        return ["pTac", "pTet", "pBAD", "pLuxStar", "pPhlF", "pCymRC"]
     
def params_custom_output(custom_bool):
    if custom_bool == True:
        return ["new_output_1"]
    else:
        return ["YFP", "RFP", "BFP", "sigmaT3", "sigmaK1FR", 
                "sigmaCGG", "sigmaT7"]


def convert_truth_table_option_to_string(tt_option_list):
    tt_str = ""
    for row in tt_option_list:
        tt_str += ", ".join([str(x) for x in row]) + " & "
    return tt_str[:-2]


#We get options for 2 inputs 1 output and 3 inputs 1 output.
def params_truth_table_text_options(input_num, output_num):
    options_list = []
    if (input_num == 2 and output_num == 1):
        op_vals = []
        for x in [0,1]:
            new_op = [[0,0],[0,1], [1,0], [1,1]]
            new_op[0].append(x)
            for y in [0,1]:
                new_op[1].append(y)
                for z in [0,1]:
                    new_op[2].append(z)
                    for w in [0,1]:
                        new_op[3].append(w)
                        op_vals.append(copy.deepcopy(new_op))
                        new_op[3].pop()
                    new_op[2].pop()
                new_op[1].pop()
            new_op[0].pop()
        return(op_vals)
    elif (input_num == 3 and output_num == 1):
        op_vals = []
        for a in [0,1]:
            new_op = [[0,0,0],[0,0,1], [0,1,0], [0,1,1],
                    [1,0,0],[1,0,1],[1,1,0],[1,1,1]]
            new_op[0].append(a)
            for b in [0,1]:
                new_op[1].append(b)
                for c in [0,1]:
                    new_op[2].append(c)
                    for d in [0,1]:
                        new_op[3].append(d)
                        for e in [0,1]:
                            new_op[4].append(e)
                            for f in [0,1]:
                                    new_op[5].append(f)
                                    for g in [0,1]:
                                        new_op[6].append(g)
                                        for h in [0,1]:
                                            new_op[7].append(h)
                                            op_vals.append(copy.deepcopy(new_op))
                                            new_op[7].pop()
                                        new_op[6].pop()
                                    new_op[5].pop()
                            new_op[4].pop()
                        new_op[3].pop()
                    new_op[2].pop()
                new_op[1].pop()
            new_op[0].pop()
        return(op_vals)
    else:
        return 0




"""
Testing needs to check:
    Custom Inputs (max/min length?)
    Custom Outputs (max/min length?)
    base plasmids (max/min length?)
    output_base/circuit_base/sensor_module combinations on/off?
    complexity of genetic circuit turth table?
    E_coli base and custom base?
    Explanation of how process works in display.yml?
"""

'''
'plasmid_output_genome_base': plasmid_output_genome_base,
'plasmid_output_insertion_bp': plasmid_output_insertion_bp,
'plasmid_circuit_genome_base': plasmid_circuit_genome_base,
'plasmid_circuit_insertion_bp':  plasmid_circuit_insertion_bp 
'''
                                                            
