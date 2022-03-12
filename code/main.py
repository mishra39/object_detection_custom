import torch
#from Ipython.display import Image  # for displaying images
import os
import random
import shutil
from sklearn.model_selection import train_test_split
import xml.etree.ElementTree  as ET
from xml.dom import minidom
from tqdm import tqdm
from PIL import Image, ImageDraw
import numpy as np
import matplotlib.pyplot as plt

random.seed(0)

# function to get the data from XML annotation
def extract_info_from_xml(xml_file):
    root = ET.parse(xml_file).getroot()

    # initialize the info dict
    info_dict = {}
    info_dict['bboxes'] = []

    # parse the XML tree
    for elem in root:
        # get the file name
        if elem.tag == "filename":
            info_dict['filename'] = elem.text
        
        # get the image size
        elif elem.tag == "size":
            image_size = []
            for subelem in elem:
                image_size.append(int(subelem.text))
            info_dict['image_size'] = image_size
        
        elif elem.tag == "object":
            bbox = {}
            for subelem in elem:
                if subelem.tag == "name":
                    bbox["class"] = subelem.text
                elif subelem.tag == "bndbox":
                    for subsubelem in subelem:
                        bbox[subsubelem.tag] = int(subsubelem.text)
            info_dict['bboxes'].append(bbox)

    return info_dict
if __name__=="__main__":
    print("running!!")
    print(extract_info_from_xml('annotations/road4.xml'))