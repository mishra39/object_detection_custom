from cmath import inf
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

random.seed(100)

class_name_to_id_mapping = {"trafficlight" : 0,
                            "stop" : 1,
                            "speedlimit" : 2,
                            "crosswalk" : 3}

def convert_to_yolov5(info_dict):
    print_buffer = []

    # for each bounding box
    for b in info_dict["bboxes"]:
        try:
            class_id = class_name_to_id_mapping[b["class"]]
        except KeyError:
            print("Invalid class. Must be one from", class_name_to_id_mapping.keys())
    
        # transform the bbox co-ordinates as the per yolov5 format
        b_center_x = (b["xmin"] + b["xmax"]) / 2
        b_center_y = (b["ymin"] + b["ymax"]) / 2
        b_width= (-b["xmin"] + b["xmax"])
        b_height = (-b["ymin"] + b["ymax"])

        # Normalize the coordinates by the dimensions of image
        image_w, image_h, image_c = info_dict["image_size"]
        b_center_x /= image_w
        b_center_y /= image_h
        b_width /= image_w
        b_height /= image_h

        # write the details to the file
        print_buffer.append("{} {:.3f} {:.3f} {:.3f} {:.3f}".format(class_id, b_center_x, b_center_y, b_width, b_height))

    # save file name
    save_file_name = os.path.join("annotations", info_dict["filename"].replace("png", "txt"))
    # save the annotation to the disk
    print("\n".join(print_buffer),file=open(save_file_name,"w"))


# convert and save the annotations
def convert_and_save_annotations(annotations):
    for ann in tqdm(annotations):
        info_dict = extract_info_from_xml(ann)
        convert_to_yolov5(info_dict)

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
    
class_id_to_name_mapping = dict(zip(class_name_to_id_mapping.values(),class_name_to_id_mapping.keys()))

def plot_bounding_box(image,annotation_list):
    annotations = np.array(annotation_list)
    w,h = image.size
    plotted_image = ImageDraw.Draw(image)

    transformed_annotations = np.copy(annotations)
    transformed_annotations[:,[1,3]] = annotations[:,[1,3]] * w
    transformed_annotations[:,[2,4]] = annotations[:,[2,4]] * h

    transformed_annotations[:,1] = transformed_annotations[:,1] - (transformed_annotations[:,3] / 2)
    transformed_annotations[:,2] = transformed_annotations[:,2] - (transformed_annotations[:,4] / 2)
    transformed_annotations[:,3] = transformed_annotations[:,1] + transformed_annotations[:,3]
    transformed_annotations[:,4] = transformed_annotations[:,2] + transformed_annotations[:,4]

    for ann in transformed_annotations:
        obj_cls, x0, y0, x1, y1 = ann
        plotted_image.rectangle(((x0,y0),(x1,y1)))

        plotted_image.text((x0,y0-10), class_id_to_name_mapping[int(obj_cls)])
    
    plt.imshow(np.array(image))
    plt.show()

def test_random_annotation(annotations):
    annotation_file = random.choice(annotations)
    with open(annotation_file, 'r') as file:
        annotation_list = file.read().split("\n")[:-1]
        annotation_list = [x.split(" ") for x in annotation_list]
        annotation_list = [[float(y) for y in x] for x in annotation_list]
    
    # Get the corresponding image file
    image_file = annotation_file.replace("annotations","images").replace("txt","png")
    print(image_file)
    assert os.path.exists(image_file)

    # Load the image
    image = Image.open(image_file)

    # Plot the bounding box
    plot_bounding_box(image, annotation_list)

if __name__=="__main__":
    print("running!!")
    #print(extract_info_from_xml('annotations/road4.xml'))
    # get the annotations
    #annotations = [os.path.join('annotations',x) for x in os.listdir('annotations') if x[-3:]=="xml"]
    #annotations.sort()
    #convert_and_save_annotations(annotations)
    annotations = [os.path.join('annotations',x) for x in os.listdir('annotations') if x[-3:]=="txt"]
    test_random_annotation(annotations)
