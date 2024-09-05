# -*- coding: utf-8 -*-
"""
Contains all the edge detection algorithms used for test runner and test driver.

@author: Mohsin Ansari
"""

import cv2
import numpy as np
from itertools import zip_longest
from PST_function import PST
import mahotas as mh
from pytesseract import pytesseract

pytesseract.tesseract_cmd = 'C:\\Users\\AnsariMohsin\\AppData\Local\\Programs\Tesseract-OCR\\tesseract.exe'

#add another module where it gets the edge data and contours data for processing and storing data

class edge_detection():
    image = None #the image here should be read using cv2.imread and then stored in this variable (by the algorithm wrapper)   
    template = None
    # Canny edge detection
    def canny(self, t_lower=100, t_upper=150):
        image_np = self.image
        image_np = np.array(image_np)
        edge = cv2.Canny(image_np, t_lower, t_upper)
        return edge
        
        
    def PST_detect(self, LPF=0.21, Phase_strength=0.48, Warp_strength=12.14, Threshold_min=-1, Threshold_max=0.0019, Morph_flag=1):
        """
        LPF = 0.21 # Gaussian Low Pass Filter
        # PST parameters
        Phase_strength = 0.48 
        Warp_strength= 12.14
        # Thresholding parameters (for post processing after the edge is computed)
        Threshold_min = -1
        Threshold_max = 0.0019
        # [] Choose to compute the analog or digital edge,
        Morph_flag =1 # [] To compute analog edge, set Morph_flag=0 and to compute digital edge, set Morph_flag=1
        """
        #Image_orig = mh.imread(self.image) # Read the image.
        Image_orig = self.image
        # To convert the color image to grayscale
        if Image_orig.ndim ==3:
            Image_orig_grey = mh.colors.rgb2grey(Image_orig)  # Image_orig is color image.
        else: 
            Image_orig_grey = Image_orig

        [Edge, PST_Kernel]= PST(Image_orig_grey, LPF, Phase_strength, Warp_strength, Threshold_min, Threshold_max, Morph_flag)

        Edge = Edge.astype(dtype=np.uint8)
        Edge[Edge ==1] = 255
        
        return Edge
        
    def detect_contours(self, edge):
        contours, _ = cv2.findContours(edge, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        
        contours_array = []
        contours_poly = [None]*len(contours)
        boundRect = [None]*len(contours)

        for i, c in enumerate(contours):
            contours_poly[i] = cv2.approxPolyDP(c, 3, True)
            boundRect[i] = cv2.boundingRect(contours_poly[i])
        
        #drawing = np.zeros((edge.shape[0], edge.shape[1], 3), dtype=np.uint8)
        drawing = self.image.copy()
        
        for i in range(len(contours)):
            #length = int(boundRect[i][2])
            width = int(boundRect[i][3])
            #area = length * width
            #print(length, width)
            if width>=10: #50 for check boxes, 500 for buttons
                contours_array.append([int(boundRect[i][0]), int(boundRect[i][1]), int(boundRect[i][2]), int(boundRect[i][3])])
                cv2.rectangle(drawing, (int(boundRect[i][0]), int(boundRect[i][1])), \
                (int(boundRect[i][0]+boundRect[i][2]), int(boundRect[i][1]+boundRect[i][3])), (0, 255, 0), 2)
         
        #print(contours_array)
        return drawing, contours_array
    
    def detect_text(self):
        #tested with thresholding, the results are not clean enough for tesseract engine
        #simple grayscale conversion seems to work best
        #check if the inverting of the image is necessary as the text gets white and 
        #surrounding area gets dark as the mouse is hovering at the button
        grey_img = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        raw_data = pytesseract.image_to_data(grey_img)
        box_array = []
        text_array = []
        text_with_box = {}
        for count, data in enumerate(raw_data.splitlines()):
            if count > 0:
                data = data.split()
                if len(data) == 12:
                    #lines commented are for testing, uncomment to see the result on the image
                    x, y, w, h, content = int(data[6]), int(data[7]), int(data[8]), int(data[9]), data[11]
                    text_array.append(content)
                    box_array.append([x, y, w, h])
                    #text_with_box[content] = [x, y, w+x, h+y]
                    # Draw rectangles around text
                    cv2.rectangle(grey_img, (x, y), (w+x, h+y), (0, 255, 0), 1)
                    # Write detected text
                    #cv2.putText(grey_img, content, (x, y), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 255) , 1)
        #the storing of data in proper format is to be implemented
        #returning the image is not necessary if there is no debugging to be done
        #the image could be useful for storing the recorded step. check how this can be implemented.
        #grayscale image is not necessary, the colored one is.            
        return grey_img, box_array, text_array
    
    def template_match(self):
        img = self.image.copy() 
        template = self.template

        s = template.shape
        threshold = 0.8
    
        methods = ['cv2.TM_CCOEFF_NORMED']
    
        for meth in methods:
            #img = img2.copy()
            method = eval(meth)
            button_loc = []
            
            res = cv2.matchTemplate(img,template,method)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
            #print(min_loc)
            # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
            if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                top_left = min_loc
            else:
                top_left = max_loc
                bottom_right = (top_left[0] + s[1], top_left[1] + s[0])
            
            loc = np.where( res >= threshold)
            for pt in zip(*loc[::-1]):
                cv2.rectangle(img, pt, (pt[0] + s[1], pt[1] + s[0]), (0,255,0), 2)
                #print(pt, s)
                #button_loc.append([int((pt[0]+s[1]/2)),int((pt[1]+s[0]/2))])
                button_loc.append([int((pt[0])),int((pt[1]))])
                #print(button_loc)

            cv2.rectangle(img,top_left, bottom_right, (0,255,0), 2)
            #cv2.imshow('Detected', img)
            #k = cv2.waitKey(0) 
            #cv2.destroyAllWindows()
            #button_loc = pt
            #print((pt[0] + s[1], pt[1] + s[0]))
            return img, button_loc
            
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    