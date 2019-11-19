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
        cls.wsName = "test_ContigFilter_" + str(suffix)
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

        gene_input_1 = {"inp_gene_name": "Test1", "low_RPU" : "0.1", "high_RPU": "3.0", "inp_DNA_sequence": "AACT"}
        gene_input_2 = {"inp_gene_name": "Test2", "low_RPU" : "0.02", "high_RPU": "2.0", "inp_DNA_sequence": "GGCC" }

        gene_inputs = [gene_input_1, gene_input_2]

        gene_output_1 = {"out_gene_name": "Out1", "out_DNA_sequence" : "TTAA" }
        gene_outputs = [gene_output_1]

        truth_table_values = [{'gene_name': 'Test1', 'truth_value': '0', 'row_number': '1'}, 
                {'gene_name': 'Test2', 'truth_value': '1', 'row_number': '1'}, 
                {'gene_name': 'Out1', 'truth_value': '1', 'row_number': '1'},
                {'gene_name': 'Test1', 'truth_value': '0', 'row_number': '2'},
                {'gene_name': 'Test2', 'truth_value': '0', 'row_number': '2'},
                {'gene_name': 'Out1', 'truth_value': '0', 'row_number': '2'},
                {'gene_name': 'Test1', 'truth_value': '1', 'row_number': '3'},
                {'gene_name': 'Test2', 'truth_value': '1', 'row_number': '3'},
                {'gene_name': 'Out1', 'truth_value': '1', 'row_number': '3'},
                {'gene_name': 'Test1', 'truth_value': '1', 'row_number': '4'}, 
                {'gene_name': 'Test2', 'truth_value': '0', 'row_number': '4'}, 
                {'gene_name': 'Out1', 'truth_value': '0', 'row_number': '4'}
                ]

        ret = self.serviceImpl.run_cello(self.ctx, {
                                                    'workspace_name': self.wsName,
                                                    'parameter_1': 'Hello World!',
                                                    'gene_inputs' : gene_inputs,
                                                    'gene_outputs' : gene_outputs,
                                                    'truth_table_values': truth_table_values,


                                                             })
