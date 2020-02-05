#python
import os
import shutil
import logging


def make_genbank_genome_dict(filepath, genome_name, workspace_name):
    gb_dict = dict()
    gb_dict['file'] = {'path': filepath}
    gb_dict['genome_name'] = genome_name
    gb_dict['genome_type'] = "plasmid"
    gb_dict['workspace_name'] = workspace_name
    gb_dict['source'] = "Cello_Output"

    return gb_dict



#TD: Only output the .ape file that has plasmid circuit in its name.
def make_kbase_genomes(output_files, kb_output_folder, output_folder, gfu, ws_name, main_output_name):

            ape_files = turn_ape_to_gbk(output_files, kb_output_folder, output_folder)

            #Uploading the ape files to KBase Genome File Object.
            genome_ref_list = []
            for ape_fp in ape_files:

                #Placeholder genome name:
                g_name = (ape_fp.split('/')[-1])[:-4]

                gbk_file_name = ape_fp[:-4] + '.gbk'

                #Adding user output_name
                replace_index = g_name.find("plasmid_")
                if replace_index != -1:
                    g_name = main_output_name + "_" + g_name[replace_index:]
                else:
                    logging.critical("Could not find plasmid_circuit in file name.")

                # Making the parameters dict: (ws_name defined at top of function ^)
                genb_gen_dict = make_genbank_genome_dict(gbk_file_name, g_name, ws_name)

                # Calling genbank to genome function
                result = gfu.genbank_to_genome(genb_gen_dict)
    
                genome_ref_list.append({'ref' : result["genome_ref"], 'description':'Genome created for file: ' + g_name + '.gbk'})
                #DEBUG
                logging.debug("Genbank to Genome Upload Results for: " + ape_fp)
                logging.debug(result)
 
            return genome_ref_list


def turn_ape_to_gbk(output_files, kb_output_folder, output_folder):
    #Locating the '.ape' files. List ape_files will contain full paths to files.
    # ape files are like genbank files.
    circuit_ape_files = []
    output_ape_files = []
    sensor_ape_files = []
    extra_ape_files = []
    for out_f in output_files:
        if out_f[-4:] == ".ape":
            if "plasmid_circuit" in out_f:
                logging.info("Recognized plasmid_circuit .ape file: " + out_f)
                circuit_ape_files.append(os.path.join(kb_output_folder, os.path.join(output_folder, out_f)))
            elif "plasmid_output" in out_f:
                logging.info("Recognized plasmid_output .ape file: " + out_f)
                output_ape_files.append(os.path.join(kb_output_folder, os.path.join(output_folder, out_f)))
            elif "sensor" in out_f:
                logging.info("Recognized sensor .ape file: " + out_f)
                sensor_ape_files.append(os.path.join(kb_output_folder, os.path.join(output_folder, out_f)))
            else:
                logging.info("Other .ape file: " + out_f)
                extra_ape_files.append(os.path.join(kb_output_folder, os.path.join(output_folder, out_f)))
                
    ape_files = circuit_ape_files + output_ape_files + sensor_ape_files
    logging.debug("Unused ape files: ")
    logging.debug(extra_ape_files)

    logging.debug("PARSED APE FILES:")
    logging.debug(ape_files)

    if len(ape_files) == 0:
        logging.critical("NO .APE FILES FOUND - CANNOT MAKE PLASMID - ONLY RETURNING OUTPUT FOLDER.")

    for ap_f in ape_files:
        #Replace "label" in .ape file with "locus_tag"
        response = replace_label_with_locus_tag(ap_f)
        
        #Add information from base plasmid files:
        replace_plasmid_sections_with_features(ap_f, config_info)

        if response != 0:
            #ISSUE - WE DO NOT CATCH IF THIS FAILS IN LATER STEPS
            logging.critical("Issue with replacing 'label' with 'locus_tag'. Could be that no 'label's exist.")
        #Placeholder genome name:
        g_name = (ap_f.split('/')[-1])[:-4]

        #renaming file to genbank type:
        gbk_file_name = ap_f[:-4] + '.gbk'
        shutil.copyfile(ap_f, gbk_file_name)

    return ape_files




# We replace the feature value "label" with "locus_tag" so KBase can recognize the name
# of the object
def replace_label_with_locus_tag(filename):

    return_val = 0
    f = open(filename, "r")
    f_str = f.read()
    f.close()
    if "/label" not in f_str:
        return_val = 1
    new_f_str = f_str.replace('/label=','/locus_tag=')
    #Overwriting old file with new_file
    g = open(filename, "w")
    g.write(new_f_str)
    g.close()

    return return_val

def replace_label_with_gene(filename):

    return_val = 0
    f = open(filename, "r")
    f_str = f.read()
    f.close()
    if "/label" not in f_str:
        return_val = 1
    new_f_str = f_str.replace('/label=','/gene=')
    #Overwriting old file with new_file
    g = open(filename, "w")
    g.write(new_f_str)
    g.close()

    return return_val



"""
plasmid_filename: (str)
config_info: (dict)
    output_base: (str) filepath to output base genbank file.
    output_insertion_bp: (int)
    circuit_base: (str) filepath to circuit base genbank file.
    circuit_insertion_bp: (int)
    sensor_base: (str) filepath to sensor module base genbank file.
    sensor_insertion_bp: (int)

"""
def replace_plasmid_sections_with_features(plasmid_filename, config_info):

    if "circuit" in plasmid_filename:
        logging.info("Recognized circuit plasmid for replacing sections")
        detailed_plasmid_insertion(plasmid_filename, config_info["circuit_base"], config_info["circuit_insertion_bp"])

    elif "output" in plasmid_filename:
        logging.info("Recognized output plasmid for replacing sections")

        detailed_plasmid_insertion(plasmid_filename, config_info["output_base"], config_info["output_insertion_bp"])
    elif "sensor" in plasmid_filename:
        logging.info("Recognized sensor plasmid for replacing sections")

        detailed_plasmid_insertion(plasmid_filename, config_info["sensor_base"], config_info["sensor_insertion_bp"])
    else:
        logging.critical("Did not recognize type of plasmid")

    #if config_info["base_plasmid_info"]



