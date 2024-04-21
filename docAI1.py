
import cv2
import pytesseract
import numpy as np
import matplotlib.pyplot as plt
import math
import re
import ImageConstantROI_GF as ImR
import ImageConstantROI_GB as ImB
import pandas as pd

class GhanaCard:
    def __init__(self):
        # Declare pytesseract executable path
        pytesseract.pytesseract.tesseract_cmd = 'r/usr/bin/tesseract'

    def display_img(self, cvImg):
        """Custom function to show open cv image on notebook."""
        cvImg = cv2.cvtColor(cvImg, cv2.COLOR_BGR2RGB)
        plt.figure(figsize=(10,8))
        plt.imshow(cvImg)
        plt.axis('off')
        plt.show()

    def cropImageRoi(self, image, roi):
        """Create a custom function to cropped image based on region of interest."""
        roi_cropped = image[
            int(roi[1]) : int(roi[1] + roi[3]), int(roi[0]) : int(roi[0] + roi[2])
        ]
        return roi_cropped
    
    def preprocessing_image(self, img):
        """Image preprocessing for better OCR results."""
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gray = cv2.multiply(gray, 1.5)

        blured1 = cv2.medianBlur(gray,3)
        blured2 = cv2.medianBlur(gray,89) 
        divided = np.ma.divide(blured1, blured2).data
        normed = np.uint8(255*divided/divided.max())

        th, threshed = cv2.threshold(normed, 100, 255, cv2.THRESH_OTSU + cv2.THRESH_BINARY)
        
        return threshed
    
    
    
    @staticmethod
    def extract_alphabets(text):
        alphabet_parts = re.findall(r'[a-zA-Z]+', text)
        cleaned_text = ''.join(alphabet_parts)
        return cleaned_text
    @staticmethod
    def extract_numbers_and_periods(text):
        numeric_parts = re.findall(r'[0-9.]+', text)
        cleaned_text = ''.join(numeric_parts)
        return cleaned_text

    @staticmethod
    def extract_dates(text):
        date_parts = re.findall(r'[0-9]+', text)
        cleaned_text = ''.join(date_parts)
        cleaned_text = cleaned_text[:2] + '/' + cleaned_text[2:4] + '/' + cleaned_text[4:]
        return cleaned_text
    
    @staticmethod
    def reverse_dates(text):
        date_parts = re.findall(r"[0-9]+", text)
        cleaned_text = "".join(date_parts)
        cleaned_text = cleaned_text[:2] + '/' + cleaned_text[2:4] + '/' + cleaned_text[4:]
        parts = cleaned_text.split('/')
        reversed_date = '/'.join(parts[::-1])
        return reversed_date

    @staticmethod
    def select_numbers_alphabets_and_hyphen(text):
        matched_parts = re.findall(r'[A-Z0-9-]+', text)
        cleaned_text = ''.join(matched_parts)
        if cleaned_text and not cleaned_text[-1].isdigit():
            cleaned_text = cleaned_text[:-1]
        return cleaned_text

    def strip_symbols(self,pos, key, text):
        alpha_keys = ['Surname', 'FirstNames','Nationality','Sex/Sexe','Place_of_Issuance','Previous_Names']
        date_keys = ['DOB','Date_of_Issuance','Date_of_Expiry']
        num_keys = ['Height/Taille']
        alphanum_keys = ['Document_number','Personal_ID_Number']
        
        if key in alpha_keys:
            cleanText = self.extract_alphabets(text)
        elif key in date_keys and pos == "F":
            cleanText = self.extract_dates(text)
        elif key in date_keys and pos == "B":
            cleanText = self.reverse_dates(text)
        elif key in alphanum_keys:
            cleanText = self.select_numbers_alphabets_and_hyphen(text)
        elif key in num_keys:
            cleanText = self.extract_numbers_and_periods(text)
        else:
            cleanText= text
        return cleanText
 
    #Extracting data from the front
    def extractDataFromIdCard(self,pos, img):
        MODEL_CONFIG = '--oem 1 --psm 6'
        datadict = {}
        if pos == "F":
            items = ImR.ImageConstantROI.CCCD.ROIS.items()
        else:
            items = ImB.ImageConstantROI.CCCD.ROIS.items()
        for key, roi in items:
            data = ''
            for r in roi:
                crop_img = self.cropImageRoi(img, r)
                if key != 'date_expire':
                    crop_img = self.preprocessing_image(crop_img)

                data += pytesseract.image_to_string(crop_img, config = MODEL_CONFIG) + ' '
            
            datadict[key] = self.strip_symbols(pos, key, data.strip())
            if key == "Previous_Names":
                datadict[key] = "" if len(re.findall(r'[a-z]', datadict[key])) > 0 else datadict[key]
        return datadict
    
    
    
    @staticmethod
    def select_transform_feature(pos, img2):
        if pos == "F":
            baseImg = cv2.imread('EmmaF.jpg')
        else:
            baseImg = cv2.imread("EmmaB.jpg")
        baseH, baseW, baseC = baseImg.shape

        orb = cv2.ORB_create(1000)

        kp, des = orb.detectAndCompute(baseImg, None)
        imgKp = cv2.drawKeypoints(baseImg,kp, None)

        PER_MATCH = 0.30

        #Detect keypoint on img2
        kp1, des1 = orb.detectAndCompute(img2, None)

        #Init BF Matcher, find the matches points of two images
        bf = cv2.BFMatcher(cv2.NORM_HAMMING)
        matches = list(bf.match(des1, des))

        #Select top 30% best matcher 
        matches.sort(key=lambda x: x.distance)
        best_matches = matches[:int(len(matches)*PER_MATCH)]

        #Show match img  
        imgMatch = cv2.drawMatches(img2, kp1, baseImg, kp, best_matches,None, flags=2)

        #Init source points and destination points for findHomography function.
        srcPoints = np.float32([kp1[m.queryIdx].pt for m in best_matches]).reshape(-1,1,2)
        dstPoints = np.float32([kp[m.trainIdx].pt for m in best_matches]).reshape(-1,1,2)

        #Find Homography of two images
        matrix_relationship, _ = cv2.findHomography(srcPoints, dstPoints,cv2.RANSAC, 5.0)

        #Transform the image to have the same structure as the base image
        img_final = cv2.warpPerspective(img2, matrix_relationship, (baseW, baseH))

        return img_final


