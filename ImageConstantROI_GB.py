#My custom class for declare region of interest.
class ImageConstantROI():
    class CCCD(object):
        ROIS = {
            
            "Country_Code": [(1194, 649, 293, 150)],
            "Personal_ID_Number": [(1166, 481, 712, 80)],
            "Line_1": [(185, 1221, 2517, 125)],
            "Line_2": [(167, 1350, 2489, 132)],
            "Line_3": [(174, 1490, 2478, 125)],
            
          
        } 
        regions = [("Country_Code","Personal_ID_Number","Line_1","Line_2", 
                   "Line_3")]
        CHECK_ROI = [(313, 174, 597, 63)]