/*
A KBase module: kb_cello
This KBase SDK module implements methods for running cello.
This specific file (UCF) is a configuration file for Cello that includes all the data it requires.
*/

/*
The UCF is divided into 4 main parts: Experimental system, Boolean logic, Genetic Gates Library, and Circuit DNA sequence. Those are the largest structures.
    Experimental system:
        header (done):
            version: <str>
            date: <str> year-month-day, eg 2015-04-08
            author: list<str> [optional] e.g. ["brian", "angela"] [optional]
            organism: <str>
            genome: <str> flexible
            media: <str> flexible
            temperature: <float> Units of Celsius
            growth: <str> flexible
        measurement_std (done):
            signal_carrier_units: <str> e.g. REU, RPU flexible
            plasmid_description: <str> flexible
            plasmid_sequence: <str> All lines of a Genbank file. An entire genbank file in string format.
            normalization_instructions: <str> flexible
    Boolean logic:
        logic_constraints:
            available_gates: list<gate_info>
                gate_info: <mapping>
                    type: <str> "NOR", "OR", "OUTPUT_OR"
                    max_instances: <int> or null. e.g. 12.
        motif_library:
           inputs: list<str> e.g. ["a","b","c"]
           outputs: list<str> e.g. ["y"]
           netlist: list<netlist_str>
                netlist_str: <str> Looks like "NOT(Wire0, b)" or "NOR(y, Wire3, Wire4)". internal components must be
                    from inputs and outputs lists. {gate_type}({wire_name}, {input_name_1}, {input_name_2}, ..., {input_name_n} )

    Genetic gates library:
        gates:
            group_name: <str> Name a group of gates that cannot be used together in a circuit design.
            gate_name: <str>
            gate_type: <str>
            system: <str>
        Data:
            response_functions:
                gate_name: <str>
                variables: list<sub_var>
                    sub_var: <str> A variable name e.g "x" or "y" used in the equation and parameters.
                parameters: list<Hill_var>
                    Hill_var: mapping:
                        name <sub_var> 
                        value: <float>
                equation: <str> This string must use sub_vars in the parameters.
                
            gate_cytometry: [optional]
                gate_name: <str> (Gate name)
                cytometry_data: list<cyt_data_obj>
                    cyt_data_obj: <mapping>
                        input: <float> A single RPU value for the current titration
                        output_bins: list<float> array of RPU values specifying histogram bins
                        output_counts: list<float> array of counts for the histogram
            gate_toxicity:
                gate_name: <str> (Gate name)
                input: list<float> Input level (promoter activity in standard units)
                growth: list<float> growth values normalized by a control cell population
        Parts:
            gate_parts:
                gate_name: <str>
                transcription_units: list<transcription_units_sub_list>
                    transcription_units_sub_list: list<transcription_unit_name>
                        transcription_unit_name: <str>
                promoter: <str>
            parts:
                part_type: <str> Related to all other strings in this part.
                part_name: <str> Related to all other strings in this part.
                dnasequence: <str> Related to all other strings in this part. 

    Circuit DNA sequence:
        genetic_location:
            locations: list<location_obj>
                location_obj:
                    genbank_file_name: <str> e.g. "pAN1201"
                    file: <str> Full Genbank File string
            sensor_module_location:
                list<module_location_object>
                    module_location_object:
                        location_name: <str> name of the genbank file in locations e.g. "pAN1201"
                        bp_range: bp_range_list
                            bp_range_list: list<int> of length 2: [bp_start, bp_end]
                        unit_convesion: <float> [optional] depending on whether output plasmid differs from plasmid used to characterize the circuit.

            circuit_module_location:
                list<module_location_object>
            output_module_location:
                list<module_location_object>
            output_module_genomic_locations: op_m_g_l_object [optional] 
                op_m_g_l_object:
                    organism: <str> organism name
                    taxid: <int>
                    location_name: <str>
                    bp_range: bp_range_list
                    flanking_upstream_sequence: <str> DNA sequence
                    flanking_downstream_sequence: <str> DNA sequence

                
        eugene_rules: (constraints on physical layout of the circuit.
            eugene_part_rules: list<EUG_RULE>
                EUG_RULE: <str> A rule in Eugene format. e.g. "STARTSWITH pTac"
            eugene_gate_ruiles: list<EUG_RULE>
                EUG_RULE: <str> A rule in Eugene format, e.g. "gatePhlF BEFORE gate_SrpR"

        


*/


