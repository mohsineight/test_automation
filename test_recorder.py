 # -*- coding: utf-8 -*-
"""
Created on Thu Mar  7 09:18:09 2024

@author: ansarimohsin
"""
import os
import algorithm_wrapper as wrapper
import algorithm
import test_organizer as to
import cv2
from time import sleep
from user_input import input_listener

def rec(test_name):
    #test_name = "text"
    step = 1
    step_data = []
    overwrite = None
    text_string = []
    print("Test recorder started")
    #logic to ask user before overwriting the test
    # stored_tests = os.listdir("test_steps")
    # print("Stored steps:")
    # print(stored_tests)
    # while True:
    #     test_name = input("Enter test name: ")
    #     if test_name in stored_tests:
    #         print("Test with given name already exists")
    #         overwrite = input("Do you want to overwrite it? [y/n]: ")
    #         if overwrite == "y":
    #             break
    #     else: break
            
    listener = input_listener()
    listener.start_listener()
    mouse_loc_screen = [None, None]
    screenshot = wrapper.take_screenshot().copy()
    # print("wait for 4sec")
    # sleep(4)
    while True:
        listener.e1.wait()
        listener.e1.clear()
        if listener.e2.is_set():
            print("Test recorder stopped")
            break
        if listener.x <= wrapper.screenWidth and listener.y <= wrapper.screenHeight:
            if mouse_loc_screen is not [] and mouse_loc_screen == [listener.x, listener.y]:
                print("clicked on same location twice")
            else:
                mouse_loc_screen = [listener.x, listener.y]
                #print(mouse_loc_screen)
                img1, array1 = wrapper.edge_detection()
                detected_array, _ = wrapper.locate_mouse_click(mouse_loc_screen, array1)
                if detected_array == []:
                    print("not clicked inside the window")
                else:
                    screenshot_np, window, text_contours, text, element, element_img, mouse_pos_element, mouse_loc_window, window_data = wrapper.information_extraction(detected_array, mouse_loc_screen)
                    step_data.append([screenshot, window, text_contours, text, element, element_img, mouse_loc_screen, mouse_pos_element, mouse_loc_window, window_data, step])
                    screenshot = wrapper.take_screenshot().copy()
                    step+=1
        else:
            print("clicked outside")
        print("text string: {}".format(listener.key_string))
        text_string.append(listener.key_string)
        listener.key_string = []
        
    print("steps recorded: {}".format(len(step_data)))
    print("text: ", text_string)
    to.save_step(step_data, text_string, test_name)
    listener.key_string =[]


# add error checks in the algorithm wrapper 
# add mechanism to for template matching
# add logging into json file
# error checks:
#     - if there is no click
#     - if the window is minimized
#     - if there algorithm is not able to detect any contour
#     - if there is keyboard input

#steps:
#take screenshot
#record the mouse click position
#do processing on the screenshot
#store the concerned date in json file
#take screenshot to store the output
#store the next mouse click of userqwe
#the output screenshot of previous step is input of next step
#check with which window the user is interacting to focus on that window, the output information is extracted from that