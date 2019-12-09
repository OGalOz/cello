#!python
#This file creates the necessary cello files from the inputs.

#Functions to send to impl: make_verilog_case_file_string, make_input_file_str, make_output_file_str.
import re
import logging

"""
Inputs: 
    truth_table: (list)
    module_name: (str)
    inp_out_dict: (dict)
        in_num: (int)
        out_num: (int)
        

"""
def make_verilog_case_file_string(truth_table, module_name, inp_out_dict):


    #First row of truth_table must be the names of the inputs and outputs.
    #Should be labelled in1, in2, ... out1, out2 ...

    check_truth_table(truth_table)

    input_num = inp_out_dict["in_num"]

    verilog_file_str = ''
    
    verilog_file_str += make_header_line(truth_table, module_name, input_num)

    verilog_file_str += make_always_line(truth_table, input_num)
    
    verilog_file_str += "\t\tbegin\n"

    verilog_file_str += make_case_block(truth_table, input_num)

    verilog_file_str += "\t\tend\n"
    verilog_file_str += "endmodule"

    logging.debug("Verilog File:")

    logging.debug(verilog_file_str)

    return verilog_file_str
    
    
def check_truth_table(truth_table):
    if len(truth_table) < 2:
        raise Exception("Truth table does not contain enough lines, must contain names of inputs and outputs and then lines for their values.")
    if len(truth_table[0]) < 2:
        raise Exception("Either inputs or outputs are missing from the truth table title row.")



def make_header_line(truth_table, module_name, input_num):

    #This is a difficult part: how to differentiate between inputs and outputs. We use inp_out_dict.
    input_names = truth_table[0][:input_num]
    output_names = truth_table[0][input_num:]
    logging.debug("Input Names (verilog creation): ")
    logging.debug(input_names)
    logging.debug("Output Names (verilog creation): ")
    logging.debug(output_names)

    #Writing header line
    header_input_str = "input "
    for inp_name in input_names:
        header_input_str += inp_name + ", "

    # Removing the final ", ":    
    header_input_str = header_input_str[:-2]
    
    header_output_str = "output "

    for output_name in output_names:
        header_output_str += output_name + ", "

    #Eventually we'll need a list of output names.
    header_output_str += output_name + ", "

    header_line = "module " + module_name + "(" + header_output_str + header_input_str + ");\n"
    
    return header_line


def make_always_line(truth_table, input_num):
    always_str = "\talways@("
    inputs = truth_table[0][:input_num]
    for inp in inputs:
        always_str += inp + ","

    #Removing the final comma and adding a close parentheses and new-line.
    always_str = always_str[:-1] + ")\n"

    return always_str

def make_case_block(truth_table, input_num):

    case_block_str = ''
    
    opening_block = '\t\t\tcase({'
    inputs = truth_table[0][:input_num]
    for inp in inputs:
        opening_block+= inp + ','

    #removing the last comma and closing the opening block
    opening_block = opening_block[:-1] + '})\n'
    case_block_str += opening_block

    #We currently have only one output
    outputs = truth_table[0][input_num:]
    output_str = ','.join(outputs)
    
    
    case_lines = ''
    for truth_row in truth_table[1:]:
        line_str = 4*'\t' + str(input_num) + "'b"
        for inp_val in truth_row[:input_num]:
            line_str += str(inp_val)
        line_str += ": {" + output_str + "} = " + str(len(outputs)) + "'b" 
        for out_val in truth_row[input_num:]:
            line_str += str(out_val)
        line_str += ';\n' 
        case_lines += line_str

    case_block_str += case_lines

    case_block_str += 3*'\t' + "endcase\n"

    return case_block_str



