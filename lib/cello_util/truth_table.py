#python
#This file takes the gene_inputs_list, the gene_outputs_list, and the truth_table_values
# and it returns a truth table
import logging




"""
(Still need to document the way Inputs are Given.)
INPUTS:
    gene_inputs_list: (list of dicts)
        gene_input_dict: (dict)
            inp_promoter_name: (str)





"""
def make_truth_table_from_text(gene_inputs_list, gene_outputs_list,truth_table_text):

    logging.debug("TRUTH TABLE FUNCTIONS: Gene Inputs List:")
    logging.debug(gene_inputs_list)
    logging.debug("TRUTH TABLE FUNCTIONS: Gene Outputs List:")
    logging.debug(gene_outputs_list)



    #orig_gene_names stores the gene names given by the Promoter and Output Names, not the Truth Table.
    # This is used as a test to compare if the truth table and the given names are the same.
    orig_gene_names = []
    for gene_dict in gene_inputs_list:
        orig_gene_names.append(gene_dict['inp_promoter_name'])
    for gene_dict in gene_outputs_list:
        orig_gene_names.append(gene_dict['out_gene_name'])

    logging.debug("Original Gene Names - Truth Table Function")
    logging.debug(orig_gene_names)


    """
    Format of truth_table_text is: (the "|" is to check for correctness"
    "In1", "In2", "Out1", "Out2" &
    "0", "0", "1", "0" &
    "0", "1", "0", "1" &
    etc.
    . 
    .
    "1", "1","1","1"

    """

    truth_table = []

    #Parsing truth_table_text:
    X = truth_table_text.split('&')
    logging.debug(X)
    
    
    # Make sure first row is all gene names from other inputs:
    gene_names_string = X[0]
    previous_gene_names = []
    truth_table_row = []
    if "," in gene_names_string:
        gene_names_rough_list = gene_names_string.split(",")
        logging.debug("Gene names rough list: ")
        logging.debug(gene_names_rough_list)
        for gn in gene_names_rough_list:
            gn = gn.strip()
            if gn not in orig_gene_names:
                raise Exception("Incorrect user input on gene name in truth table- doesn't match input/output gene names: " + gn)
            else:
                if gn in previous_gene_names:
                    raise Exception("Repeat input or output name, cannot continue. Do not use the same name twice as input or output. Repeat: " + gn)
                else:
                    previous_gene_names.append(gn)
                    truth_table_row.append(gn)
    truth_table.append(truth_table_row)

    # We remove the gene names from the input list. Now it is only 1's and 0's.
    X = X[1:]

    #Now we add the values (1 or 0)
    for l in X:
        truth_table_row = []
        if "," in l:
            values = l.split(",")
            for v in values:
                #removing whitespace
                v = v.strip()
                if v != "":
                    if v in ["0","1"]:
                        truth_table_row.append(v)
                    else:
                        raise Exception("Value is not 0 or 1, cannot recognize it: " + str(v))
        else:
            raise Exception("Truth Table Format Incorrect- Row does not contain any commas.")
        truth_table.append(truth_table_row)

    return truth_table








# The following function is out of use.
def make_truth_table_from_values(gene_inputs_list, gene_outputs_list, truth_table_values):
    # We find the number of rows in the truth table aside from the names of the genes.
    num_rows = max([int(ttv['row_number']) for ttv in truth_table_values])
    num_inputs = len(gene_inputs_list)
    num_outputs = len(gene_outputs_list)
    num_columns = num_inputs + num_outputs

    #We create an empty truth table with the proper dimensions
    '''
    truth_table = []
    empty_row = num_columns * ['']
    for i in range(num_rows):
        truth_table.append(empty_row)
    '''

    #We reserve all gene names to make sure the truth table values accurately list existing genes.
    all_gene_names = []
    for gene_dict in gene_inputs_list:
        all_gene_names.append(gene_dict['inp_promoter_name'])
    for gene_dict in gene_outputs_list:
        all_gene_names.append(gene_dict['out_gene_name'])

    tt_dict = dict()
    for gene_name in all_gene_names:
        tt_dict[gene_name] = num_rows * ['']

    for tt_val in truth_table_values:
        if tt_val['inp_promoter_name'] in tt_dict:
            tt_dict[tt_val['inp_promoter_name']][int(tt_val['row_number'])-1] = tt_val['truth_value']
        else:
            raise Exception("Gene name not inputs or output genes, cannot continue")
    
    logging.debug("Truth Table Dictionary")
    logging.debug(tt_dict)

    out_genes = [[].copy() for i in range(num_rows + 1) ]
    logging.debug(out_genes)
    #Create out gene list:
    for gene_dict in gene_outputs_list:
        out_genes[0].append(gene_dict['out_gene_name'])
        out_genes_column = tt_dict[gene_dict['out_gene_name']]
        for i in range(len(out_genes_column)):
            out_genes[i+1].append(out_genes_column[i])
    logging.debug(out_genes)

    inp_genes = [[].copy() for i in range(num_rows + 1) ]
    for gene_dict in gene_inputs_list:
        inp_genes[0].append(gene_dict['inp_promoter_name'])
        inp_genes_column = tt_dict[gene_dict['inp_promoter_name']]
        for i in range(len(inp_genes_column)):
            inp_genes[i+1].append(inp_genes_column[i])
    logging.debug(inp_genes)

    truth_table = []
    #Length of inp_genes should be the same as length of out_genes
    for i in range(len(inp_genes)):
        truth_table.append(inp_genes[i] + out_genes [i])

    logging.debug(truth_table)

    #Start by making a dictionary where each gene name has it's own list


    return truth_table




