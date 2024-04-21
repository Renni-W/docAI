#My custom class for declare region of interest.
class ImageConstantROI():
    class CCCD(object):
        ROIS = {
            # "id": [(456, 308, 403, 53)],
            # "name": [(325, 393, 771, 64),],
            # "birth_date": [(658, 451, 216, 54)],
            # "gender": [(538, 495, 95, 44)],
            # "address": [(786, 639, 343, 39), (318, 672, 791, 52)],
            # "place_birth": [(326, 586, 792, 47)],
            # "date_expire": [(155, 653, 152, 31)],

            "Surname": [(742, 441, 825, 79)],
            "FirstNames": [(742, 563, 1160, 76)],
            "Previous_Names": [(749, 676, 679, 69)],
            "Nationality": [(739, 806, 679, 76)],
            "DOB": [(736, 915, 553, 82)],
            "Date_of_Issuance": [(739, 1399, 623, 79)],
            "Personal_ID_Number": [(736, 1041, 726, 76)],
            "Height/Taille": [(1538, 1054, 268, 63)],
            "Sex/Sexe": [(1482, 802, 265, 79)],
            "Document_number": [(732, 1160, 719, 76)],
            "Place_of_Issuance": [(729, 1280, 517, 76)],
            "Date_of_Expiry": [(729, 1512, 543, 86)],
          #   "ID_Pic": [(1820, 500, 785, 945)],
          #  "Ghana_flag": [(172, 1220, 185, 222)]
          
        } 
        regions = [("Surname/Nom","FirstNames/Prenorms","Previous or Maiden Names","Nationality/Nationalite", "Date of Birth/Date de Naissance", 
                   "Date of Issuance/Date de d'emission", "Personal ID Number", "Height/Taille", "Sex/Sexe",
                     "Document number/ Numero du document", "Place of Issuance/ Lieu de delivrance", "Date of Expiry/ Date d'expiratin",
                       "ID_Pic", "Ghana_flag")]
        CHECK_ROI = [(313, 174, 597, 63)]