'''
Inputs:
    inp_file_list (list of dicts):
        inp_dict (dict):
            custom_var: (bool) states if input is custom by user or given
            gene_name: (str)
            low_RPU: (float)
            high_RPU: (float)
            custom_inp_DNA_sequence: (optional, if custom var is True)
Output:
    inp_file_str: (str) entire file
'''
def make_input_file_str(inp_file_list):

    #Test
    if len(inp_file_list) == 0:
        raise Exception("There must be at least one input gene.")

    inp_file_str = ''

    for inp_dict in inp_file_list:

        #We check if the input is custom made or from the list. If not custom, bool False
        custom_var = inp_dict['custom_var']



        # We make sure the gene name doesn't contain weird characters:
        gene_name = check_gene_name(inp_dict['inp_promoter_name'])

        low_RPU = str(inp_dict['low_RPU'])
        high_RPU = str(inp_dict['high_RPU'])

        if custom_var == True:
            #We make the DNA sequence entirely uppercase
            DNA_Sequence = check_DNA_seq(inp_dict['custom_inp_DNA_sequence'], True)
        else:
            DNA_Sequence = corresponding_DNA_to_inp_name(gene_name)

        inp_file_str += gene_name + ' ' + low_RPU + ' ' + high_RPU + ' ' + DNA_Sequence + '\n'

    return inp_file_str



'''
Inputs:
    output_file_list: (list of dicts)
        out_dict: (dict)
            custom_var: (bool) if input is custom (by user) or given
            out_gene_name: (str)
            out_DNA_sequence: (str) [optional] - if custom_var is True
Output:
    output_file_str: (str) The string of the file.
'''
def make_output_file_str(output_file_list):
    
    #Test
    if len(output_file_list) == 0:
        raise Exception("There must be at least one output gene.")

    output_file_str = ''


    for out_dict in output_file_list:
        # We make sure the gene name doesn't contain weird characters:
        gene_name = check_gene_name(out_dict['out_gene_name'])

        if "custom_var" in out_dict:
            custom_var = out_dict["custom_var"]
        else:
            logging.critical(out_dict)
            raise Exception("No custom var in an output dict, logged above.")
        if custom_var == False:
            DNA_Sequence = corresponding_DNA_to_output_name(gene_name)
        else:
            # We make the DNA sequence entirely upper case, bool in input controls that.
            DNA_Sequence = check_DNA_seq(out_dict['out_DNA_sequence'], True)
        output_file_str += gene_name + ' ' + DNA_Sequence + '\n'
    

    return output_file_str


'''
Inputs:
    DNA_Sequence: (str)
    upper_bool: (bool) which controls whether you want the entire DNA to be uppercase (True means uppercase).
Outputs:
    DNA_Sequence: (str)
'''
def check_DNA_seq(DNA_Sequence, upper_bool):
    if not isinstance(DNA_Sequence, str):
        raise Exception("Inputted DNA sequence not 'string'.")

    for i in range(len(DNA_Sequence)):
        if DNA_Sequence[i] not in ["A","C","T","G", "a","c","t","g"]:
            raise Exception("DNA Sequence for input must only contain A, C, T, or G. Instead it contains: " + DNA_Sequence[i])
    if upper_bool == True:
        return DNA_Sequence.upper()
    else:
        return DNA_Sequence





def check_gene_name(gene_name):
    
    regex = re.compile('[@ !#$%^&*()<>?/\|}{~:]')
    if regex.search(gene_name) == None:
        return gene_name
    else:
        raise Exception("Gene Name Contains illegal characters: " + gene_name)



'''
inp_name: (str)

output: (str) either "-1" if not found, or DNA sequence if found.
'''
def corresponding_DNA_to_inp_name(inp_name):

    DNA_Promoters_dict = dict_of_promoter_relations()
    if inp_name in DNA_Promoters_dict:
        logging.info("Input name " + inp_name + " found in list of promoters.")
        DNA_Seq = DNA_Promoters_dict[inp_name]
        return DNA_Seq
    else:
        raise Exception("DNA Input name not found in our database.")



