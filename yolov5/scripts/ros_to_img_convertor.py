#!/usr/bin/env python
from __future__ import print_function
from asyncore import write

import os
import sys
import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_convertor:
  def __init__(self):
    self.counter = 0
    self.img_counter = 1
    self.save_dir = '~/firefly_data/deck_ir_images/deck_'
    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/nea_realsense/camera1/ir_image", Image, self.callback)

  def callback(self, ir_img_data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(ir_img_data, "mono8")
      self.counter += 1
    except CvBridgeError as err:
      print(err)
    
    
    # if cols > 60 and rows > 60:
    #   cv2.circle(cv_image, (50,50), 10, 255)
    cv2.imshow("Image Window", cv_image)
    cv2.waitKey(1)
    if (self.counter > 0 and self.counter % 10 is 0):
      try:
        write_dir = "deck_" + str(self.img_counter) + ".jpg"
        cv2.imwrite(write_dir, cv_image)
        print("Saving IR Image at:" + write_dir)
        self.img_counter += 1
      except:
        print("Unable to save image")

      cv2.imshow("Image Window", cv_image)
      cv2.waitKey(3)

def main(args):
  ic = image_convertor()
  rospy.init_node('image_convertor', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting Down")
  cv2.destroyAllWindows()

if __name__=="__main__":
  main(sys.argv)      
