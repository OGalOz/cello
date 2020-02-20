# -*- coding: utf-8 -*-
import os
import time
import unittest
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

        gene_input_1 = {"inp_promoter_name": "pTac", "low_RPU" : "0.1", "high_RPU": "3.0"}
        gene_input_2 = {"inp_promoter_name": "pTet", "low_RPU" : "0.02", "high_RPU": "2.0"}

        gene_inputs = [gene_input_1, gene_input_2]

        gene_output_1 = {"out_gene_name": "YFP"}
        gene_outputs = [gene_output_1]

       
        truth_table_text =    ' pTac, pTet, YFP & 0, 0, 1 & 0, 1, 0 & 1,0,1 & 1,1,0'

        #base_plasmid_info can be one of "none", "e_coli", "tetrlaci", "custom"
        base_plasmid_info = "e_coli" #info

        plasmid_output_genome_base = "33901/141/1"  #pAN4020
        plasmid_output_insertion_bp = "953"

        plasmid_circuit_genome_base = "33901/139/1" #pAN1201 
        plasmid_circuit_insertion_bp = "54"

        sensor_module_base = "33901/139/1" #pAN1201
        sensor_insertion_bp = "150"

        plasmid_output_base = {"output_genome_base": plasmid_output_genome_base,"output_insertion_bp": plasmid_output_insertion_bp}
        plasmid_circuit_base =  {"circuit_genome_base": plasmid_circuit_genome_base,"circuit_insertion_bp": plasmid_circuit_insertion_bp} 
        
        sensor_module_info = {"sensor_module_base": sensor_module_base, "sensor_insertion_bp": sensor_insertion_bp}
        

        main_output_name = "Test_2_1_19"

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

'''
'plasmid_output_genome_base': plasmid_output_genome_base,
'plasmid_output_insertion_bp': plasmid_output_insertion_bp,
'plasmid_circuit_genome_base': plasmid_circuit_genome_base,
'plasmid_circuit_insertion_bp':  plasmid_circuit_insertion_bp 
'''
                                                            
