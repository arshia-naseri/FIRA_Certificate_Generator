# main.py
from participants import Participants
from awards import Awards
from badges import Badges
import pandas as pd

excel_file_name = "dummy_list.xlsx"

if __name__ == "__main__":
    
    while True:
        print(">> Please Select an Item:")
        print("1- Generate Participant")
        print("2- Generate Awards")
        print("3- Generate Badges")
        print("4- Exit Program")
        inp = input(">> ").strip()

        if inp == "1":     # participants
            cert = Participants(pd.read_excel(excel_file_name, sheet_name="participants"))
            cert.generate()
        elif inp == "2":   # Awards
            award = Awards(pd.read_excel(excel_file_name, sheet_name="awards"))
            award.generate()
        elif inp == "3":   # Badges
            df_part = pd.read_excel(excel_file_name, sheet_name="participants") #Member, Mentor
            df_others = pd.read_excel(excel_file_name, sheet_name="badge") #Vip, Org, Tc
            df_all = pd.concat([df_part, df_others],ignore_index=True)
            badg = Badges(df_all)
            badg.generate()
        elif inp == "4":
            break
        else:
            print(">> ERROR: Wrong Input. Try Again")
        print(5*"-")