#python3
#This file is solely to combine two genbank files.


import os
import shutil
import logging
from Bio import SeqIO, SeqRecord, SeqFeature


"""
new_fp: (str) Filepath to newly made plasmid
base_fp: (str) Filepath to base plasmid
insertion_point: (int) Point at which new material was inserted.

"""
def merge_plasmids(new_fp, base_fp, insertion_point, out_fp):
    """
    Usually, in the new plasmid, everything borrowed from
    the base plasmid is called "backbone" in the features.
    So we find all locations of "backbone", and then
    compare that to the parts of the base_fp, and see if
    the sequences match up. We label the backbones with
    the individual parts from the base_fp and rewrite
    the new_fp to include those labels.
    SENSOR MODULE LENGTH NORMALLY: 3076 bp
    """

    logging.info("\n\n---MERGING PLASMID GENBANKS---\n\nNew: {} \nBase: {}\nOut: {}\n\n-------------------------\n".format(new_fp, base_fp, out_fp))

    SENSOR_MOD_LENGTH = 3076

    #We start off assuming the sensor module is not in the new plasmid.
    sensor_mod_bool = False

    #Getting features from new gbk file
    new_gb_record = SeqIO.read(open(new_fp,"r"), "genbank")
    new_features = new_gb_record.features

    #Getting features from base gbk file
    base_gb_record = SeqIO.read(open(base_fp,"r"), "genbank")
    base_features = base_gb_record.features

    #Marking backbone locations in new_fp:
    backbone_dicts_list, backbone_loc_list, SENSOR_MOD_LENGTH, sensor_mod_bool, sensor_mod_dict = find_backbones(new_features, SENSOR_MOD_LENGTH, sensor_mod_bool)

    #Debugging checking lengths:
    check_lengths(backbone_loc_list, base_gb_record, sensor_mod_bool)


    #Creating a difference space list (difference between each consecutive backbone piece)
    bb_space = make_diff_list(backbone_loc_list)


    #Create features to replace backbone with
    replace_backbone_dict_list = make_backbone_replacement_features(backbone_dicts_list, new_features, base_gb_record, bb_space)

    
    #Replace the features of the new plasmid with the base features.
    combined_gb_record = replace_backbone_features(new_gb_record, replace_backbone_dict_list)

    SeqIO.write(combined_gb_record, out_fp, "genbank")





"""
Inputs:
    gb_record: A bio Python record object - Bio.SeqRecord.SeqRecord:
        https://biopython.org/DIST/docs/api/Bio.SeqRecord.SeqRecord-class.html
    new_feature_list: (list) A list of dicts containing new_feature_dicts:
        new_feature_dict:
            "SeqIO_feat": The newly minted bioPython feature (new length and location)
            "sequence": ACTCG...
            "feature_type": the type of feature
            "new_plasmid_start": ?
            "new_plasmid_end": ?
Outputs:
    gb_record: Modified version of gb_record in the input
"""
def replace_backbone_features(gb_record, new_feature_list):
    
    gb_record.features += [x["SeqIO_feat"] for x in new_feature_list]

    feats_to_remove = []
    for i in range(len(gb_record.features)):
        feat = gb_record.features[i]
        if feat.type == "backbone":
            if not "sensor_module" in [x[0] for x in feat.qualifiers.values()]:
                logging.debug(feat)
                feats_to_remove.append(feat)

    logging.warning(feats_to_remove)

    for f in feats_to_remove:
            gb_record.features.remove(f)

    gb_record.features = sorted(gb_record.features, key=lambda x: x.location.start)

    return gb_record


"""
INPUTS:
    new_features: list of Bio SeqFeatures
    SENSOR_MOD_LENGTH: (int) Length of Sensor Module
    sensor_mod_bool: (bool) True if sensor module in plasmid, False otherwise.
OUTPUTS:
    backbone_dicts_list: list of backbone_dicts:
        backbone_dict:
            feat_index: (int)
            start_bp: (int)
            end_bp: (int)
    backbone_loc_list: (list) of lists,
        internal_list: (list) [start_bp, end_bp] for each backbone item
    SENSOR_MOD_LENGTH: (int)
    sensor_mod_bool: (bool)
    sensor_mod_dict: Bio SeqFeature
"""
def find_backbones(new_features, SENSOR_MOD_LENGTH, sensor_mod_bool):

    #Marking backbone locations in new_fp:
    backbone_dicts_list = []
    backbone_loc_list = [[0,0]]
    for i in range(len(new_features)):
        feat = new_features[i]
        typ = feat.type
        logging.debug(typ)
        if typ == "backbone":
            bb_dict = {
                    "feat_index": i,
                    "start_bp": feat.location.nofuzzy_start,
                    "end_bp": feat.location.nofuzzy_end,
                    }

            #If its the sensor module, we don't take it into the regular backbone list
            if "sensor_module" in [x[0] for x in feat.qualifiers.values()]:
                sensor_mod_bool = True
                sensor_mod_dict = feat
                if abs((bb_dict["end_bp"] - bb_dict["start_bp"]) - SENSOR_MOD_LENGTH) > 1 :
                    logging.critical("Sensor Module not expected length of 3076, instead it is: {}".format(bb_dict["end_bp"] - bb_dict["start_bp"]))
                    SENSOR_MOD_LENGTH = bb_dict["end_bp"] - bb_dict["start_bp"]
                else:
                    logging.info("Sensor Module length 3076 as expected")
            else:
                backbone_dicts_list.append(bb_dict)
                backbone_loc_list.append([feat.location.nofuzzy_start, feat.location.nofuzzy_end])

    return [backbone_dicts_list, backbone_loc_list, SENSOR_MOD_LENGTH, sensor_mod_bool, sensor_mod_dict]



