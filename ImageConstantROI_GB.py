#My custom class for declare region of interest.
class ImageConstantROI():
    class CCCD(object):
        ROIS = {
            
            "Country_Code": [(1194, 649, 293, 150)],
            "Personal_ID_Number": [(1166, 481, 712, 80)],
            "FirstNames": [(761, 1500, 670, 115)],
            "Surname": [(174, 1497, 411, 111)],
            "DOB": [(174, 1361, 499, 111)],
            "Date_of_Expiry": [(844, 1354, 502, 122)],
            "Document_number": [(593, 1218, 757, 118)]
          
        } 
        regions = [("Country_Code","Personal_ID_Number","Line_1","Line_2", 
                   "Line_3")]
        CHECK_ROI = [(313, 174, 597, 63)]
        
