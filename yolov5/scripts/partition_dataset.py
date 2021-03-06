from __future__ import annotations
import os
from sklearn.model_selection import train_test_split
import shutil

# Read images and annotations
images = [os.path.join('images', x) for x in os.listdir('images')]
#annotations = [os.path.join('annotations', x) for x in os.listdir('annotations') if x[-3:] == "txt"]

images.sort()
#annotations.sort()

# Split the dataset into train-valid-test splits
#print(len(images), len(annotations))
#images = images[:len(annotations)]
#print(len(images), len(annotations))
train_images, val_images= train_test_split(images, test_size = 0.2, random_state = 1)
val_images, test_images= train_test_split(val_images, test_size = 0.5, random_state = 1)

#Utility function to move images 
def move_files_to_folder(list_of_files, destination_folder):
    for f in list_of_files:
        try:
            shutil.move(f, destination_folder)
        except:
            print(f)
            assert False

# Move the splits into their folders
#move_files_to_folder(train_images, 'images/train')
move_files_to_folder(val_images, 'images/val/')
#move_files_to_folder(test_images, 'images/test/')