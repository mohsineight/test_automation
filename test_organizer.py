import json
import cv2
import os


def clear_dir(test_name):
    path = "test_steps\{}".format(test_name)
    for root, dirs, files in os.walk(path, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))
    if os.path.exists(path):
        os.rmdir(path)
    print("deleted test")

def save_step(step_data, key_string, test_name):
    clear_dir(test_name)
    test_steps = []
    key_input = False
    #as a lookup table, using names instead of numbers for better readability
    screenshot, window, text_contours, text, element, element_img, mouse_loc_screen, mouse_pos_element, mouse_loc_window, window_data, step = 0,1,2,3,4,5,6,7,8,9,10
    for i in range(len(step_data)):
        path = ("test_steps\{}\step{}".format(test_name, step_data[i][step]))
        CHECK_FOLDER = os.path.isdir(path)
        
        # If folder doesn't exist, then create it.
        if not CHECK_FOLDER:
            os.makedirs(path)
            print("created folder : ", path)
        else:
            print(path, "folder already exists.")
            
        screenshot_name = path + "\\screenshot{}.jpg".format(step_data[i][step])
        window_name = path + "\\window{}.jpg".format(step_data[i][step])
        if step_data[i][element_img] is not None:
            element_name = path + "\\element{}.jpg".format(step_data[i][step])
            cv2.imwrite(element_name, step_data[i][element_img])
        else:
            element_name = None
    
        cv2.imwrite(screenshot_name, step_data[i][screenshot])
        cv2.imwrite(window_name, step_data[i][window])
        #cv2.imwrite(element_name, element_img)
        if key_string[i] == []:
            key_input = False
        else:
            key_input = True
        step_data[i][step]= { 
            "id": step_data[i][step],
            "screen": screenshot_name,
            "window":  {
                "id": 2,
                "window image": window_name,
                "window data": step_data[i][window_data], #[posx, posy, sizex, sizey]
            "detected element": {
                "text": step_data[i][text],
                "text location": step_data[i][text_contours],
                "element": element_name,
                "element location": step_data[i][element],
                "element mouse location": step_data[i][mouse_pos_element]
                    },
            "user input": {
                "mouse input": "XXtrue/false",
                "mouse input value": "XXclick/scroll",
                "mouse click location": {"screenshot": step_data[i][mouse_loc_screen], "window": step_data[i][mouse_loc_window]},
                "key input": key_input,
                "key input value": key_string[i]
                    }
                } 
            }
    
        test_steps.append(step_data[i][step])
    output = json.dumps(test_steps)
    with open("test_steps\{}\steps.json".format(test_name), "w") as outfile:
        outfile.write(output)
    print(output)