"""
Debugging function to check lengths
"""
def check_lengths(backbone_loc_list, base_gb_record, sensor_mod_bool):
    #Checking sum length of backbone
    logging.info(backbone_loc_list)
    diff = [(x[1]-x[0]) for x in backbone_loc_list]
    logging.info(diff)
    bbone_sum_length = sum(diff)
    logging.info("Backbone sum length: {}".format(str(bbone_sum_length)))

    #Checking length of base plasmid:
    base_plasmid_len = len(base_gb_record.seq)
    logging.info("Base plasmid length: {}".format(str(base_plasmid_len)))

    if abs(bbone_sum_length - base_plasmid_len) > 1:
        if sensor_mod_bool:
            if abs(bbone_sum_length - (base_plasmid_len + SENSOR_MOD_LENGTH)) > 1:
                logging.critical("Backbone and Base Plasmid Lengths not the same!")
            else:
                logging.info("Backbone and Base Plasmid Lengths are the same length taking into account sensor module.")
        else:
            logging.critical("Backbone and Base Plasmid Lengths not the same!")
    else:
        logging.info("Backbone and Base Plasmid Lengths are the same length")



"""
Inputs:
    backbone_loc_list: (list) list of lists:
        internal_list: [start_bp, end_bp] for each backbone
Outputs:
    bb_space: (list) list of ints. Each int represents the difference between the location in the new plasmid and the base plasmid.
        
"""
def make_diff_list(backbone_loc_list):
    #Creating a difference space list (difference between each consecutive backbone piece)
    bb_space = [0]
    if len(backbone_loc_list) > 1:
        for i in range(1, len(backbone_loc_list)):
            bb_space.append( (backbone_loc_list[i][0] - backbone_loc_list[i-1][1]) + bb_space[-1])
    return bb_space



"""
Inputs:
    backbone_dicts_list: (list) backbone_dicts
    new_features: (list) of BioPython SeqFeatures
    base_gb_record: (BioPython Record object)
    bb_space: (list) of ints representing differences in location
Outputs:
    replace_backbone_dict_list: (list)
        replace_backbone_dict: (dict)
            SeqIO_feat: BioPython SeqFeature
            sequence: (str) DNA sequence
            feature_type: (str)
            new_plasmid_start: (int)
            new_plasmid_end: 

"""
def make_backbone_replacement_features(backbone_dicts_list, new_features, base_gb_record, bb_space ):

    #Now we replace the features of the new plasmid with the base features.
    #We keep track of where in our new plasmid we are:
    start_bp = 0
    replace_backbone_dict_list= []
    base_features = base_gb_record.features
    for i in range(len(backbone_dicts_list)):
        bb_dict = backbone_dicts_list[i]
        b_ind = bb_dict["feat_index"]
        #New features backbone
        nf_backbone = new_features[b_ind]

        #bb_space keeps track of the differences
        bb_start = bb_dict["start_bp"] - bb_space[i+1]
        bb_end = bb_dict["end_bp"] - bb_space[i+1]
        logging.debug("BACKBONE start: {}, end: {}".format(str(bb_start),str(bb_end)))
        for base_feat in base_features:
            s = base_feat.location.nofuzzy_start
            e = base_feat.location.nofuzzy_end
            logging.debug("\tbase feat start: {}, end: {}".format(str(s),str(e)))
            #This is how we check for overlap:
            if (s < bb_end and e > bb_start):
                logging.debug("Overlapping features")
                #We are looking for overlapping indices
                if s <= bb_start:
                    overlap_start = bb_start
                elif s > bb_start:
                    overlap_start = s
                if e >= bb_end:
                    overlap_end = bb_end
                elif e < bb_end:
                    overlap_end = e
                overlapping_indices = [overlap_start, overlap_end]
                logging.debug("overlapping_indices")
                logging.debug(overlapping_indices)

                #Following variable not in use!
                internal_start_end = [overlap_start - s, overlap_end - s]
                logging.debug("internal_start_end")
                logging.debug(internal_start_end)

                #We get the sequence for the overlapping feature
                seq_slice = base_gb_record.seq[overlap_start:overlap_end]
                logging.debug(seq_slice)

                #We make a new Bio Python seq feature:
                new_location = SeqFeature.FeatureLocation(overlap_start + bb_space[i+1],overlap_end + bb_space[i+1])

                new_feat_from_base_feat = SeqFeature.SeqFeature(location=new_location, type=base_feat.type, strand=base_feat.location.strand, id=base_feat.id, ref_db = base_feat.location.ref_db )
                replace_backbone_dict = {
                        "SeqIO_feat": new_feat_from_base_feat,
                        "sequence": seq_slice,
                        "feature_type": base_feat.type,
                        "new_plasmid_start": overlap_start + bb_space[i+1],
                        "new_plasmid_end": overlap_end + bb_space[i+1],
                        }
                replace_backbone_dict_list.append(replace_backbone_dict)

    return replace_backbone_dict_list


def test():
    logging.basicConfig(level=logging.INFO)
    logging.debug("\n\n-----\nNEW TEST\n-----\n")
    new_fp = "/Users/omreeg/KBase/apps/cello/test_local/workdir/tmp/cello_output/job_1580764268958/job_1580764268958_A000_plasmid_circuit_P000.ape"
    base_fp = "/Users/omreeg/KBase/apps/cello/test_local/workdir/tmp/KBase_derived_pAN1201.gbk_genome.gbff"
    out_fp = "new_test_out.gbk"
    insertion_point = 54
    merge_plasmids(new_fp, base_fp, insertion_point, out_fp)

    return 0

def main():
    test()

    return 0


main()


