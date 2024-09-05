"""
Module for emulation of user input. The module consists of a listener class and input controller class.
The listener class listens to the user input and input controller class is for emulating the steps.

@author: Mohsin Ansari
"""

from pynput import mouse, keyboard
from pynput.mouse import Button
from pynput.mouse import Controller as Mouse_Controller
from pynput.keyboard import Key
from pynput.keyboard import Controller as Keyboard_Controller
import time
import threading

class input_listener():
    e1 = threading.Event()
    e2 = threading.Event()
    x,y = None, None
    key = None
    key_string = []
    is_stopped = True
    recorder_flag = False
    def on_click(self, x, y, button, pressed):
        if pressed:
            #print('{0} at {1}'.format('Pressed', (x, y)))
            self.x = x
            self.y = y
            print('{0} at {1}'.format('Pressed', (self.x, self.y)))
            self.key = []
            self.e1.set()

    def on_scroll(x, y, dx, dy):
        print('Scrolled {0} at {1}'.format(
            'down' if dy < 0 else 'up',
            (x, y)))
        
    def on_press(self, key):
        try:
            print('{0} pressed'.format(
                key.char))
            self.key = key
            self.key_string.append(key.char)
        except AttributeError:
            print('special key {0} pressed'.format(
                key))
            self.key = key
            self.key_string.append(key)
            self.key = key
        if key == Key.esc:
            self.e1.set()
            self.e2.set()
            self.recorder_flag = True
            self.stop_listener()
            

            
    def start_listener(self):
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.key_listener = keyboard.Listener(on_press=self.on_press)
        self.mouse_listener.start()
        self.key_listener.start()
        print('Listener started')
        self.is_stopped = False
        
    def stop_listener(self):
        self.key_listener.stop()
        self.mouse_listener.stop()
        self.x = None
        self.y = None
        self.key = None
        self.is_stopped = True
        print('Listener stopped')
 
        
#class for emulating keyboard and mouse input
#steps to emulate input:
#    create class instance
#    call start_controller function
#    call press_key, type_key or mouse_move_click functions
class input_controller():
    mouse_controller = None
    key_controller = None
    #initialization of the controller
    #need to check if this will cause conflict if there are two controllers
    #one for listener and other for controller
    #check also if it needs to be set to None after destroying it
    def start_controller(self):
        self.mouse_controller = Mouse_Controller()
        self.key_controller =  Keyboard_Controller()
        #print('Controller started')
    
    #function to press one key    
    def press_key(self, key):
        # Press and release space
        self.key_controller.press(key)
        self.key_controller.release(key)
    
    #function to type string
    #check if capital letters can be input or not in UNIX    
    def type_key(self, keys):
        self.key_controller.type(keys)
        
    #function to move mouse and emulate click
    #check if the click mechanism needs to be in separate function
    def mouse_move_click(self, x,y):
        self.mouse_controller.position = (x, y)
        #click mechanism
        self.mouse_controller.press(Button.left)
        time.sleep(0.1)
        self.mouse_controller.release(Button.left)
    
# x = input_listener()
# x.start_listener()

# y = input_controller()
# y.start_controller()

# startt = time.time()
# while(x.is_stopped == False):
#     y.mouse_move_click(600, 600)
#     time.sleep(5)
    
# endt = time.time()
# print(endt-startt)

