# -*- coding: utf-8 -*-
"""
Created on Mon Feb 12 13:51:00 2024

@author: ansarimohsin
"""

"""
TODOs:
-add check in case the getwindow gets empty array. (done)
-add aditional logic for storing the contour information from both gui and text
detection. (done)
add all this logic in a function
-add a function to create a yaml file to store the recorded information
-parallelize the functionality
-create a logic to detect and repeat the recorded step

Points of failure:
    point of failure 1: if the detection at some point fails then the possible cause
    could be that the small contour is too small to be used for template matching
    and gives false positives when used for template matching.
    one possible solution for that could be to use second smallest contour array.
"""


#this module is to act as a bridge between algorithms and test runner
#it will get images from screenshot and provide with contours and text information (yet to be implemented)
#the screenshot will be triggered by test runner and the processing will be done by this module

import cv2
import algorithm
#import user_input
import pyautogui
import numpy as np
import threading
import json
import collections
from time import sleep

#pos1 = [940, 263] #944, 294     940, 263
#pos2 = [1178, 131]
detector = algorithm.edge_detection()
screenWidth, screenHeight = pyautogui.size()

def locate_mouse_click(mouse_pos, contour_array):
    '''
    takes mouse click position and all the detected contours. the contours are detected
    using edge detection algorithms (PST or Canny). the output is the list of all contours
    which have the mouse click inside them.
    '''
    detected_contours = []
    indexes = []
    
    #parallelize this part
    for i in range(len(contour_array)):
        if mouse_pos[0] >= contour_array[i][0] \
        and mouse_pos[1] >= contour_array[i][1] \
        and mouse_pos[0] < contour_array[i][0]+contour_array[i][2] \
        and mouse_pos[1] < contour_array[i][1]+contour_array[i][3]:
            detected_contours.append(contour_array[i])
            indexes.append(i)
    
    #print(detected_contours)
    return detected_contours, indexes

#gets the biggest contour which has the mouse click inside it.
#this contour is the window
#gets the smallest contour which has the mouse click inside it.
#this contour is the gui element detected
#find the contours with mouse click inside them using locate_mouse_click
#then use this function to get the biggest and smallest contour
def get_contours(contour_array):
    '''
    takes the list of contours and finds the biggest and smallest contour in the list
    '''
    area = []
    
    for i in range(len(contour_array)):
        area.append(contour_array[i][2] * contour_array[i][3])
      
    #if area == []:
    #    sys.exit("Mouse click not detected within a window.")
    
    #point of failure 1: 
    if area != []:
        big_contour_index = area.index(max(area))
        big_contour = contour_array[big_contour_index]
        
        small_contour_index = area.index(min(area))
        small_contour = contour_array[small_contour_index]
    
        return big_contour, big_contour_index, small_contour, small_contour_index
    else:
        return None,None,None,None

def take_screenshot():
    '''
    takes the screenshot of first screen, gives it to algorithm module and 
    returns it as well.
    make sure that the exceed window is maximized on the first screen if there
    is multiple screen setup.
    '''
    screenshot = pyautogui.screenshot()
    screenshot_np = np.array(screenshot)
    screenshot_np = cv2.cvtColor(screenshot_np, cv2.COLOR_BGR2RGB)
    detector.image = screenshot_np
    return screenshot_np
    
def edge_detection(mode= 'canny'):
    '''
    selects the edge detection method and then passes it to algorithm module.
    gets the output from the detector and returns it.
    '''
    if mode == 'canny':
        edge = detector.canny()
    elif mode == 'PST':
        edge = detector.PST()
    else:
        edge = detector.canny()
        
    img, array = detector.detect_contours(edge)
    return img, array

