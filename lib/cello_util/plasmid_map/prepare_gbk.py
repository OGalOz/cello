#python3


"""

This file is created to prepare a genbank file to be visualized by the plasmid map program.

Things to consider: The space between labeled sequences (labeled by features) 
    will be called "unlabeled".
How do you choose, out of multiple overlapping features, which is the one that will be shown?
Should you designate an inner circle and an outer circle for sequences going in opposite directions?

"""

import logging
from Bio import SeqIO
import json




"""
Inputs:
    type_str: (str) string of type
    priority_list: (list) a list of lists,
        each sub list containst str with types.
Output:
   int: Index of array within priority list in which type_str exists.
"""
def find_index(type_str, priority_list):
    for i in range(len(priority_list)):
        if type_str in priority_list[i]:
            return i
    logging.warning(type_str + " not found in priority_list.")
    return 1000



"""
Inputs:
    type_a: (str) Type
    type_b: (str) Type
    priority_list: (list) a list of lists,
        each sub list containst str with types.
Outputs:
    priority: "a", "b", or "same" (str). If "a", then a has priority over b.
"""
def get_priority(type_a, type_b, priority_list, merged_priority_list):
    if type_a == type_b:
        priority = "same"
    if type_a not in merged_priority_list and type_b not in merged_priority_list:
        raise Exception("Neither inputted types have values in the priority list.\
        Cannot calculate priority")
    elif type_a not in merged_priority_list:
        priority = "b"
    elif type_b not in merged_priority_list:
        priority = "a"
    else:
        #both are in merged priority list
        a_index = find_index(type_a, priority_list)
        b_index = find_index(type_b, priority_list) 
        if a_index < b_index:
            priority = "a"
        elif b_index > a_index:
            priority = "b"
        else:
            priority = "same"

    return priority





"""
Inputs:
    feature_a: BioPython SeqFeature
    feature_b: BioPython SeqFeature
Outputs:
    overlap_bool: (bool) True if overlapping, False otherwise
"""
def check_overlap(feature_a, feature_b):
    a_start = feature_a.location.nofuzzy_start + 1
    a_end = feature_a.location.nofuzzy_end
    b_start = feature_b.location.nofuzzy_start + 1
    b_end = feature_b.location.nofuzzy_end
    if a_start <= b_end and a_end >= b_start:
        overlap_bool = True
        logging.debug("overlap found: {}-{}, \
                {}-{}".format(a_start,a_end,b_start,b_end) )
    else:
        overlap_bool = False
    return overlap_bool




"""
Info:
    How the algorithm will work:
    Run time is N^2 on feature list of size N
    For each pair of features, check if they overlap.
    If they do overlap, mark the one whose feature
    is lower on the priority list and add it to the
    removal list.

Inputs:
    feature_list: (list) A list of SeqFeatures (BioPython)
    priority_list: (list) A list of types in descending priority:
        0th index is highest priority, last index is lowest.
        
Outputs:
    removal_list: (list) A list of indices of the items to remove
        from the feature list.

"""
def make_removal_list(feature_list, priority_list):
    #Removal list stores indices of items to remove from feature_list.
    removal_list = []

    merged_priority_list = []
    for l in priority_list:
        merged_priority_list += l
        
    logging.debug("merged_priority_list")
    logging.debug(merged_priority_list)

    for i in range(len(feature_list)):
        for j in range( i+1, len(feature_list)):
            feature_a = feature_list[i]
            feature_b = feature_list[j]
            overlap_bool = check_overlap(feature_a, feature_b)
            if overlap_bool:
                type_a, type_b = feature_a.type, feature_b.type
                priority = get_priority(type_a, type_b, priority_list, merged_priority_list)
                if priority == "a":
                    removal_list.append(j)
                elif priority == "b":
                    removal_list.append(i)
                else:
                    #priority is the same we remove i
                    removal_list.append(i)

    return list(set(removal_list))

"""
Inputs:
    gb_record: A Bio SeqRecord
    removal_list: (list) A list of indices of features to remove
Outputs:
    gb_record: A BioSeqRecord with removed overlaps (hopefully)
"""
def remove_items(gb_record, removal_list):

    features = gb_record.features
    removal_list.sort(reverse=True)
    for ind in removal_list:
        del features[ind]
    gb_record.features = features

    return gb_record
    

def find_and_remove_duplicates(gb_record, priority_list):

    gb_features = gb_record.features
    logging.info("Number of features before removing \
            duplicates: {}.".format(len(gb_features)))

    removal_list = make_removal_list(gb_features, priority_list)
    logging.debug(removal_list)
    gb_record = remove_items(gb_record, removal_list)

    logging.info("Number of features after removing \
            duplicates: {}.".format(len(gb_record.features)))
    return gb_record



def genbank_prep(gbk_fp, config_fp):
    gb_record = SeqIO.read(open(gbk_fp, "r"), "genbank")
    config_dict = json.loads((open(config_fp,"r")).read())
    priority_list = config_dict["feature_priority_list"]

    #Running program:
    gb_record = find_and_remove_duplicates(gb_record, priority_list)

    SeqIO.write(gb_record, "tmp/prepared_genbank.gbk", "genbank")  





def test():
    logging.basicConfig(level=logging.DEBUG)
    test_gbk = "../new_test_out.gbk"
    gb_record = SeqIO.read(open(test_gbk, "r"), "genbank")
    config_dict = json.loads( (open("config.json","r")).read())
    priority_list = config_dict["feature_priority_list"]

    #Running program:
    gb_record = find_and_remove_duplicates(gb_record, priority_list)

    SeqIO.write(gb_record,"../second_test.gbk", "genbank")  




def main():
    test()

    return 0

if __name__ == "__main__":
    main()
