import tempfile,os
import cv2
import numpy as np
# import matplotlib.pyplot as plt
import ImageConstantROI_GF as ImR
import ImageConstantROI_GB as ImB
import pandas as pd
import streamlit as st
from PIL import Image

# Assuming GhanaCard is a class you've defined to handle ID card processing
from docAI1 import GhanaCard

def match(f_dict, b_dict):
    check = all(f_dict.get(key) == b_dict.get(key) for key in b_dict if key != "Date_of_Expiry")
    return [check, "information on both sides do match" if check else "Information on both sides do not match"]

# def confirmData(f_dict, data):
#     person_detail = data[data["Personal_ID_Number"] == f_dict["Personal_ID_Number"]]
#     check = all(f_dict[key] == person_detail[key].iloc[0] for key in f_dict)
#     return [check, "Information is verified in database" if check else "Information is not verified in database"]

def confirmData(f_dict, data):
    check = True
    keys = f_dict.keys()
    print(keys)
    personldetail = data.loc[data["Personal_ID_Number"] == f_dict["Personal_ID_Number"]]
    for key in keys:
        if f_dict[key] != personldetail[key].values[0]:
            check = False
            print(personldetail[key].values[0])
    if check == True:
        return [check,"Information is verified in database"]
    else:
        return [check, "Information is not verified in database"]


st.title("Annologic Document Card Verification")

uploaded_file = st.file_uploader("Choose an ID card image for the front side...", type=['jpg', 'png'])
if uploaded_file is not None:
    # image = Image.open(uploaded_file)
    # st.image(image, caption='Uploaded Image.', use_column_width=True)
    # st.write("")
    # st.write("Processing...")
    # # Convert the file to an opencv image.
    # file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    # opencv_image = cv2.imdecode(file_bytes, 1)
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Processing...")

    # Save the uploaded file to a temporary file to read with cv2.imread
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file.getvalue())
    tfile.close()

    opencv_image = cv2.imread(tfile.name)
    extractor = GhanaCard()
    imgf = extractor.select_transform_feature("F", opencv_image)
    A = extractor.extractDataFromIdCard("F", imgf)
    st.write("Extracted Data:", A)
    os.unlink(tfile.name)

if st.button("Next Step: Process Back Side"):
    st.session_state['front_data'] = A  # Save front data in session state
    st.write("Please upload the back side of the ID card.")

uploaded_file_back = st.file_uploader("Choose an ID card image for the back side...", key="2", type=['jpg', 'png'])
if uploaded_file_back is not None:
    # image_back = Image.open(uploaded_file_back)
    # st.image(image_back, caption='Uploaded Back Image.', use_column_width=True)
    # st.write("Processing...")
    # file_bytes_back = np.asarray(bytearray(uploaded_file_back.read()), dtype=np.uint8)
    # opencv_image_back = cv2.imdecode(file_bytes_back, 1)
    image = Image.open(uploaded_file_back)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Processing...")

    # Save the uploaded file to a temporary file to read with cv2.imread
    tfile = tempfile.NamedTemporaryFile(delete=False) 
    tfile.write(uploaded_file_back.getvalue())
    tfile.close()

    opencv_image_back = cv2.imread(tfile.name)


    extractor_back = GhanaCard()
    imgb = extractor_back.select_transform_feature("B", opencv_image_back)
    B = extractor_back.extractDataFromIdCard("B", imgb)
    st.write("Extracted Data:", B)

if st.button("Confirm Details"):
    # Retrieve data from session state
    front_data = st.session_state.get('front_data', {})
    result_match = match(front_data, B)
    st.write(result_match[1])

    # Assuming 'data' is loaded from an Excel file or similar
    data = pd.read_csv("database.csv")
    st.write(data)
    result_confirm = confirmData(front_data, data)
    st.write(result_confirm[1])

    if result_match[0] and result_confirm[0]:
        st.write("All details are correct! Saving the ID image for future reference.")
        # Code to save image could go here

st.sidebar.button("Restart")