def information_extraction(detected_array, mouse_pos):
    '''
    processes the data for each step and then passes it to test recorder.
    the steps are mentioned below:
    - input the mouse click position and list of all contours and pass it to
    locate_mouse_click function. the function outputs list of all contours
    which have mouse click detected in them.
    - pass this list to get_contours function which gives the biggest contour
    (window) and smallest contour (GUI element).
    - crop the window to store it as information for the step.
    - do text detection on the window and get the text data and location
    information for the detected text to store for step.
    - get mouse click position in the window.
    - find the detected text and its location corresponding to the mouse click
    position in the window.
    - parse all this information to a json file

    '''
    detected_text = []
    mouse_pos_element = []
    # detected_array, _ = locate_mouse_click(mouse_pos, array)

    window, index1, element, index2 = get_contours(detected_array)
    
    #calculate click position in the template match element
    #this is required if template match element is big
    print('element: ', element)
    print('mouse pos:', mouse_pos)
    mouse_pos_element = [mouse_pos[0]-element[0],mouse_pos[1]-element[1]]
    print('mouse pos element: ', mouse_pos_element) #pass this var too!!!!!!!!!!!!!!!!!!
    
    #to store
    screenshot_np = detector.image
    print("window: ", window)

    cropped_screenshot = screenshot_np[window[1]:window[1]+window[3], 
                                       window[0]:window[0]+window[2]].copy()
    #to store
    detector.image = cropped_screenshot
    grey_image , box, text = detector.detect_text()
    #print('box: ',box)
    #to store
    pos_for_window = [mouse_pos[0]-window[0], mouse_pos[1]-window[1]]
    print("pos in window: ",pos_for_window)
    #to store
    text_contours, indexes = locate_mouse_click(pos_for_window, box)
    print('text contours: ',text_contours)
    for i in indexes: 
        print('text: ', text[i])
        detected_text.append(text[i])
    #_, _, cropped_element, cropped_index = get_contours(text_contours)
    #to store
    #print('GUI element: ',element)
    #print('Window: ',window)
    if window == element:
        print('no GUI element found')
        element_img = None
    else:
        element_img =  screenshot_np[element[1]:element[1]+element[3], 
                                     element[0]:element[0]+element[2]].copy()
    if text_contours == []:
        print('no text found')
        detected_text = None
        
    
    #if cropped_element != None:
    for i in range(len(detected_array)):
        cv2.rectangle(screenshot_np, (detected_array[i][0], detected_array[i][1]), 
                      (detected_array[i][0]+detected_array[i][2], 
                       detected_array[i][1]+detected_array[i][3]), (0, 255, 0), 2)
    # cv2.rectangle(screenshot_np, (cropped_element[0]+window[0], 
    #                               cropped_element[1]+window[1]), 
    #               (cropped_element[0]+cropped_element[2]+window[0], 
    #                cropped_element[1]+cropped_element[3]+window[1]),
    #               (0, 0, 255), 2 )
    #cv2.rectangle(screenshot_np, (element[0], element[1]), (element[0]+element[2], element[1]+element[3]), (0, 255, 0), 2 )
    # cv2.imshow('drawing', screenshot_np)
    # cv2.imshow('window', cropped_screenshot)
    # cv2.imshow('text', grey_image)
    # cv2.imshow('PST', img2)

    # k = cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return screenshot_np, cropped_screenshot, text_contours, detected_text, element, element_img, mouse_pos_element, pos_for_window, window
    
##############################################
# steps for template matching
##############################################
# image = "C:\MOHSIN\Python\Virgil\padstack_editor.jpg"
# template = "C:\MOHSIN\Python\Virgil\check.jpg"

# detector = algorithm.edge_detection()
# detector.image = cv2.imread(image)
# detector.template = cv2.imread(template)

# grey_image , box, text = detector.detect_text()
# match = detector.template_match()

# #print(text)
# cv2.imshow('image', match)
# k = cv2.waitKey(0)
# cv2.destroyAllWindows()


##############################################
# the steps start from here
##############################################
# 1- taking screenshot
#detector = algorithm.edge_detection()
#screenshot_np = take_screenshot()
#detector.image = screenshot_np

