#python
#This file takes the gene_inputs_list, the gene_outputs_list, and the truth_table_values
# and it returns a truth table
import logging

def make_truth_table(gene_inputs_list, gene_outputs_list, truth_table_values):
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
        all_gene_names.append(gene_dict['inp_gene_name'])
    for gene_dict in gene_outputs_list:
        all_gene_names.append(gene_dict['out_gene_name'])

    tt_dict = dict()
    for gene_name in all_gene_names:
        tt_dict[gene_name] = num_rows * ['']

    for tt_val in truth_table_values:
        if tt_val['gene_name'] in tt_dict:
            tt_dict[tt_val['gene_name']][int(tt_val['row_number'])-1] = tt_val['truth_value']
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
        inp_genes[0].append(gene_dict['inp_gene_name'])
        inp_genes_column = tt_dict[gene_dict['inp_gene_name']]
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


