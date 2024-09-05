# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 14:39:03 2024

@author: ansarimohsin
"""

import json

# test_steps = {
#         "step": [
#            { 
#             "id": 0,
#             "screen": "img_path",
#             "window": "img_path",
#             "detected element": {
#                 "text": "text_string",
#                 "text location": ["array of points"],
#                 "element": "img_path",
#                 "element locaton": ["array of points"]
#                 },
#             "user input":
#                 {
#                 "mouse input": "true/false",
#                 "mouse input value": "click/scroll",
#                 "mouse click locaton": ["array of x,y"],
#                 "key input": "true/false",
#                 "key input value": "char/string"
                
#                 }
#             },
    
#             {
#             "id": 1,
#             "screen": "img_path",
#             "window": "img_path",
#             "detected element": {
#                 "text": "text_string",
#                 "text location": ["array of points"],
#                 "element": "img_path",
#                 "element locaton": ["array of points"]
#                 },
#             "user input":
#                 {
#                 "mouse input": "true/false",
#                 "mouse input value": "click/scroll",
#                 "mouse click locaton": ["array of x,y"],
#                 "key input": "true/false",
#                 "key input value": "char/string"
                
#                 }
#             }
#         ]
#     }
    
step0= { 
    "id": 0,
    "screen": "img_path",
    "window": [ {
        "id": 0,
        "window image": "img_path",
    "detected element": {
        "text": "text_string",
        "text location": ["array of points"],
        "element": "img_path",
        "element locaton": ["array of points"]
        },
    "user input":
        {
        "mouse input": "true/false",
        "mouse input value": "click/scroll",
        "mouse click locaton": ["array of x,y"],
        "key input": "true/false",
        "key input value": "char/string"
        
        }
    },
        {
        "id": 1,
        "window image": "img_path",
    "detected element": {
        "text": "text_string",
        "text location": ["array of points"],
        "element": "img_path",
        "element locaton": ["array of points"]
        },
    "user input":
        {
        "mouse input": "true/false",
        "mouse input value": "click/scroll",
        "mouse click locaton": ["array of x,y"],
        "key input": "true/false",
        "key input value": "char/string"
        
        }
    } ]
}
    
step1= { 
    "id": 1,
    "screen": "img_path",
    "window": [ {
        "id": 2,
        "window image": "img_path",
    "detected element": {
        "text": "text_string",
        "text location": ["array of points"],
        "element": "img_path",
        "element locaton": ["array of points"]
        },
    "user input":
        {
        "mouse input": "true/false",
        "mouse input value": "click/scroll",
        "mouse click locaton": ["array of x,y"],
        "key input": "true/false",
        "key input value": "char/string"
        
        }
    },
        {
        "id": 3,
        "window image": "img_path",
    "detected element": {
        "text": "text_string",
        "text location": ["array of points"],
        "element": "img_path",
        "element locaton": ["array of points"]
        },
    "user input":
        {
        "mouse input": "true/false",
        "mouse input value": "click/scroll",
        "mouse click locaton": ["array of x,y"],
        "key input": "true/false",
        "key input value": "char/string"
        
        }
    } ]
}
  
test_steps = [step0,step1]
output = json.dumps(test_steps)
#output = json.loads(output)
#print(output['step'][0])

with open("test_steps\steps.json", "w") as outfile:
    outfile.write(output)
    
    
# Opening JSON file
with open("test_steps\steps.json", 'r') as openfile:
 
    # Reading from json file
    json_object = json.load(openfile)
    
print(json_object[1])