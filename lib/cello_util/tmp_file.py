




"""

Long code removed:

        if html_init_dict["wiring_diagram_found"] == True:
            svg_file_full_path = html_init_dict["wiring_grn_svg"]
            svg_file_obj = {"path": svg_file_full_path,"name": "Wiring_Diagram", "label": "Logic Circuit Diagram" }
            wiring_diagram_links = [svg_file_obj]

        if html_init_dict["pdf_files_found"]:
            pdf_file_links = []
            pdf_files = html_init_dict['pdf_files']
            for i in range(len(pdf_files)):
                    pdf_file_dict = {"path":pdf_files[i], "name": "pdf_file_" + str(i+1), "label": "Truth RPU diagram " + str(i+1)}
                    pdf_file_links.append(pdf_file_dict)

        if html_init_dict["wiring_diagram_found"] and html_init_dict["pdf_files_found"]:
            ext_report_params['html_links'] = wiring_diagram_links + pdf_file_links
            ext_report_params["direct_html_link_index"] = 0
        elif html_init_dict["wiring_diagram_found"]:
            ext_report_params['html_links'] = wiring_diagram_links
            ext_report_params["direct_html_link_index"] = 0
        elif html_init_dict["pdf_files_found"]:
            #Note, there may be an issue with having the html link be a pdf file.
            ext_report_params['html_links'] = pdf_file_links
            ext_report_params["direct_html_link_index"] = 0



"""
