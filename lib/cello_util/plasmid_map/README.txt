# Plasmid_Map_In_Browser

This program makes a plasmid map that you can view in a browser that supports Javascript and Canvas objects in HTML5.

Depends on:
python3
Biopython

How to run the program:
    Command line: "python plasmid_map_viewer.py test.gbk my_html.html"

test.gbk and my_html.html are variable.

Use your own gbk file (with fewer than 100 features) instead of "test.gbk" (first argument) and name your html file what you'd like the output to be (instead of my_html.html, unless you want it to be my_html.html).

The program writes (or overwrites) the html file you named.

The config.json file contains variables you can control in the design of the file - most importantly is how the features/parts are labelled.
In gb_info in the config file you can label how the parts are named, and what "type-name" (promoter, terminator) in the file corresponds to the type listed in the "types_dict" list.



* Make sure the gbk file and html file locations are readable/writable.