# This function contains the names of the promoters and their sequences.
def dict_of_promoter_relations():

    DNA_Promoters_dict = {

        "pTac" : "AACGATCGTTGGCTGTGTTGACAATTAATCATCGGCTCGTATAATGTGTGGAATTGTGAGCGCTCACAATT",
        "pTet" : "TACTCCACCGTTGGCTTTTTTCCCTATCAGTGATAGAGATTGACATCCCTATCAGTGATAGAGATAATGAGCAC",
        "pBAD" : 'ACTTTTCATACTCCCGCCATTCAGAGAAGAAACCAATTGTCCATATTGCATCAGACATTGCCGTCACTGCGTCTTTTACTGGCTCTTCTCGCTAACCAAACCGGTAACCCCGCTTATTAAAAGCATTCTGTAACAAAGCGGGACCAAAGCCATGACAAAAACGCGTAACAAAAGTGTCTATAATCACGGCAGAAAAGTCCACATTGATTATTTGCACGGCGTCACACTTTGCTATGCCATAGCATTTTTATCCATAAGATTAGCGGATCCTACCTGACGCTTTTTATCGCAACTCTCTACTGTTTCTCCATACCCGTTTTTTTGGGCTAGC',
        "pLuxStar" : "ACCTGTAGGATCGTACAGGTTTACGCAAGAAAATGGTTTGTTACTTTCGAATAAA",
        "pPhlF": 'CGACGTACGGTGGAATCTGATTCGTTACCAATTGACATGATACGAAACGTACCGTATCGTTAAGGT',
        "pCymRC": "AACAAACAGACAATCTGGTCTGTTTGTATTATGGAAAATTTTTCTGTATAATAGATTCAACAAACAGACAATCTGGTCTGTTTGTATTAT"
            }



    return DNA_Promoters_dict





'''
Inputs:
    output_name: (str) Name of output gene

Outputs:
    DNA_Sequence: (str) corresponding to output_name
'''
def corresponding_DNA_to_output_name(output_name):

    DNA_Out_dict = dict_of_out_gene_relations()
    if output_name in DNA_Out_dict:
        logging.info("Output name " + output_name + " found in list of promoters.")
        DNA_Seq = DNA_Out_dict[output_name]
        return DNA_Seq
    else:
        raise Exception("DNA Output name not found in our database.")




