#python

#This file stores the original code to run the demo.


def demo_run():
        #Just running the cello_demo eventually replace cello_demo with cello_kb, and demo with test.
        cello_demo = os.path.join(cello_dir, 'demo')
        os.chdir(cello_demo)
        op = os.system('mvn -e -f /cello/pom.xml -DskipTests=true -PCelloMain -Dexec.args="-verilog demo_verilog.v -input_promoters demo_inputs.txt -output_genes demo_outputs.txt"')
        logging.debug(op)
        dir_list = os.listdir(cello_demo)
        logging.debug(dir_list)
        output_dirpath = 'placeholder'
        for f in dir_list:
            if f not in ['0xFE_verilog.v', 'demo_inputs.txt', 'demo_outputs.txt', 'demo_verilog.v', 'exports']:
                output_dirpath = os.path.join(cello_demo, f)
                dir_name = f
                logging.debug(output_dirpath)
                break
        if output_dirpath == 'placeholder':
            raise Exception("did not get output from Cello")
        else:
            if (os.path.isfile(output_dirpath)):
                raise Exception("Expected directory as output from Cello, got a file: " + output_dirpath)
            elif (os.path.isdir(output_dirpath)):
                logging.info("Succesfully produced directory: " + output_dirpath)
                if dir_name[:3] == 'job':
                    logging.info("Directory name begins with job")
                    shutil.move(output_dirpath, kb_output_folder)
            else:
                logging.critical("Unknown destination")