module cello_UCF {


    /*
    version string, e.g. "Eco1C1G1T1",
    format is {Organism Identifier}{a}{Experimental conditions ID}{b}{Genetic gates ID}{c}{Tech mapping id}{d}
    where a, b, c, d are integers representing the ids. 
    */
    typedef string version;

    /*
    A string for the date.
    Format is year-month-day, e.g. 2015-04-08
    */
    typedef string date;


    /*
    An optional list of authors, e.g. ["Dwight", "Angela", "Andy"]
    */
    typedef list<string> author_list

    /*
    organism example "Escherichia coli NEB 10-beta" 
    The name of the organism.
    It is a flexible string.
    */
    typedef string organism_name;


    /*
    genome information, (flexible) eg: 
    "NEB 10-beta Δ(ara-leu) 7697 araD139 fhuA 
    ΔlacX74 galK16 galE15 e14- φ80dlacZΔM15 recA1 relA1 endA1 nupG 
    rpsL (StrR) rph spoT1 Δ(mrr-hsdRMS-mcrBC) (New England Biolabs)"
    */
    typedef string genome_info;


    /*
    media info, (flexible)  e.g.:

    "
    M9 minimal media composed of M9 media salts (6.78 g/L Na2HPO4, 3 g/L KH2PO4, 
    1 g/L NH4Cl, 0.5 g/L NaCl, 0.34 g/L thiamine hydrochloride, 0.4% D-glucose, 
    0.2% Casamino acids, 2 mM MgSO4, and 0.1 mM CaCl2; kanamycin (50 ug/ml), 
    spectinomycin (50 ug/ml)
    "

    */
    typedef string media_info;

    /*
    Temperature in Celsius (float)
    */
    typedef float temperature;

    /*
    growth_info example (flexible):
    "
    Inoculation: Individual colonies into M9 media, 16 hours overnight in plate shaker.
    Dilution: Next day, cells dilute ~200-fold into M9 media with antibiotics, growth for 3 hours. 
    Induction: Cells diluted ~650-fold into M9 media with antibiotics. 
    Growth: shaking incubator for 5 hours. Arrest protein production: PBS and 2mg/ml kanamycin. 
    Measurement: flow cytometry, data processing for REU normalization.
    "
    */
    typedef string growth_info;
    

    typedef structure {
        version version;
        date date;
        author_list author;
        organism_name organism;
        genome_info genome;
        media_info media;
        temperature temperature;
        growth_info growth;

    } Header;




    /*
    signal carrier units are represented in "RPU" or "REU"

    */
    typedef string signal_carrier_units;

    /*
    plasmid description, flexible:
    "
    p15A plasmid backbone with kanamycin resistance and a YFP expression cassette. 
    Upstream isulation by terminator L3S3P21 and a 5’-promoter spacer. 
    Promoter BBa_J23101, ribozyme RiboJ, RBS BBa_B0064 drives constitutive YFP expression, 
    with transcriptional termination by L3S3P21.
    "
    
    */
    typedef string plasmid_info;

    /*
    plasmid_sequence is a string of the entire genbank file for the measurement standard plasmid.
    This string is placed inside a list, in which every row of the file is a new item in the list.
    EG:
    ["LOCUS       pAN801star__LacI        2853 bp ds-DNA     circular     27-MAR-2015",
    "SOURCE      ",
     ...,
     "//"]
    */
    typedef list<string> plasmid_sequence;


    /*
    normalization_instructions
    A flexible string, a "set of instructions describing how data is normalized
    using the measurement standard" (Cello Suppplementary Material).
    e.g. "The following equation converts the median YFP fluorescence to REU. 
    REU = (YFP – YFP0)/(YFPREU – YFP0), where YFP is the median fluorescence of the cells of interest, 
    YFP0 is the median autofluorescence, and YFPREU is the median fluorescence of the cells 
    containing the measurement standard plasmid"
    */
    typedef string normalization_instructions;

    typedef structure {
    signal_carrier_units signal_carrier_units;
    plasmid_info plasmid_info;
    plasmid_sequence plasmid_sequence;
    normalization_instructions normalization_instructions;

    } Measurement_Std;



};
