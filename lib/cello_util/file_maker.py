#!python
#This file creates the necessary cello files from the inputs.

#Functions to send to impl: make_verilog_case_file_string, make_input_file_str, make_output_file_str.




def make_verilog_case_file_string(truth_table, module_name):


    #First row of truth_table must be the names of the inputs and outputs.
    #Should be labelled in1, in2, ... out1.

    check_truth_table(truth_table)

    #For now, assume there is only one output.


    verilog_file_str = ''
    
    verilog_file_str += make_header_line(truth_table, module_name)

    verilog_file_str += make_always_line(truth_table)
    
    verilog_file_str += "\t\tbegin\n"

    verilog_file_str += make_case_block(truth_table)

    verilog_file_str += "\t\tend\n"
    verilog_file_str += "endmodule"

    return verilog_file_str
    
    
def check_truth_table(truth_table):
    if len(truth_table) < 2:
        raise Exception("Truth table does not contain enough lines, must contain names of inputs and outputs and then lines for their values.")
    if len(truth_table[0]) < 2:
        raise Exception("Either inputs or outputs are missing from the truth table title row.")



def make_header_line(truth_table, module_name):

    input_names = truth_table[0][:-1]
    header_input_str = "input "
    for inp_name in input_names:
        header_input_str += inp_name + ", "

    # Removing the final ", ":    
    header_input_str = header_input_str[:-2]
    
    header_output_str = "output "

    #For now we have only one output
    output_name = truth_table[0][-1]

    #Eventually we'll need a list of output names.
    header_output_str += output_name + ", "

    header_line = "module " + module_name + "(" + header_output_str + header_input_str + ");\n"
    
    return header_line


def make_always_line(truth_table):
    always_str = "\talways@("
    inputs = truth_table[0][:-1]
    for inp in inputs:
        always_str += inp + ","

    #Removing the final comma and adding a close parentheses and new-line.
    always_str = always_str[:-1] + ")\n"

    return always_str

def make_case_block(truth_table):

    case_block_str = ''
    
    opening_block = '\t\t\tcase({'
    inputs = truth_table[0][:-1]
    for inp in inputs:
        opening_block+= inp + ','

    #removing the last comma and closing the opening block
    opening_block = opening_block[:-1] + '})\n'
    case_block_str += opening_block

    #We currently have only one output
    output = truth_table[0][-1]
    
    case_lines = ''
    for truth_row in truth_table[1:]:
        line_str = 4*'\t' + str(len(inputs)) + "'b"
        for inp_val in truth_row[:-1]:
            line_str += str(inp_val)
        line_str += ": {" + output + "} = 1'b" + str(truth_row[-1]) + ';\n' 
        case_lines += line_str

    case_block_str += case_lines

    case_block_str += 3*'\t' + "endcase\n"

    return case_block_str

    
def make_input_file_str(inp_file_list):

    #Test
    if len(inp_file_list) == 0:
        raise Exception("There must be at least one input gene.")

    inp_file_str = ''

    for inp_dict in inp_file_list:
        low_RPU = str(inp_dict['low_RPU'])
        high_RPU = str(inp_dict['high_RPU'])
        DNA_Sequence = check_DNA_seq(inp_dict['inp_DNA_sequence'])
        inp_file_str += inp_dict['inp_gene_name'] + ' ' + low_RPU + ' ' + high_RPU + ' ' + DNA_Sequence + '\n'

    return inp_file_str


def make_output_file_str(output_file_list):
    
    #Test
    if len(output_file_list) == 0:
        raise Exception("There must be at least one output gene.")

    output_file_str = ''


    for out_dict in output_file_list:

        DNA_Sequence = check_DNA_seq(out_dict['out_DNA_sequence'])
        output_file_str += out_dict['out_gene_name'] + ' ' + DNA_Sequence + '\n'
    

    return output_file_str

# Could add conversion to uppercase
def check_DNA_seq(DNA_Sequence):
    if not isinstance(DNA_Sequence, str):
        raise Exception("Inputted DNA sequence not 'string'.")

    for i in range(len(DNA_Sequence)):
        if DNA_Sequence[i] not in ["A","C","T","G", "a","c","t","g"]:
            raise Exception("DNA Sequence for input must only contain A, C, T, or G. Instead it contains: " + DNA_Sequence[i])
    return DNA_Sequence.upper()

