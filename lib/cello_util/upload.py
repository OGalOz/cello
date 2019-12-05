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
    gb_dict['source'] = "Cello Output"

    return gb_dict



#TD: Only output the .ape file that has plasmid circuit in its name.
def make_kbase_genomes(output_files, kb_output_folder, output_folder, gfu, ws_name, main_output_name):
            #Locating the '.ape' files. List ape_files will contain full paths to files.
            # ape files are like genbank files.
            ape_files = []
            for out_f in output_files:
                if out_f[-4:] == ".ape":
                    if "plasmid_circuit" in out_f:
                        logging.info("Recognized .ape file: " + out_f)
                        ape_files.append(os.path.join(kb_output_folder, os.path.join(output_folder, out_f)))


            logging.debug("APE FILES:")
            logging.debug(ape_files)

            #Replace "label" in .ape file with "locus_tag"

            for ap_f in ape_files:
               response = replace_label_with_locus_tag(ap_f)
               if response != 0:
                   logging.critical("Issue with replacing 'label' with 'locus_tag'. Could be that no 'label's exist.")




            #Uploading the ape files to KBase Genome File Object.
            genome_ref_list = []
            for ape_fp in ape_files:

                #Placeholder genome name:
                g_name = (ape_fp.split('/')[-1])[:-4]

                #renaming file to genbank type:
                gbk_file_name = ape_fp[:-4] + '.gbk'
                shutil.copyfile(ape_fp, gbk_file_name)

                #Adding user output_name
                replace_index = g_name.find("plasmid_circuit")
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




    


