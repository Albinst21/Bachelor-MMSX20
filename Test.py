import xml.etree.ElementTree as ET

# TWIST VALUES
SWEEPValues = ["1", "1", "1", "1", "1", "1", "1", "1"]

# Choose geometry to run simulation for
ORIGINAL_GEOMETRY_NAME = "{}".format(filename)

filename_org = r"{}\{}.vsp3".format(path_org, ORIGINAL_GEOMETRY_NAME)

# Part of script that can change twist in wing sections by changing value of Theta
tree = ET.parse(filename_org)
root = tree.getroot()

k = 0  # Counter for the different sections
for sweep in root.iter('Sweep'):

    if k == 0:  # This changes twist for section 1 for example
        value = list(dict.items(sweep.attrib))
        value[0] = ('Value', '{}'.format(SWEEPValues[k]))
        new_att = dict(value)
        sweep.attrib = new_att
    elif k == 1:  # This for section 2
        value = list(dict.items(sweep.attrib))
        value[0] = ('Value', '{}'.format(SWEEPValues[k]))
        new_att = dict(value)
        sweep.attrib = new_att
    elif k == 2:
        value = list(dict.items(sweep.attrib))
        value[0] = ('Value', '{}'.format(SWEEPValues[k]))
        new_att = dict(value)
        sweep.attrib = new_att
    elif k == 3:
        value = list(dict.items(sweep.attrib))
        value[0] = ('Value', '{}'.format(SWEEPValues[k]))
        new_att = dict(value)
        sweep.attrib = new_att
    elif k == 4:
        value = list(dict.items(sweep.attrib))
        value[0] = ('Value', '{}'.format(SWEEPValues[k]))
        new_att = dict(value)
        sweep.attrib = new_att
    elif k == 5:
        value = list(dict.items(sweep.attrib))
        value[0] = ('Value', '{}'.format(SWEEPValues[k]))
        new_att = dict(value)
        sweep.attrib = new_att
    elif k == 6:
        value = list(dict.items(sweep.attrib))
        value[0] = ('Value', '{}'.format(SWEEPValues[k]))
        new_att = dict(value)
        sweep.attrib = new_att
    elif k == 7:
        value = list(dict.items(sweep.attrib))
        value[0] = ('Value', '{}'.format(SWEEPValues[k]))
        new_att = dict(value)
        sweep.attrib = new_att
    k += 1


# Writes to a new .vsp3 file that can be analyzed in OpenVSP
Newfile = "output"
tree.write('{}.vsp3'.format(Newfile))