# 2- performing edge detection
#img1, array1 = edge_detection()

# 3- processing mouse click and finding the concerned element
# # 4- finding the mouse click location in the cropped image
#information_extraction(pos1, array1)

# drawing rectangles on the screenshot
# if cropped element is not found then it means the user clicked on the window itself
# and there was no GUI element detected within the clicked position
# use this logic to add data to the test step in yaml file


#############################################
# section for test runner
#############################################

#given a screenshot, find the windows in it
def find_window(screenshot):
    area = []
    contours = []
    cropped_windows = []
    screenshot = screenshot
    detector.image = screenshot.copy()
    
    img, array = edge_detection()
    
    #add only those contours which are bigger than a certain size
    #the size is set using hit and trial method
    #and would need adjustment
    for i in range(len(array)):
        area.append(array[i][2] * array[i][3])
        if area[i] >= 10000:
            #cv2.rectangle(screenshot, (array[i][0], array[i][1]),(array[i][0]+array[i][2], array[i][1]+array[i][3]), (0,255,0),2)
            contours.append([array[i][0], array[i][1], array[i][2], array[i][3]])
   
   #to find the duplicates in the contours and remove them
   #this function gives only 1 contour for 1 window
   #this is required to detect the element within the windows correctly
    windows_loc = contours.copy() #the location of windows in the screenshot
    found = []
    
    for i in range(len(contours)):
        for j in range(i):
            if contours[i] == contours[j]:
                found.append(j)

    for i in range(len(found)):
        windows_loc.pop(found[i]-i)
                
    #print(contours)
    #print(found)
    #print(windows_loc)

    #this loop gives the cropped windows from the taken screenshot
    for i in range(len(windows_loc)):
        cropped_windows.append(screenshot[windows_loc[i][1]:windows_loc[i][1]+windows_loc[i][3], windows_loc[i][0]:windows_loc[i][0]+windows_loc[i][2]])
        #cv2.imshow('window {}'.format(i) ,cropped_windows[i])

    # detector.image = screenshot
    # cv2.imshow('screenshot', screenshot)
    # k = cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return cropped_windows, windows_loc


def find_element_loc(window, window_loc, text=None, template=None):
    #loop over each window
    #do text detection and template matching here
    #find the location of the found element
    #find the mouse location on the screenshot
    #after finding the location, check if mouse
    #keyboard input is to be done
    if text is None and template is None:
        print('no text or GUI element passed')
        return []
    mouse_loc = []
    print("detected windows: {}".format(len(window)))
    for i in range(len(window)):
        detector.image = window[i]
        #print("searching in window {}".format(i))
        if text is not None:
            img, text_loc_arr, text_arr = detector.detect_text()
            #print(text_arr)
            #idx = text_arr.index("rowse")
            if text not in text_arr:
                #need to add some logic here
                #pass
                print('no text found in window {}'.format(i))
            else:
                idx = text_arr.index(text)
                text_loc = text_loc_arr[idx]
                mouse_loc.append( [text_loc[0]+window_loc[i][0]+text_loc[2]/2, text_loc[1]+window_loc[i][1]+text_loc[3]/2 ] )
                # print(mouse_loc)
                print("text location: {}".format(text_loc_arr[i]))
                break
                #cv2.imshow('text {}'.format(i), img)
        elif template is not None:
            if template.shape[0] >= window[i].shape[0] or \
            template.shape[1] >= window[i].shape[1]:
                break
            detector.template = template
            detector.image = window[i]
            image, location = detector.template_match()
            if location != []:
                mouse_loc.append( [location[0][0]+window_loc[i][0], location[0][1]+window_loc[i][1]] )
                print("element location: {}".format(mouse_loc))
                break
                #cv2.imshow('Template {}'.format(i), image)
            else:
                print('no GUI element in window {}'.format(i))
        else:
            print('no text or GUI element detected in window {}'.format(i))
            return None
            #if no object detected then use the stored click location
            
    return mouse_loc
 
    