def dict_of_out_gene_relations():

    DNA_Out_Genes_dict = {


        'YFP': 'CTGAAGCTGTCACCGGATGTGCTTTCCGGTCTGATGAGTCCGTGAGGACGAAACAGCCTCTACAAATAATTTTGTTTAATACTAGAGAAAGAGGGGAAATACTAGATGGTGAGCAAGGGCGAGGAGCTGTTCACCGGGGTGGTGCCCATCCTGGTCGAGCTGGACGGCGACGTAAACGGCCACAAGTTCAGCGTGTCCGGCGAGGGCGAGGGCGATGCCACCTACGGCAAGCTGACCCTGAAGTTCATCTGCACCACAGGCAAGCTGCCCGTGCCCTGGCCCACCCTCGTGACCACCTTCGGCTACGGCCTGCAATGCTTCGCCCGCTACCCCGACCACATGAAGCTGCACGACTTCTTCAAGTCCGCCATGCCCGAAGGCTACGTCCAGGAGCGCACCATCTTCTTCAAGGACGACGGCAACTACAAGACCCGCGCCGAGGTGAAGTTCGAGGGCGACACCCTGGTGAACCGCATCGAGCTGAAGGGCATCGACTTCAAGGAGGACGGCAACATCCTGGGGCACAAGCTGGAGTACAACTACAACAGCCACAACGTCTATATCATGGCCGACAAGCAGAAGAACGGCATCAAGGTGAACTTCAAGATCCGCCACAACATCGAGGACGGCAGCGTGCAGCTCGCCGACCACTACCAGCAGAACACCCCAATCGGCGACGGCCCCGTGCTGCTGCCCGACAACCACTACCTTAGCTACCAGTCCGCCCTGAGCAAAGACCCCAACGAGAAGCGCGATCACATGGTCCTGCTGGAGTTCGTGACCGCCGCCGGGATCACTCTCGGCATGGACGAGCTGTACAAGTAACTCGGTACCAAATTCCAGAAAAGAGGCCTCCCGAAAGGGGGGCCTTTTTTCGTTTTGGTCC',
        'RFP': 'CTGAAGTGGTCGTGATCTGAAACTCGATCACCTGATGAGCTCAAGGCAGAGCGAAACCACCTCTACAAATAATTTTGTTTAATACTAGAGTCACACAGGAAAGTACTAGATGGCTTCCTCCGAAGACGTTATCAAAGAGTTCATGCGTTTCAAAGTTCGTATGGAAGGTTCCGTTAACGGTCACGAGTTCGAAATCGAAGGTGAAGGTGAAGGTCGTCCGTACGAAGGTACCCAGACCGCTAAACTGAAAGTTACCAAAGGTGGTCCGCTGCCGTTCGCTTGGGACATCCTGTCCCCGCAGTTCCAGTACGGTTCCAAAGCTTACGTTAAACACCCGGCTGACATCCCGGACTACCTGAAACTGTCCTTCCCGGAAGGTTTCAAATGGGAACGTGTTATGAACTTCGAAGACGGTGGTGTTGTTACCGTTACCCAGGACTCCTCCCTGCAAGACGGTGAGTTCATCTACAAAGTTAAACTGCGTGGTACCAACTTCCCGTCCGACGGTCCGGTTATGCAGAAAAAAACCATGGGTTGGGAAGCTTCCACCGAACGTATGTACCCGGAAGACGGTGCTCTGAAAGGTGAAATCAAAATGCGTCTGAAACTGAAAGACGGTGGTCACTACGACGCTGAAGTTAAAACCACCTACATGGCTAAAAAACCGGTTCAGCTGCCGGGTGCTTACAAAACCGACATCAAACTGGACATCACCTCCCACAACGAAGACTACACCATCGTTGAACAGTACGAACGTGCTGAAGGTCGTCACTCCACCGGTGCTTAATAACAGATAAAAAAAATCCTTAGCTTTCGCTAAGGATGATTTCT',
        'BFP' : 'CTGAAGTTCCAGTCGAGACCTGAAGTGGGTTTCCTGATGAGGCTGTGGAGAGAGCGAAAGCTTTACTCCCGCACAAGCCGAAACTGGAACCTCTACAAATAATTTTGTTTAAGAGTCACACAGGAAAGTACTAGATGAGCGAGCTGATTAAGGAGAACATGCACATGAAGCTGTACATGGAGGGCACCGTGGACAACCATCACTTCAAGTGCACATCCGAGGGCGAAGGCAAGCCCTACGAGGGCACCCAGACCATGAGAATCAAGGTGGTCGAGGGCGGCCCTCTCCCCTTCGCCTTCGACATCCTGGCTACTAGCTTCCTCTACGGCAGCAAGACCTTCATCAACCACACCCAGGGCATCCCCGACTTCTTCAAGCAGTCCTTCCCTGAGGGCTTCACATGGGAGAGAGTCACCACATACGAAGATGGGGGCGTGCTGACCGCTACCCAGGACACCAGCCTCCAGGACGGCTGCCTCATCTACAACGTCAAGATCAGAGGGGTGAACTTCACATCCAACGGCCCTGTGATGCAGAAGAAAACACTCGGCTGGGAGGCCTTCACCGAGACGCTGTACCCCGCTGACGGCGGCCTGGAAGGCAGAAACGACATGGCCCTGAAGCTCGTGGGCGGGAGCCATCTGATCGCAAACATCAAGACCACATATAGATCCAAGAAACCCGCTAAGAACCTCAAGATGCCTGGCGTCTACTATGTGGACTACAGACTGGAAAGAATCAAGGAGGCCAACAACGAGACCTACGTCGAGCAGCACGAGGTGGCAGTGGCCAGATACTGCGACCTCCCTAGCAAACTGGGGCACTAACCAGGCATCAAATAAAACGAAAGGCTCAGTCGAAAGACTGGGCCTTTCGTTTTATCTGTTGTTTGTCGGTGAACGCTCTCTACTAGAGTCACACTGGCTCACCTTCGGGTGGGCCTTTCTGCGTTTATA',
        'sigmaT3' : 'ATGAGCATCGCGGCGACCCTGGAGAACGATCTGGCGCGTCTGGAAAACGAAAACGCTCGTCTCGAAAAAGACATCGCGAACCTGGAACGTGACCTGGCGAAACTGGAGCGTGAAGAAGCGTACTTCGGAGGTTCAGGTGGTAAGAACACTGGTGAAATCTCTGAGAAAGTCAAGCTGGGCACTAAGGCACTGGCTGGTCAATGGCTGGCTTACGGTGTTACTCGCAGTGTGACTAAGCGTTCAGTCATGACGCTGGCTTACGGGTCCAAAGAGTTCGGCTTCCGTCAACAAGTGCTGGAAGATACCATTCAGCCAGCTATTGATTCCGGCAAGGGTCTGATGTTCACTCAGCCGAATCAGGCTGCTGGATACATGGCTAAGCTGATTTGGGAATCTGTGAGCGTGACGGTGGTAGCTGCGGTTGAAGCAATGAACTGGCTTAAGTCTGCTGCTAAGCTGCTGGCTGCTGAGGTCAAAGATAAGAAGACTGGAGAGATTCTTCGCAAGCGTTGCGCTGTGCATTGGGTAACTCCTGATGGTTTCCCTGTGTGGCAGGAATACAAGAAGCCTATTCAGAAGCGCCTGGACATGATTTTCTTGGGTCAATTTCGCTTGCAACCTACCATTAACACCAACAAAGATAGCGAGATTGATGCACACAAACAGGAGTCTGGTATCGCTCCTAACTTTGTACACAGCCAAGACGGTAGCCACCTTCGTAAGACTGTAGTGTGGGCACACGAGAAGTACGGAATCGAATCTTTTGCACTGATTCACGACTCCTTCGGTACGATTCCGGCTGACGCTGCGAACCTGTTCAAAGCAGTGCGCGAAACTATGGTTGACACATATGAGTCTTGTGATGTACTGGCTGATTTCTACGACCAGTTCGCTGACCAGTTGCACGAGTCTCAATTGGACAAAATGCCAGCACTTCCGGCTAAAGGTAACTTGAACCTCCGTGACATCTTAGAGTCGGACTTCGCGTTCGCG',
        'sigmaK1FR' : 'ATGAGCATCGCGGCGACCCTGGAGAACGATCTGGCGCGTCTGGAAAACGAAAACGCTCGTCTCGAAAAAGACATCGCGAACCTGGAACGTGACCTGGCGAAACTGGAGCGTGAAGAAGCGTACTTCGGAGGTTCAGGTGGTAAGAACACTGGTGAAATCTCTGAGAAAGTCAAGCTGGGCACTAAGGCACTGGCTGGTCAATGGCTGGCTTACGGTGTTACTCGCAGTGTGACTAAGCGTTCAGTCATGACGCTGGCTTACGGGTCCAAAGAGTTCGGCTTCCGTCAACAAGTGCTGGAAGATACCATTCAGCCAGCTATTGATTCCGGCAAGGGTCTGATGTTCACTCAGCCGAATCAGGCTGCTGGATACATGGCTAAGCTGATTTGGGAATCTGTGAGCGTGACGGTGGTAGCTGCGGTTGAAGCAATGAACTGGCTTAAGTCTGCTGCTAAGCTGCTGGCTGCTGAGGTCAAAGATAAGAAGACTGGAGAGATTCTTCGCAAGCGTTGCGCTGTGCATTGGGTAACTCCTGATGGTTTCCCTGTGTGGCAGGAATACAAGAAGCCTATTCAGACGCGCTTGAACCTGAGGTTCCTCGGTTCGTTCAACCTCCAGCCGACCGTCAACACCAACAAAGATAGCGAGATTGATGCACACAAACAGGAGTCTGGTATCGCTCCTAACTTTGTACACAGCCAAGACGGTAGCCACCTTCGTAAGACTGTAGTGTGGGCACACGAGAAGTACGGAATCGAATCTTTTGCACTGATTCACGACTCCTTCGGTACGATTCCGGCTGACGCTGCGAACCTGTTCAAAGCAGTGCGCGAAACTATGGTTGACACATATGAGTCTTGTGATGTACTGGCTGATTTCTACGACCAGTTCGCTGACCAGTTGCACGAGTCTCAATTGGACAAAATGCCAGCACTTCCGGCTAAAGGTAACTTGAACCTCCGTGACATCTTAGAGTCGGACTTCGCGTTCGCG',
        'sigmaCGG' : 'ATGAGCATCGCGGCGACCCTGGAGAACGATCTGGCGCGTCTGGAAAACGAAAACGCTCGTCTCGAAAAAGACATCGCGAACCTGGAACGTGACCTGGCGAAACTGGAGCGTGAAGAAGCGTACTTCGGAGGTTCAGGTGGTAAGAACACTGGTGAAATCTCTGAGAAAGTCAAGCTGGGCACTAAGGCACTGGCTGGTCAATGGCTGGCTTACGGTGTTACTCGCAGTGTGACTAAGCGTTCAGTCATGACGCTGGCTTACGGGTCCAAAGAGTTCGGCTTCCGTCAACAAGTGCTGGAAGATACCATTCAGCCAGCTATTGATTCCGGCAAGGGTCTGATGTTCACTCAGCCGAATCAGGCTGCTGGATACATGGCTAAGCTGATTTGGGAATCTGTGAGCGTGACGGTGGTAGCTGCGGTTGAAGCAATGAACTGGCTTAAGTCTGCTGCTAAGCTGCTGGCTGCTGAGGTCAAAGATAAGAAGACTGGAGAGATTCTTCGCAAGCGTTGCGCTGTGCATTGGGTAACTCCTGATGGTTTCCCTGTGTGGCAGGAATACAAGAAGCCTATTAAAACGCGCGTGCATATTATGTTCCTCGGTCAGTTCGAAATGCAGCCTACCATTAACACCAACAAAGATAGCGAGATTGATGCACGCAAACAGGAGTCTGGTATCGCTCCTAACTTTGTACACAGCCAAGACGGTAGCCACCTTCGTAAGACTGTAGTGTGGGCACACGAGAAGTACGGAATCGAATCTTTTGCACTGATTCACGACTCCTTCGGTACGATTCCGGCTGACGCTGCGAACCTGTTCAAAGCAGTGCGCGAAACTATGGTTGACACATATGAGTCTTGTGATGTACTGGCTGATTTCTACGACCAGTTCGCTGACCAGTTGCACGAGTCTCAATTGGACAAAATGCCAGCACTTCCGGCTAAAGGTAACTTGAACCTCCGTGACATCTTAGAGTCGGACTTCGCGTTCGCG',
        'sigmaT7' : 'ATGAGCATCGCGGCGACCCTGGAGAACGATCTGGCGCGTCTGGAAAACGAAAACGCTCGTCTCGAAAAAGACATCGCGAACCTGGAACGTGACCTGGCGAAACTGGAGCGTGAAGAAGCGTACTTCGGAGGTTCAGGTGGTAAGAACACTGGTGAAATCTCTGAGAAAGTCAAGCTGGGCACTAAGGCACTGGCTGGTCAATGGCTGGCTTACGGTGTTACTCGCAGTGTGACTAAGAGTTCAGTCATGACGCTGGCTTACGGGTCCAAAGAGTTCGGCTTCCGTCAACAAGTGCTGGAAGATACCATTCAGCCAGCTATTGATTCCGGCAAGGGTCTGATGTTCACTCAGCCGAATCAGGCTGCTGGATACATGGCTAAGCTGATTTGGGAATCTGTGAGCGTGACGGTGGTAGCTGCGGTTGAAGCAATGAACTGGCTTAAGTCTGCTGCTAAGCTGCTGGCTGCTGAGGTCAAAGATAAGAAGACTGGAGAGATTCTTCGCAAGCGTTGCGCTGTGCATTGGGTAACTCCTGATGGTTTCCCTGTGTGGCAGGAATACAAGAAGCCTATTCAGACGCGCTTGAACCTGATGTTCCTCGGTCAGTTCCGCTTACAGCCTACCATTAACACCAACAAAGATAGCGAGATTGATGCACACAAACAGGAGTCTGGTATCGCTCCTAACTTTGTACACAGCCAAGACGGTAGCCACCTTCGTAAGACTGTAGTGTGGGCACACGAGAAGTACGGAATCGAATCTTTTGCACTGATTCACGACTCCTTCGGTACGATTCCGGCTGACGCTGCGAACCTGTTCAAAGCAGTGCGCGAAACTATGGTTGACACATATGAGTCTTGTGATGTACTGGCTGATTTCTACGACCAGTTCGCTGACCAGTTGCACGAGTCTCAATTGGACAAAATGCCAGCACTTCCGGCTAAAGGTAACTTGAACCTCCGTGACATCTTAGAGTCGGACTTCGCGTTCGCG',





            }

    return DNA_Out_Genes_dict



