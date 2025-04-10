# main.py
from participants import Participants
import pandas as pd

excel_file_name = "dummy_list.xlsx"

if __name__ == "__main__":
    
    while True:
        print(">> Please Select an Item:")
        print("1- Generate Participant")
        print("2- Generate Awards")
        print("3- Generate Badges")
        print("4- Exit Program")
        # inp = input(">> ").strip()
        inp = "1"

        if inp == "1":     # participants
            part = Participants(pd.read_excel(excel_file_name, sheet_name="participants"))
            print(part.generateCertificates())
        elif inp == "2":   # Awards
            print("Awards")
        elif inp == "3":   # Badges
            print("Badges")
        elif inp == "4":
            break
        else:
            print(">> ERROR: Wrong Input. Try Again")
        
        break
        print(5*"-")