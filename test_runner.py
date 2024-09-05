import os
from pathlib import Path
import json
import cv2
from time import sleep
import algorithm_wrapper as wrapper
import algorithm
import test_organizer as to
from user_input import input_controller


#no logic added in case the recorded text or element is not detected by runner
#no logic for wait
#no error handling if the output of the step differs from the recorder

def run(test_to_run):
    # check = True
    test_steps = []
    print("Test runner started")
    # stored_tests = os.listdir("test_steps")
    # print("Stored_tests:")
    # print(stored_tests)
    # while True:
    #     test_to_run = input("Enter test to run: ")
    #     if test_to_run in stored_tests:
    #         with open("test_steps\{}\steps.json".format(test_to_run), 'r') as openfile:
    #             # Reading from json file
    #             test_steps = json.load(openfile)
    #         break
    #     else:
    #         print("Cannot find the test case")
        
    # print("wait for 4sec")
    # sleep(4)
    
    with open("test_steps\{}\steps.json".format(test_to_run), 'r') as openfile:
        test_steps = json.load(openfile)
    
    controller = input_controller()  
    for i in range(0, len(test_steps)):
        text = None
        text_arr = test_steps[i]['window']['detected element']['text']
        element= test_steps[i]['window']['detected element']['element']
        element_size = test_steps[i]['window']['detected element']['element location']
        recorded_mouse_loc_win = test_steps[i]['window']['user input']['mouse click location']['screenshot']
        text_input = test_steps[i]['window']['user input']['key input']
        text_string = test_steps[i]['window']['user input']['key input value']
        if 'element mouse location' in test_steps[i]:
            mouse_pos_element = test_steps[i]['window']['detected element']['element mouse location'] #remove from JSON (redundant)!!!!!!!!!!!!!!!!
        element_loc = [] #remove from JSON file (redundant)
        #print('click within template: ', mouse_pos_element)
        #print(text_arr)
        if text_arr is not None:
            text = text_arr[0]
        
        if text is not None:
            print("text: {}".format(text))
            
        if element is not None:
            element_file = Path(element)
            if element_file.is_file():
                print("GUI element")
                element = cv2.imread(element)
            else:
                #print("cannot find")
                element = None
            #print("GUI element")
            #element = cv2.imread(element)
            #element_loc = test_steps[i]['window']['user input']['mouse click location']['window']
            #cv2.imshow('element', element)
            
        screenshot = wrapper.take_screenshot().copy()
        
        window, window_loc = wrapper.find_window(screenshot)
        #print('windows: ', window_loc)
        mouse_loc = wrapper.find_element_loc1(window, window_loc, recorded_mouse_loc_win, element_size, text, element)
        # for j in range(len(window_loc)):
        #     cv2.imshow('window {}'.format(j) ,window[j])
        # k = cv2.waitKey(0)
        # cv2.destroyAllWindows()
        #if no text or element is found than click on the same location within the window
        #this logic is not robust enough. it is assumed that the size of window remains
        #same for test recorder and runner.
        if len(mouse_loc) == 0:
            print("using stored mouse location")
            #for i in range(len(window_loc)):
                #print(window_loc[i], recorded_window_size)
                #if window_loc[i] == recorded_window_size:
            # if not element_loc:
            mouse_loc = [[recorded_mouse_loc_win[0], recorded_mouse_loc_win[1]]]
            # else:
            #     print('template match loc')
                #mouse_loc = [[element_loc[0], element_loc[1]]]
                #print(mouse_loc)
        print("mouse loc: {}".format(mouse_loc))
        controller.start_controller()
        controller.mouse_move_click(mouse_loc[0][0], mouse_loc[0][1])
        
        if text_input:
            controller.type_key(text_string)
        sleep(0.5)
      
    
# for i in range(len(window_loc)):
#     cv2.imshow('window {}'.format(i) ,window[i])
# k = cv2.waitKey(0)
# cv2.destroyAllWindows()