def find_element_loc1(window, window_loc, mouse_loc_element, temp_size, text=None, template=None):
    #loop over each window
    #do text detection and template matching here
    #find the location of the found element
    #find the mouse location on the screenshot
    #after finding the location, check if mouse
    #keyboard input is to be done
    if text is None and template is None:
        print('no text or GUI element passed')
        return []
    mouse_loc = []
    print("detected windows: {}".format(len(window)))
    #this loop is only for text detection
    #tesseract cannot do text detection on the screenshot
    #so we find windows and do text detection on individual windows
    if template is not None:
        # if template.shape[0] >= window[i].shape[0] or \
        # template.shape[1] >= window[i].shape[1]:
        #     return []
        xoff = mouse_loc_element[0] - temp_size[0]
        yoff = mouse_loc_element[1] - temp_size[1]
        detector.template = template
        detector.image = take_screenshot().copy()
        image, location = detector.template_match()
        # cv2.imshow('image', image)
        # k = cv2.waitKey(0)
        # cv2.destroyAllWindows()
        if location != []:
            if len(location) ==1:
                #print('location: ',location)
                mouse_loc.append( [location[0][0]+xoff, location[0][1]+yoff] )
                #print("GUI element location: {}".format(mouse_loc))
                return mouse_loc
            else: return []
            #cv2.imshow('Template {}'.format(i), image)
        else:
            print('no GUI element in window')
            
    elif text is not None:
        for i in range(len(window)):
            detector.image = window[i]
            text_occrs =[]
            #print("searching in window {}".format(i))
            if text is not None:
                img, text_loc_arr, text_arr = detector.detect_text()
                #print(text_arr)
                #idx = text_arr.index("rowse")
                # if len(text_arr) == 1:
                if text not in text_arr:
                    #need to add some logic here
                    #pass
                    print('no text found in window {}'.format(i))
                else:
                    idx = text_arr.index(text)
                    text_loc = text_loc_arr[idx]
                    for j in range(len(text_arr)):
                        if text == text_arr[j]:
                            text_occrs.append(j)
                    #print('text occrs :',len(text_occrs))
                    mouse_loc.append( [text_loc[0]+window_loc[i][0]+text_loc[2]/2, text_loc[1]+window_loc[i][1]+text_loc[3]/2 ] )
                    # print(mouse_loc)
                    print("text location: {}".format(text_loc_arr[idx]))
                    break
                # else: return []
                    #cv2.imshow('text {}'.format(i), img)
    # elif template is not None:
    #     # if template.shape[0] >= window[i].shape[0] or \
    #     # template.shape[1] >= window[i].shape[1]:
    #     #     return []
    #     detector.template = template
    #     detector.image = take_screenshot().copy()
    #     image, location = detector.template_match()
    #     # cv2.imshow('image', image)
    #     # k = cv2.waitKey(0)
    #     # cv2.destroyAllWindows()
    #     if location != []:
    #         if len(location) ==1:
    #             mouse_loc.append( [location[0][0], location[0][1]] )
    #             print("element location: {}".format(mouse_loc))
    #             return mouse_loc
    #         else: return []
    #         #cv2.imshow('Template {}'.format(i), image)
    #     else:
    #         print('no GUI element in window')
    else:
        print('no text or GUI element detected')
        return []
            #if no object detected then use the stored click location
            
    return mouse_loc

#the steps for test runner start from here   
#text= AIF, Design, Infineon
#template = template

# windows, windows_loc = find_window()
# template = "C:\\MOHSIN\\Python\\Virgil\\templates\\browse.jpg"
# template = cv2.imread(template)
# mouse_loc = find_element_loc(windows, windows_loc, template=template)
# print('found locations {}'.format(mouse_loc))
# k = cv2.waitKey(0)
# cv2.destroyAllWindows()