def match(f_dict, b_dict):
    check = True
    # ls = list()
    keys = b_dict.keys()
    for key in keys:
        if key in f_dict.keys():
            if f_dict[key] != b_dict[key]:
                check = False
    if check == True:
        return [check,"information on both sides do match"]
    else:
        return [check, "Information on both sides do not match"]

def confirmData(f_dict, data):
    check = True
    keys = f_dict.keys()
    personldetail = data[data["Personal_ID_Number"] == f_dict["Personal_ID_Number"]]
    for key in keys:
        if f_dict[key] != personldetail[key].iloc[0]:
            check = True
            print(personldetail[key].iloc[0,0])
    if check == True:
        return [check,"Information is verified in database"]
    else:
        return [check, "Information is not verified in database"]


# #Sample of how you will use it.
# #First read the image to be verified
# # Extract information from the front side
# Imag = cv2.imread("EmmaF.jpg")
# extract = GhanaCard()
# imgf = extract.select_transform_feature("F",Imag) # F for a front image and B for a back image.
# A = extract.extractDataFromIdCard("F",imgf)

# #Now extract information from te back side
# bel = cv2.imread("EmmaB.jpg")
# obj = GhanaCard()
# imgf = obj.select_transform_feature("B",bel)
# B = obj.extractDataFromIdCard("B",imgf)



# print(A)
# print(B)
# print(match(A,B))
# print(confirmData(f_dict = A, data = pd.read_csv("data1.csv")))


