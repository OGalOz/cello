#python




def make_genbank_genome_dict(filepath, genome_name, workspace_name):
    gb_dict = dict()
    gb_dict['file'] = {'path': filepath}
    gb_dict['genome_name'] = genome_name
    gb_dict['workspace_name'] = workspace_name

    return gb_dict

